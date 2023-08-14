#!/usr/bin/env python3

#######################################################################
#
# Author: Martha Maria Del Toro Carballo
# Copyright 2023
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

"""
TODO: explain the stuff
"""


import argparse
import subprocess
import sys
from copy import deepcopy
from collections import defaultdict


from plan_parser import parse_plan
from sas_parser import parse_task

def get_operators_from_plan(operators, plan, operator_name_to_index, ordered):

    plan_operators= []
    added = set()
    
    for op in plan:   
        if 'skip-action' in op:
            plan_operators += [None]
        else:    
            if ordered:
                # Ordered tasks create a different operator for each operator in the plan
                plan_operators += [deepcopy(operators[operator_name_to_index[op]])]
            else:
                # Unordered tasks create a different operator for each unique operator in the plan
                # added.add(op) is only used for its' side effects.
                # set.add(x) always returns None so it doesn't affect the condition
                if (not op in added or added.add(op)):
                    plan_operators += [operators[operator_name_to_index[op]]] 

    return plan_operators

def is_perfectly_justified(plan):
    for action in plan:
        if 'skip-action' in action:
            return False
    return True


# TODO: revise this code. It was modified to make it more readable
def get_var_pre_post_list(operators): 
    """
    Obtains a list where each position represents an action, and contains a list of tuples in the form 
    [list of (var, precond_val), list of (var, prevail_val), list of (var, eff_val)]
      """
    op_precond_list = []
    op_prevail_list = [] 
    op_eff_list = []  
      
    for op in operators:
        op_precond = []
        op_prevail = []
        op_eff = []
        
        if not op is None:
            for prevail_val in op.prevail:
                op_prevail+= [(prevail_val[0], prevail_val[1])]

        if not op is None:
            for var, precond_val, eff_val, _ in op.pre_post:
                op_precond += [(var, precond_val)]
                op_eff += [(var, eff_val)]

        op_precond_list += [op_precond]
        op_prevail_list += [op_prevail]
        op_eff_list += [op_eff]

    precond_prevail_list = []
    for precond_sublist, prevail_sublist in zip(op_precond_list, op_prevail_list):
        if not prevail_sublist:
            precond_prevail_list.append(precond_sublist)
        else:
            precond_prevail_combined = precond_sublist + prevail_sublist
            precond_prevail_list.append(precond_prevail_combined)

    return list(zip(precond_prevail_list, op_eff_list)), op_prevail_list
    
def get_prevail_link(prevail_link):
    producers_list, fact , consumer = prevail_link
    producers_list.sort()
  
    last_producer_for_consumer = max(filter(lambda x: x < consumer, producers_list))
   
    return (last_producer_for_consumer, fact, consumer)

# TODO: make this code more readable    
def extract_causal_links(task, plan_operators):

    # Obtain the values of the initial state of the form (var,val)
    list_causal_links = [[[0], (var, task.init.values[var]), []] for var in range(len(task.init.values))]

    list_causal_links_prevail =[]

    list_var_pre_post, op_prevail_list = get_var_pre_post_list(plan_operators)
    
    for i in range(len(list_var_pre_post)):
        list_precond = list_var_pre_post[i][0]
        list_effects = list_var_pre_post[i][1]
        for j in range(len(list_precond)):
            fact= list_precond[j]
            for k in range(len(list_causal_links)):
                causal_link_temp = list_causal_links[k]           
                if causal_link_temp[1] == fact or (causal_link_temp[1][1] == -fact[1] and causal_link_temp[1][0] == fact[0]):
                    if fact not in op_prevail_list[i]:
                        list_causal_links[k][2].append(i+1)
                    else:
                        # Analyze if the producer its ok, because I always assume that its the first
                        causal_link_prevail = (list_causal_links[k][0],fact,i+1)
                        list_causal_links_prevail.append(causal_link_prevail)
    
        for l in range(len(list_effects)):
            fact= list_effects[l]
            exist=False
            for k in range(len(list_causal_links)):
                causal_link_temp=list_causal_links[k]
                if causal_link_temp[1] == fact:
                    exist=True
                    list_causal_links[k][0].append(i+1)
                    break;
            if exist == False:
                list_causal_links.append([[i+1],fact,[]])

    list_causal_links_prevail = [get_prevail_link(prevail_link) for prevail_link in list_causal_links_prevail]

    list_causal_links_final=[]
    for i in range(len(list_causal_links)):
        causal_link_temp = list_causal_links[i]
        fact = task.variables.value_names[causal_link_temp[1][0]][causal_link_temp[1][1]]
        producers = causal_link_temp[0]
        consumers = causal_link_temp[2]
        if "NegatedAtom" not in fact: 
            for j in range(len(producers)):
                if j < len(consumers):
                    list_causal_links_final.append((producers[j], causal_link_temp[1], consumers[j]))
                else:
                    list_causal_links_final.append((producers[j], causal_link_temp[1], -1))
    
    list_prevail_links_final=[]
    for i in range(len(list_causal_links_prevail)):
        causal_link_prevail = list_causal_links_prevail[i]
        fact = task.variables.value_names[causal_link_prevail[1][0]][causal_link_prevail[1][1]]
        producer = causal_link_prevail[0]
        consumer = causal_link_prevail[2]
        if "NegatedAtom" not in fact: 
            list_prevail_links_final.append((producer, causal_link_prevail[1], consumer))
    
    return list_causal_links_final, list_prevail_links_final


