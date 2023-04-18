#! /usr/bin/env python3

#######################################################################
#
# Author: Mauricio Salerno
# Copyright 2022
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

"""
Creates an action elimination task for an automated planning task and a valid plan.
Examples: <param> is a nec. parameter, while [param=val] is an optional parameter with default value = val
Maintain order of actions and compute triv. nec actions in original plan call string:
    ./action_elim.py  -t <output.sas> -p <sas_plan> -s -e -r [reduction=MR] -f [file=reformulation.sas] -d [directory=.]
Allow reorder of actions in original plan call string:
    ./action_elim.py  -t <output.sas> -p <sas_plan> -r [reduction=MR] -f [file=reformulation.sas] -d [directory=.]
"""

import argparse
import json
import os.path
import sys
from time import process_time
from math import inf, ceil
from copy import deepcopy

from plan_parser import parse_plan
from sas_parser import parse_task
from sas_tasks import SASTask, SASVariables, SASOperator, SASInit, SASGoal, SASAxiom, SASMutexGroup
from simplify import TriviallySolvable, filter_unreachable_propositions
from variable_order import find_and_apply_variable_order


# Type of reduction
MR  = 'MR'
MLR = 'MLR'
# Macro-operator string
MACRO_OP_STRING = "-triv-nec-macro-"
# Cost scalin file
ORGINAL_OP_COSTS_FILE = 'original-op-costs.txt'

# Clean domains as proposed by Jendrik (I think)
def create_action_elim_task(sas_task, plan, operator_name_to_index, ordered, enhanced, reduction, add_pos_to_goal, enhanced_fix_point, enhanced_unnecessary, use_macro_ops, scale_costs):
    # Process operators. Later on, variable to maintain order of actions will be var_(n + 1) (n=num vars originally)
    print("Plan length:", len(plan))
    print("Unique operators in plan:", len(set(plan)))
    new_operators = get_operators_from_plan(sas_task.operators, plan, operator_name_to_index, ordered)

    triv_nec = [False] * len(plan)
    triv_unnec = [False] * len(plan)
    fact_achievers = []

    # Use original operator costs
    use_action_costs = reduction == MR and sas_task.metric
    # Deal with zero cost actions if specified
    if reduction == MR and scale_costs:
        mult_factor, num_zero_cost_ops = compute_mult_factor(new_operators)
        original_op_cost_map = {}
        assert mult_factor >= 1
        if num_zero_cost_ops > 0:
            for op in new_operators:
                original_op_cost_map[op.name] = op.cost
                if op.cost == 0:
                    op.cost = 1
                else:
                    op.cost *= mult_factor

        # Map of all cost scaling information
        cost_scaling_info = {
            "num_zero_cost_operators": num_zero_cost_ops,
            "cost_scaling_factor": mult_factor,
            "original_costs": original_op_cost_map
        }

        # Store original operator costs
        with open(ORGINAL_OP_COSTS_FILE, 'w') as original_costs_file:
            original_costs_file.write(json.dumps(cost_scaling_info))

    if ordered and enhanced:
        # Find triv. neccessary actions. Operators have same order as original plan!
        triv_nec, fact_achievers = find_triv_nec_actions(sas_task.init, sas_task.goal, sas_task.variables, new_operators, enhanced_fix_point)
        if enhanced_unnecessary:
            triv_unnec = find_triv_unnec_actions(sas_task.init, sas_task.goal, sas_task.variables, new_operators, triv_nec, fact_achievers)

        # Create macro operators from triv. nec. actions streaks
        if use_macro_ops:
            new_operators = process_macro_operators(new_operators, triv_nec, triv_unnec, use_action_costs)
            print(f"Number of op withtout macro-ops: {len(plan)}\nNumb of ops with macros: {len(new_operators)}")
            plan_with_macros = new_operators

    # Find relevant facts for action elim task
    relevant_facts = find_relevant_facts(sas_task, new_operators, operator_name_to_index)

    # Prune domains of variables to only contain relevant facts
    new_variables, vars_vals_map = prune_irrelevant_domain_values(sas_task.variables, relevant_facts, new_operators, ordered)

    # Map operators variable values to new domains
    new_operators = process_operators(new_operators, relevant_facts, vars_vals_map, new_variables, ordered, use_action_costs, triv_nec, triv_unnec)

    # Map init values to new domains
    new_init = process_init(sas_task.init, vars_vals_map, relevant_facts, new_variables, ordered)

    # Map mutexes values new domains
    new_mutexes = process_mutex_groups(sas_task.mutexes, vars_vals_map, relevant_facts)

    # Map goal values to new domains
    new_goal_facts = [(var, vars_vals_map[var][val]) for var, val in sas_task.goal.pairs]
    if ordered and add_pos_to_goal:
        pos_goal_fact = (len(sas_task.variables.ranges), len(plan)) if not use_macro_ops else (len(sas_task.variables.ranges), len(plan_with_macros))
        new_goal = SASGoal(new_goal_facts + [pos_goal_fact])
    else:
        new_goal = SASGoal(new_goal_facts)

    # Map axioms
    new_axioms = process_axioms(sas_task.axioms, new_variables, vars_vals_map, relevant_facts)

    new_task = SASTask(variables=new_variables, mutexes=new_mutexes,
                   init=new_init, goal=new_goal, operators=new_operators, axioms=new_axioms, metric=True)

    try:
        # Remove unreachable facts and useless variables using FD code
        filter_unreachable_propositions(new_task)
    except TriviallySolvable:
        sys.exit("Action elimination task is trivially solvable. New task will not be generated.")

    find_and_apply_variable_order(new_task, reorder_vars=True, filter_unimportant_vars=True)

    return new_task


