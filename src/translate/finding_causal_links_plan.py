import argparse
import json
import sys
from time import process_time
from math import inf, ceil
from copy import deepcopy

from plan_parser import parse_plan
from sas_parser import parse_task

from itertools import zip_longest

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
    
def extracting_causal_links(init_values_list,final_precond_effects_list):
    list_final=[]

    for i in range(len(init_values_list)):
        elem= init_values_list[i]
        list_final.append([[0],elem,[]]) 


    for i in range(len(final_precond_effects_list)):
        action = final_precond_effects_list[i]
        precond = action[1]
        effects = action[2]
        for j in range(len(precond)):
            fact= precond[j]
            for k in range(len(list_final)):
                elem=list_final[k]
                if elem[1] == fact:
                    if elem[2] == [-1]:
                        list_final[k][2]=[i+1]
                    else:
                        list_final[k][2].append(i+1) # se añadió para ese fact la action que lo consumió
        for l in range(len(effects)):
            elem= effects[l]
            exist=False
            for k in range(len(list_final)):
                elem2=list_final[k]
                if elem2[1] == elem:
                    exist=True
                    list_final[k][0].append(i+1)
                    break;
            if exist == False:
                list_final.append([[i+1],elem,[]]) 

    list_final2=[]
    for i in range(len(list_final)):
        elem = list_final[i]
        producers = elem[0]
        consumers = elem[2]
        for j in range(len(producers)):
            if j < len(consumers):
                list_final2.append((producers[j], elem[1], consumers[j]))
            else:
                list_final2.append((producers[j], elem[1], -1))

        
    print(list_final2) 
        
    # for i in range(len(final_precond_effects_list)):
    #     precond = final_precond_effects_list[i][1]
    #     effects = final_precond_effects_list[i][2]
    #     for j in range(len(precond)):
    #         fact= precond[j]
    #         for k in range(len(list_temp)):
    #             elem=list_temp[k]
    #             if elem[1] == fact:
    #                 if(elem[2] == -1):
    #                     list_temp[k][2]=i+1
    #                 else:
    #                     list_temp.append([elem[0],elem[1],i+1])

                  
                    
           
        # for j in range(len(effects)):
        #     fact= effects[j]
        #     for k in range(len(list_temp)):
        #         elem=list_temp[k]
        #         if elem[1] == fact:
        #             list_temp.append([i+1,elem[1],-1])
  
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

    
    init_values_list = []
    for i in range(len(task.init.values)):
        elemento = task.init.values[i]
        fact = task.variables.value_names[i][elemento]
        init_values_list.append(fact)
    
      
    new_operators = get_operators_from_plan(task.operators, plan1, operator_name_to_index_map, options.subsequence)
    #print("---> Operators in Plan <---")
    operators_list = []
    precond_actions_list = []
    effects_actions_list = []
    for i in range(len(new_operators)):
        #print(new_operators[i].name)
        #print(f"Prevail: {new_operators[i].prevail}")
        #AÑadir el prevail
        operators_list.append(new_operators[i].name)
        pre_post=new_operators[i].pre_post
        precond_temp = []
        effects_temp = []
        for j in range(len(pre_post)):
            #print(pre_post[j])
            precond = task.variables.value_names[pre_post[j][0]][pre_post[j][1]]
            effects = task.variables.value_names[pre_post[j][0]][pre_post[j][2]]
            precond_temp.append(precond)
            effects_temp.append(effects)
            #print(f"Precond: {precond}")
            #print(f"Effects: {effects}")
        precond_actions_list.append(precond_temp)
        effects_actions_list.append(effects_temp)
        #print()

    final_precond_effects_list = list(zip(operators_list, precond_actions_list, effects_actions_list))
    #print(final_precond_effects_list)

    #printing_consumer_producer(init_values_list,final_precond_effects_list)

    #creating_cons_prod(init_values_list,final_precond_effects_list)

    extracting_causal_links(init_values_list,final_precond_effects_list)
  
if __name__ == '__main__':
    main()