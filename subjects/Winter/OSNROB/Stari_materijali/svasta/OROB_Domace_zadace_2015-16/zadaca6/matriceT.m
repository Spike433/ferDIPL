syms theta d alfa a
syms l1 l2 l3 l4
syms q1 q2 q3
Topci=[cos(theta), -cos(alfa)*sin(theta), sin(alfa)*sin(theta), a*cos(theta); sin(theta), cos(alfa)*cos(theta), -sin(alfa)*cos(theta), a*sin(theta); 0, sin(alfa), cos(alfa), d; 0, 0, 0, 1];
T01=subs(Topci, [theta, d, alfa, a], [q1+pi, 0, -pi/2, 0]);
T12=subs(Topci, [theta, d, alfa, a], [-pi/2, 0, pi/2, l1]);
T23=subs(Topci, [theta, d, alfa, a], [pi/2, l2, -pi/2, 0]);
T34=subs(Topci, [theta, d, alfa, a], [q4, 0, pi/2, 0]);
T45=subs(Topci, [theta, d, alfa, a], [q5, l3+l4, pi/2, 0]);
T01
T02=T01*T12
T03=T02*T23
T04=T03*T34
T05=T04*T45