def get_operators_from_plan(operators, plan, operator_name_to_index, ordered):
    if ordered:
        # Ordered tasks create a different operator for each operator in the plan
        return [deepcopy(operators[operator_name_to_index[op]]) for op in plan]
    else:
        # Unordered tasks create a different operator for each unique operator in the plan
        added = set()
        # added.add(op) is only used for its' side effects.
        # set.add(x) always returns None so it doesn't affect the condition
        return [operators[operator_name_to_index[op]] for op in plan if not (op in added or added.add(op))]


def compute_mult_factor(new_operators):
    # Finds factor a to multiply cost of non-zero cost ops, so zero cost ops can be set to 1.
    # Must comply with a * min_cost > m
    # Mult. factor is computed as a = cei((m/min_cost) + eps))
    # m is number of zero cost operators, min_cost is smallest op cost larger than 0 and eps an arbitrarily small number
    eps = 0.001
    num_zero_cost_ops = 0
    min_positive_cost = inf
    for op in new_operators:
        if op.cost == 0:
            num_zero_cost_ops += 1
        else:
            min_positive_cost = min(min_positive_cost, op.cost)

    return ceil((num_zero_cost_ops / min_positive_cost) + eps), num_zero_cost_ops


# Given information about triv. nec. actions, create macro operators for streaks of consecutive triv. nec. actions in plan
# Only makes sense when maintaining order of actions in input plan
def process_macro_operators(plan, triv_nec, triv_unnec, use_op_cost):
    def has_eff_cond(op):
        for var, _, _, eff_cond in op.pre_post:
            if eff_cond:
                return True
        return False

    # Number of operators composing current macro operator
    op_count = 0

    # Prevail and pre_post of current macro operator
    # Should we use lists for this?
    current_prev = {}
    current_pre_post = {}
    new_name = ""
    current_cost = 0

    # Operators after creating the macro-operators
    new_operators = []

    # Update triv. nec. and unnec. actions with new action indices
    new_triv_nec = []
    new_triv_unnec = []

    for index, op in enumerate(plan):
        if triv_nec[index] and not has_eff_cond(plan[index]):
            # If no streak of triv. nec. actions, do not process operator for new macro op.
            if op_count < 1 and  (not triv_nec[index + 1] or (index < len(plan) - 1 and has_eff_cond(plan[index + 1]))):
                op_count = 1
                continue

            # First needed precond. for a variable is the precond. for the macro op.
            for var, val in op.prevail:
                if var not in current_prev and var not in current_pre_post:
                    current_prev[var] = (var, val)

            # Keep last effect and first precond. for each var
            for var, old_val, new_val, cond_effects in op.pre_post:
                old_prev = current_prev.get(var)
                old_pre_post = current_pre_post.get(var)
                if old_prev is not None:
                    # Keep original precondition and update effects
                    current_pre_post[var] = (var, old_prev[1], new_val, cond_effects)
                    del current_prev[var]
                elif old_pre_post is not None:
                    # Keep original precondition and update effects
                    current_pre_post[var] = (var, old_pre_post[1], new_val, cond_effects)
                else:
                    # New precond and affects
                    current_pre_post[var] = (var, old_val, new_val, cond_effects)

            new_name += f"{MACRO_OP_STRING}{op.name.lstrip('(').rstrip(')')}"
            current_cost += op.cost if use_op_cost else 1
            op_count += 1
        else:
            # If macro operator was created
            if op_count > 1:
                new_operators.append(SASOperator(f"({new_name})", list(current_prev.values()), list(current_pre_post.values()), current_cost))
                new_operators[-1].is_macro = True
                current_prev.clear()
                current_pre_post.clear()
                new_name = ""
                current_cost = 0
                new_triv_nec.append(True)
                new_triv_unnec.append(False)

            # If last act. is triv. nec. but no macro was created
            if op_count == 1:
                new_operators.append(plan[index - 1])
                new_triv_nec.append(True)
                new_triv_unnec.append(False)

            op_count = 0
            # Current op. is not triv. nec. add without changing it
            new_operators.append(op)
            new_triv_nec.append(False)
            new_triv_unnec.append(triv_unnec[index])

    if current_pre_post:
        new_operators.append(SASOperator(f"({new_name})", list(current_prev.values()), list(current_pre_post.values()), current_cost))
        new_operators[-1].is_macro = True
        new_triv_nec.append(True)
        new_triv_unnec.append(False)

    triv_nec[:] = new_triv_nec
    triv_unnec[:] = new_triv_unnec

    return new_operators


