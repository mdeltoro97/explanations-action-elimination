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
Atom clear(d)
Atom irrelevant-fact()
end_variable
begin_variable
var1
-1
2
Atom clear(b)
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
2
Atom on(a, b)
Atom ontable(a)
end_variable
begin_variable
var6
-1
4
Atom plan-pos-0()
Atom plan-pos-1()
Atom plan-pos-2()
Atom plan-pos-3()
end_variable
3
begin_mutex_group
2
1 0
5 0
end_mutex_group
begin_mutex_group
2
2 0
3 0
end_mutex_group
begin_mutex_group
2
2 0
4 0
end_mutex_group
begin_state
0
0
1
0
0
1
0
end_state
begin_goal
2
5 0
6 3
end_goal
5
begin_operator
 triv-nec-macro pick-up a triv-nec-macro stack a b
1
4 0
3
0 1 0 1
0 5 1 0
0 6 2 3
2
end_operator
begin_operator
pick-up c
0
4
0 2 1 0
0 3 0 1
0 4 0 1
0 6 0 1
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
stack c d
0
5
0 2 0 2
0 3 -1 0
0 0 0 1
0 4 -1 0
0 6 1 2
1
end_operator
0
