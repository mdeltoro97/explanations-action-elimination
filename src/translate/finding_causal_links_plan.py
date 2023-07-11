import argparse
import subprocess
import sys
from copy import deepcopy

from plan_parser import parse_plan
from sas_parser import parse_task


# TODO: This method is already implemented in action_elim.py but if I import it, the execution of my file does not work, however if I copy it here it works. Why does this happen?
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

def perfectly_justified(sas_plan_ae):
    for action in sas_plan_ae:
        if 'skip-action' in action:
            return False
    return True

def getting_var_pre_post_list(new_operators): 
    # Obtain a list where each position represents an action, and each position contains a list of tuples in the form (list of (var, precond), list of (var,effect)]
    precond_actions_list = []
    effects_actions_list = []

    for i in range(len(new_operators)):
        pre_post=new_operators[i].pre_post
        precond_temp = []
        effects_temp = []
        for j in range(len(pre_post)):
            var = pre_post[j][0]
            precond = pre_post[j][1]
            effects = pre_post[j][2]
            precond_temp.append((var,precond))
            effects_temp.append((var,effects))
        precond_actions_list.append(precond_temp)
        effects_actions_list.append(effects_temp)

    final_precond_effects_list = list(zip(precond_actions_list, effects_actions_list))

    return final_precond_effects_list
    
def extracting_causal_links(planning_task_path, plan, ordered):

    task, operator_name_to_index_map = parse_task(planning_task_path) 

    # Obtain the values of the initial state of the form (var,val)
    list_causal_links = []

    for i in range(len(task.init.values)):
        value = task.init.values[i]
        fact = (i,value)
        list_causal_links.append([[0],fact,[]])
    
    new_operators = get_operators_from_plan(task.operators, plan, operator_name_to_index_map, ordered)

    # Create a list of operators where each position corresponds to a plan action, and each position contains a tuple with the precondition and effect lists for that action
    list_var_pre_post = getting_var_pre_post_list(new_operators)

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
    
def convert_to_dict(list_causal_links_sas_plan):
    dict_consumer_producer = {}
    for causal_link_temp in list_causal_links_sas_plan:
        key = causal_link_temp[2]
        value = (causal_link_temp[0],causal_link_temp[1])
        if key in dict_consumer_producer:
            dict_consumer_producer[key].append(value)
        else:
            dict_consumer_producer[key] = [value]
    ordered_dict = dict(sorted(dict_consumer_producer.items()))   
    return ordered_dict

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

def generating_explanations(plan, list_pos_redundant_actions,list_causal_links_sas_plan,list_causal_links_sas_plan_ae, causal_chain_list): 
    for i in range(len(plan)):
        if (i+1) in list_pos_redundant_actions:
            print(f"{i+1} (redundant action) --> {plan[i]}")
        else:
            print(f"{i+1} {plan[i]}")
    
    print()
    explain = input("Do you want to generate explanations for the plan's actions? (Yes/No): ")

    if explain.lower() != "no" and explain.lower() != "yes":
        print("You have entered an invalid option.")
    else: 
        while explain.lower() == "yes" or explain.lower() == "no":
            if explain.lower() == "no":
                print("Explanation generation execution is finished.")
                break;
            else:
                action_number = int(input("Enter the number of the action:"))
                if 0<action_number<=len(plan):
                    print("implement!!!")
                else:
                    print("You have entered an invalid action number.")
                explain= input("Would you like to generate more explanations? (Yes/No): ")
                if explain.lower() != "no" and explain.lower() != "yes":
                    print("You have entered an invalid option.")
            
  



def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-d', '--domain', help='Path to domain file.',type=str, required=True)
    required_named.add_argument('-p', '--problem', help='Path to problem file.', type=str, required=True)
    required_named.add_argument('-plan', '--plan', help='Path to sas plan file.', type=str, required=True)
    parser.add_argument('--subsequence', help='Compiled task must guarantee maintaining order of original actions', action='store_true', default=False)
    options = parser.parse_args()

    # Check files required as parameters
    if options.domain == None or options.problem == None or options.plan == None:
        parser.print_help()
        sys.exit(2)

    # Generate SAS+ representation from a domain and problem -> output.sas
    domain_path = options.domain
    problem_path = options.problem
    sas_plan_file_path= options.plan
    #TODO: preguntarle a mauricio como llamar a esto desde el driver y lo mismo para las dudas de más abajo
    executing_fast_downward(domain_path, problem_path)

    # Obtain the path of output.sas and sas_plan to generate the action_elim.sas file -> action-elimination.sas
    # TODO: How to obtain the paths to these files instead of getting them manually?
    #TODO: por qué si ejecuto desde domains/block me sobreescribe el fichero sas_plan?
    output_sas_file_path ="output.sas"
    #sas_plan_file_path = "sas_plan"
    generating_ae_sas_file(output_sas_file_path,sas_plan_file_path)

    # Solve the action elimination task using an optimal planner -> sas_plan
    # TODO: How to obtain the path to this file instead of getting it manually?
    ae_sas_file_path ="action-elimination.sas"
    solving_ae_task(ae_sas_file_path)   

    # Determine if a plan is or not perfectly justified
    # TODO: How to obtain the path to this file instead of getting it manually?
    sas_plan_ae_path = "sas_plan"
    plan_ae, plan_ae_cost = parse_plan(sas_plan_ae_path)
    plan_perf_justf = perfectly_justified(plan_ae)
    
    print()
    if(plan_perf_justf):
        print("The plan is perfectly justified.")
    else:
        print("The plan is not perfectly justified.")

        # Extract causal links from the input plan
        plan, plan_cost = parse_plan(sas_plan_file_path)
        task, operator_name_to_index_map = parse_task(output_sas_file_path)
        list_causal_links_sas_plan = extracting_causal_links(output_sas_file_path, plan, options.subsequence)

        # Extract causal link from the justified plan (with skip actions).
        task_ae, ae_operator_name_to_index_map = parse_task(ae_sas_file_path) 
        list_causal_links_sas_plan_ae = extracting_causal_links(ae_sas_file_path, plan_ae, options.subsequence)

        # Convert it into a dictionary where the keys represent the consumers and the values are lists of (producers, fact) to simplify the search for causal chains
        ordered_dict = convert_to_dict(list_causal_links_sas_plan)

        # Obtain the causal chains
        # The causal chains is formed by a list containing tuples, which are formed by the causal link of the justified plan and its causal chain of the unjustified plan
        causal_chain_list = causal_chains(list_causal_links_sas_plan_ae,task_ae,task, list_causal_links_sas_plan,ordered_dict )
        #print(causal_chain_list) 

        list_pos_redundant_actions = pos_redundant_actions(plan_ae)
        #print(f"Positions of the redundant actions in the plan: {list_pos_redundant_actions}\n")

        # Generating explanations for actions
        generating_explanations(plan, list_pos_redundant_actions,list_causal_links_sas_plan,list_causal_links_sas_plan_ae, causal_chain_list)


if __name__ == '__main__':
    main()