def find_relevant_facts(sas_task, operators, operator_name_to_index):
    is_fact_relevant = [[False] * domain_size for domain_size in sas_task.variables.ranges]
    # All facts in goal are needed.
    for var, val in sas_task.goal.pairs:
        is_fact_relevant[var][val] = True

    # All facts in operator preconditions are needed.
    for op in operators:
        # op = sas_task.operators[operator_name_to_index[op_name]]
        for var, val in op.prevail:
            is_fact_relevant[var][val] = True

        for var, old_val, _, conditions in op.pre_post:
            if old_val > -1:
                is_fact_relevant[var][old_val] = True
            for cond_var, cond_val in conditions:
                is_fact_relevant[cond_var][cond_val] = True

    # All facts in axiom conditions are relevant
    for axiom in sas_task.axioms:
        for var, val in axiom.condition:
            is_fact_relevant[var][val] = True
        if axiom.effect[1] > -1:
            is_fact_relevant[axiom.effect[0]][axiom.effect[1]] = True

    return is_fact_relevant


def prune_irrelevant_domain_values(variables, is_fact_relevant, plan, ordered):
    # For each var, store value mapping to new domain
    vars_new_vals_map = [[-1] * domain_size for domain_size in variables.ranges]
    new_value_names = []
    new_axiom_layers = []
    new_ranges = []

    # For each relevant fact, add to new domain
    for var, rel_facts in enumerate(is_fact_relevant):
        next_val = 0
        current_val_names = []
        for val, is_rel in enumerate(rel_facts):
            if is_rel:
                vars_new_vals_map[var][val] = next_val
                current_val_names.append(variables.value_names[var][val])
                next_val += 1
        # Irrelevant facts will al be mapped to a new domain value
        # This will potentially reduce the domain size of the variables
        # This new value will always be the greater val of the domain
        current_val_names.append('Atom irrelevant-fact()')
        next_val += 1
        # End code for some value not in any precond
        new_ranges.append(next_val)
        new_axiom_layers.append(variables.axiom_layers[var])
        new_value_names.append(current_val_names)

    # Add variable to maintain action order
    if ordered:
        new_ranges.append(len(plan) + 1)
        new_axiom_layers.append(-1)
        new_value_names.append(['Atom plan-pos-%i()' % i for i in range(len(plan) + 1)])
        vars_new_vals_map.append([i for i in range(len(plan) + 1)])
        is_fact_relevant.append([True] * (len(plan) + 1))

    return SASVariables(ranges=new_ranges, axiom_layers=new_axiom_layers, value_names=new_value_names)\
           , vars_new_vals_map


