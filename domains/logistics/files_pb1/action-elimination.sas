begin_version
3
end_version
begin_metric
1
end_metric
13
begin_variable
var0
-1
3
Atom at(airplane2, bosairport)
Atom at(airplane2, jfkairport)
Atom at(airplane2, parairport)
end_variable
begin_variable
var1
-1
4
Atom at(airplane1, bosairport)
Atom at(airplane1, jfkairport)
Atom at(airplane1, lonairport)
Atom at(airplane1, parairport)
end_variable
begin_variable
var2
-1
3
Atom at(mxf, bosairport)
Atom at(mxf, parairport)
Atom in(mxf, airplane2)
end_variable
begin_variable
var3
-1
3
Atom at(jason, bosairport)
Atom at(jason, jfkairport)
Atom in(jason, airplane2)
end_variable
begin_variable
var4
-1
3
Atom at(pencil, bosairport)
Atom at(pencil, lonairport)
Atom in(pencil, airplane1)
end_variable
begin_variable
var5
-1
3
Atom at(paper, lonairport)
Atom at(paper, parairport)
Atom in(paper, airplane1)
end_variable
begin_variable
var6
-1
3
Atom at(michelle, jfkairport)
Atom at(michelle, lonairport)
Atom in(michelle, airplane1)
end_variable
begin_variable
var7
-1
3
Atom at(lisa, lonairport)
Atom at(lisa, parairport)
Atom in(lisa, airplane1)
end_variable
begin_variable
var8
-1
3
Atom at(betty, jfkairport)
Atom at(betty, lonairport)
Atom in(betty, airplane1)
end_variable
begin_variable
var9
-1
3
Atom at(avrim, jfkairport)
Atom at(avrim, parairport)
Atom in(avrim, airplane1)
end_variable
begin_variable
var10
-1
3
Atom at(april, bosairport)
Atom at(april, lonairport)
Atom in(april, airplane1)
end_variable
begin_variable
var11
-1
3
Atom at(alex, jfkairport)
Atom at(alex, parairport)
Atom in(alex, airplane1)
end_variable
begin_variable
var12
-1
29
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
Atom plan-pos-17()
Atom plan-pos-18()
Atom plan-pos-19()
Atom plan-pos-20()
Atom plan-pos-21()
Atom plan-pos-22()
Atom plan-pos-23()
Atom plan-pos-24()
Atom plan-pos-25()
Atom plan-pos-26()
Atom plan-pos-27()
Atom plan-pos-28()
end_variable
0
begin_state
0
1
1
1
1
0
1
0
1
1
1
1
0
end_state
begin_goal
11
2 0
3 0
4 0
5 1
6 0
7 1
8 0
9 0
10 0
11 0
12 28
end_goal
56
begin_operator
flyairplane airplane1 bosairport jfkairport
0
2
0 1 0 1
0 12 17 18
1
end_operator
begin_operator
flyairplane airplane1 jfkairport lonairport
0
2
0 1 1 2
0 12 2 3
1
end_operator
begin_operator
flyairplane airplane1 jfkairport parairport
0
2
0 1 1 3
0 12 19 20
1
end_operator
begin_operator
flyairplane airplane1 lonairport bosairport
0
2
0 1 2 0
0 12 14 15
1
end_operator
begin_operator
flyairplane airplane1 parairport jfkairport
0
2
0 1 3 1
0 12 24 25
1
end_operator
begin_operator
flyairplane airplane2 bosairport jfkairport
0
2
0 0 0 1
0 12 0 1
1
end_operator
begin_operator
flyairplane airplane2 jfkairport parairport
0
2
0 0 1 2
0 12 3 4
1
end_operator
begin_operator
flyairplane airplane2 parairport bosairport
0
2
0 0 2 0
0 12 5 6
1
end_operator
begin_operator
loadairplane alex airplane1 parairport
1
1 3
2
0 11 1 2
0 12 23 24
1
end_operator
begin_operator
loadairplane april airplane1 lonairport
1
1 2
2
0 10 1 2
0 12 13 14
1
end_operator
begin_operator
loadairplane avrim airplane1 parairport
1
1 3
2
0 9 1 2
0 12 22 23
1
end_operator
begin_operator
loadairplane betty airplane1 lonairport
1
1 2
2
0 8 1 2
0 12 12 13
1
end_operator
begin_operator
loadairplane jason airplane2 jfkairport
1
0 1
2
0 3 1 2
0 12 1 2
1
end_operator
begin_operator
loadairplane lisa airplane1 lonairport
1
1 2
2
0 7 0 2
0 12 11 12
1
end_operator
begin_operator
loadairplane michelle airplane1 lonairport
1
1 2
2
0 6 1 2
0 12 10 11
1
end_operator
begin_operator
loadairplane mxf airplane2 parairport
1
0 2
2
0 2 1 2
0 12 4 5
1
end_operator
begin_operator
loadairplane paper airplane1 lonairport
1
1 2
2
0 5 0 2
0 12 9 10
1
end_operator
begin_operator
loadairplane pencil airplane1 lonairport
1
1 2
2
0 4 1 2
0 12 8 9
1
end_operator
begin_operator
skip-action plan-pos-0
0
1
0 12 0 1
0
end_operator
begin_operator
skip-action plan-pos-1
0
1
0 12 1 2
0
end_operator
begin_operator
skip-action plan-pos-10
0
1
0 12 10 11
0
end_operator
begin_operator
skip-action plan-pos-11
0
1
0 12 11 12
0
end_operator
begin_operator
skip-action plan-pos-12
0
1
0 12 12 13
0
end_operator
begin_operator
skip-action plan-pos-13
0
1
0 12 13 14
0
end_operator
begin_operator
skip-action plan-pos-14
0
1
0 12 14 15
0
end_operator
begin_operator
skip-action plan-pos-15
0
1
0 12 15 16
0
end_operator
begin_operator
skip-action plan-pos-16
0
1
0 12 16 17
0
end_operator
begin_operator
skip-action plan-pos-17
0
1
0 12 17 18
0
end_operator
begin_operator
skip-action plan-pos-18
0
1
0 12 18 19
0
end_operator
begin_operator
skip-action plan-pos-19
0
1
0 12 19 20
0
end_operator
begin_operator
skip-action plan-pos-2
0
1
0 12 2 3
0
end_operator
begin_operator
skip-action plan-pos-20
0
1
0 12 20 21
0
end_operator
begin_operator
skip-action plan-pos-21
0
1
0 12 21 22
0
end_operator
begin_operator
skip-action plan-pos-22
0
1
0 12 22 23
0
end_operator
begin_operator
skip-action plan-pos-23
0
1
0 12 23 24
0
end_operator
begin_operator
skip-action plan-pos-24
0
1
0 12 24 25
0
end_operator
begin_operator
skip-action plan-pos-25
0
1
0 12 25 26
0
end_operator
begin_operator
skip-action plan-pos-26
0
1
0 12 26 27
0
end_operator
begin_operator
skip-action plan-pos-27
0
1
0 12 27 28
0
end_operator
begin_operator
skip-action plan-pos-3
0
1
0 12 3 4
0
end_operator
begin_operator
skip-action plan-pos-4
0
1
0 12 4 5
0
end_operator
begin_operator
skip-action plan-pos-5
0
1
0 12 5 6
0
end_operator
begin_operator
skip-action plan-pos-6
0
1
0 12 6 7
0
end_operator
begin_operator
skip-action plan-pos-7
0
1
0 12 7 8
0
end_operator
begin_operator
skip-action plan-pos-8
0
1
0 12 8 9
0
end_operator
begin_operator
skip-action plan-pos-9
0
1
0 12 9 10
0
end_operator
begin_operator
unloadairplane alex airplane1 jfkairport
1
1 1
2
0 11 2 0
0 12 27 28
1
end_operator
begin_operator
unloadairplane april airplane1 bosairport
1
1 0
2
0 10 2 0
0 12 16 17
1
end_operator
begin_operator
unloadairplane avrim airplane1 jfkairport
1
1 1
2
0 9 2 0
0 12 26 27
1
end_operator
begin_operator
unloadairplane betty airplane1 jfkairport
1
1 1
2
0 8 2 0
0 12 25 26
1
end_operator
begin_operator
unloadairplane jason airplane2 bosairport
1
0 0
2
0 3 2 0
0 12 7 8
1
end_operator
begin_operator
unloadairplane lisa airplane1 parairport
1
1 3
2
0 7 2 1
0 12 21 22
1
end_operator
begin_operator
unloadairplane michelle airplane1 jfkairport
1
1 1
2
0 6 2 0
0 12 18 19
1
end_operator
begin_operator
unloadairplane mxf airplane2 bosairport
1
0 0
2
0 2 2 0
0 12 6 7
1
end_operator
begin_operator
unloadairplane paper airplane1 parairport
1
1 3
2
0 5 2 1
0 12 20 21
1
end_operator
begin_operator
unloadairplane pencil airplane1 bosairport
1
1 0
2
0 4 2 0
0 12 15 16
1
end_operator
0
