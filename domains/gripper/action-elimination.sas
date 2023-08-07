begin_version
3
end_version
begin_metric
1
end_metric
6
begin_variable
var0
-1
2
Atom atrobby(rooma)
Atom atrobby(roomb)
end_variable
begin_variable
var1
-1
2
Atom free(right)
Atom irrelevant-fact()
end_variable
begin_variable
var2
-1
2
Atom free(left)
Atom irrelevant-fact()
end_variable
begin_variable
var3
-1
3
Atom at(ball2, rooma)
Atom at(ball2, roomb)
Atom carry(ball2, left)
end_variable
begin_variable
var4
-1
4
Atom at(ball1, rooma)
Atom at(ball1, roomb)
Atom carry(ball1, left)
Atom carry(ball1, right)
end_variable
begin_variable
var5
-1
10
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
end_variable
2
begin_mutex_group
3
2 0
4 2
3 2
end_mutex_group
begin_mutex_group
2
1 0
4 3
end_mutex_group
begin_state
0
0
0
0
0
0
end_state
begin_goal
3
3 1
4 1
5 9
end_goal
18
begin_operator
drop ball1 roomb left
1
0 1
3
0 2 -1 0
0 4 2 1
0 5 2 3
1
end_operator
begin_operator
drop ball1 roomb right
1
0 1
3
0 1 -1 0
0 4 3 1
0 5 8 9
1
end_operator
begin_operator
drop ball2 roomb left
1
0 1
3
0 2 -1 0
0 3 2 1
0 5 7 8
1
end_operator
begin_operator
move rooma roomb
0
2
0 0 0 1
0 5 1 2
1
end_operator
begin_operator
move rooma roomb
0
2
0 0 0 1
0 5 6 7
1
end_operator
begin_operator
move roomb rooma
0
2
0 0 1 0
0 5 4 5
1
end_operator
begin_operator
pick ball1 rooma left
1
0 0
3
0 2 0 1
0 4 0 2
0 5 0 1
1
end_operator
begin_operator
pick ball1 roomb right
1
0 1
3
0 1 0 1
0 4 1 3
0 5 3 4
1
end_operator
begin_operator
pick ball2 rooma left
1
0 0
3
0 2 0 1
0 3 0 2
0 5 5 6
1
end_operator
begin_operator
skip-action plan-pos-0
0
1
0 5 0 1
0
end_operator
begin_operator
skip-action plan-pos-1
0
1
0 5 1 2
0
end_operator
begin_operator
skip-action plan-pos-2
0
1
0 5 2 3
0
end_operator
begin_operator
skip-action plan-pos-3
0
1
0 5 3 4
0
end_operator
begin_operator
skip-action plan-pos-4
0
1
0 5 4 5
0
end_operator
begin_operator
skip-action plan-pos-5
0
1
0 5 5 6
0
end_operator
begin_operator
skip-action plan-pos-6
0
1
0 5 6 7
0
end_operator
begin_operator
skip-action plan-pos-7
0
1
0 5 7 8
0
end_operator
begin_operator
skip-action plan-pos-8
0
1
0 5 8 9
0
end_operator
0
