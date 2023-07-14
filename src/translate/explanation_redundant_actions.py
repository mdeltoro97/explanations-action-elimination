#!/usr/bin/env python3

#######################################################################
#
# Author: TODO: fill this
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

# TODO: This method is already implemented in action_elim.py but if I import it, the execution of my file does not work, however if I copy it here it works. 
# Why does this happen?
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
    
# TODO: remove this fuction when component ready in driver
def executing_fast_downward(domain_path,problem_path):
    # Fast Downward file path
    # TODO: How to obtain the path to this file instead of getting it manually?
    fast_downward_path = '../../fast-downward.py'

    # Build the command
    command = f'{sys.executable} {fast_downward_path} --translate {domain_path} {problem_path}'

    try:
        # Execute the command on the system
        subprocess.run(command, shell=True, check=True)
        print("Successful Fast Downward execution.")
    except subprocess.CalledProcessError:
        print("Error: Fast Downward execution failed.")
        sys.exit(1)

# TODO: remove this function when component ready in driver
def generating_ae_sas_file(output_sas_path, sas_plan_path):
    # action_elim file path
    # TODO: How to obtain the path to this file instead of getting it manually?
    action_elim_path = '../../src/translate/action_elim.py'

    # Build the command
    command = f'{sys.executable} {action_elim_path} -t {output_sas_path} -p {sas_plan_path} --reduction MLR --enhanced-fix-point --subsequence --add-pos-to-goal'

    try:
        # Execute the command on the system
        subprocess.run(command, shell=True, check=True)
        print("Generation of action_elimination.sas file successfully completed.")
    except subprocess.CalledProcessError:
        print("Error: Failed to generate the action_elimination.sas file.")
        sys.exit(1)

# TODO: remove this function when component ready in driver
def solving_ae_task(ae_sas_path):
    # Fast Downward file path
    # TODO: How to obtain the path to this file instead of getting it manually?
    fast_downward_path = '../../fast-downward.py'

    # Build the command
    command = f'{sys.executable} {fast_downward_path} {ae_sas_path} --search "astar(hmax())"'

    try:
        # Execute the command on the system
        subprocess.run(command, shell=True, check=True)
        print("Completed resolution Action Elimination task.")
    except subprocess.CalledProcessError:
        print("Error: Fast Downward execution failed. Resolution Action Elimination task not completed.")
        sys.exit(1)

def is_perfectly_justified(plan):
    for action in plan:
        if 'skip-action' in action:
            return False
    return True

# TODO: code modified to make it more readable.
def get_var_pre_post_list(operators): 
    """
    Obtains a list where each position represents an action, and contains a list of tuples in the form 
    [list of (var, pre_val), list of (var, eff_val)]
      """
    op_pre_list = []
    op_eff_list = []    

    for op in operators:
        op_pre = []
        op_eff = []
    
        for var, pre_val, eff_val, _ in op.pre_post:
            op_pre += [(var, pre_val)]
            op_eff += [(var, eff_val)]

        op_pre_list += [op_pre]
        op_eff_list += [op_eff]

    return list(zip(op_pre_list, op_eff_list))
    
def extract_causal_links(task, operator_name_to_index_map, plan, ordered):

    # Obtain the values of the initial state of the form (var,val)
    list_causal_links = []
   
    for var, value in enumerate(task.init.values):
        list_causal_links.append
    
    for i in range(len(task.init.values)):
        value = task.init.values[i]
        fact = (i, value)
        list_causal_links.append([[0], fact, []])
    
    new_operators = get_operators_from_plan(task.operators, plan, operator_name_to_index_map, ordered)

    # Create a list of operators where each position corresponds to a plan action, and each position contains a tuple 
    # with the precondition and effect lists for that action
    list_var_pre_post = get_var_pre_post_list(new_operators)

    for i in range(len(list_var_pre_post)):
        list_precond = list_var_pre_post[i][0]
        list_effects = list_var_pre_post[i][1]
        for j in range(len(list_precond)):
            fact= list_precond[j]
            for k in range(len(list_causal_links)):
                causal_link_temp = list_causal_links[k]

                if causal_link_temp[1] == fact or (causal_link_temp[1][1] == -fact[1] and causal_link_temp[1][0] == fact[0]):
                    list_causal_links[k][2].append(i+1)
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
    
    list_final=[]
    for i in range(len(list_causal_links)):
        causal_link_temp = list_causal_links[i]
        fact = task.variables.value_names[causal_link_temp[1][0]][causal_link_temp[1][1]]
        producers = causal_link_temp[0]
        consumers = causal_link_temp[2]
        if "plan-pos" not in fact and "irrelevant-fact" not in fact: 
            for j in range(len(producers)):
                if j < len(consumers):
                    list_final.append((producers[j], causal_link_temp[1], consumers[j]))
                else:
                    list_final.append((producers[j], causal_link_temp[1], -1))
  
    return list_final
    
