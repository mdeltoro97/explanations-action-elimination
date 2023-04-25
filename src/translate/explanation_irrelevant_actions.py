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

def main():
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-t', '--task', help='Path to task file in SAS+ format.',type=str, required=True)
    required_named.add_argument('-p1', '--plan1', help='Path to plan file.', type=str, required=True)
    required_named.add_argument('-p2', '--plan2', help='Path to plan with skip actions file.', type=str, required=True)
    parser.add_argument('--macro-operators', help='Compiled task only creates macro operators for streaks of triv. nec. actions', action='store_true', default=False)
    options = parser.parse_args()
    options.file = 'action-elimination.sas'

    if options.task == None or options.plan1 == None or options.plan2 == None:
        parser.print_help()
        sys.exit(2)

    parse_input_sas_time = process_time()
    task, operator_name_to_index_map = parse_task(options.task)
    plan1, plan_cost1 = parse_plan(options.plan1)
    plan2, plan_cost2 = parse_plan(options.plan2)
    parse_input_sas_time = process_time() - parse_input_sas_time
    print(f"Parse input SAS task and plan time: {parse_input_sas_time:.3f}")

    # Measure create task time
    create_task_time = process_time()
    #new_task = create_action_elim_task(task, plan, operator_name_to_index_map, options.subsequence, \
    #                                   options.enhanced, options.reduction, options.add_pos_to_goal, \
    #                                   options.enhanced_fix_point, options.enhanced_unnecessary, \
    #                                   options.macro_operators, options.scale_costs)

    #with open(os.path.join(options.directory, options.file), mode='w') as output_file:
    #    new_task.output(stream=output_file)

    #print(f"Axiom layers: {task.variables.axiom_layers}\n")
    print(f"Operators: {operator_name_to_index_map}\n")
    print(f"Plan#1 : {plan1}\n")
    print(f"Plan (without skip actions) cost: {plan_cost1}\n")
    print(f"Plan#2 : {plan2}\n")
    print(f"Plan (with skip actions) cost: {plan_cost2}\n")
    task.dump()
    create_task_time = process_time() - create_task_time
    
    print()
    print("---> Initial State <---")  
    print(f"{task.init.values}")
    for i in range(len(task.init.values)):
        elemento = task.init.values[i]
        print(task.variables.value_names[i][elemento]) 
    
    print()
    print("---> Goal State <---")
    print(f"{task.goal.pairs}")
    for i in range(len(task.goal.pairs)):
        elemento = task.goal.pairs[i]
        print(task.variables.value_names[elemento[0]][elemento[1]]) 

    print()
    print("---> Variables <---")
    for i in range(len(task.variables.ranges)):
        print(f"var{i}")
        print(f"number of different values: {task.variables.ranges[i]}")
        for j in range(task.variables.ranges[i]):
             print(task.variables.value_names[i][j])
        print()
    
    print()
    print(f"Create explanation task time: {create_task_time:.3f}")

if __name__ == '__main__':
    main()