def pretty_print_causal_links (list_cl, plan_op, task):
    for (prod, (var, value), cons) in list_cl:
        prod_name = plan_op[prod-1].name if prod > 0 else "Init"
        cons_name = plan_op[cons-1].name if cons > 0 else "None"
        print(f"{prod_name :<25} -> {task.variables.value_names[var][value] :<25} -> {cons_name}")


def list_cl_to_dict(list_cl, is_key_producer = True):
    """
    Converts a list of causal links in the form [(producer, (var, value), consumer),...]
    into a dict where the keys can be the producers or the consumers depending
    on is_key_producer and the values lists of the remaining elements:
    producer: (consumer, var_value)
    consumer: (producer, var_value)
    """

    dict_cl = defaultdict(list)

    for (producer, var_value, consumer) in list_cl:
        dict_cl[producer if is_key_producer else consumer].append((consumer if is_key_producer else producer, var_value))
  
    return dict_cl

def exist_in_sas_plan(causal_link_temp_renamed, task, list_causal_links_sas_plan):
    for causal_link_temp in list_causal_links_sas_plan:
        fact_sas_plan = (causal_link_temp[0],task.variables.value_names[causal_link_temp[1][0]][causal_link_temp[1][1]], causal_link_temp[2])
        if fact_sas_plan == causal_link_temp_renamed:
            return True
    return False

def causal_chain(elements,ordered_dict, element, list_temp):
    for val in elements:
        if val not in list_temp:
            list_temp.append(val)
            list_temp2 = ordered_dict.get(val,[])
            elements2 = list(set([valor[0] for valor in list_temp2]))
            causal_chain(elements2,ordered_dict, element, list_temp)
    return list_temp
    
def causal_chains(list_cl_plan_ae, task, list_cl_plan, ordered_dict):
    causal_chain_list = []
    for causal_link_temp in list_cl_plan_ae:
        causal_link_temp_renamed = (causal_link_temp[0], task.variables.value_names[causal_link_temp[1][0]][causal_link_temp[1][1]], causal_link_temp[2])
        is_in_sas_plan = exist_in_sas_plan(causal_link_temp_renamed, task,list_cl_plan)
        # Identify the causal links of the justified plan that are not in the unjustified plan to find the casual chains
        if  is_in_sas_plan == False and causal_link_temp[2]!=-1:  
            for causal_link_dict in ordered_dict[causal_link_temp[2]]:
                fact_renamed = task.variables.value_names[causal_link_dict[1][0]][causal_link_dict[1][1]]
                if fact_renamed== causal_link_temp_renamed[1]:
                    list_temp = ordered_dict.get(causal_link_dict[0],[])
                    elements = list(set([value[0] for value in list_temp]))
                    causal_chain_temp= [causal_link_dict[0]]
                    causal_chain_temp.extend(causal_chain(elements,ordered_dict,causal_link_temp_renamed[0],[]))
                    causal_chain_list.append((causal_link_temp,sorted(causal_chain_temp))) 
    return causal_chain_list 