def convert_to_dict_OLD(list_causal_links_sas_plan, specified_key):
    # TODO: remove this function, it was changed by a clearer one: list_cl_to_dict
    mapping = {1: (2,0), 2:(0,2)}
    key_cons, value_prod = mapping.get(specified_key, (0,0))       

    dict_consumer_producer = {}
    for causal_link_temp in list_causal_links_sas_plan:
        key = causal_link_temp[key_cons]
        value = (causal_link_temp[value_prod],causal_link_temp[1])
        if key in dict_consumer_producer:
            dict_consumer_producer[key].append(value)
        else:
            dict_consumer_producer[key] = [value]
    ordered_dict = dict(sorted(dict_consumer_producer.items()))   
    return ordered_dict


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
    # TODO: is it necessary this sort?    
    ordered_dict_cl = dict(sorted(dict_cl.items()))      
    return ordered_dict_cl

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
    
def causal_chains(list_causal_links_sas_plan_ae,task_ae,task, list_causal_links_sas_plan,ordered_dict):
    causal_chain_list = []
    for causal_link_temp in list_causal_links_sas_plan_ae:
        causal_link_temp_renamed = (causal_link_temp[0],task_ae.variables.value_names[causal_link_temp[1][0]][causal_link_temp[1][1]], causal_link_temp[2])
        is_in_sas_plan = exist_in_sas_plan(causal_link_temp_renamed,task,list_causal_links_sas_plan)
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

def get_redundant_producer(action_number, fact, task_ae, causal_chain_list):
    for causal_link_and_chain in causal_chain_list:
        if causal_link_and_chain[0][2]== action_number and fact == task_ae.variables.value_names[causal_link_and_chain[0][1][0]][causal_link_and_chain[0][1][1]]:
            return causal_link_and_chain[1][-1]

def get_relevant_causal_links(relevant_action_causal_links, task_ae):
    list_explanations = []
    list_fact_produced_initial_state = []
   
    for causal_link_temp in relevant_action_causal_links:
        fact_index = causal_link_temp[1]
        fact = task_ae.variables.value_names[fact_index[0]][fact_index[1]]
        producer = causal_link_temp[0]
       
        if producer == 0:
            list_fact_produced_initial_state.append(fact)
        else:
            str = f"{fact} as a precondition which is obtained through the effects produced by the relevant action {producer}"
            list_explanations.append(str)
   
    if len(list_fact_produced_initial_state) > 1:
        facts_str = ", ".join(list_fact_produced_initial_state[:-1]) + " and " + list_fact_produced_initial_state[-1] + " as preconditions which are obtained from the initial state"
    else:
        facts_str = list_fact_produced_initial_state[0] + " as a precondition which is obtained from the initial state"
    list_explanations.append(facts_str)
    return list_explanations

