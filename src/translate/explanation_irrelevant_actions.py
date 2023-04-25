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


def main():
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-t', '--task', help='Path to task file in SAS+ format.',type=str, required=True)
    required_named.add_argument('-p1', '--plan1', help='Path to plan file.', type=str, required=True)
    required_named.add_argument('-p2', '--plan2', help='Path to plan with skip actions file.', type=str, required=True)
    parser.add_argument('--subsequence', help='Compiled task must guarantee maintaining order of original actions', action='store_true', default=False)
    parser.add_argument('--macro-operators', help='Compiled task only creates macro operators for streaks of triv. nec. actions', action='store_true', default=False)
    options = parser.parse_args()
    options.file = 'action-elimination2.sas'

    if options.task == None or options.plan1 == None or options.plan2 == None:
        parser.print_help()
        sys.exit(2)

    parse_input_sas_time = process_time()
    task, operator_name_to_index_map = parse_task(options.task)
    plan1, plan_cost1 = parse_plan(options.plan1)
    plan2, plan_cost2 = parse_plan(options.plan2)
    parse_input_sas_time = process_time() - parse_input_sas_time
    
    print()
    print(f"Parse input SAS task and plan time: {parse_input_sas_time:.3f}")
    print()

    print(f"Plan (without skip actions): {plan1}  cost: {plan_cost1}\n")
    print(f"Plan (with skip actions): {plan2}  cost: {plan_cost2}\n")

    # Measure create task time
    create_task_time = process_time()
 

    #print(f"Operators: {operator_name_to_index_map}\n")
    #print()
    
    #task.dump()
    create_task_time = process_time() - create_task_time
    
    print()
    print("---> Initial State <---")  
    print(f"{task.init.values}")
    init_values_list = []
    for i in range(len(task.init.values)):
        elemento = task.init.values[i]
        fact = task.variables.value_names[i][elemento].replace("Atom ", "") 
        init_values_list.append(fact)
        print(init_values_list[i]) 
    
    print()
    print("---> Goal State <---")
    goal_values_list = []
    print(f"{task.goal.pairs}")
    for i in range(len(task.goal.pairs)):
        elemento = task.goal.pairs[i]
        fact = task.variables.value_names[elemento[0]][elemento[1]].replace("Atom ", "")
        goal_values_list.append(fact)
        print(goal_values_list[i]) 

    print()
    print("---> Variables <---")
    for i in range(len(task.variables.ranges)):
        print(f"var{i}")
        print(f"number of different values: {task.variables.ranges[i]}")
        for j in range(task.variables.ranges[i]):
             print(task.variables.value_names[i][j])
        print()
    
    new_operators = get_operators_from_plan(task.operators, plan1, operator_name_to_index_map, options.subsequence)
    print("---> Operators <---")
    for i in range(len(new_operators)):
        print(new_operators[i].name)
        pre_post=new_operators[i].pre_post
        for j in range(len(pre_post)):
            print(pre_post[j])
            print(f"Precond: {task.variables.value_names[pre_post[j][0]][pre_post[j][1]]}")
            print(f"Effects: {task.variables.value_names[pre_post[j][0]][pre_post[j][2]]}")
        
        print()

    print()
    print(f"Create explanation task time: {create_task_time:.3f}")
  
if __name__ == '__main__':
    main()