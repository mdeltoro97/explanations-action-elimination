begin_version
3
end_version
begin_metric
0
end_metric
7
begin_variable
var0
-1
2
Atom locked(node0-2)
Atom open(node0-2)
end_variable
begin_variable
var1
-1
2
Atom locked(node2-0)
Atom open(node2-0)
end_variable
begin_variable
var2
-1
9
Atom at-robot(node0-0)
Atom at-robot(node0-1)
Atom at-robot(node0-2)
Atom at-robot(node1-0)
Atom at-robot(node1-1)
Atom at-robot(node1-2)
Atom at-robot(node2-0)
Atom at-robot(node2-1)
Atom at-robot(node2-2)
end_variable
begin_variable
var3
-1
2
Atom locked(node1-1)
Atom open(node1-1)
end_variable
begin_variable
var4
-1
2
Atom arm-empty()
NegatedAtom arm-empty()
end_variable
begin_variable
var5
-1
10
Atom at(key0, node0-0)
Atom at(key0, node0-1)
Atom at(key0, node0-2)
Atom at(key0, node1-0)
Atom at(key0, node1-1)
Atom at(key0, node1-2)
Atom at(key0, node2-0)
Atom at(key0, node2-1)
Atom at(key0, node2-2)
Atom holding(key0)
end_variable
begin_variable
var6
-1
10
Atom at(key1, node0-0)
Atom at(key1, node0-1)
Atom at(key1, node0-2)
Atom at(key1, node1-0)
Atom at(key1, node1-1)
Atom at(key1, node1-2)
Atom at(key1, node2-0)
Atom at(key1, node2-1)
Atom at(key1, node2-2)
Atom holding(key1)
end_variable
1
begin_mutex_group
3
4 0
5 9
6 9
end_mutex_group
begin_state
0
0
0
0
0
3
1
end_state
begin_goal
2
5 8
6 5
end_goal
86
begin_operator
move node0-0 node0-1
0
1
0 2 0 1
1
end_operator
begin_operator
move node0-0 node1-0
0
1
0 2 0 3
1
end_operator
begin_operator
move node0-1 node0-0
0
1
0 2 1 0
1
end_operator
begin_operator
move node0-1 node0-2
1
0 1
1
0 2 1 2
1
end_operator
begin_operator
move node0-1 node1-1
1
3 1
1
0 2 1 4
1
end_operator
begin_operator
move node0-2 node0-1
0
1
0 2 2 1
1
end_operator
begin_operator
move node0-2 node1-2
0
1
0 2 2 5
1
end_operator
begin_operator
move node1-0 node0-0
0
1
0 2 3 0
1
end_operator
begin_operator
move node1-0 node1-1
1
3 1
1
0 2 3 4
1
end_operator
begin_operator
move node1-0 node2-0
1
1 1
1
0 2 3 6
1
end_operator
begin_operator
move node1-1 node0-1
0
1
0 2 4 1
1
end_operator
begin_operator
move node1-1 node1-0
0
1
0 2 4 3
1
end_operator
begin_operator
move node1-1 node1-2
0
1
0 2 4 5
1
end_operator
begin_operator
move node1-1 node2-1
0
1
0 2 4 7
1
end_operator
begin_operator
move node1-2 node0-2
1
0 1
1
0 2 5 2
1
end_operator
begin_operator
move node1-2 node1-1
1
3 1
1
0 2 5 4
1
end_operator
begin_operator
move node1-2 node2-2
0
1
0 2 5 8
1
end_operator
begin_operator
move node2-0 node1-0
0
1
0 2 6 3
1
end_operator
begin_operator
move node2-0 node2-1
0
1
0 2 6 7
1
end_operator
begin_operator
move node2-1 node1-1
1
3 1
1
0 2 7 4
1
end_operator
begin_operator
move node2-1 node2-0
1
1 1
1
0 2 7 6
1
end_operator
begin_operator
move node2-1 node2-2
0
1
0 2 7 8
1
end_operator
begin_operator
move node2-2 node1-2
0
1
0 2 8 5
1
end_operator
begin_operator
move node2-2 node2-1
0
1
0 2 8 7
1
end_operator
begin_operator
pickup node0-0 key0
1
2 0
2
0 4 0 1
0 5 0 9
1
end_operator
begin_operator
pickup node0-0 key1
1
2 0
2
0 4 0 1
0 6 0 9
1
end_operator
begin_operator
pickup node0-1 key0
1
2 1
2
0 4 0 1
0 5 1 9
1
end_operator
begin_operator
pickup node0-1 key1
1
2 1
2
0 4 0 1
0 6 1 9
1
end_operator
begin_operator
pickup node0-2 key0
1
2 2
2
0 4 0 1
0 5 2 9
1
end_operator
begin_operator
pickup node0-2 key1
1
2 2
2
0 4 0 1
0 6 2 9
1
end_operator
begin_operator
pickup node1-0 key0
1
2 3
2
0 4 0 1
0 5 3 9
1
end_operator
begin_operator
pickup node1-0 key1
1
2 3
2
0 4 0 1
0 6 3 9
1
end_operator
begin_operator
pickup node1-1 key0
1
2 4
2
0 4 0 1
0 5 4 9
1
end_operator
begin_operator
pickup node1-1 key1
1
2 4
2
0 4 0 1
0 6 4 9
1
end_operator
begin_operator
pickup node1-2 key0
1
2 5
2
0 4 0 1
0 5 5 9
1
end_operator
begin_operator
pickup node1-2 key1
1
2 5
2
0 4 0 1
0 6 5 9
1
end_operator
begin_operator
pickup node2-0 key0
1
2 6
2
0 4 0 1
0 5 6 9
1
end_operator
begin_operator
pickup node2-0 key1
1
2 6
2
0 4 0 1
0 6 6 9
1
end_operator
begin_operator
pickup node2-1 key0
1
2 7
2
0 4 0 1
0 5 7 9
1
end_operator
begin_operator
pickup node2-1 key1
1
2 7
2
0 4 0 1
0 6 7 9
1
end_operator
begin_operator
pickup node2-2 key0
1
2 8
2
0 4 0 1
0 5 8 9
1
end_operator
begin_operator
pickup node2-2 key1
1
2 8
2
0 4 0 1
0 6 8 9
1
end_operator
begin_operator
pickup-and-loose node0-0 key0 key1
1
2 0
2
0 5 0 9
0 6 9 0
1
end_operator
begin_operator
pickup-and-loose node0-0 key1 key0
1
2 0
2
0 5 9 0
0 6 0 9
1
end_operator
begin_operator
pickup-and-loose node0-1 key0 key1
1
2 1
2
0 5 1 9
0 6 9 1
1
end_operator
begin_operator
pickup-and-loose node0-1 key1 key0
1
2 1
2
0 5 9 1
0 6 1 9
1
end_operator
begin_operator
pickup-and-loose node0-2 key0 key1
1
2 2
2
0 5 2 9
0 6 9 2
1
end_operator
begin_operator
pickup-and-loose node0-2 key1 key0
1
2 2
2
0 5 9 2
0 6 2 9
1
end_operator
begin_operator
pickup-and-loose node1-0 key0 key1
1
2 3
2
0 5 3 9
0 6 9 3
1
end_operator
begin_operator
pickup-and-loose node1-0 key1 key0
1
2 3
2
0 5 9 3
0 6 3 9
1
end_operator
begin_operator
pickup-and-loose node1-1 key0 key1
1
2 4
2
0 5 4 9
0 6 9 4
1
end_operator
begin_operator
pickup-and-loose node1-1 key1 key0
1
2 4
2
0 5 9 4
0 6 4 9
1
end_operator
begin_operator
pickup-and-loose node1-2 key0 key1
1
2 5
2
0 5 5 9
0 6 9 5
1
end_operator
begin_operator
pickup-and-loose node1-2 key1 key0
1
2 5
2
0 5 9 5
0 6 5 9
1
end_operator
begin_operator
pickup-and-loose node2-0 key0 key1
1
2 6
2
0 5 6 9
0 6 9 6
1
end_operator
begin_operator
pickup-and-loose node2-0 key1 key0
1
2 6
2
0 5 9 6
0 6 6 9
1
end_operator
begin_operator
pickup-and-loose node2-1 key0 key1
1
2 7
2
0 5 7 9
0 6 9 7
1
end_operator
begin_operator
pickup-and-loose node2-1 key1 key0
1
2 7
2
0 5 9 7
0 6 7 9
1
end_operator
begin_operator
pickup-and-loose node2-2 key0 key1
1
2 8
2
0 5 8 9
0 6 9 8
1
end_operator
begin_operator
pickup-and-loose node2-2 key1 key0
1
2 8
2
0 5 9 8
0 6 8 9
1
end_operator
begin_operator
putdown node0-0 key0
1
2 0
2
0 4 -1 0
0 5 9 0
1
end_operator
begin_operator
putdown node0-0 key1
1
2 0
2
0 4 -1 0
0 6 9 0
1
end_operator
begin_operator
putdown node0-1 key0
1
2 1
2
0 4 -1 0
0 5 9 1
1
end_operator
begin_operator
putdown node0-1 key1
1
2 1
2
0 4 -1 0
0 6 9 1
1
end_operator
begin_operator
putdown node0-2 key0
1
2 2
2
0 4 -1 0
0 5 9 2
1
end_operator
begin_operator
putdown node0-2 key1
1
2 2
2
0 4 -1 0
0 6 9 2
1
end_operator
begin_operator
putdown node1-0 key0
1
2 3
2
0 4 -1 0
0 5 9 3
1
end_operator
begin_operator
putdown node1-0 key1
1
2 3
2
0 4 -1 0
0 6 9 3
1
end_operator
begin_operator
putdown node1-1 key0
1
2 4
2
0 4 -1 0
0 5 9 4
1
end_operator
begin_operator
putdown node1-1 key1
1
2 4
2
0 4 -1 0
0 6 9 4
1
end_operator
begin_operator
putdown node1-2 key0
1
2 5
2
0 4 -1 0
0 5 9 5
1
end_operator
begin_operator
putdown node1-2 key1
1
2 5
2
0 4 -1 0
0 6 9 5
1
end_operator
begin_operator
putdown node2-0 key0
1
2 6
2
0 4 -1 0
0 5 9 6
1
end_operator
begin_operator
putdown node2-0 key1
1
2 6
2
0 4 -1 0
0 6 9 6
1
end_operator
begin_operator
putdown node2-1 key0
1
2 7
2
0 4 -1 0
0 5 9 7
1
end_operator
begin_operator
putdown node2-1 key1
1
2 7
2
0 4 -1 0
0 6 9 7
1
end_operator
begin_operator
putdown node2-2 key0
1
2 8
2
0 4 -1 0
0 5 9 8
1
end_operator
begin_operator
putdown node2-2 key1
1
2 8
2
0 4 -1 0
0 6 9 8
1
end_operator
begin_operator
unlock node0-1 node0-2 key1 triangle
2
6 9
2 1
1
0 0 0 1
1
end_operator
begin_operator
unlock node0-1 node1-1 key0 diamond
2
5 9
2 1
1
0 3 0 1
1
end_operator
begin_operator
unlock node1-0 node1-1 key0 diamond
2
5 9
2 3
1
0 3 0 1
1
end_operator
begin_operator
unlock node1-0 node2-0 key0 diamond
2
5 9
2 3
1
0 1 0 1
1
end_operator
begin_operator
unlock node1-2 node0-2 key1 triangle
2
6 9
2 5
1
0 0 0 1
1
end_operator
begin_operator
unlock node1-2 node1-1 key0 diamond
2
5 9
2 5
1
0 3 0 1
1
end_operator
begin_operator
unlock node2-1 node1-1 key0 diamond
2
5 9
2 7
1
0 3 0 1
1
end_operator
begin_operator
unlock node2-1 node2-0 key0 diamond
2
5 9
2 7
1
0 1 0 1
1
end_operator
0