def generating_explanations(plan, list_pos_redundant_actions, list_causal_links_sas_plan, task, task_ae, causal_chain_list):

    relevant_action_causal_links_dict = convert_to_dict([tupla[0] for tupla in causal_chain_list], 1)
    redundant_action_causal_links_dict = convert_to_dict(list_causal_links_sas_plan, 2)
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
                        if action_number in list_pos_redundant_actions:
                            consumers_list = redundant_action_causal_links_dict.get(action_number, [])
                            dict_temp = convert_to_dict_producer_fact(consumers_list)
                            explanation_str += "This action is redundant in the plan because it produces:"
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
                                    explanation_str += f"\n--> {facts_str} which is consumed by the action {consumer} also redundant."
                                else:
                                    relevant_causal_links = get_relevant_causal_links(relevant_action_causal_links_dict[consumer], task_ae)
                                    rel_expl_str = ""
                                    if len(relevant_causal_links) == 1:
                                        rel_expl_str = relevant_causal_links[0]
                                    else:
                                        rel_expl_str = ', '.join(relevant_causal_links[:-1]) + ' and ' + relevant_causal_links[-1]
                                    explanation_str += f"\n--> {facts_str} which is consumed by the action {consumer} that is relevant. Action {consumer} in the justified plan needs {rel_expl_str}."
                        else:
                            producers_list = relevant_action_causal_links_dict.get(action_number, [])
                            explanation_str += "In the justified plan, in order for this relevant action to be executed, it requires the fact:"
                            list_fact_produced_initial_state = []
                            for element in producers_list:
                                producer, (var_index, val_index) = element
                                fact = task_ae.variables.value_names[var_index][val_index]
                                if producer == 0:
                                    list_fact_produced_initial_state.append(fact)
                                else:
                                    redundant_action = get_redundant_producer(action_number, fact, task_ae, causal_chain_list)
                                    explanation_str += f"\n--> {fact} as a precondition which is obtained through the effects produced by the relevant action {producer}. This fact, in the unjustified plan, action {action_number} obtained it through the redundant action {redundant_action}."
                            if len(list_fact_produced_initial_state) > 1:
                                facts_str = ", ".join(list_fact_produced_initial_state[:-1]) + " and " + list_fact_produced_initial_state[-1] + " as preconditions which are obtained from the initial state."
                            else:
                                facts_str = list_fact_produced_initial_state[0] + " as a precondition which is obtained from the initial state."
                            explanation_str += f"\n--> {facts_str}"
                        
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
    show_irrelevant_objects = input("\nWould you like to obtain redundant objects? (Yes/No): ").lower()
    if show_irrelevant_objects == "no":
        print("Obtaining redundant objects finished.")
    elif show_irrelevant_objects == "yes":
        init_values_list = []
        for i in range(len(task.init.values)):
            var = task.init.values[i]
            fact=(i, var)
            init_values_list.append(fact)
    
        list_objects_initial_state = obtaining_objects_from_actions(init_values_list, task)

        goal_values_list = []
        for i in range(len(task.goal.pairs)):
            fact = task.goal.pairs[i]
            goal_values_list.append(fact) 

        list_objects_goal_state = obtaining_objects_from_actions(goal_values_list,task)
    
        #Identifying non-goal state objects that could be irrelevant if not included in relevant actions.
        list_objects = [obj for obj in list_objects_initial_state if obj not in list_objects_goal_state]

        # Objects present in relevant actions are considered relevant, regardless of their presence in the goal state; otherwise, they are not considered relevant.
        for i, action in enumerate(list_actions_plan):
            if (i+1) not in list_pos_redundant_actions:
                objects = action[action.find(' ') + 1:-1].split()
                for temp in objects:
                    if temp in list_objects:
                        list_objects.remove(temp)
        # Printing irrelevant objects, in case they exist (those not found in relevant actions) 
        if len(list_objects) == 0:
            print('\nThere are no irrelevant objects.\n')   
        elif len(list_objects) > 1:
                objects_str = ", ".join(list_objects[:-1]) + " and " + list_objects[-1]
                print(f"--> Objects {objects_str} are irrelevant because they are not used in any relevant action.")
        else:
                objects_str = list_objects[0] 
                print(f"--> Object {objects_str} is irrelevant because it is not used in any relevant action.")
    else:
        print("You have entered an invalid option.")
    
