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

def obtaining_objects_from_actions(list_actions):
    list_objects = []
    for elemento in list_actions:
        inicio = elemento.find('(')
        fin = elemento.find(')')
        if inicio != -1 and fin != -1:
            contenido = elemento[inicio + 1:fin]
            if contenido:
                subelementos = [x.strip() for x in contenido.split(',') if x.strip()]
                for subelemento in subelementos:
                    if subelemento not in list_objects:
                        list_objects.append(subelemento)
    return list_objects

def identifying_irrelevant_objects(list_initial_state, list_goal_state, list_actions_plan, list_pos_irr_actions):
    print('---> Identifying irrelevant objects <---')
    
    #Identifying non-goal state objects that could be irrelevant if not included in relevant actions.
    list_objects = [elemento for elemento in list_initial_state if elemento not in list_goal_state]

    # Objects present in relevant actions are considered relevant, regardless of their presence in the goal state; otherwise, they are not considered relevant.
    for i, element in enumerate(list_actions_plan):
        if i not in list_pos_irr_actions:
           objects = element[element.find(' ') + 1:-1].split()
           for temp in objects:
                if temp in list_objects:
                    list_objects.remove(temp)
    # Printing irrelevant objects, in case they exist (those not found in relevant actions) 
    if len(list_objects) == 0:
        print(f"There are no irrelevant objects.\n")   
    else:
        elementos = ", ".join(list_objects)
        print(f"Objects [{elementos}] are irrelevant.\n")

def main():
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-t', '--task', help='Path to task file in SAS+ format.',type=str, required=True)
    required_named.add_argument('-p1', '--plan1', help='Path to plan file.', type=str, required=True)
    required_named.add_argument('-p2', '--plan2', help='Path to plan with skip actions file.', type=str, required=True)
    parser.add_argument('--subsequence', help='Compiled task must guarantee maintaining order of original actions', action='store_true', default=False)
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
    print(f"Parse input SAS task and plan time: {parse_input_sas_time:.3f}\n")
   

    print(f"Plan (without skip actions): {plan1}  cost: {plan_cost1}\n")
    print(f"Plan (with skip actions): {plan2}  cost: {plan_cost2}\n")

    list_pos_irr_actions=[]
    for elemento in plan2:
        if 'skip-action' in elemento:
            numero = ''.join(filter(str.isdigit, elemento))
            list_pos_irr_actions.append(int(numero))

    print(f"Positions of the irrelevant actions in the plan: {list_pos_irr_actions}\n")
   
    init_values_list = []
    for i in range(len(task.init.values)):
        elemento = task.init.values[i]
        fact = task.variables.value_names[i][elemento]
        init_values_list.append(fact)

    list_objects_initial_state = obtaining_objects_from_actions(init_values_list)
    print(f"List of objects contained in the initial state: {list_objects_initial_state}\n")
    
    goal_values_list = []
    for i in range(len(task.goal.pairs)):
        elemento = task.goal.pairs[i]
        fact = task.variables.value_names[elemento[0]][elemento[1]]
        goal_values_list.append(fact) 

    list_objects_goal_state = obtaining_objects_from_actions(goal_values_list)
    print(f"List of objects contained in the goal state: {list_objects_goal_state}\n")

    identifying_irrelevant_objects(list_objects_initial_state,list_objects_goal_state, plan1, list_pos_irr_actions)
  
if __name__ == '__main__':
    main()