def process_operators(operators, is_fact_relevant, vars_vals_map, variables, ordered, use_costs, triv_nec, triv_unnec):
    processed_operators = []
    # Variable to maintain order is ALWAYS the last variable
    ordered_var = len(variables.ranges) - 1
    for op_index, op in enumerate(operators):
        # Remove triv. unnec. operators
        if triv_unnec[op_index]:
            # Include ONLY a skip actions to avoid messing with the pos_var values.
            # TODO: should we change this?
            processed_operators.append(SASOperator(name='(skip-action plan-pos-%i)' % op_index, prevail=[], pre_post=[(ordered_var, op_index, op_index + 1, [])], cost=0))
            continue

        # Might not need to check if prevail is relevant -- was set as relevant before
        new_prev = [(var, vars_vals_map[var][val]) for var, val in op.prevail if is_fact_relevant[var][val]]
        new_pre_post = [(var, old_val if old_val == -1 else vars_vals_map[var][old_val],
                        vars_vals_map[var][new_val] if is_fact_relevant[var][new_val] else variables.ranges[var] - 1,
                        [(cond_var, vars_vals_map[cond_var][cond_val] if is_fact_relevant[cond_var][cond_val] else variables.ranges[cond_var] -1)
                        for cond_var, cond_val in cond])
                        for var, old_val, new_val, cond in op.pre_post]
        # Add ordered constraint pre_post
        if ordered:
            new_pre_post.append((ordered_var, op_index, op_index + 1, []))
            # Only actions that are not triv. nec can be skipped
            if not triv_nec[op_index]:
                processed_operators.append(SASOperator(name='(skip-action plan-pos-%i)' % op_index, prevail=[], pre_post=[(ordered_var, op_index, op_index + 1, [])], cost=0))

        # For MLR we need op_cost of 1 and skip actions of cost=0
        # For MR we need to maintain the operators' original cost
        op_cost = op.cost if use_costs or getattr(op, 'is_macro', False) else 1
        processed_operators.append(SASOperator(name=op.name, prevail=new_prev, pre_post=new_pre_post, cost=op_cost))

    return processed_operators


def process_init(init, vars_val_map, is_fact_relevant, variables, ordered):
    new_init_values = []
    for var, val in enumerate(init.values):
        # If fact is relevant add to init. Else add 'some value'
        if is_fact_relevant[var][val]:
            new_init_values.append(vars_val_map[var][val])
        else:
            new_init_values.append(variables.ranges[var] - 1)

    # Order var always last one. Initial plan position 0
    if ordered:
        new_init_values.append(0)

    return SASInit(values=new_init_values)


def process_mutex_groups(mutex_groups, vars_val_map, is_fact_relevant):
    new_groups = []
    for group in mutex_groups:
        new_mutex = [(var, vars_val_map[var][val]) for var, val in group.facts if is_fact_relevant[var][val]]
        if len(new_mutex) > 1:
            new_groups.append(SASMutexGroup(facts=new_mutex))

    return new_groups


