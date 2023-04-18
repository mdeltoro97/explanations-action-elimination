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

from numpy import var
from sas_tasks import SASTask, SASVariables, SASOperator, SASInit, SASGoal, SASAxiom, SASMutexGroup
from plan_parser import parse_plan
from sas_parser import parse_task
from simplify import filter_unreachable_propositions
from variable_order import find_and_apply_variable_order
import argparse

MR  = 'MR'
MLR = 'MLR'

def create_action_elim_task(sas_task, plan, operator_name_to_index, ordered=False):
    # Used to remove unused variables from task
    var_number = 0

    if ordered:
        order_var_index = 0
        var_number = 1
        ordered_var_range = len(plan) + 1
        ordered_var_values = ['Atom last-action(%i)' % i for i in range(ordered_var_range)]

    new_vars_dict = dict()

    # Process new goal
    new_goal, var_number = process_goal_state(sas_task.goal, new_vars_dict, var_number)

    # Process operators
    new_operators = process_operators(sas_task.operators, plan, operator_name_to_index, var_number, new_vars_dict, ordered)
    
    # Process mutexes
    new_mutexes = process_mutex_groups(sas_task.mutexes, new_vars_dict)

    # Process init state
    new_init = process_init_state(sas_task.init, new_vars_dict, ordered)

    # Process axioms
    new_axioms = process_axioms(sas_task.axioms, new_vars_dict, sas_task.init)

    # Process variables
    if ordered:
        new_variables = process_variables(sas_task.variables, new_vars_dict, (ordered_var_range, -1, ordered_var_values))
    else:
        new_variables = process_variables(sas_task.variables, new_vars_dict)
        
    new_task = SASTask(variables=new_variables,
            mutexes=new_mutexes, init=new_init, goal=new_goal,
            operators=new_operators, axioms=new_axioms, metric=sas_task.metric)

    return new_task

def process_goal_state(goal_state, new_vars_dict, var_number=0):
    new_goal = list()
    for var, val in goal_state.pairs:
        new_vars_dict[var] = var_number
        new_goal.append((var_number, val))
        var_number += 1

    return SASGoal(pairs=new_goal), var_number

def process_operators(operators, plan, operator_name_to_index, var_number, new_vars_dict, ordered=False):
    new_operators = list()
    for op_index, operator in enumerate(plan):
        current_op = operators[operator_name_to_index[operator]]
        prevail = list()
        pre_post = list()
        conditionals = list()

        if ordered:
            print('what')
            # Adding skip action i action
            # The var used to maitain order has index 0!
            new_operators.append(SASOperator(name='(skip-action(%i))' % op_index, prevail=[], pre_post=[(0, op_index, op_index + 1, [])], cost=0))

        # Map variables to new vars...
        # Start with prevail
        for var, val in current_op.prevail:
            # Add to map if it's not there. Take value otherwise
            if var not in new_vars_dict:
                current_var = var_number
                new_vars_dict[var] = var_number
                var_number += 1
            else:
                current_var = new_vars_dict[var]
            prevail.append((current_var, val))

        # Pre_post var mapping..
        for var, old_val, new_val, conditional_eff in current_op.pre_post:
            
            if var not in new_vars_dict:
                current_var = var_number
                new_vars_dict[var] = var_number
                var_number += 1
            else:
                current_var = new_vars_dict[var]
            
            # Mapping cond effects...
            for cond_var, cond_old, cond_new in conditional_eff:
                if cond_var not in new_vars_dict:
                    current_cond_var = var_number
                    new_vars_dict[cond_var] = var_number
                    var_number += 1
                else:
                    current_cond_var = new_vars_dict[cond_var]
                
                conditionals.append((current_cond_var, cond_old, cond_new))
            
            # Add the pre_post
            pre_post.append((current_var, old_val, new_val, conditionals))
        
        if ordered:
            # Add order constraint to pre_post
            pre_post.append((0, op_index, op_index + 1, []))

        new_operators.append(SASOperator(name=operator, prevail=prevail, pre_post=pre_post, cost=current_op.cost))       

    print([op.name for op in new_operators])
    return new_operators

def process_mutex_groups(mutex_groups, new_vars_dict):
    new_mutexes = list()
    for group in mutex_groups:
        new_group = list()
        for var, val in group.facts:
            if var in new_vars_dict:
                new_group.append(((new_vars_dict[var], val)))
        
        if len(new_group) > 1: 
            new_mutexes.append(SASMutexGroup(facts=new_group))
    
    return  new_mutexes

def process_init_state(init_state, new_vars_dict, ordered=False):
    new_init = list()

    if ordered:
        # Add initial order var value. Order var index is always 0!
        new_init.append(0)

    for old_index, _ in sorted(new_vars_dict.items(), key=lambda x: x[1]):
        new_init.append(init_state.values[old_index])

    return SASInit(values=new_init)

def process_axioms(axioms, new_vars_dict, init_state):
    new_axioms = list()
    for axiom in axioms:
        valid_axiom = True
        conditions = list()
        if axiom.effect[0] in new_vars_dict:
            for var, val in axiom.condition:
                # If var is not affected by new operators and values is not in init, useless axiom
                if var not in new_vars_dict and init_state.values[var] != val:
                    valid_axiom = False
                    break
                # If var is in new operators, add condition.
                elif var in new_vars_dict:
                    conditions.append((var, val))
            
            if valid_axiom:
                new_axioms.append(SASAxiom(condition=conditions, effect=(new_vars_dict[axiom.effect[0]], axiom.effect[1])))
    
    return axioms

def process_variables(variables, new_vars_dict, order_var_info=None):
    new_ranges = list()
    new_axiom_layers = list()
    new_value_names = list()

    # Add variable to maintain action order
    if order_var_info:
        new_ranges.append(order_var_info[0])
        new_axiom_layers.append(order_var_info[1])
        new_value_names.append(order_var_info[2])
    
    for old_index, new_index in sorted(new_vars_dict.items(), key=lambda x: x[1]):
        new_ranges.append(variables.ranges[old_index])
        new_axiom_layers.append(variables.axiom_layers[old_index])
        new_value_names.append(variables.value_names[old_index])

    return SASVariables(ranges=new_ranges, axiom_layers=new_axiom_layers, value_names=new_value_names)

def main():
    parser = argparse.ArgumentParser(description='Creates an action elimination domain for an automated planning task and a valid plan.')
    parser.add_argument('-t', '--task', help='Path to task file in SAS+ format.',type=str)
    parser.add_argument('-p', '--plan', help='Path to plan file.', type=str)
    parser.add_argument('-s', '--subsequece', help='Compiled task must guarantee maintaing order of original actions', type=bool, default=True)
    parser.add_argument('-r', '--reduction', help='MR or MLR. MR=minimal reduction, MLR=minimal length reduction',type=str, default=MR)
    parser.add_argument('-f', '--file', help='Output file',type=str,default='')
    parser.add_argument('-d', '--directory', help='Output directory',type=str, default='.')
    options = parser.parse_args()
    
    if options.task == None or options.plan == None:
        parser.print_help()
        exit(-1)

    task, operator_name_to_index_map = parse_task(options.task)
    plan_size, plan, plan_cost = parse_plan(options.plan)
    new_task = create_action_elim_task(task, plan, operator_name_to_index_map, True)
    
    with open('salida1.txt', mode='w') as output_file:
        new_task.output(stream=output_file)
    
if __name__ == '__main__':
    main()