def showing_causal_chains(causal_chain_list, task_ae):
    show_causal_chains = input("\nWould you like to obtain the causal chains present in the unjustified plan? (Yes/No): ").lower()
    if show_causal_chains == "no":
        print("Obtaining causal chains finished.")
    elif show_causal_chains == "yes":
        for causal_link_chain in causal_chain_list:
            explanation_str=""
            causal_link = causal_link_chain[0]
            causal_chain = causal_link_chain[1]
            fact_instantiated = task_ae.variables.value_names[causal_link[1][0]][causal_link[1][1]]
            explanation_str = f"--> Fact {fact_instantiated} is produced by the "
            if causal_link[0] == 0:
                explanation_str += "initial state"
            else:
                explanation_str += f"action {causal_link[0] }"
            explanation_str += f" and is consumed by action {causal_link[2]} in the justified plan. In the unjustified plan, this fact would be obtained through the following causal chain of actions: "
            producer = causal_link[0]

            causal_chain_str = ""
            found = False
            for action in causal_chain:
                if action == producer:
                    found = True
                if found and action!=0:
                    causal_chain_str += str(action) + ","
            explanation_str += causal_chain_str.rstrip(",")
            print(explanation_str)
    else:
        print("You have entered an invalid option.")
   

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-t', '--task', help='Path to task file in SAS+ format.',type=str, required=True)
    required_named.add_argument('-a', '--aetask', help='Path to AE task file in SAS+ format.',type=str, required=True)
    required_named.add_argument('-p', '--plan', help='Path to original plan file.', type=str, required=True)
    required_named.add_argument('-s', '--splan', help='Path to skip plan file.', type=str, required=True)
    parser.add_argument('--subsequence', help='Compiled task must guarantee maintaining order of original actions', action='store_true', default=False)
    options = parser.parse_args()

    # Check files required as parameters
    if options.task == None or options.aetask == None or options.plan == None or options.splan == None :
        parser.print_help()
        sys.exit(2)

    print(f"\nParsing AE plan")
    ae_plan, ae_plan_ae_costcost = parse_plan(options.splan)
  
    
    if (is_perfectly_justified(ae_plan)):
        print("The original plan is perfectly justified.")
    else:
        print("The original plan is not perfectly justified.")

        # Extract causal links from the input plan 
        print(f"Parsing original task")
        task, operator_name_to_index_map = parse_task(options.task)
        # print(operator_name_to_index_map)
        # task.dump()

        print(f"\nParsing original plan")
        plan, plan_cost = parse_plan(options.plan)
        # print(plan)

        print(f"\nExtracting causal links from original plan")
        list_cl_plan = extract_causal_links(task, operator_name_to_index_map, plan, options.subsequence)
        print(list_cl_plan)

        # Extract causal link from the justified plan (with skip actions).
        print(f"\nParsing AE planning task")        
        ae_task, ae_operator_name_to_index_map = parse_task(options.aetask)
        print(ae_operator_name_to_index_map)
        # task_ae.dump()
        print(f"\nExtracting causal links from ae plan")
        print(ae_plan)
        list_cl_ae_plan = extract_causal_links(ae_task, ae_operator_name_to_index_map, ae_plan, options.subsequence)
        print(list_cl_ae_plan)

        # Convert causal links of original plan into a dictionary where the keys represent the consumers and the values are lists of (producers, fact)
        # to simplify the search for causal chains
        dict_cl_plan_consumer_ordered = list_cl_to_dict(list_cl_plan, False)
        print("\nOrdered dictionary (consumer key) causal links original plan\n", dict_cl_plan_consumer_ordered)

        # Obtain the causal chains
        # The causal chains is formed by a list containing tuples, which are formed by the causal link of the justified plan and its causal chain
        # of the unjustified plan
        print(f"Extracting causal chains")
        causal_chain_list = causal_chains(list_cl_ae_plan, ae_task, task, list_cl_plan, dict_cl_plan_consumer_ordered)
        #print(causal_chain_list) 

        list_pos_redundant_actions = pos_redundant_actions(ae_plan)
        #print(f"Positions of the redundant actions in the plan: {list_pos_redundant_actions}\n")

        # Print plan with action elimination
        show_plan_ae(plan, plan_ae_cost, list_pos_redundant_actions)

        # Show irrelevant objects, which are those that are not needed in the perfectly justified plan
        identifying_redundant_objects(task, plan, list_pos_redundant_actions)

        # Show causal chains
        showing_causal_chains(causal_chain_list, task_ae)

        # Generating explanations for actions
        generating_explanations(plan, list_pos_redundant_actions, list_causal_links_sas_plan, task,task_ae, causal_chain_list)

if __name__ == '__main__':
    main()