def process_axioms(axioms, variables, vars_vals_map, is_fact_relevant):
    new_axioms = []
    for axiom in axioms:
        # All conditions of axioms are marked as relevant, we could skip this?
        conditions = [(var, vars_vals_map[var][val] if is_fact_relevant[var][val] else variables.ranges[var] - 1) for var, val in axiom.condition]
        effect_var = axiom.effect[0]
        effect_pre = axiom.effect[1]
        if effect_pre != -1:
            # All conditions of axioms are marked as relevant, we could skip this?
            effect_pre = vars_vals_map[effect_var][effect_pre] if is_fact_relevant[effect_var][effect_pre] else variables.ranges[effect_var] - 1
        effect_pos = axiom.effect[2] if is_fact_relevant[effect_var][axiom.effect[2]] else variables.ranges[effect_var] - 1
        effect = (effect_var, effect_pos)
        new_axioms.append(SASAxiom(conditions, effect))

    return new_axioms


# With a task and a plan, finds trivially necessary actions in the plan. (related to landmarks)
# When solving MR and MLR (action order maintained), trivially necessary actions are those that cannot be skipped.
# Either because they are the only action that achieves a goal
# Or because they are the only action that achieves a precondition for another triv. nec. action
def find_triv_nec_actions(init, goal, variables, plan, reach_fix_point):
    # Meassure time to identify triv. nec. actions
    init_time = process_time()

    # Find achievers for each fact
    fact_achievers = [[[] for _ in range(dom_size)] for dom_size in variables.ranges]

    # Facts achieved by the initial state
    for var, val in enumerate(init.values):
        fact_achievers[var][val].append([-1, len(plan) + 2])

    # For each operator what facts they achieve
    for index, op in enumerate(plan):
        for var, _, new_val, _  in op.pre_post:
            # Keeping track of until when a value is true. When a new triv. nec. action is found this value might be updated
            fact_achievers[var][new_val].append([index, len(plan) + 2])

    # Add virtual goal action. prevail is goal conditions, used for ease of implementation
    virtual_goal_action = SASOperator(name='virtual_goal', prevail=[(var, val) for var, val in goal.pairs], pre_post=[], cost=0)
    # Copy the operators
    extended_plan = plan[:]
    extended_plan.append(virtual_goal_action)

    # List to store what operators are triv. nec. If an op. is triv. nec., is because one of it's effects is needed
    # Here we keep track of what effects (var, new_val) make each operator triv. nec.
    # An empty means the operator is not triv. nec.
    triv_nec = [set() for _ in extended_plan]

    # The virtual goal is triv. nec., but by definition and not because of it's effects
    triv_nec[-1] = (set([-1]))
    is_fix_point = False

    while not is_fix_point:
        is_fix_point = True
        # Check, in reverse order, for trivially nec actions
        for op_index in range(len(extended_plan) - 1, -1, -1):
            # If current act is triv. nec, its' preconds are neccessary
            if triv_nec[op_index]:
                current_op = extended_plan[op_index]
                for var, val in current_op.prevail:
                    # Find achievers for current precondition at current plan step.
                    current_achievers = [achiever[0] for achiever in fact_achievers[var][val] if achiever[0] < op_index and achiever[1] >= op_index]

                    # If the op. is triv nec, update the fact achievers information
                    if check_and_update_triv_nec(var, val, current_achievers, triv_nec) and reach_fix_point:
                        update_achievers(current_achievers[0], extended_plan[current_achievers[0]], fact_achievers, triv_nec)
                        is_fix_point = False

                # Now checking for preconditions in pre_post.
                for var, val, new_val, eff_conditions in current_op.pre_post:
                    # If there are no effect conditions, the pre is necessary
                    # If there are effect conditions and this particular effect was the reason the current op. was labeled as triv. nec
                    # Then all it's effect conditions are necessary
                    if not eff_conditions or (var, new_val) in triv_nec[op_index]:
                        current_achievers = [achiever[0] for achiever in fact_achievers[var][val] if achiever[0] < op_index and achiever[1] >= op_index]
                        if check_and_update_triv_nec(var, val, current_achievers, triv_nec) and reach_fix_point:
                            update_achievers(current_achievers[0], extended_plan[current_achievers[0]], fact_achievers, triv_nec)
                            is_fix_point = False

                        # Check for new triv. nec. ops in the effect conditions
                        for (cond_var, cond_val) in eff_conditions:
                            current_achievers = [achiever[0] for achiever in fact_achievers[cond_var][cond_val] if achiever[0] < op_index and achiever[1] >= op_index]
                            if check_and_update_triv_nec(cond_var, cond_val, current_achievers, triv_nec) and reach_fix_point:
                                update_achievers(current_achievers[0], extended_plan[current_achievers[0]], fact_achievers, triv_nec)
                                is_fix_point = False

    print(f"Trivially necessary actions time: {process_time() - init_time:.3f}")
    print(f"Number of triv. nec. actions: {sum(1 for elem in triv_nec if elem)}")
    return [bool(elem) for elem in triv_nec], fact_achievers