def pos_redundant_actions(sas_plan_ae):
    list_pos_redundant_actions=[]
    for action in sas_plan_ae:
        if 'skip-action' in action:
            pos = ''.join(filter(str.isdigit, action))
            list_pos_redundant_actions.append(int(pos)+1)
    return list_pos_redundant_actions

def convert_to_dict_producer_fact(list_action_fact):
    dict_final = {}
    for tuple in list_action_fact:
        key = tuple[0]
        value = tuple[1]

        if key in dict_final:
            dict_final[key].append(value)
        else:
            dict_final[key] = [value]
    return dict_final

def show_plan_ae(plan, plan_ae_cost, list_pos_redundant_actions):
    print("\nPerfectly justified plan (the redundant actions contained in the unjustified plan are shown)")
    for i in range(len(plan)):
        if (i+1) in list_pos_redundant_actions:
            print(f"{i+1} (redundant action) --> {plan[i]}")
        else:
            print(f"{i+1} {plan[i]}")
    print(f"; cost = {plan_ae_cost} (general cost)")

def get_redundant_producer(action_number, fact, task, causal_chain_list):
    for causal_link_and_chain in causal_chain_list:
        if causal_link_and_chain[0][2]== action_number and fact == task.variables.value_names[causal_link_and_chain[0][1][0]][causal_link_and_chain[0][1][1]]:
            return causal_link_and_chain[1][-1]

def get_relevant_causal_links(plan,relevant_action_causal_links, list_prevail_links, task):
    list_explanations = []
    list_fact_produced_initial_state = []
   
    for causal_link_temp in relevant_action_causal_links:
        fact_index = causal_link_temp[1]
        fact = task.variables.value_names[fact_index[0]][fact_index[1]]
        producer = causal_link_temp[0]
       
        if producer == 0:
            list_fact_produced_initial_state.append(fact)
        else:
            str = f"{fact} as a precondition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}"
            list_explanations.append(str)
    
    if len(list_fact_produced_initial_state) > 0:
        if len(list_fact_produced_initial_state) > 1:
            facts_str = ", ".join(list_fact_produced_initial_state[:-1]) + " and " + list_fact_produced_initial_state[-1] + " as preconditions which are obtained from the initial state"
        else:
            facts_str = list_fact_produced_initial_state[0] + " as a precondition which is obtained from the initial state"
        list_explanations.append(facts_str)

    if len(list_prevail_links)>0:
        list_explanations+=get_justif_prevail_conditions(plan,list_prevail_links, task)

    return list_explanations

def get_justif_prevail_conditions(plan,list_prevail_links, task):
    list_explanations = []
    list_fact_produced_initial_state = []
    
    for prevail_link_temp in list_prevail_links:
        fact_var_val = prevail_link_temp[1]
        fact = task.variables.value_names[fact_var_val[0]][fact_var_val[1]]
        producer = prevail_link_temp[0]

        if producer == 0:
            list_fact_produced_initial_state.append(fact)
        else:
            str = f"{fact} as a prevail-condition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}"
            list_explanations.append(str)

    if len(list_fact_produced_initial_state) > 0:
        if len(list_fact_produced_initial_state) > 1:
            facts_str = ", ".join(list_fact_produced_initial_state[:-1]) + " and " + list_fact_produced_initial_state[-1] + " as prevail-conditions which are obtained from the initial state."
        else:
            facts_str = list_fact_produced_initial_state[0] + " as a prevail-condition which is obtained from the initial state."
        list_explanations.append(facts_str)

    return list_explanations

