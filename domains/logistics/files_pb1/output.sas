begin_version
3
end_version
begin_metric
0
end_metric
12
begin_variable
var0
-1
4
Atom at(airplane2, bosairport)
Atom at(airplane2, jfkairport)
Atom at(airplane2, lonairport)
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
6
Atom at(pencil, bosairport)
Atom at(pencil, jfkairport)
Atom at(pencil, lonairport)
Atom at(pencil, parairport)
Atom in(pencil, airplane1)
Atom in(pencil, airplane2)
end_variable
begin_variable
var3
-1
6
Atom at(paper, bosairport)
Atom at(paper, jfkairport)
Atom at(paper, lonairport)
Atom at(paper, parairport)
Atom in(paper, airplane1)
Atom in(paper, airplane2)
end_variable
begin_variable
var4
-1
6
Atom at(mxf, bosairport)
Atom at(mxf, jfkairport)
Atom at(mxf, lonairport)
Atom at(mxf, parairport)
Atom in(mxf, airplane1)
Atom in(mxf, airplane2)
end_variable
begin_variable
var5
-1
6
Atom at(michelle, bosairport)
Atom at(michelle, jfkairport)
Atom at(michelle, lonairport)
Atom at(michelle, parairport)
Atom in(michelle, airplane1)
Atom in(michelle, airplane2)
end_variable
begin_variable
var6
-1
6
Atom at(lisa, bosairport)
Atom at(lisa, jfkairport)
Atom at(lisa, lonairport)
Atom at(lisa, parairport)
Atom in(lisa, airplane1)
Atom in(lisa, airplane2)
end_variable
begin_variable
var7
-1
6
Atom at(jason, bosairport)
Atom at(jason, jfkairport)
Atom at(jason, lonairport)
Atom at(jason, parairport)
Atom in(jason, airplane1)
Atom in(jason, airplane2)
end_variable
begin_variable
var8
-1
6
Atom at(betty, bosairport)
Atom at(betty, jfkairport)
Atom at(betty, lonairport)
Atom at(betty, parairport)
Atom in(betty, airplane1)
Atom in(betty, airplane2)
end_variable
begin_variable
var9
-1
6
Atom at(avrim, bosairport)
Atom at(avrim, jfkairport)
Atom at(avrim, lonairport)
Atom at(avrim, parairport)
Atom in(avrim, airplane1)
Atom in(avrim, airplane2)
end_variable
begin_variable
var10
-1
6
Atom at(april, bosairport)
Atom at(april, jfkairport)
Atom at(april, lonairport)
Atom at(april, parairport)
Atom in(april, airplane1)
Atom in(april, airplane2)
end_variable
begin_variable
var11
-1
6
Atom at(alex, bosairport)
Atom at(alex, jfkairport)
Atom at(alex, lonairport)
Atom at(alex, parairport)
Atom in(alex, airplane1)
Atom in(alex, airplane2)
end_variable
0
begin_state
0
1
2
2
3
2
2
1
2
3
2
3
end_state
begin_goal
10
2 0
3 3
4 0
5 1
6 3
7 0
8 1
9 1
10 0
11 1
end_goal
184
begin_operator
flyairplane airplane1 bosairport jfkairport
0
1
0 1 0 1
1
end_operator
begin_operator
flyairplane airplane1 bosairport lonairport
0
1
0 1 0 2
1
end_operator
begin_operator
flyairplane airplane1 bosairport parairport
0
1
0 1 0 3
1
end_operator
begin_operator
flyairplane airplane1 jfkairport bosairport
0
1
0 1 1 0
1
end_operator
begin_operator
flyairplane airplane1 jfkairport lonairport
0
1
0 1 1 2
1
end_operator
begin_operator
flyairplane airplane1 jfkairport parairport
0
1
0 1 1 3
1
end_operator
begin_operator
flyairplane airplane1 lonairport bosairport
0
1
0 1 2 0
1
end_operator
begin_operator
flyairplane airplane1 lonairport jfkairport
0
1
0 1 2 1
1
end_operator
begin_operator
flyairplane airplane1 lonairport parairport
0
1
0 1 2 3
1
end_operator
begin_operator
flyairplane airplane1 parairport bosairport
0
1
0 1 3 0
1
end_operator
begin_operator
flyairplane airplane1 parairport jfkairport
0
1
0 1 3 1
1
end_operator
begin_operator
flyairplane airplane1 parairport lonairport
0
1
0 1 3 2
1
end_operator
begin_operator
flyairplane airplane2 bosairport jfkairport
0
1
0 0 0 1
1
end_operator
begin_operator
flyairplane airplane2 bosairport lonairport
0
1
0 0 0 2
1
end_operator
begin_operator
flyairplane airplane2 bosairport parairport
0
1
0 0 0 3
1
end_operator
begin_operator
flyairplane airplane2 jfkairport bosairport
0
1
0 0 1 0
1
end_operator
begin_operator
flyairplane airplane2 jfkairport lonairport
0
1
0 0 1 2
1
end_operator
begin_operator
flyairplane airplane2 jfkairport parairport
0
1
0 0 1 3
1
end_operator
begin_operator
flyairplane airplane2 lonairport bosairport
0
1
0 0 2 0
1
end_operator
begin_operator
flyairplane airplane2 lonairport jfkairport
0
1
0 0 2 1
1
end_operator
begin_operator
flyairplane airplane2 lonairport parairport
0
1
0 0 2 3
1
end_operator
begin_operator
flyairplane airplane2 parairport bosairport
0
1
0 0 3 0
1
end_operator
begin_operator
flyairplane airplane2 parairport jfkairport
0
1
0 0 3 1
1
end_operator
begin_operator
flyairplane airplane2 parairport lonairport
0
1
0 0 3 2
1
end_operator
begin_operator
loadairplane alex airplane1 bosairport
1
1 0
1
0 11 0 4
1
end_operator
begin_operator
loadairplane alex airplane1 jfkairport
1
1 1
1
0 11 1 4
1
end_operator
begin_operator
loadairplane alex airplane1 lonairport
1
1 2
1
0 11 2 4
1
end_operator
begin_operator
loadairplane alex airplane1 parairport
1
1 3
1
0 11 3 4
1
end_operator
begin_operator
loadairplane alex airplane2 bosairport
1
0 0
1
0 11 0 5
1
end_operator
begin_operator
loadairplane alex airplane2 jfkairport
1
0 1
1
0 11 1 5
1
end_operator
begin_operator
loadairplane alex airplane2 lonairport
1
0 2
1
0 11 2 5
1
end_operator
begin_operator
loadairplane alex airplane2 parairport
1
0 3
1
0 11 3 5
1
end_operator
begin_operator
loadairplane april airplane1 bosairport
1
1 0
1
0 10 0 4
1
end_operator
begin_operator
loadairplane april airplane1 jfkairport
1
1 1
1
0 10 1 4
1
end_operator
begin_operator
loadairplane april airplane1 lonairport
1
1 2
1
0 10 2 4
1
end_operator
begin_operator
loadairplane april airplane1 parairport
1
1 3
1
0 10 3 4
1
end_operator
begin_operator
loadairplane april airplane2 bosairport
1
0 0
1
0 10 0 5
1
end_operator
begin_operator
loadairplane april airplane2 jfkairport
1
0 1
1
0 10 1 5
1
end_operator
begin_operator
loadairplane april airplane2 lonairport
1
0 2
1
0 10 2 5
1
end_operator
begin_operator
loadairplane april airplane2 parairport
1
0 3
1
0 10 3 5
1
end_operator
begin_operator
loadairplane avrim airplane1 bosairport
1
1 0
1
0 9 0 4
1
end_operator
begin_operator
loadairplane avrim airplane1 jfkairport
1
1 1
1
0 9 1 4
1
end_operator
begin_operator
loadairplane avrim airplane1 lonairport
1
1 2
1
0 9 2 4
1
end_operator
begin_operator
loadairplane avrim airplane1 parairport
1
1 3
1
0 9 3 4
1
end_operator
begin_operator
loadairplane avrim airplane2 bosairport
1
0 0
1
0 9 0 5
1
end_operator
begin_operator
loadairplane avrim airplane2 jfkairport
1
0 1
1
0 9 1 5
1
end_operator
begin_operator
loadairplane avrim airplane2 lonairport
1
0 2
1
0 9 2 5
1
end_operator
begin_operator
loadairplane avrim airplane2 parairport
1
0 3
1
0 9 3 5
1
end_operator
begin_operator
loadairplane betty airplane1 bosairport
1
1 0
1
0 8 0 4
1
end_operator
begin_operator
loadairplane betty airplane1 jfkairport
1
1 1
1
0 8 1 4
1
end_operator
begin_operator
loadairplane betty airplane1 lonairport
1
1 2
1
0 8 2 4
1
end_operator
begin_operator
loadairplane betty airplane1 parairport
1
1 3
1
0 8 3 4
1
end_operator
begin_operator
loadairplane betty airplane2 bosairport
1
0 0
1
0 8 0 5
1
end_operator
begin_operator
loadairplane betty airplane2 jfkairport
1
0 1
1
0 8 1 5
1
end_operator
begin_operator
loadairplane betty airplane2 lonairport
1
0 2
1
0 8 2 5
1
end_operator
begin_operator
loadairplane betty airplane2 parairport
1
0 3
1
0 8 3 5
1
end_operator
begin_operator
loadairplane jason airplane1 bosairport
1
1 0
1
0 7 0 4
1
end_operator
begin_operator
loadairplane jason airplane1 jfkairport
1
1 1
1
0 7 1 4
1
end_operator
begin_operator
loadairplane jason airplane1 lonairport
1
1 2
1
0 7 2 4
1
end_operator
begin_operator
loadairplane jason airplane1 parairport
1
1 3
1
0 7 3 4
1
end_operator
begin_operator
loadairplane jason airplane2 bosairport
1
0 0
1
0 7 0 5
1
end_operator
begin_operator
loadairplane jason airplane2 jfkairport
1
0 1
1
0 7 1 5
1
end_operator
begin_operator
loadairplane jason airplane2 lonairport
1
0 2
1
0 7 2 5
1
end_operator
begin_operator
loadairplane jason airplane2 parairport
1
0 3
1
0 7 3 5
1
end_operator
begin_operator
loadairplane lisa airplane1 bosairport
1
1 0
1
0 6 0 4
1
end_operator
begin_operator
loadairplane lisa airplane1 jfkairport
1
1 1
1
0 6 1 4
1
end_operator
begin_operator
loadairplane lisa airplane1 lonairport
1
1 2
1
0 6 2 4
1
end_operator
begin_operator
loadairplane lisa airplane1 parairport
1
1 3
1
0 6 3 4
1
end_operator
begin_operator
loadairplane lisa airplane2 bosairport
1
0 0
1
0 6 0 5
1
end_operator
begin_operator
loadairplane lisa airplane2 jfkairport
1
0 1
1
0 6 1 5
1
end_operator
begin_operator
loadairplane lisa airplane2 lonairport
1
0 2
1
0 6 2 5
1
end_operator
begin_operator
loadairplane lisa airplane2 parairport
1
0 3
1
0 6 3 5
1
end_operator
begin_operator
loadairplane michelle airplane1 bosairport
1
1 0
1
0 5 0 4
1
end_operator
begin_operator
loadairplane michelle airplane1 jfkairport
1
1 1
1
0 5 1 4
1
end_operator
begin_operator
loadairplane michelle airplane1 lonairport
1
1 2
1
0 5 2 4
1
end_operator
begin_operator
loadairplane michelle airplane1 parairport
1
1 3
1
0 5 3 4
1
end_operator
begin_operator
loadairplane michelle airplane2 bosairport
1
0 0
1
0 5 0 5
1
end_operator
begin_operator
loadairplane michelle airplane2 jfkairport
1
0 1
1
0 5 1 5
1
end_operator
begin_operator
loadairplane michelle airplane2 lonairport
1
0 2
1
0 5 2 5
1
end_operator
begin_operator
loadairplane michelle airplane2 parairport
1
0 3
1
0 5 3 5
1
end_operator
begin_operator
loadairplane mxf airplane1 bosairport
1
1 0
1
0 4 0 4
1
end_operator
begin_operator
loadairplane mxf airplane1 jfkairport
1
1 1
1
0 4 1 4
1
end_operator
begin_operator
loadairplane mxf airplane1 lonairport
1
1 2
1
0 4 2 4
1
end_operator
begin_operator
loadairplane mxf airplane1 parairport
1
1 3
1
0 4 3 4
1
end_operator
begin_operator
loadairplane mxf airplane2 bosairport
1
0 0
1
0 4 0 5
1
end_operator
begin_operator
loadairplane mxf airplane2 jfkairport
1
0 1
1
0 4 1 5
1
end_operator
begin_operator
loadairplane mxf airplane2 lonairport
1
0 2
1
0 4 2 5
1
end_operator
begin_operator
loadairplane mxf airplane2 parairport
1
0 3
1
0 4 3 5
1
end_operator
begin_operator
loadairplane paper airplane1 bosairport
1
1 0
1
0 3 0 4
1
end_operator
begin_operator
loadairplane paper airplane1 jfkairport
1
1 1
1
0 3 1 4
1
end_operator
begin_operator
loadairplane paper airplane1 lonairport
1
1 2
1
0 3 2 4
1
end_operator
begin_operator
loadairplane paper airplane1 parairport
1
1 3
1
0 3 3 4
1
end_operator
begin_operator
loadairplane paper airplane2 bosairport
1
0 0
1
0 3 0 5
1
end_operator
begin_operator
loadairplane paper airplane2 jfkairport
1
0 1
1
0 3 1 5
1
end_operator
begin_operator
loadairplane paper airplane2 lonairport
1
0 2
1
0 3 2 5
1
end_operator
begin_operator
loadairplane paper airplane2 parairport
1
0 3
1
0 3 3 5
1
end_operator
begin_operator
loadairplane pencil airplane1 bosairport
1
1 0
1
0 2 0 4
1
end_operator
begin_operator
loadairplane pencil airplane1 jfkairport
1
1 1
1
0 2 1 4
1
end_operator
begin_operator
loadairplane pencil airplane1 lonairport
1
1 2
1
0 2 2 4
1
end_operator
begin_operator
loadairplane pencil airplane1 parairport
1
1 3
1
0 2 3 4
1
end_operator
begin_operator
loadairplane pencil airplane2 bosairport
1
0 0
1
0 2 0 5
1
end_operator
begin_operator
loadairplane pencil airplane2 jfkairport
1
0 1
1
0 2 1 5
1
end_operator
begin_operator
loadairplane pencil airplane2 lonairport
1
0 2
1
0 2 2 5
1
end_operator
begin_operator
loadairplane pencil airplane2 parairport
1
0 3
1
0 2 3 5
1
end_operator
begin_operator
unloadairplane alex airplane1 bosairport
1
1 0
1
0 11 4 0
1
end_operator
begin_operator
unloadairplane alex airplane1 jfkairport
1
1 1
1
0 11 4 1
1
end_operator
begin_operator
unloadairplane alex airplane1 lonairport
1
1 2
1
0 11 4 2
1
end_operator
begin_operator
unloadairplane alex airplane1 parairport
1
1 3
1
0 11 4 3
1
end_operator
begin_operator
unloadairplane alex airplane2 bosairport
1
0 0
1
0 11 5 0
1
end_operator
begin_operator
unloadairplane alex airplane2 jfkairport
1
0 1
1
0 11 5 1
1
end_operator
begin_operator
unloadairplane alex airplane2 lonairport
1
0 2
1
0 11 5 2
1
end_operator
begin_operator
unloadairplane alex airplane2 parairport
1
0 3
1
0 11 5 3
1
end_operator
begin_operator
unloadairplane april airplane1 bosairport
1
1 0
1
0 10 4 0
1
end_operator
begin_operator
unloadairplane april airplane1 jfkairport
1
1 1
1
0 10 4 1
1
end_operator
begin_operator
unloadairplane april airplane1 lonairport
1
1 2
1
0 10 4 2
1
end_operator
begin_operator
unloadairplane april airplane1 parairport
1
1 3
1
0 10 4 3
1
end_operator
begin_operator
unloadairplane april airplane2 bosairport
1
0 0
1
0 10 5 0
1
end_operator
begin_operator
unloadairplane april airplane2 jfkairport
1
0 1
1
0 10 5 1
1
end_operator
begin_operator
unloadairplane april airplane2 lonairport
1
0 2
1
0 10 5 2
1
end_operator
begin_operator
unloadairplane april airplane2 parairport
1
0 3
1
0 10 5 3
1
end_operator
begin_operator
unloadairplane avrim airplane1 bosairport
1
1 0
1
0 9 4 0
1
end_operator
begin_operator
unloadairplane avrim airplane1 jfkairport
1
1 1
1
0 9 4 1
1
end_operator
begin_operator
unloadairplane avrim airplane1 lonairport
1
1 2
1
0 9 4 2
1
end_operator
begin_operator
unloadairplane avrim airplane1 parairport
1
1 3
1
0 9 4 3
1
end_operator
begin_operator
unloadairplane avrim airplane2 bosairport
1
0 0
1
0 9 5 0
1
end_operator
begin_operator
unloadairplane avrim airplane2 jfkairport
1
0 1
1
0 9 5 1
1
end_operator
begin_operator
unloadairplane avrim airplane2 lonairport
1
0 2
1
0 9 5 2
1
end_operator
begin_operator
unloadairplane avrim airplane2 parairport
1
0 3
1
0 9 5 3
1
end_operator
begin_operator
unloadairplane betty airplane1 bosairport
1
1 0
1
0 8 4 0
1
end_operator
begin_operator
unloadairplane betty airplane1 jfkairport
1
1 1
1
0 8 4 1
1
end_operator
begin_operator
unloadairplane betty airplane1 lonairport
1
1 2
1
0 8 4 2
1
end_operator
begin_operator
unloadairplane betty airplane1 parairport
1
1 3
1
0 8 4 3
1
end_operator
begin_operator
unloadairplane betty airplane2 bosairport
1
0 0
1
0 8 5 0
1
end_operator
begin_operator
unloadairplane betty airplane2 jfkairport
1
0 1
1
0 8 5 1
1
end_operator
begin_operator
unloadairplane betty airplane2 lonairport
1
0 2
1
0 8 5 2
1
end_operator
begin_operator
unloadairplane betty airplane2 parairport
1
0 3
1
0 8 5 3
1
end_operator
begin_operator
unloadairplane jason airplane1 bosairport
1
1 0
1
0 7 4 0
1
end_operator
begin_operator
unloadairplane jason airplane1 jfkairport
1
1 1
1
0 7 4 1
1
end_operator
begin_operator
unloadairplane jason airplane1 lonairport
1
1 2
1
0 7 4 2
1
end_operator
begin_operator
unloadairplane jason airplane1 parairport
1
1 3
1
0 7 4 3
1
end_operator
begin_operator
unloadairplane jason airplane2 bosairport
1
0 0
1
0 7 5 0
1
end_operator
begin_operator
unloadairplane jason airplane2 jfkairport
1
0 1
1
0 7 5 1
1
end_operator
begin_operator
unloadairplane jason airplane2 lonairport
1
0 2
1
0 7 5 2
1
end_operator
begin_operator
unloadairplane jason airplane2 parairport
1
0 3
1
0 7 5 3
1
end_operator
begin_operator
unloadairplane lisa airplane1 bosairport
1
1 0
1
0 6 4 0
1
end_operator
begin_operator
unloadairplane lisa airplane1 jfkairport
1
1 1
1
0 6 4 1
1
end_operator
begin_operator
unloadairplane lisa airplane1 lonairport
1
1 2
1
0 6 4 2
1
end_operator
begin_operator
unloadairplane lisa airplane1 parairport
1
1 3
1
0 6 4 3
1
end_operator
begin_operator
unloadairplane lisa airplane2 bosairport
1
0 0
1
0 6 5 0
1
end_operator
begin_operator
unloadairplane lisa airplane2 jfkairport
1
0 1
1
0 6 5 1
1
end_operator
begin_operator
unloadairplane lisa airplane2 lonairport
1
0 2
1
0 6 5 2
1
end_operator
begin_operator
unloadairplane lisa airplane2 parairport
1
0 3
1
0 6 5 3
1
end_operator
begin_operator
unloadairplane michelle airplane1 bosairport
1
1 0
1
0 5 4 0
1
end_operator
begin_operator
unloadairplane michelle airplane1 jfkairport
1
1 1
1
0 5 4 1
1
end_operator
begin_operator
unloadairplane michelle airplane1 lonairport
1
1 2
1
0 5 4 2
1
end_operator
begin_operator
unloadairplane michelle airplane1 parairport
1
1 3
1
0 5 4 3
1
end_operator
begin_operator
unloadairplane michelle airplane2 bosairport
1
0 0
1
0 5 5 0
1
end_operator
begin_operator
unloadairplane michelle airplane2 jfkairport
1
0 1
1
0 5 5 1
1
end_operator
begin_operator
unloadairplane michelle airplane2 lonairport
1
0 2
1
0 5 5 2
1
end_operator
begin_operator
unloadairplane michelle airplane2 parairport
1
0 3
1
0 5 5 3
1
end_operator
begin_operator
unloadairplane mxf airplane1 bosairport
1
1 0
1
0 4 4 0
1
end_operator
begin_operator
unloadairplane mxf airplane1 jfkairport
1
1 1
1
0 4 4 1
1
end_operator
begin_operator
unloadairplane mxf airplane1 lonairport
1
1 2
1
0 4 4 2
1
end_operator
begin_operator
unloadairplane mxf airplane1 parairport
1
1 3
1
0 4 4 3
1
end_operator
begin_operator
unloadairplane mxf airplane2 bosairport
1
0 0
1
0 4 5 0
1
end_operator
begin_operator
unloadairplane mxf airplane2 jfkairport
1
0 1
1
0 4 5 1
1
end_operator
begin_operator
unloadairplane mxf airplane2 lonairport
1
0 2
1
0 4 5 2
1
end_operator
begin_operator
unloadairplane mxf airplane2 parairport
1
0 3
1
0 4 5 3
1
end_operator
begin_operator
unloadairplane paper airplane1 bosairport
1
1 0
1
0 3 4 0
1
end_operator
begin_operator
unloadairplane paper airplane1 jfkairport
1
1 1
1
0 3 4 1
1
end_operator
begin_operator
unloadairplane paper airplane1 lonairport
1
1 2
1
0 3 4 2
1
end_operator
begin_operator
unloadairplane paper airplane1 parairport
1
1 3
1
0 3 4 3
1
end_operator
begin_operator
unloadairplane paper airplane2 bosairport
1
0 0
1
0 3 5 0
1
end_operator
begin_operator
unloadairplane paper airplane2 jfkairport
1
0 1
1
0 3 5 1
1
end_operator
begin_operator
unloadairplane paper airplane2 lonairport
1
0 2
1
0 3 5 2
1
end_operator
begin_operator
unloadairplane paper airplane2 parairport
1
0 3
1
0 3 5 3
1
end_operator
begin_operator
unloadairplane pencil airplane1 bosairport
1
1 0
1
0 2 4 0
1
end_operator
begin_operator
unloadairplane pencil airplane1 jfkairport
1
1 1
1
0 2 4 1
1
end_operator
begin_operator
unloadairplane pencil airplane1 lonairport
1
1 2
1
0 2 4 2
1
end_operator
begin_operator
unloadairplane pencil airplane1 parairport
1
1 3
1
0 2 4 3
1
end_operator
begin_operator
unloadairplane pencil airplane2 bosairport
1
0 0
1
0 2 5 0
1
end_operator
begin_operator
unloadairplane pencil airplane2 jfkairport
1
0 1
1
0 2 5 1
1
end_operator
begin_operator
unloadairplane pencil airplane2 lonairport
1
0 2
1
0 2 5 2
1
end_operator
begin_operator
unloadairplane pencil airplane2 parairport
1
0 3
1
0 2 5 3
1
end_operator
0