# When a new triv. nec. action was found, update the fact achievers
# Using prepost the triv. nec. operator, change until when each achiever
# is actually an achiever.
def update_achievers(triv_nec_op_index, triv_nec_op, fact_achievers, triv_nec):
    # For each variable in the pre_post
    for var, _, new_val, eff_conditons in triv_nec_op.pre_post:
        # If there are no effect conditions, always update achiever information
        # Otherwise, only update information if this op. was labeled as triv. nec. because of this effect
        if not eff_conditons or (var, new_val) in triv_nec[triv_nec_op_index]:
            # For each val of the var
            for var_value, var_value_achievers in enumerate(fact_achievers[var]):
                if var_value != new_val:
                    # For each achiever of the val
                    for achiever in var_value_achievers:
                        # If the op. index is greater than operator used to update, break (ordered list)
                        if achiever[0] >= triv_nec_op_index:
                            break
                        # Else, update the last index in which this operator is an achiever for this var=val
                        achiever[1] = min(triv_nec_op_index, achiever[1])


# Checks if a new triv. nec. op was discovered and adds it to the list of triv. nec. ops if it was
def check_and_update_triv_nec(var, old_val, current_achievers, triv_nec):
    # If the precondition is not a wildcard and there's exactly one achiever
    if old_val > -1 and len(current_achievers) < 2:
        # If the achiever is not the initial state
        # And the achiever was not labeled as triv. nec. because of this fact before, update triv. nec. info
        if current_achievers[0] > -1 and (var, old_val) not in triv_nec[current_achievers[0]]:
            triv_nec[current_achievers[0]].add((var, old_val))
            return True

    # Op. was not idetified as triv. nec. for this fact.
    return False


