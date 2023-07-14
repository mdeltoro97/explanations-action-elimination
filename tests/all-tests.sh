#!/bin/bash
 
./general-test.sh ../domains/ipc2014/seq-agl/barman/domain.pddl ../domains/ipc2014/seq-agl/barman/p01.pddl ../plans/lama-first/barman/barman01.solution sas_plan_original

./general-test.sh ../domains/blocks/domain.pddl ../domains/blocks/problem.pddl

./general-test.sh ../domains/blocks/domain.pddl ../domains/blocks/problem.pddl ../domains/blocks/sas_plan
