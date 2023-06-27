import argparse
import os
import subprocess
import sys

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

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-d', '--domain', help='Path to domain file.',type=str, required=True)
    required_named.add_argument('-p', '--problem', help='Path to problem file.', type=str, required=True)
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

    # Obtain the path of output.sas and sas_plan to generate the action_elim.sas file
    # TODO: When I execute the commands, the results are automatically generated in the translate folder. How can I put them in the folder I want?
    # TODO: How to obtain the paths to these files instead of getting them manually?
    output_sas_file_path ="../../domains/blocks/output.sas"
    sas_plan_file_path = "../../domains/blocks/sas_plan"
    generating_ae_sas_file(output_sas_file_path,sas_plan_file_path)

    # Solve the action elimination task using an optimal planner
    ae_sas_file_path ="/home/mmdtc/Documents/Codes/ae-explanation/action-elimination/src/translate/action-elimination.sas"
    solving_ae_task(ae_sas_file_path)   

if __name__ == '__main__':
    main()