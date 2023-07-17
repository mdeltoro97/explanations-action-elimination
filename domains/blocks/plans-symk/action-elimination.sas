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
Atom on(c, b)
Atom ontable(c)
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
4
Atom holding(a)
Atom on(a, b)
Atom on(a, d)
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
9
Atom plan-pos-0()
Atom plan-pos-1()
Atom plan-pos-2()
Atom plan-pos-3()
Atom plan-pos-4()
Atom plan-pos-5()
Atom plan-pos-6()
Atom plan-pos-7()
Atom plan-pos-8()
end_variable
5
begin_mutex_group
2
5 0
6 0
end_mutex_group
begin_mutex_group
3
2 1
1 0
5 1
end_mutex_group
begin_mutex_group
2
2 0
3 0
end_mutex_group
begin_mutex_group
2
0 0
5 2
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
2
0
0
3
0
0
end_state
begin_goal
3
5 1
6 0
7 8
end_goal
16
begin_operator
pick-up a
0
4
0 4 0 1
0 5 3 0
0 6 0 1
0 7 2 3
1
end_operator
begin_operator
pick-up c
0
4
0 2 2 0
0 3 0 1
0 4 0 1
0 7 0 1
1
end_operator
begin_operator
put-down c
0
4
0 2 0 2
0 3 -1 0
0 4 -1 0
0 7 5 6
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
skip-action plan-pos-4
0
1
0 7 4 5
0
end_operator
begin_operator
skip-action plan-pos-5
0
1
0 7 5 6
0
end_operator
begin_operator
skip-action plan-pos-6
0
1
0 7 6 7
0
end_operator
begin_operator
skip-action plan-pos-7
0
1
0 7 7 8
0
end_operator
begin_operator
stack a b
0
5
0 1 0 1
0 4 -1 0
0 5 0 1
0 6 -1 0
0 7 7 8
1
end_operator
begin_operator
stack a d
0
5
0 0 0 1
0 4 -1 0
0 5 0 2
0 6 -1 0
0 7 3 4
1
end_operator
begin_operator
stack c b
0
5
0 2 0 1
0 3 -1 0
0 1 0 1
0 4 -1 0
0 7 1 2
1
end_operator
begin_operator
unstack a d
0
5
0 0 -1 0
0 4 0 1
0 5 2 0
0 6 0 1
0 7 6 7
1
end_operator
begin_operator
unstack c b
0
5
0 2 1 0
0 3 0 1
0 1 -1 0
0 4 0 1
0 7 4 5
1
end_operator
0
