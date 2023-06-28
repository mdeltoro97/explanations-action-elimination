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
    action_elim_path = 'action_elim.py'

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

def getting_var_pre_post_list(task,new_operators): 
    #FIXME: No sé si hara falta el task para lo que quiero abajo
    #TODO: Modificar para que sea una lista con tuplas de la forma( liasta de precondiciones, lista de efectos) donde cada posicion de la lista representa la accion
    
    operators_list = []
    precond_actions_list = []
    effects_actions_list = []

    for i in range(len(new_operators)):
        operators_list.append(new_operators[i].name)
        pre_post=new_operators[i].pre_post
        precond_temp = []
        effects_temp = []
        for j in range(len(pre_post)):
            precond = task.variables.value_names[pre_post[j][0]][pre_post[j][1]]
            effects = task.variables.value_names[pre_post[j][0]][pre_post[j][2]]
            precond_temp.append(precond)
            effects_temp.append(effects)
        precond_actions_list.append(precond_temp)
        effects_actions_list.append(effects_temp)

    final_precond_effects_list = list(zip(operators_list, precond_actions_list, effects_actions_list))

    print(final_precond_effects_list)
    return final_precond_effects_list

def extracting_causal_links(planning_task_path, plan, ordered):

    task, operator_name_to_index_map = parse_task(planning_task_path) 

    # Obtain the values of the initial state of the form (var,val)
    init_values_list = []
    for i in range(len(task.init.values)):
        value = task.init.values[i]
        fact = (i,value)
        init_values_list.append(fact)
    
    
    new_operators = get_operators_from_plan(task.operators, plan, operator_name_to_index_map, ordered)

    # Create a list of operators where each position corresponds to a plan action, and each position contains a tuple with the precondition and effect lists for that action
    list_var_pre_post = getting_var_pre_post_list(task,new_operators)
    
    #TODO: CONTINUE
    
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-d', '--domain', help='Path to domain file.',type=str, required=True)
    required_named.add_argument('-p', '--problem', help='Path to problem file.', type=str, required=True)
    parser.add_argument('--subsequence', help='Compiled task must guarantee maintaining order of original actions', action='store_true', default=False)
    options = parser.parse_args()

    # Check files required as parameters
    if options.domain == None or options.problem == None:
        parser.print_help()
        sys.exit(2)

    # Generate SAS+ representation from a domain and problem -> output.sas
    domain_path = options.domain
    problem_path = options.problem
    executing_fast_downward(domain_path, problem_path)

    # Solve the planning task 
    # TODO:  When I run python3 ../../fast-downward.py output.sas --search "astar(hmax())" I don't get the sas_plan with irrelevant actions that I had before

    # Obtain the path of output.sas and sas_plan to generate the action_elim.sas file -> action-elimination.sas
    # TODO: When I execute the commands, the results are automatically generated in the translate folder. How can I put them in the folder I want?
    # TODO: How to obtain the paths to these files instead of getting them manually?
    output_sas_file_path ="../../domains/blocks/output.sas"
    sas_plan_file_path = "../../domains/blocks/sas_plan"
    generating_ae_sas_file(output_sas_file_path,sas_plan_file_path)

    # Solve the action elimination task using an optimal planner -> sas_plan
    # TODO: How to obtain the path to this file instead of getting it manually?
    ae_sas_file_path ="/home/mmdtc/Documents/Codes/ae-explanation/action-elimination/src/translate/action-elimination.sas"
    solving_ae_task(ae_sas_file_path)   

    # Determine if a plan is or not perfectly justified
    # TODO: How to obtain the path to this file instead of getting it manually?
    sas_plan_ae_path = "/home/mmdtc/Documents/Codes/ae-explanation/action-elimination/src/translate/sas_plan"
    plan_ae, plan_ae_cost = parse_plan(sas_plan_ae_path)
    plan_perf_justf = perfectly_justified(plan_ae)
    
    if(plan_perf_justf):
        print("The plan is perfectly justified.")
    else:
        print("The plan is not perfectly justified.")

        # Extract causal links from the input plan
        plan, plan_cost = parse_plan(sas_plan_file_path)
        list_causal_links_sas_plan = extracting_causal_links(output_sas_file_path, plan, options.subsequence)

        # Extract causal link from the justified plan (with skip actions).
        task_plan_ae, plan_ae_operator_name_to_index_map = parse_task(ae_sas_file_path) 
        list_causal_links_sas_plan_ae = extracting_causal_links(ae_sas_file_path, plan_ae, options.subsequence)

        #TODO: CONTINUE


if __name__ == '__main__':
    main()