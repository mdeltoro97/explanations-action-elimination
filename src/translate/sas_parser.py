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

import sys, os
from sas_tasks import SASTask, SASVariables, SASOperator, SASInit, SASGoal, SASAxiom, SASMutexGroup
import subprocess


def parse_task(task_file, verify_parsed_task=False):
    variables = []
    domains = []
    mutex_groups = []
    init_values = []
    goal_values = []
    operators = []
    axiom_layers = []
    axioms = []
    current_line = ""
    ranges = []
    operator_name_to_index = {}

    def get_next_line():
        return sas_task.readline().strip()

    def get_next_int():
        return int(get_next_line())

    def get_next_int_pair():
        p1, p2 = get_next_line().split()
        return int(p1), int(p2)

    with open(task_file, 'r') as sas_task:
        # Read version
        current_line = get_next_line()
        assert(current_line == 'begin_version')
        version = get_next_int()
        if version != 3:
            sys.exit("Only version 3 supported.")
        current_line = get_next_line()
        assert(current_line == 'end_version')

        # Check metric
        current_line = get_next_line()
        assert(current_line == 'begin_metric')
        metric = get_next_line() != '0'
        current_line = get_next_line()
        assert(current_line == 'end_metric')

        # Read variables
        num_vars = get_next_int()
        for _ in range(num_vars):
            current_line = get_next_line()
            assert(current_line == 'begin_variable')

            # Name and axiom
            var_name = get_next_line()
            axiom_layer =  get_next_int()

            # Domain
            dom_size = get_next_int()
            ranges.append(dom_size)
            domain_vals = []
            for _ in range(dom_size):
                domain_vals.append(get_next_line())

            current_line = get_next_line()
            assert(current_line == 'end_variable')

            # Store var info
            variables.append(var_name)
            axiom_layers.append(axiom_layer)
            domains.append(domain_vals)

        variables = SASVariables(ranges=ranges, axiom_layers=axiom_layers,value_names=domains)
        # Read mutex groups
        num_mutex_groups = get_next_int()
        for _ in range(num_mutex_groups):
            current_line = get_next_line()
            assert(current_line == 'begin_mutex_group')
            current_group = []
            facts_in_group = get_next_int()
            for _ in range(facts_in_group):
                var, fact = get_next_int_pair()
                current_group.append((int(var), int(fact)))

            current_line = get_next_line()
            assert(current_line == 'end_mutex_group')

            # Create mutex group with empty facts
            # The constructor of SASMutexGroup reorders the facts.
            # This causes the parsed task to not be exactly equal to the task defined in the input file (diff. order facts in mutexes)
            # Creating the SASMutex and then adding the facts maintains order of the input task file
            mutex_groups.append(SASMutexGroup(facts=[]))
            mutex_groups[-1].facts = current_group

        # Read initial state
        current_line = get_next_line()
        assert(current_line == 'begin_state')

        for _ in range(num_vars):
            # Not going to check for domain of each variable, assume input sas is valid
            init_values.append(get_next_int())
        init_state = SASInit(init_values)

        current_line = get_next_line()
        assert(current_line == 'end_state')

        # Read goal
        current_line = get_next_line()
        assert(current_line == 'begin_goal')

        num_goals = get_next_int()
        for _ in range(num_goals):
            var, val = get_next_int_pair()
            goal_values.append((var,val))

        goal = SASGoal(pairs=goal_values)

        current_line = get_next_line()
        assert(current_line == 'end_goal')

        # Read operators
        num_operators = get_next_int()
        for operator_index in range(num_operators):
            current_line = get_next_line()
            assert(current_line == 'begin_operator')

            # Name and prevail conditions.
            operator_name = '(%s)' % sas_task.readline().rstrip('\n')
            prevail_cond = []
            num_prevail_cond = get_next_int()
            for _ in range(num_prevail_cond):
                var, val = get_next_int_pair()
                prevail_cond.append((var,val))

            # Effects
            effects = []
            num_effects = get_next_int()
            for _ in range(num_effects):
                cond_effects = []
                effect_information = sas_task.readline().strip().split()
                effect_information = [int(x) for x in effect_information]
                num_cond_effects, *cond_effects, var_number, old_val, new_val = effect_information
                cond_effects = list(zip(cond_effects[0::2], cond_effects[1::2]))
                effects.append((var_number, old_val, new_val, cond_effects))

            cost = get_next_int()
            current_line = get_next_line()
            assert(current_line == 'end_operator')

            # Create operator with empty prev, pre_post.
            # The constructor of SASOperator reorders the prevail and pre_post.
            # This causes the parsed task to not be exactly equal to the task defined in the input file (diff. order of prevails, pre_posts)
            # Creating the SASOpertor and then adding the prevail, pre_post maintains order of the input task file.
            operators.append(SASOperator(name=operator_name, prevail=[], pre_post=[], cost=cost))
            operators[-1].prevail = prevail_cond
            operators[-1].pre_post = effects
            if operator_name in operator_name_to_index:
                sys.exit("Multiple actions with the same name not supported by action elimination.")
            operator_name_to_index[operator_name] = operator_index

        # Axioms...
        num_axioms = get_next_int()
        if num_axioms > 0:
            sys.exit("Axioms not supported by action elimination module.")
        for _ in range(num_axioms):
            current_line = get_next_line()
            assert(current_line == 'begin_rule')

            num_cond = get_next_int()
            conditions = []
            for _ in range(num_cond):
                var, val = get_next_int_pair()
                conditions.append((var, val))

            var, old_val, new_val = sas_task.readline().strip().split()
            effect = (int(var), int(old_val), int(new_val))

            current_line = get_next_line()
            assert(current_line == 'end_rule')

            axioms.append(SASAxiom(condition=conditions, effect=effect))


    # Verify that the read task is equal to original file
    if verify_parsed_task:
        task = SASTask(variables=variables, mutexes=mutex_groups, init=init_state, goal=goal, operators=operators, axioms=axioms, metric=metric)
        verify_file = task_file + ".verify-contents.sas"
        with open(verify_file, mode='w') as output_file:
            task.output(stream=output_file)

        try:
            # Some trailing whitespaces and empty lines might mess with filecmp, so now using this.
            # Did not find a direct way to use filecmp while ignoring trailing whtiespaces and empty lines.
            are_different = subprocess.check_output(['diff', '-ZB', task_file, verify_file]).decode('utf-8')
        except subprocess.CalledProcessError as e:
            are_different = True
        assert not are_different, "Read task is not equal to input task."

        os.remove(verify_file)

    return SASTask(variables=variables, mutexes=mutex_groups, init=init_state, goal=goal, operators=operators, axioms=axioms, metric=metric), operator_name_to_index