begin_version
3
end_version
begin_metric
0
end_metric
3
begin_variable
var0
-1
3
Atom at(airplane1, jkairport)
Atom at(airplane1, lonairport)
Atom at(airplane1, parairport)
end_variable
begin_variable
var1
-1
4
Atom at(jason, jkairport)
Atom at(jason, lonairport)
Atom at(jason, parairport)
Atom in(jason, airplane1)
end_variable
begin_variable
var2
-1
4
Atom at(alex, jkairport)
Atom at(alex, lonairport)
Atom at(alex, parairport)
Atom in(alex, airplane1)
end_variable
0
begin_state
1
1
1
end_state
begin_goal
2
1 2
2 2
end_goal
18
begin_operator
flyairplane airplane1 jkairport lonairport
0
1
0 0 0 1
1
end_operator
begin_operator
flyairplane airplane1 jkairport parairport
0
1
0 0 0 2
1
end_operator
begin_operator
flyairplane airplane1 lonairport jkairport
0
1
0 0 1 0
1
end_operator
begin_operator
flyairplane airplane1 lonairport parairport
0
1
0 0 1 2
1
end_operator
begin_operator
flyairplane airplane1 parairport jkairport
0
1
0 0 2 0
1
end_operator
begin_operator
flyairplane airplane1 parairport lonairport
0
1
0 0 2 1
1
end_operator
begin_operator
loadairplane alex airplane1 jkairport
1
0 0
1
0 2 0 3
1
end_operator
begin_operator
loadairplane alex airplane1 lonairport
1
0 1
1
0 2 1 3
1
end_operator
begin_operator
loadairplane alex airplane1 parairport
1
0 2
1
0 2 2 3
1
end_operator
begin_operator
loadairplane jason airplane1 jkairport
1
0 0
1
0 1 0 3
1
end_operator
begin_operator
loadairplane jason airplane1 lonairport
1
0 1
1
0 1 1 3
1
end_operator
begin_operator
loadairplane jason airplane1 parairport
1
0 2
1
0 1 2 3
1
end_operator
begin_operator
unloadairplane alex airplane1 jkairport
1
0 0
1
0 2 3 0
1
end_operator
begin_operator
unloadairplane alex airplane1 lonairport
1
0 1
1
0 2 3 1
1
end_operator
begin_operator
unloadairplane alex airplane1 parairport
1
0 2
1
0 2 3 2
1
end_operator
begin_operator
unloadairplane jason airplane1 jkairport
1
0 0
1
0 1 3 0
1
end_operator
begin_operator
unloadairplane jason airplane1 lonairport
1
0 1
1
0 1 3 1
1
end_operator
begin_operator
unloadairplane jason airplane1 parairport
1
0 2
1
0 1 3 2
1
end_operator
0