def generating_explanations(plan, list_pos_redundant_actions, list_causal_links_sas_plan, list_causal_links_ae_sas_plan, task, causal_chain_list, list_links_prevail_ae_plan):
    
    explanations_dict = {}

    while True:
        explain = input("\nWould you like to generate explanations? (Yes/No): ").lower()
        if explain == "no":
            print("Explanation generation execution is finished.")
            break
        elif explain == "yes":
            action_number_input = input("Enter the number of the action: ")
            if not action_number_input.isdigit():
                print("You have entered an invalid action number.")
            else:
                action_number = int(action_number_input)
                if 0 < action_number <= len(plan):
                    if action_number in explanations_dict:
                        print(explanations_dict[action_number])               
                    else:
                        explanation_str = ""
                        explanation_str += f"\nAction #{action_number}: {plan[action_number-1]}\n"
                        
                        relevant_action_causal_links_dict = list_cl_to_dict([tuple[0] for tuple in causal_chain_list], False)
                        if len(relevant_action_causal_links_dict) == 0 or action_number not in relevant_action_causal_links_dict:
                            relevant_action_causal_links_dict = list_cl_to_dict(list_causal_links_ae_sas_plan, False)
                        redundant_action_causal_links_dict = list_cl_to_dict(list_causal_links_sas_plan, True)

                        prevail_links_dict = list_cl_to_dict(list_links_prevail_ae_plan, False)

                        if action_number in list_pos_redundant_actions:
                            consumers_list = redundant_action_causal_links_dict.get(action_number, [])
                            dict_temp = convert_to_dict_producer_fact(consumers_list)
                            explanation_str += "This Action is Redundant in the plan because it produces:"
                            for consumer, fact_list in dict_temp.items():
                                fact_list_renamed = [task.variables.value_names[fact[0]][fact[1]] for fact in fact_list]
                                facts_str = ""
                                if len(fact_list) == 1:
                                    facts_str = fact_list_renamed[0]
                                else:
                                    facts_str = ', '.join(fact_list_renamed[:-1]) + ' and ' + fact_list_renamed[-1]
                                if consumer == -1:
                                    explanation_str += f"\n--> {facts_str} that is not consumed by any other action."
                                elif consumer in list_pos_redundant_actions:
                                    explanation_str += f"\n--> {facts_str} which is consumed by the Action {consumer} {plan[consumer-1]} also Redundant."
                                else:
                                    if consumer in prevail_links_dict:                                        
                                        relevant_causal_links = get_relevant_causal_links(plan, relevant_action_causal_links_dict[consumer], prevail_links_dict[consumer], task)
                                    else:
                                        relevant_causal_links = get_relevant_causal_links(plan, relevant_action_causal_links_dict[consumer], [], task)
                                    rel_expl_str = ""
                                    if len(relevant_causal_links) == 1:
                                        rel_expl_str = relevant_causal_links[0]
                                    else:
                                        rel_expl_str = '; '.join(relevant_causal_links[:-1]) + ' and ' + relevant_causal_links[-1]
                                    explanation_str += f"\n--> {facts_str} which is consumed by the Action {consumer} {plan[consumer-1]} that is Relevant. Action {consumer} in the justified plan needs {rel_expl_str}."

                        else:
                            producers_list = relevant_action_causal_links_dict.get(action_number, [])
                            explanation_str += "In the justified plan, in order for this Relevant Action to be executed, it requires the fact:"
                            list_fact_produced_initial_state = []
                            for element in producers_list:
                                producer, (var_index, val_index) = element
                                fact = task.variables.value_names[var_index][val_index]
                                if producer == 0:
                                    list_fact_produced_initial_state.append(fact)
                                else:
                                    redundant_action = get_redundant_producer(action_number, fact, task, causal_chain_list)
                                    if redundant_action is None:
                                        explanation_str += f"\n--> {fact} as a precondition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}."
                                    else:
                                        explanation_str += f"\n--> {fact} as a precondition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}. This fact, in the unjustified plan, Action {action_number} {plan[action_number-1]} obtained it through the Redundant Action {redundant_action} {plan[redundant_action-1]}."
                            
                            facts_str = ""
                            if len(list_fact_produced_initial_state) > 1:
                                facts_str = ", ".join(list_fact_produced_initial_state[:-1]) + " and " + list_fact_produced_initial_state[-1] + " as preconditions which are obtained from the initial state."
                            if len(list_fact_produced_initial_state) == 1:
                                facts_str = list_fact_produced_initial_state[0] + " as a precondition which is obtained from the initial state."
                            
                            if len(facts_str) > 0:
                                explanation_str += f"\n--> {facts_str}"
                        
                            if action_number in prevail_links_dict: 
                                list_prevail_justif = get_justif_prevail_conditions(plan, prevail_links_dict[action_number], task)
                                if len(list_prevail_justif)>0:
                                    for prevail_justif in list_prevail_justif:
                                        explanation_str += f"\n--> {prevail_justif}"

                        explanations_dict[action_number] = explanation_str
                        print(explanation_str)
                else:
                    print("You have entered an invalid action number.")
        else:
            print("You have entered an invalid option.")
    
