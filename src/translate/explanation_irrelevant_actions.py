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

def printing_consumer_producer(init_values_list,final_precond_effects_list):
    #falta el prevail
    all_facts_list = init_values_list
    for i in range(len(final_precond_effects_list)):
        action = final_precond_effects_list[i]
        print(f"Action {action[0]}")
        print("    Consumes:")
        for j in range(len(action[1])):
            fact_temp=action[1][j]  
            print(f"     -{fact_temp}")
            all_facts_list.remove(fact_temp)
        print("    Produces:")
        for j in range(len(action[2])):
            fact_temp=action[2][j]
            print(f"     -{fact_temp}")
            all_facts_list.append(fact_temp)                
        print()
    print(all_facts_list)

def creating_cons_prod(init_values_list,goal_values_list,final_precond_effects_list):
    #añadir los prevail DESDE ANTES
    list_final=[]

    for i in range(len(init_values_list)):
        elem= init_values_list[i]
        list_final.append((elem,[],[],[0])) # lista que tiene los elementos de la forma (fact,list prevail,list cons, list prod)

    for i in range(len(final_precond_effects_list)):
        action = final_precond_effects_list[i]
        precond = action[1]
        effects = action[2]
        for j in range(len(precond)):
            fact= precond[j]
            for k in range(len(list_final)):
                elem=list_final[k]
                if elem[0] == fact:
                    list_final[k][2].append(i+1) # se añadió para ese fact la action que lo consumió
        for l in range(len(effects)):
            elem= effects[l]
            exist=False
            for k in range(len(list_final)):
                elem2=list_final[k]
                if elem2[0] == elem:
                    exist=True
                    list_final[k][3].append(i+1)
                    break;
            if exist == False:
                list_final.append((elem,[],[],[i+1])) 

    for i in range(len(list_final)):
        elem = list_final[i]
        print(elem[0])
        print(f"Prevail list: {elem[1]}")
        print(f"Consumers list: {elem[2]}")
        print(f"Producers list: {elem[3]}")
        print() 
  
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
    print(f"Parse input SAS task and plan time: {parse_input_sas_time:.3f}")
    print()

    print(f"Plan (without skip actions): {plan1}  cost: {plan_cost1}\n")
    print(f"Plan (with skip actions): {plan2}  cost: {plan_cost2}\n")

    print()
    print("---> Initial State <---")  
    print(f"{task.init.values}")
    init_values_list = []
    for i in range(len(task.init.values)):
        elemento = task.init.values[i]
        fact = task.variables.value_names[i][elemento]
        init_values_list.append(fact)
        print(init_values_list[i]) 
    
    print()
    print("---> Goal State <---")
    goal_values_list = []
    print(f"{task.goal.pairs}")
    for i in range(len(task.goal.pairs)):
        elemento = task.goal.pairs[i]
        fact = task.variables.value_names[elemento[0]][elemento[1]]
        goal_values_list.append(fact)
        print(goal_values_list[i]) 

    print()
    print("---> Variables <---")
    var_values_list = []
    for i in range(len(task.variables.ranges)):
        print(f"var{i}")
        #print(f"number of different values: {task.variables.ranges[i]}")
        temp_list = []
        for j in range(task.variables.ranges[i]):
             val = task.variables.value_names[i][j]
             temp_list.append(val)
             
        var_values_list.append(temp_list)
        print(var_values_list[i])
        print()
    
    new_operators = get_operators_from_plan(task.operators, plan1, operator_name_to_index_map, options.subsequence)
    print("---> Operators in Plan <---")
    operators_list = []
    precond_actions_list = []
    effects_actions_list = []
    for i in range(len(new_operators)):
        print(new_operators[i].name)
        print(f"Prevail: {new_operators[i].prevail}")
        operators_list.append(new_operators[i].name)
        pre_post=new_operators[i].pre_post
        precond_temp = []
        effects_temp = []
        for j in range(len(pre_post)):
            print(pre_post[j])
            precond = task.variables.value_names[pre_post[j][0]][pre_post[j][1]]
            effects = task.variables.value_names[pre_post[j][0]][pre_post[j][2]]
            precond_temp.append(precond)
            effects_temp.append(effects)
            print(f"Precond: {precond}")
            print(f"Effects: {effects}")
        precond_actions_list.append(precond_temp)
        effects_actions_list.append(effects_temp)
        print()

    final_precond_effects_list = list(zip(operators_list, precond_actions_list, effects_actions_list))
    print(final_precond_effects_list)

    #printing_consumer_producer(init_values_list,final_precond_effects_list)

    creating_cons_prod(init_values_list,goal_values_list,final_precond_effects_list)
  
if __name__ == '__main__':
    main()