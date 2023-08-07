begin_version
3
end_version
begin_metric
1
end_metric
7
begin_variable
var0
-1
2
Atom locked(node0-2)
Atom irrelevant-fact()
end_variable
begin_variable
var1
-1
2
Atom locked(node1-1)
Atom open(node1-1)
end_variable
begin_variable
var2
-1
7
Atom at-robot(node0-0)
Atom at-robot(node0-1)
Atom at-robot(node1-0)
Atom at-robot(node1-1)
Atom at-robot(node1-2)
Atom at-robot(node2-1)
Atom at-robot(node2-2)
end_variable
begin_variable
var3
-1
2
Atom arm-empty()
Atom irrelevant-fact()
end_variable
begin_variable
var4
-1
3
Atom at(key0, node1-0)
Atom at(key0, node2-2)
Atom holding(key0)
end_variable
begin_variable
var5
-1
3
Atom at(key1, node0-1)
Atom at(key1, node1-2)
Atom holding(key1)
end_variable
begin_variable
var6
-1
17
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
Atom plan-pos-16()
end_variable
1
begin_mutex_group
3
3 0
4 2
5 2
end_mutex_group
begin_state
0
0
0
0
0
0
0
end_state
begin_goal
3
4 1
5 1
6 16
end_goal
32
begin_operator
move node0-0 node1-0
0
2
0 2 0 2
0 6 0 1
1
end_operator
begin_operator
move node0-1 node1-1
1
1 1
2
0 2 1 3
0 6 12 13
1
end_operator
begin_operator
move node1-0 node1-1
1
1 1
2
0 2 2 3
0 6 3 4
1
end_operator
begin_operator
move node1-1 node0-1
0
2
0 2 3 1
0 6 9 10
1
end_operator
begin_operator
move node1-1 node1-2
0
2
0 2 3 4
0 6 13 14
1
end_operator
begin_operator
move node1-1 node2-1
0
2
0 2 3 5
0 6 4 5
1
end_operator
begin_operator
move node1-2 node1-1
1
1 1
2
0 2 4 3
0 6 8 9
1
end_operator
begin_operator
move node1-2 node1-1
1
1 1
2
0 2 4 3
0 6 15 16
1
end_operator
begin_operator
move node2-1 node2-2
0
2
0 2 5 6
0 6 5 6
1
end_operator
begin_operator
move node2-2 node1-2
0
2
0 2 6 4
0 6 7 8
1
end_operator
begin_operator
pickup node0-1 key1
1
2 1
3
0 3 0 1
0 5 0 2
0 6 10 11
1
end_operator
begin_operator
pickup node1-0 key0
1
2 2
3
0 3 0 1
0 4 0 2
0 6 1 2
1
end_operator
begin_operator
putdown node1-2 key1
1
2 4
3
0 3 -1 0
0 5 2 1
0 6 14 15
1
end_operator
begin_operator
putdown node2-2 key0
1
2 6
3
0 3 -1 0
0 4 2 1
0 6 6 7
1
end_operator
begin_operator
skip-action plan-pos-0
0
1
0 6 0 1
0
end_operator
begin_operator
skip-action plan-pos-1
0
1
0 6 1 2
0
end_operator
begin_operator
skip-action plan-pos-10
0
1
0 6 10 11
0
end_operator
begin_operator
skip-action plan-pos-11
0
1
0 6 11 12
0
end_operator
begin_operator
skip-action plan-pos-12
0
1
0 6 12 13
0
end_operator
begin_operator
skip-action plan-pos-13
0
1
0 6 13 14
0
end_operator
begin_operator
skip-action plan-pos-14
0
1
0 6 14 15
0
end_operator
begin_operator
skip-action plan-pos-15
0
1
0 6 15 16
0
end_operator
begin_operator
skip-action plan-pos-2
0
1
0 6 2 3
0
end_operator
begin_operator
skip-action plan-pos-3
0
1
0 6 3 4
0
end_operator
begin_operator
skip-action plan-pos-4
0
1
0 6 4 5
0
end_operator
begin_operator
skip-action plan-pos-5
0
1
0 6 5 6
0
end_operator
begin_operator
skip-action plan-pos-6
0
1
0 6 6 7
0
end_operator
begin_operator
skip-action plan-pos-7
0
1
0 6 7 8
0
end_operator
begin_operator
skip-action plan-pos-8
0
1
0 6 8 9
0
end_operator
begin_operator
skip-action plan-pos-9
0
1
0 6 9 10
0
end_operator
begin_operator
unlock node0-1 node0-2 key1 triangle
2
2 1
5 2
2
0 0 0 1
0 6 11 12
1
end_operator
begin_operator
unlock node1-0 node1-1 key0 diamond
2
2 2
4 2
2
0 1 0 1
0 6 2 3
1
end_operator
0
