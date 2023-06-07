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

    return list_final2
        

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
    operators_list = []
    precond_actions_list = []
    effects_actions_list = []
    for i in range(len(new_operators)):
        #print(f"Prevail: {new_operators[i].prevail}")
        #Añadir el prevail
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
        precond_actions_list.append(precond_temp)
        effects_actions_list.append(effects_temp)

    final_precond_effects_list = list(zip(operators_list, precond_actions_list, effects_actions_list))

    list_causal_links = extracting_causal_links(init_values_list,final_precond_effects_list)
    print(list_causal_links)

    #aqui tengo que determinar si el plan esta perfectamente justificado o no. En caso negativo hacer lo de abajo, sino sacar un mensaje de que está perfect justif y que no hay acciones irr
    
    list_pos_irr_actions=[]
    for elemento in plan2:
        if 'skip-action' in elemento:
            numero = ''.join(filter(str.isdigit, elemento))
            list_pos_irr_actions.append(int(numero)+1)

    print()
    print(f"Irrelevant actions in the plan: {list_pos_irr_actions}\n")

    #list_causal_links = [(0, 'Atom ontable(c)', 1), (0, 'Atom ontable(d)', -1), (0, 'Atom clear(c)', 1), (2, 'Atom clear(c)', -1), (0, 'Atom clear(d)', 2), (0, 'Atom clear(b)', 4), (0, 'Atom handempty()', 1), (2, 'Atom handempty()', -1), (4, 'Atom handempty()', -1), (0, 'Atom ontable(b)', -1), (0, 'Atom ontable(a)', 3), (0, 'Atom clear(a)', 3), (4, 'Atom clear(a)', -1), (1, 'NegatedAtom clear(c)', -1), (1, 'NegatedAtom handempty()', -1), (3, 'NegatedAtom handempty()', 4), (1, 'Atom holding(c)', -1), (2, 'NegatedAtom clear(d)', -1), (2, 'Atom on(c, d)', -1), (3, 'NegatedAtom clear(a)', 4), (3, 'Atom holding(a)', 4), (4, 'NegatedAtom clear(b)', -1), (4, 'Atom on(a, b)', -1)]
   
          
    for i in range(len(plan1)):
        todos_menos_uno = True
        irr = False
        temp_list = []
        
        for j in range(len(list_causal_links)):
            elemento = list_causal_links[j]
            if elemento[0] == i and i in list_pos_irr_actions:
                irr = True
                temp_list.append(elemento)

        for elemento in temp_list:
            if elemento[2] != -1:
                todos_menos_uno = False
                break

        if todos_menos_uno and irr:
            print(f"Action #{i}", plan1[i], " is irrelevant since it produces facts that are not consumed by anyone.")
          




        







    # dict_case1 = {}
    # list_case2 = []
    # list_case3 = []

    # for i in range(len(list_causal_links)):
    #     elemento = list_causal_links[i]
    #     if elemento[0] in list_pos_irr_actions:            
    #         if  elemento[2]==-1: 
    #             # Case 1: What irrelevant actions produce is not consumed by anyone
    #             key = str(elemento[0])  # Convertir el primer elemento de la tupla a cadena
    #             value = elemento[1]  # Segundo elemento de la tupla
    #             if key in dict_case1:
    #                 dict_case1[key].append(value)
    #             else:
    #                 dict_case1[key] = [value]
                
                
    #     #     elif elemento[2] in list_pos_irr_actions:
    #     #         # Case 2: What irrelevant actions produce are consumed only by irrelevant actions
    #     #         list_case2.append(elemento)
    #     # else:
    #     #     # Case #3: Presence of at least one relevant action in the causal link
    #     #     list_case3.append(elemento)

    
    # if bool(dict_case1):
    #     for key, values in dict_case1.items():
    #         print(f"Action #{key}", plan1[int(key)-1], " is irrelevant since it produces", ", ".join(values), "that are facts that are not consumed by anyone.")
  
if __name__ == '__main__':
    main()