begin_version
3
end_version
begin_metric
1
end_metric
4
begin_variable
var0
-1
2
Atom at(airplane1, lonairport)
Atom at(airplane1, parairport)
end_variable
begin_variable
var1
-1
3
Atom at(jason, lonairport)
Atom at(jason, parairport)
Atom in(jason, airplane1)
end_variable
begin_variable
var2
-1
3
Atom at(alex, lonairport)
Atom at(alex, parairport)
Atom in(alex, airplane1)
end_variable
begin_variable
var3
-1
7
Atom plan-pos-0()
Atom plan-pos-1()
Atom plan-pos-2()
Atom plan-pos-3()
Atom plan-pos-4()
Atom plan-pos-5()
Atom plan-pos-6()
end_variable
0
begin_state
0
0
0
0
end_state
begin_goal
3
1 1
2 1
3 6
end_goal
12
begin_operator
flyairplane airplane1 lonairport parairport
0
2
0 0 0 1
0 3 2 3
1
end_operator
begin_operator
flyairplane airplane1 parairport lonairport
0
2
0 0 1 0
0 3 5 6
1
end_operator
begin_operator
loadairplane alex airplane1 lonairport
1
0 0
2
0 2 0 2
0 3 1 2
1
end_operator
begin_operator
loadairplane jason airplane1 lonairport
1
0 0
2
0 1 0 2
0 3 0 1
1
end_operator
begin_operator
skip-action plan-pos-0
0
1
0 3 0 1
0
end_operator
begin_operator
skip-action plan-pos-1
0
1
0 3 1 2
0
end_operator
begin_operator
skip-action plan-pos-2
0
1
0 3 2 3
0
end_operator
begin_operator
skip-action plan-pos-3
0
1
0 3 3 4
0
end_operator
begin_operator
skip-action plan-pos-4
0
1
0 3 4 5
0
end_operator
begin_operator
skip-action plan-pos-5
0
1
0 3 5 6
0
end_operator
begin_operator
unloadairplane alex airplane1 parairport
1
0 1
2
0 2 2 1
0 3 4 5
1
end_operator
begin_operator
unloadairplane jason airplane1 parairport
1
0 1
2
0 1 2 1
0 3 3 4
1
end_operator
0
