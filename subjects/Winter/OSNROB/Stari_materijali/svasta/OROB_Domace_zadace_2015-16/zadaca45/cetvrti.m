syms theta d alfa a
syms l1 l2 l3 l4
syms q1 q2 q3 q4 q5
syms m1 m2 m3 m4 m5
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
z0=[0; 0; 1];
z1=[T01(1, 3); T01(2, 3); T01(3, 3)];
z2=[T02(1, 3); T02(2, 3); T02(3, 3)];
z3=[T03(1, 3); T03(2, 3); T03(3, 3)];
z4=[T04(1, 3); T04(2, 3); T04(3, 3)];
H1=[1, 0, 0, 0; 0, 1, 0, 0; 0, 0, 1, 0];
%k=1
deltac1=[0; 0; 0; 1];
D1=m1*[0, 0, 0; 0, 0, 0; 0, 0, 0];
c1=H1*T01*deltac1;
R01=[T01(1,1), T01(1,2), T01(1,3); T01(2,1), T01(2,2), T01(2,3); T01(3,1), T01(3,2), T01(3,3)];
D1q=R01*D1*transpose(R01);
A1=[diff(c1(1), q1), 0, 0, 0, 0; diff(c1(2), q1), 0, 0, 0, 0; diff(c1(3), q1), 0, 0, 0, 0];
B1=[z0, [0; 0; 0], [0; 0; 0], [0; 0; 0], [0; 0; 0]];
%k=2
deltac2=[-l1/2; 0; 0; 1];
D2=1/12*m2*l1^2*[0, 0, 0; 0, 1, 0; 0, 0, 1];
c2=H1*T02*deltac2;
R02=[T02(1,1), T02(1,2), T02(1,3); T02(2,1), T02(2,2), T02(2,3); T02(3,1), T02(3,2), T02(3,3)];
D2q=R02*D2*transpose(R02);
A2=[diff(c2(1), q1), diff(c2(1), q2), 0, 0, 0; diff(c2(2), q1), diff(c2(2), q2), 0, 0, 0; diff(c2(3), q1), diff(c2(3), q2), 0, 0, 0];
B2=[z0, z1, [0; 0; 0], [0; 0; 0], [0; 0; 0]];
%k=3
deltac3=[0; l2/2; 0; 1];
D3=1/12*m3*l2^2*[1, 0, 0; 0, 0, 0; 0, 0, 1];
c3=H1*T03*deltac3;
R03=[T03(1,1), T03(1,2), T03(1,3); T03(2,1), T03(2,2), T03(2,3); T03(3,1), T03(3,2), T03(3,3)];
D3q=R03*D3*transpose(R03);
A3=[diff(c3(1), q1), diff(c3(1), q2), diff(c3(1), q3), 0, 0; diff(c3(2), q1), diff(c3(2), q2), diff(c3(2), q3), 0, 0; diff(c3(3), q1), diff(c3(3), q2), diff(c3(3), q3), 0, 0];
B3=[z0, z1, z2, [0; 0; 0], [0; 0; 0]];
%k=4
deltac4=[0; 0; 0; 1];
D4=m4*[0, 0, 0; 0, 0, 0; 0, 0, 0];
c4=H1*T04*deltac4;
R04=[T04(1,1), T04(1,2), T04(1,3); T04(2,1), T04(2,2), T04(2,3); T04(3,1), T04(3,2), T04(3,3)];
D4q=R04*D4*transpose(R04);
A4=[diff(c4(1), q1), diff(c4(1), q2), diff(c4(1), q3), diff(c4(1), q4), 0; diff(c4(2), q1), diff(c4(2), q2), diff(c4(2), q3), diff(c4(2), q4), 0; diff(c4(3), q1), diff(c4(3), q2), diff(c4(3), q3), diff(c4(3), q4), 0];
B4=[z0, z1, z2, z3, [0; 0; 0]];
%k=5
deltac5=[0; -(l3+l4)/2; 0; 1];
D5=1/12*m5*(l3+l4)^2*[1, 0, 0; 0, 0, 0; 0, 0, 1];
c5=H1*T05*deltac5;
R05=[T05(1,1), T05(1,2), T05(1,3); T05(2,1), T05(2,2), T05(2,3); T05(3,1), T05(3,2), T05(3,3)];
D5q=R05*D5*transpose(R05);
A5=[diff(c5(1), q1), diff(c5(1), q2), diff(c5(1), q3), diff(c5(1), q4), diff(c5(1), q5); diff(c5(2), q1), diff(c5(2), q2), diff(c5(2), q3), diff(c5(2), q4), diff(c5(2), q5); diff(c5(3), q1), diff(c5(3), q2), diff(c5(3), q3), diff(c5(3), q4), diff(c5(3), q5)];
B5=[z0, z1, z2, z3, z4];

D=transpose(A1)*m1*A1+transpose(B1)*D1q*B1+transpose(A2)*m2*A2+transpose(B2)*D2q*B2+transpose(A3)*m3*A3+transpose(B3)*D3q*B3+transpose(A4)*m4*A4+transpose(B4)*D4q*B4+transpose(A5)*m5*A5+transpose(B5)*D5q*B5;
qdiff=[-200; 0; 0; -200; -200];
T=transpose(qdiff)*D*qdiff/2;
T=subs(T, [q1, q2, q3, q4, q5, l1, l2, l3, l4], [pi/3 0 pi/2 pi/6 pi/2, 0.015, 0.105, 0.05595, 0.0575]);
vpa(T, 6)