def obtaining_objects_from_actions(init_values_list,task):
    list_objects = []
    for var_val in init_values_list:
        fact_instantiated = task.variables.value_names[var_val[0]][var_val[1]]
        begin = fact_instantiated.find('(')
        end = fact_instantiated.find(')')
        if begin != -1 and end != -1:
            fact_objects = fact_instantiated[begin + 1:end]
            if fact_objects:
                objects_list = [x.strip() for x in fact_objects.split(',') if x.strip()]
                for object_temp in objects_list:
                    if object_temp not in list_objects:
                        list_objects.append(object_temp)
    return list_objects

def identifying_redundant_objects(task, list_actions_plan, list_pos_redundant_actions):
    
    while True:
        show_irrelevant_objects = input("\nWould you like to obtain redundant objects? (Yes/No): ").lower()
        if show_irrelevant_objects == "no":
            print("Obtaining redundant objects finished.")
            break
        elif show_irrelevant_objects == "yes":
            
            init_values_list = []
            for i in range(len(task.init.values)):
                val = task.init.values[i]
                fact = (i, val)
                init_values_list.append(fact) 

            list_objects_init_state = obtaining_objects_from_actions(init_values_list,task)

            list_all_objects = list_objects_init_state

            for action in list_actions_plan:
                objects = action[action.find(' ') + 1:-1].split()
                for temp in objects:
                    if temp not in list_all_objects:
                        list_all_objects.append(temp)

            goal_values_list = []
            for i in range(len(task.goal.pairs)):
                fact = task.goal.pairs[i]
                goal_values_list.append(fact) 

            list_objects_goal_state = obtaining_objects_from_actions(goal_values_list,task)

            for rel_obj in list_objects_goal_state:
                if rel_obj in list_all_objects:
                    list_all_objects.remove(rel_obj)
            
            # Objects present in relevant actions are considered relevant, regardless of their presence in the goal state; otherwise, they are not considered relevant.
            for i, action in enumerate(list_actions_plan):
                if (i+1) not in list_pos_redundant_actions:
                    objects = action[action.find(' ') + 1:-1].split()
                    for temp in objects:
                        if temp in list_all_objects:
                            list_all_objects.remove(temp)

            # Printing irrelevant objects, in case they exist (those not found in relevant actions) 
            if len(list_all_objects) == 0:
                print('There are no irrelevant objects.')   
            elif len(list_all_objects) > 1:
                    objects_str = ", ".join(list_all_objects[:-1]) + " and " + list_all_objects[-1]
                    print(f"--> Objects {objects_str} are irrelevant because they are not used in any Relevant Action.")
            else:
                    objects_str = list_all_objects[0] 
                    print(f"--> Object {objects_str} is irrelevant because it is not used in any Relevant Action.")
            break
        else:
            print("You have entered an invalid option.")

