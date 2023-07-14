
#!/bin/bash
#-------------------------------------------------------------------------------------------------------------------------------------
#
# general-test domain-file problem-file [plan-file]
#
#-------------------------------------------------------------------------------------------------------------------------------------

# Remove previous output files
rm output.sas action-elimination.sas original-op-costs.txt sas_plan_original sas_plan_skip

# 1 FD translate. Generates: output.sas
../fast-downward.py --translate  $1 $2

# 2 FD solving. Generates sas_plan

if [ -z "$3" ]
  then
    echo "No plan supplied. Plan generated with lama-first"
    ../fast-downward.py --alias lama-first  output.sas
    mv sas_plan sas_plan_original
  else      
    cp $3 sas_plan_original
    
fi

# 3 AE call
../src/translate/action_elim.py -t output.sas -p sas_plan_original --subsequence --enhanced --reduction MR

# 4 FD call solve action elimination task
../fast-downward.py action-elimination.sas --search "astar(hmax())"
mv sas_plan sas_plan_skip

# 5 EXP generation call
../src/translate/explanation_redundant_actions.py -t output.sas  -a action-elimination.sas -p sas_plan_original -s sas_plan_skip 

#-------------------------------------------------------------------------------------------------------------------------------------

# OTHER COMMANDS:

# FD solving keep sas file. Generates output.sas and sas_plan
#../fast-downward.py --keep-sas-file  --alias lama-first $1 $2

# Overall call: generate plan and action elimination
#../fast-downward.py --translate --eliminate-action --search  --alias lama-first  $1 $2 -- --action-elimination-options --reduction MR --subsequence --enhanced --action-elimination-planner-config --search "astar(hmax())"
# generates action-elimination.sas original-op-costs.txt output-sas sas_plan.1 and sas_plan.2
