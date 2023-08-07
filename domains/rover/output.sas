begin_version
3
end_version
begin_metric
0
end_metric
8
begin_variable
var0
-1
4
Atom at(rover1, waypoint1)
Atom at(rover1, waypoint2)
Atom at(rover1, waypoint3)
Atom at(rover1, waypoint4)
end_variable
begin_variable
var1
-1
2
Atom taken-image(objective2)
NegatedAtom taken-image(objective2)
end_variable
begin_variable
var2
-1
2
Atom taken-image(objective1)
NegatedAtom taken-image(objective1)
end_variable
begin_variable
var3
-1
3
Atom carry(rover1, sample1)
Atom is-in(sample1, waypoint1)
Atom is-in(sample1, waypoint4)
end_variable
begin_variable
var4
-1
3
Atom carry(rover1, sample2)
Atom is-in(sample2, waypoint1)
Atom is-in(sample2, waypoint3)
end_variable
begin_variable
var5
-1
2
Atom empty(rover1)
NegatedAtom empty(rover1)
end_variable
begin_variable
var6
-1
2
Atom stored-sample(sample1)
NegatedAtom stored-sample(sample1)
end_variable
begin_variable
var7
-1
2
Atom stored-sample(sample2)
NegatedAtom stored-sample(sample2)
end_variable
1
begin_mutex_group
3
3 0
4 0
5 0
end_mutex_group
begin_state
1
1
1
2
2
0
1
1
end_state
begin_goal
5
0 1
1 0
2 0
6 0
7 0
end_goal
15
begin_operator
drop-sample rover1 sample1 waypoint1
1
0 0
3
0 3 0 1
0 5 -1 0
0 6 -1 0
1
end_operator
begin_operator
drop-sample rover1 sample2 waypoint1
1
0 0
3
0 4 0 1
0 5 -1 0
0 7 -1 0
1
end_operator
begin_operator
move rover1 waypoint1 waypoint3
0
1
0 0 0 2
1
end_operator
begin_operator
move rover1 waypoint2 waypoint1
0
1
0 0 1 0
1
end_operator
begin_operator
move rover1 waypoint2 waypoint3
0
1
0 0 1 2
1
end_operator
begin_operator
move rover1 waypoint2 waypoint4
0
1
0 0 1 3
1
end_operator
begin_operator
move rover1 waypoint3 waypoint1
0
1
0 0 2 0
1
end_operator
begin_operator
move rover1 waypoint3 waypoint2
0
1
0 0 2 1
1
end_operator
begin_operator
move rover1 waypoint4 waypoint2
0
1
0 0 3 1
1
end_operator
begin_operator
take-image rover1 objective1 waypoint4
1
0 3
1
0 2 -1 0
1
end_operator
begin_operator
take-image rover1 objective2 waypoint3
1
0 2
1
0 1 -1 0
1
end_operator
begin_operator
take-sample rover1 sample1 waypoint1
1
0 0
2
0 3 1 0
0 5 0 1
1
end_operator
begin_operator
take-sample rover1 sample1 waypoint4
1
0 3
2
0 3 2 0
0 5 0 1
1
end_operator
begin_operator
take-sample rover1 sample2 waypoint1
1
0 0
2
0 4 1 0
0 5 0 1
1
end_operator
begin_operator
take-sample rover1 sample2 waypoint3
1
0 2
2
0 4 2 0
0 5 0 1
1
end_operator
0
