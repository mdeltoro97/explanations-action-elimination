#rm *.sas *.txt *plan*
#-------------------------------------------------------------------------------------------------------------------------------------
# OPTION A

# # 1 FD translate. Generates: output.sas
# ../fast-downward.py --translate  ../domains/ipc2014/seq-agl/barman/domain.pddl ../domains/ipc2014/seq-agl/barman/p01.pddl
# 
# # 2 FD solving generates sas_plan
# ../fast-downward.py --alias lama-first  output.sas
# mv sas_plan sas_plan_original
# 
# # 3 AE call
# ../src/translate/action_elim.py -t output.sas -p sas_plan_original --subsequence --enhanced --reduction MR
# 
# # 4 FD call solve action elimination task
# ../fast-downward.py action-elimination.sas --search "astar(hmax())"
# mv sas_plan sas_plan_skip

#-------------------------------------------------------------------------------------------------------------------------------------
# OPTION B: Take plan from previously generated plans

# 1 FD translate. Generates: output.sas
../fast-downward.py --translate  ../domains/ipc2014/seq-agl/barman/domain.pddl ../domains/ipc2014/seq-agl/barman/p01.pddl

# 2 FD solving generates sas_plan
#../fast-downward.py --alias lama-first  output.sas
#mv sas_plan sas_plan_original
cp ../plans/lama-first/barman/barman01.solution sas_plan_original

# 3 AE call
../src/translate/action_elim.py -t output.sas -p sas_plan_original --subsequence --enhanced --reduction MR

# 4 FD call solve action elimination task
../fast-downward.py action-elimination.sas --search "astar(hmax())"
mv sas_plan sas_plan_skip

# 5 EXP generation call
../src/translate/explanation_redundant_actions.py -t output.sas  -a action-elimination.sas -p sas_plan_original -s sas_plan_skip 


#-------------------------------------------------------------------------------------------------------------------------------------

# OTHER:

# FD solving keep sas file. Generates output.sas and sas_plan
#../fast-downward.py --keep-sas-file  --alias lama-first ../domains/ipc2014/seq-agl/barman/domain.pddl ../domains/ipc2014/seq-agl/barman/p01.pddl

# Overall call: generate plan and action elimination
#../fast-downward.py --translate --eliminate-action --search  --alias lama-first  ../domains/ipc2014/seq-agl/barman/domain.pddl ../domains/ipc2014/seq-agl/barman/p01.pddl -- --action-elimination-options --reduction MR --subsequence --enhanced --action-elimination-planner-config --search "astar(hmax())"
# generates action-elimination.sas original-op-costs.txt output-sas sas_plan.1 and sas_plan.2
