begin_version
3
end_version
begin_metric
0
end_metric
5
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
Atom free(left)
NegatedAtom free(left)
end_variable
begin_variable
var2
-1
2
Atom free(right)
NegatedAtom free(right)
end_variable
begin_variable
var3
-1
4
Atom at(ball1, rooma)
Atom at(ball1, roomb)
Atom carry(ball1, left)
Atom carry(ball1, right)
end_variable
begin_variable
var4
-1
4
Atom at(ball2, rooma)
Atom at(ball2, roomb)
Atom carry(ball2, left)
Atom carry(ball2, right)
end_variable
2
begin_mutex_group
3
3 2
4 2
1 0
end_mutex_group
begin_mutex_group
3
3 3
4 3
2 0
end_mutex_group
begin_state
0
0
0
0
0
end_state
begin_goal
2
3 1
4 1
end_goal
18
begin_operator
drop ball1 rooma left
1
0 0
2
0 3 2 0
0 1 -1 0
1
end_operator
begin_operator
drop ball1 rooma right
1
0 0
2
0 3 3 0
0 2 -1 0
1
end_operator
begin_operator
drop ball1 roomb left
1
0 1
2
0 3 2 1
0 1 -1 0
1
end_operator
begin_operator
drop ball1 roomb right
1
0 1
2
0 3 3 1
0 2 -1 0
1
end_operator
begin_operator
drop ball2 rooma left
1
0 0
2
0 4 2 0
0 1 -1 0
1
end_operator
begin_operator
drop ball2 rooma right
1
0 0
2
0 4 3 0
0 2 -1 0
1
end_operator
begin_operator
drop ball2 roomb left
1
0 1
2
0 4 2 1
0 1 -1 0
1
end_operator
begin_operator
drop ball2 roomb right
1
0 1
2
0 4 3 1
0 2 -1 0
1
end_operator
begin_operator
move rooma roomb
0
1
0 0 0 1
1
end_operator
begin_operator
move roomb rooma
0
1
0 0 1 0
1
end_operator
begin_operator
pick ball1 rooma left
1
0 0
2
0 3 0 2
0 1 0 1
1
end_operator
begin_operator
pick ball1 rooma right
1
0 0
2
0 3 0 3
0 2 0 1
1
end_operator
begin_operator
pick ball1 roomb left
1
0 1
2
0 3 1 2
0 1 0 1
1
end_operator
begin_operator
pick ball1 roomb right
1
0 1
2
0 3 1 3
0 2 0 1
1
end_operator
begin_operator
pick ball2 rooma left
1
0 0
2
0 4 0 2
0 1 0 1
1
end_operator
begin_operator
pick ball2 rooma right
1
0 0
2
0 4 0 3
0 2 0 1
1
end_operator
begin_operator
pick ball2 roomb left
1
0 1
2
0 4 1 2
0 1 0 1
1
end_operator
begin_operator
pick ball2 roomb right
1
0 1
2
0 4 1 3
0 2 0 1
1
end_operator
0
