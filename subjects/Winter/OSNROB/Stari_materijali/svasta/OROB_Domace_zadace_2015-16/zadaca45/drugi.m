syms theta d alfa a
syms l1 l2 l3 l4
syms q1 q2 q3 q4 q5
Topci=[cos(theta), -cos(alfa)*sin(theta), sin(alfa)*sin(theta), a*cos(theta); sin(theta), cos(alfa)*cos(theta), -sin(alfa)*cos(theta), a*sin(theta); 0, sin(alfa), cos(alfa), d; 0, 0, 0, 1];
T01=subs(Topci, [theta, d, alfa, a], [q1+pi, 0, -pi/2, 0]);
T12=subs(Topci, [theta, d, alfa, a], [q2-pi/2, 0, pi/2, l1]);
T23=subs(Topci, [theta, d, alfa, a], [q3, l2, -pi/2, 0]);
T34=subs(Topci, [theta, d, alfa, a], [q4, 0, pi/2, 0]);
T45=subs(Topci, [theta, d, alfa, a], [q5, l3+l4, pi/2, 0]);
T02=T01*T12;
T03=T02*T23;
T04=T03*T34;
T05=T04*T45;
p5=[T05(1, 4); T05(2, 4); T05(3, 4)];
A=[diff(p5(1), q1), diff(p5(1), q2), diff(p5(1), q3), diff(p5(1), q4), diff(p5(1), q5); diff(p5(2), q1), diff(p5(2), q2), diff(p5(2), q3), diff(p5(2), q4), diff(p5(2), q5); diff(p5(3), q1), diff(p5(3), q2), diff(p5(3), q3), diff(p5(3), q4), diff(p5(3), q5)];
A=subs(A, [q1, q2, q3, q4, q5, l1, l2, l3, l4], [pi/3 0 pi/2 pi/6 pi/2, 0.015, 0.105, 0.05595, 0.0575]);
z0=[0; 0; 1];
z1=[T01(1, 3); T01(2, 3); T01(3, 3)];
z2=[T02(1, 3); T02(2, 3); T02(3, 3)];
z3=[T03(1, 3); T03(2, 3); T03(3, 3)];
z4=[T04(1, 3); T04(2, 3); T04(3, 3)];
B=[z0, z1, z2, z3, z4];
B=subs(B, [q1, q2, q3, q4, q5, l1, l2, l3, l4], [pi/3 0 pi/2 pi/6 pi/2, 0.015, 0.105, 0.05595, 0.0575]);
qdiff=[-200; 0; 0; -200; -200];
v=vpa(A*qdiff, 6)
w=vpa(B*qdiff, 6)