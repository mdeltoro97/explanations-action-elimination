begin_version
3
end_version
begin_metric
1
end_metric
8
begin_variable
var0
-1
2
Atom clear(b)
Atom irrelevant-fact()
end_variable
begin_variable
var1
-1
2
Atom clear(d)
Atom irrelevant-fact()
end_variable
begin_variable
var2
-1
3
Atom holding(c)
Atom ontable(c)
Atom irrelevant-fact()
end_variable
begin_variable
var3
-1
2
Atom clear(c)
Atom irrelevant-fact()
end_variable
begin_variable
var4
-1
2
Atom handempty()
Atom irrelevant-fact()
end_variable
begin_variable
var5
-1
3
Atom holding(a)
Atom on(a, b)
Atom ontable(a)
end_variable
begin_variable
var6
-1
2
Atom clear(a)
Atom irrelevant-fact()
end_variable
begin_variable
var7
-1
5
Atom plan-pos-0()
Atom plan-pos-1()
Atom plan-pos-2()
Atom plan-pos-3()
Atom plan-pos-4()
end_variable
4
begin_mutex_group
2
5 0
6 0
end_mutex_group
begin_mutex_group
2
0 0
5 1
end_mutex_group
begin_mutex_group
2
2 0
3 0
end_mutex_group
begin_mutex_group
3
2 0
4 0
5 0
end_mutex_group
begin_state
0
0
1
0
0
2
0
0
end_state
begin_goal
3
5 1
6 0
7 4
end_goal
8
begin_operator
pick-up a
0
4
0 4 0 1
0 5 2 0
0 6 0 1
0 7 2 3
1
end_operator
begin_operator
pick-up c
0
4
0 2 1 0
0 3 0 1
0 4 0 1
0 7 0 1
1
end_operator
begin_operator
skip-action plan-pos-0
0
1
0 7 0 1
0
end_operator
begin_operator
skip-action plan-pos-1
0
1
0 7 1 2
0
end_operator
begin_operator
skip-action plan-pos-2
0
1
0 7 2 3
0
end_operator
begin_operator
skip-action plan-pos-3
0
1
0 7 3 4
0
end_operator
begin_operator
stack a b
0
5
0 0 0 1
0 4 -1 0
0 5 0 1
0 6 -1 0
0 7 3 4
1
end_operator
begin_operator
stack c d
0
5
0 2 0 2
0 3 -1 0
0 1 0 1
0 4 -1 0
0 7 1 2
1
end_operator
0