def showing_causal_chains(plan, causal_chain_list, task):
    while True:
        show_causal_chains = input("\nWould you like to obtain the causal chains present in the unjustified plan? (Yes/No): ").lower()
        if show_causal_chains == "no":
            print("Obtaining causal chains finished.")
            break
        elif show_causal_chains == "yes":
            if len(causal_chain_list) > 0:
                for causal_link_chain in causal_chain_list:
                    explanation_str=""
                    causal_link = causal_link_chain[0]
                    causal_chain = causal_link_chain[1]
                    fact_instantiated = task.variables.value_names[causal_link[1][0]][causal_link[1][1]]
                    explanation_str = f"--> Fact {fact_instantiated} is produced by the "
                    if causal_link[0] == 0:
                        explanation_str += "initial state"
                    else:
                        explanation_str += f"Action {causal_link[0]} {plan[causal_link[0]-1]} "
                    explanation_str += f" and is consumed by Action {causal_link[2]} {plan[causal_link[2]-1]} in the perfectly justified plan. In the unjustified plan, this fact would be obtained through the following causal chain of actions:"
                    producer = causal_link[0]

                    causal_chain_str = ""
                    found = False
                    for action in causal_chain:
                        if action == producer:
                            found = True
                        if found and action!=0:
                            temp =  f" {plan[action-1]}" 
                            causal_chain_str += " " + str(action) + temp + ","
                    explanation_str += causal_chain_str.rstrip(",")
                    print(explanation_str)
                    
            else:
                print("There are no causal chains because the Relevant Actions of the justified plan do not consume facts produced by Redundant Actions in the unjustified plan.")
            break
        else:
            print("You have entered an invalid option.")   

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-t', '--task', help='Path to task file in SAS+ format.',type=str, required=True)
    required_named.add_argument('-p', '--plan', help='Path to original plan file.', type=str, required=True)
    required_named.add_argument('-s', '--splan', help='Path to skip plan file.', type=str, required=True)
    parser.add_argument('--subsequence', help='Compiled task must guarantee maintaining order of original actions', action='store_true', default=False)
    options = parser.parse_args()

    # Check files required as parameters
    if options.task == None or options.plan == None or options.splan == None :
        parser.print_help()
        sys.exit(2)

    print(f"\nParsing AE plan")
    ae_plan, plan_ae_cost = parse_plan(options.splan)
    print(ae_plan)

  
    if (is_perfectly_justified(ae_plan)):
        print("\nThe original plan is perfectly justified.")
    else:
        print("\nThe original plan is not perfectly justified.")

        #Extract causal links from the input plan 
        #print(f"\nParsing original task")
        task, operator_name_to_index_map = parse_task(options.task)
        # print(operator_name_to_index_map)
        # task.dump()

        print(f"\nParsing original plan")
        plan, plan_cost = parse_plan(options.plan)
        print(plan)

        print(f"\nExtracting causal links from original plan")
        plan_operators = get_operators_from_plan(task.operators, plan, operator_name_to_index_map, options.subsequence)
        list_cl_plan, list_cl_prevail_plan = extract_causal_links(task, plan_operators)
        print(list_cl_plan)
        #print(list_cl_prevail_plan)
        #pretty_print_causal_links (list_cl_plan, plan_operators, task)        

        print(f"\nExtracting causal links from the justified plan (with skip actions) using original task")   
        # # print(f"\nOp name index orig task")
        # # print(operator_name_to_index_map)     
        # # print(f"\nOp name index ae task")
        # # print(operator_name_to_index_map_ae)
        ae_plan_operators = get_operators_from_plan(task.operators, ae_plan, operator_name_to_index_map, options.subsequence)      
        list_cl_ae_plan, list_cl_prevail_ae_plan  = extract_causal_links(task, ae_plan_operators)
        print(list_cl_ae_plan)
        #print(list_cl_prevail_ae_plan)
        #pretty_print_causal_links (list_cl_ae_plan, ae_plan_operators, task)

        # Convert causal links of original plan into a dictionary where the keys represent the consumers and the values are lists of (producers, fact)
        # to simplify the search for causal chains
        dict_cl_plan_consumer_ordered = list_cl_to_dict(list_cl_plan, False)
        #print("\nOrdered dictionary (consumer key) causal links original plan\n", dict_cl_plan_consumer_ordered)

        # Obtain the causal chains
        # The causal chains is formed by a list containing tuples, which are formed by the causal link of the justified plan and its causal chain
        # of the unjustified plan
        print(f"\nExtracting causal chains")
        # causal_chain_list = causal_chains(list_cl_ae_plan,ae_task,task, list_cl_plan,dict_cl_plan_consumer_ordered )
        causal_chain_list = causal_chains(list_cl_ae_plan, task, list_cl_plan, dict_cl_plan_consumer_ordered)        
        print(causal_chain_list) 

        list_pos_redundant_actions = pos_redundant_actions(ae_plan)
        print(f"\nPositions of the redundant actions in the plan: {list_pos_redundant_actions}")

        # Print plan with action elimination
        show_plan_ae(plan, plan_ae_cost, list_pos_redundant_actions)

        # # Show irrelevant objects, which are those that are not needed in the perfectly justified plan
        identifying_redundant_objects(task, plan, list_pos_redundant_actions)

        # Show causal chains
        showing_causal_chains(plan, causal_chain_list, task)

        # # Generating explanations for actions
        generating_explanations(plan, list_pos_redundant_actions, list_cl_plan, list_cl_ae_plan, task, causal_chain_list, list_cl_prevail_ae_plan)

if __name__ == '__main__':
    main()
