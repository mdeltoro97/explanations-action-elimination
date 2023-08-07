begin_version
3
end_version
begin_metric
1
end_metric
9
begin_variable
var0
-1
3
Atom carry(rover1, sample2)
Atom is-in(sample2, waypoint3)
Atom irrelevant-fact()
end_variable
begin_variable
var1
-1
3
Atom carry(rover1, sample1)
Atom is-in(sample1, waypoint1)
Atom is-in(sample1, waypoint4)
end_variable
begin_variable
var2
-1
2
Atom empty(rover1)
Atom irrelevant-fact()
end_variable
begin_variable
var3
-1
4
Atom at(rover1, waypoint1)
Atom at(rover1, waypoint2)
Atom at(rover1, waypoint3)
Atom at(rover1, waypoint4)
end_variable
begin_variable
var4
-1
16
Atom plan-pos-0()
Atom plan-pos-1()
Atom plan-pos-2()
Atom plan-pos-3()
Atom plan-pos-4()
Atom plan-pos-5()
Atom plan-pos-6()
Atom plan-pos-7()
Atom plan-pos-8()
Atom plan-pos-9()
Atom plan-pos-10()
Atom plan-pos-11()
Atom plan-pos-12()
Atom plan-pos-13()
Atom plan-pos-14()
Atom plan-pos-15()
end_variable
begin_variable
var5
-1
2
Atom stored-sample(sample1)
Atom irrelevant-fact()
end_variable
begin_variable
var6
-1
2
Atom stored-sample(sample2)
Atom irrelevant-fact()
end_variable
begin_variable
var7
-1
2
Atom taken-image(objective1)
Atom irrelevant-fact()
end_variable
begin_variable
var8
-1
2
Atom taken-image(objective2)
Atom irrelevant-fact()
end_variable
1
begin_mutex_group
3
1 0
0 0
2 0
end_mutex_group
begin_state
1
2
0
1
0
1
1
1
1
end_state
begin_goal
6
3 1
4 15
5 0
6 0
7 0
8 0
end_goal
30
begin_operator
drop-sample rover1 sample1 waypoint1
1
3 0
4
0 1 0 1
0 2 -1 0
0 5 -1 0
0 4 7 8
1
end_operator
begin_operator
drop-sample rover1 sample2 waypoint1
1
3 0
4
0 0 0 2
0 2 -1 0
0 6 -1 0
0 4 11 12
1
end_operator
begin_operator
move rover1 waypoint1 waypoint3
0
2
0 3 0 2
0 4 8 9
1
end_operator
begin_operator
move rover1 waypoint1 waypoint3
0
2
0 3 0 2
0 4 13 14
1
end_operator
begin_operator
move rover1 waypoint2 waypoint3
0
2
0 3 1 2
0 4 4 5
1
end_operator
begin_operator
move rover1 waypoint2 waypoint4
0
2
0 3 1 3
0 4 0 1
1
end_operator
begin_operator
move rover1 waypoint3 waypoint1
0
2
0 3 2 0
0 4 6 7
1
end_operator
begin_operator
move rover1 waypoint3 waypoint1
0
2
0 3 2 0
0 4 10 11
1
end_operator
begin_operator
move rover1 waypoint3 waypoint2
0
2
0 3 2 1
0 4 14 15
1
end_operator
begin_operator
move rover1 waypoint4 waypoint2
0
2
0 3 3 1
0 4 3 4
1
end_operator
begin_operator
skip-action plan-pos-0
0
1
0 4 0 1
0
end_operator
begin_operator
skip-action plan-pos-1
0
1
0 4 1 2
0
end_operator
begin_operator
skip-action plan-pos-10
0
1
0 4 10 11
0
end_operator
begin_operator
skip-action plan-pos-11
0
1
0 4 11 12
0
end_operator
begin_operator
skip-action plan-pos-12
0
1
0 4 12 13
0
end_operator
begin_operator
skip-action plan-pos-13
0
1
0 4 13 14
0
end_operator
begin_operator
skip-action plan-pos-14
0
1
0 4 14 15
0
end_operator
begin_operator
skip-action plan-pos-2
0
1
0 4 2 3
0
end_operator
begin_operator
skip-action plan-pos-3
0
1
0 4 3 4
0
end_operator
begin_operator
skip-action plan-pos-4
0
1
0 4 4 5
0
end_operator
begin_operator
skip-action plan-pos-5
0
1
0 4 5 6
0
end_operator
begin_operator
skip-action plan-pos-6
0
1
0 4 6 7
0
end_operator
begin_operator
skip-action plan-pos-7
0
1
0 4 7 8
0
end_operator
begin_operator
skip-action plan-pos-8
0
1
0 4 8 9
0
end_operator
begin_operator
skip-action plan-pos-9
0
1
0 4 9 10
0
end_operator
begin_operator
take-image rover1 objective1 waypoint4
1
3 3
2
0 7 -1 0
0 4 1 2
1
end_operator
begin_operator
take-image rover1 objective2 waypoint3
1
3 2
2
0 8 -1 0
0 4 5 6
1
end_operator
begin_operator
take-sample rover1 sample1 waypoint1
1
3 0
3
0 1 1 0
0 2 0 1
0 4 12 13
1
end_operator
begin_operator
take-sample rover1 sample1 waypoint4
1
3 3
3
0 1 2 0
0 2 0 1
0 4 2 3
1
end_operator
begin_operator
take-sample rover1 sample2 waypoint3
1
3 2
3
0 0 1 0
0 2 0 1
0 4 9 10
1
end_operator
0
