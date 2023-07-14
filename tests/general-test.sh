
#!/bin/bash
#-------------------------------------------------------------------------------------------------------------------------------------
#
# general-test domain-file problem-file [plan-file]
#
#-------------------------------------------------------------------------------------------------------------------------------------
YELLOW='\033[0;33m' 
WHITE='\033[0;37m'
# Remove previous output files
rm output.sas action-elimination.sas original-op-costs.txt sas_plan_original sas_plan_skip

# 1 FD translate. Generates: output.sas
echo -e "${YELLOW}TESTING: Calling FD translator for original task${WHITE}"
../fast-downward.py --translate  $1 $2

# 2 FD solving. Generates sas_plan

if [ -z "$3" ]
  then
    echo -e "${YELLOW}TESTING: No plan supplied. Plan will be generated with lama-first${WHITE}"
    ../fast-downward.py --alias lama-first  output.sas
    mv sas_plan sas_plan_original
  else      
    cp $3 sas_plan_original
    
fi
echo -e "${YELLOW}TESTING: Plan generated in sas_plan-original{WHITE}"

# 3 AE call
echo -e "${YELLOW}TESTING: Calling Action Elimination${WHITE}"
../src/translate/action_elim.py -t output.sas -p sas_plan_original --subsequence --enhanced --reduction MR

# 4 FD call solve action elimination task
echo -e "${YELLOW}TESTING: Solving Action Elimination task${WHITE}"
../fast-downward.py action-elimination.sas --search "astar(hmax())"
mv sas_plan sas_plan_skip

# 5 EXP generation call
echo -e "${YELLOW}TESTING: Calling Explanation Generator${WHITE}"
../src/translate/explanation_redundant_actions.py -t output.sas  -a action-elimination.sas -p sas_plan_original -s sas_plan_skip 

#-------------------------------------------------------------------------------------------------------------------------------------

# OTHER COMMANDS:

# FD solving keep sas file. Generates output.sas and sas_plan
#../fast-downward.py --keep-sas-file  --alias lama-first $1 $2

# Overall call: generate plan and action elimination
#../fast-downward.py --translate --eliminate-action --search  --alias lama-first  $1 $2 -- --action-elimination-options --reduction MR --subsequence --enhanced --action-elimination-planner-config --search "astar(hmax())"
# generates action-elimination.sas original-op-costs.txt output-sas sas_plan.1 and sas_plan.2