# Finds triv. unnec. actions.
def find_triv_unnec_actions(init, goal, variables, plan, triv_nec, fact_achievers):
    # Add virtual goal action. prevail is goal conditions, used for ease of implementation
    virtual_goal_action = SASOperator(name='virtual_goal', prevail=[(var, val) for var, val in goal.pairs], pre_post=[], cost=0)
    # Extended plan for ease of implementation
    extended_plan = plan[:]
    extended_plan.append(virtual_goal_action)

    # For each action (index) what actions (possibly) consume its' effects on a variable
    producer_consumer = [set() for _ in extended_plan]

    # Keep track of variables overwritten by triv. nec. actions
    fact_overwritten = [[] for _ in variables.ranges]
    triv_unnec = [False for _ in extended_plan]

    for index, op in enumerate(extended_plan):
        for var, old_val, new_val, _  in op.pre_post:
            if triv_nec[index]:
                fact_overwritten[var].append(index)
            # All posible producers of this preconditon
            if old_val > -1:
                # For each operator, which values it produces are read by what other operators
                for producer_index in fact_achievers[var][old_val]:
                    if producer_index[0] > -1 and producer_index[0] < index <= producer_index[1]:
                        producer_consumer[producer_index[0]].add((index, var))

        for var, val in op.prevail:
            for producer_index in fact_achievers[var][val]:
                if producer_index[0] > -1 and producer_index[0] < index <= producer_index[1]:
                    producer_consumer[producer_index[0]].add((index, var))

    # Check, in reverse order, for trivially unnec. actions
    for op_index in range(len(extended_plan) - 1, -1, -1):
        if triv_nec[op_index]:
            # Triv nec actions cannot be triv. unnec.
            continue

        # All effects are only  read by other triv. unnec. actions. This covers the "not read by any action", too (vacuous truth).
        is_unnec = all(triv_unnec[consumer[0]] for consumer in producer_consumer[op_index])

        if not is_unnec:
            is_unnec = True
            for consumer_index, var in producer_consumer[op_index]:
                # For each consumer, at least one triv. nec. action overwrites the var before it's read!
                is_unnec &= any(op_index < over_writer < consumer_index for over_writer in fact_overwritten[var])

        triv_unnec[op_index] = is_unnec

    return triv_unnec


def main():
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-t', '--task', help='Path to task file in SAS+ format.',type=str, required=True)
    required_named.add_argument('-p', '--plan', help='Path to plan file.', type=str, required=True)
    parser.add_argument('--subsequence', help='Compiled task must guarantee maintaining order of original actions', action='store_true', default=False)
    parser.add_argument('--enhanced', help='Compiled task only creates skip actions for skippable actions', action='store_true', default=False)
    parser.add_argument('--macro-operators', help='Compiled task only creates macro operators for streaks of triv. nec. actions', action='store_true', default=False)
    parser.add_argument('--enhanced-unnecessary', help='Compiled task only includes actions that are not trivially unnecessary', action='store_true', default=False)
    parser.add_argument('--add-pos-to-goal', help='Add position variable to goals', action='store_true', default=False)
    parser.add_argument('--enhanced-fix-point', help='Iteratively find triv. nec. actions until a fixpoint is reached', action='store_true', default=False)
    parser.add_argument('--reduction', help='MR or MLR. MR=minimal reduction, MLR=minimal length reduction',type=str, default=MR)
    # Remove -f option for simplicity. Might want to add this again later
    # parser.add_argument('-f', '--file', help='Output file where reformulated SAS+ will be stored',type=str,default='minimal-reduction.sas')
    parser.add_argument('-d', '--directory', help='Output directory',type=str, default='.')
    parser.add_argument('--no-cost-scaling', dest="scale_costs", help='Do not scale costs even if the input task contains zero-cost actions. Using this option means that plans found with MR might not be perfectly justified.', action='store_false', default=True)
    options = parser.parse_args()
    options.file = 'action-elimination.sas'

    if options.task == None or options.plan == None:
        parser.print_help()
        sys.exit(2)

    parse_input_sas_time = process_time()
    task, operator_name_to_index_map = parse_task(options.task)
    plan, plan_cost = parse_plan(options.plan)
    parse_input_sas_time = process_time() - parse_input_sas_time
    print(f"Parse input SAS task and plan time: {parse_input_sas_time:.3f}")

    # Measure create task time
    create_task_time = process_time()
    new_task = create_action_elim_task(task, plan, operator_name_to_index_map, options.subsequence, \
                                       options.enhanced, options.reduction, options.add_pos_to_goal, \
                                       options.enhanced_fix_point, options.enhanced_unnecessary, \
                                       options.macro_operators, options.scale_costs)

    with open(os.path.join(options.directory, options.file), mode='w') as output_file:
        new_task.output(stream=output_file)

    create_task_time = process_time() - create_task_time
    print(f"Create AE task time: {create_task_time:.3f}")


if __name__ == '__main__':
    main()
