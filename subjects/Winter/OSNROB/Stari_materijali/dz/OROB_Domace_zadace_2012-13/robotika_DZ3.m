clear
clc
%% Inicijalizacija potrebnih varijabli 
syms theta_k alpha_k a_k d_k L2 m1 m2 L1

syms q1 q2                      % varijable zglobova
alpha = [0 pi];                 % DH parametri alpha
syms d1 d2                      % DH parametri d
syms a1 a2                      % DH parametri a

%% Definiranje opcenite matrice homogene transformacije koja koja povezuje
%  koordinatne sustave k i k-1.

T_k = [
cos(theta_k),-cos(alpha_k)*sin(theta_k),sin(alpha_k)*sin(theta_k),a_k*cos(theta_k) ;
sin(theta_k),cos(alpha_k)*cos(theta_k),-sin(alpha_k)*cos(theta_k),a_k*sin(theta_k) ;
0, sin(alpha_k), cos(alpha_k),d_k ;
0, 0, 0,1 ;
];

%% Zamjena varijabli u opcenitoj matrici homogene trasnformacije s
%  DH parametrima 

T_00 = eye(4);
T_01 = subs(T_k, [theta_k, d_k, a_k, alpha_k], [0, q1, 0, 0]);
T_12 = subs(T_k, [theta_k, d_k, a_k, alpha_k], [q2, 0, L2, pi]);

% Izracun matrice koja povezuje koordinatne sustave baze i alata

T_02 = simple(T_01*T_12);

% Iz matrice T_02 uzimamo vektor polozaja p

p = T_02(1:3,4);

% Iz matrice T_02 uzimamo matricu rotacije R
R_00= T_00(1:3,1:3);
R_01 = T_01(1:3,1:3);
R_12 = T_12(1:3,1:3);
R_02 = T_02(1:3,1:3);

% Definiranje deltaC vektora
deltaC1 = transpose([0 0 -L1/2 1]);  % mora biti konstanta? treba bit [0 0 -L1/2 1] 
                                     % to znaci da se zglob cijeli mice nekako, tj sve se podize
deltaC2 = transpose([-L2/2 0 0 1]);

%% Definiranje vektora z0
z0 = R_00*transpose([0 0 1]);

% Definiranje matrice H1

H1 = [eye(3), zeros(3,1)];

%% Izracun c1 i c2 vektora

c1 = H1*T_01*deltaC1;
c2 = H1*T_02*deltaC2;


%% Tenzori inercije clanaka s obzirom na CM
D_1_cm = m1*L1^2/12*[1 0 0; 0 1 0; 0 0 0];
D_2_cm =  m2*L2^2/12*[0 0 0; 0 1 0; 0 0 1];

% Izracun D1
D1 = R_01*D_1_cm*transpose(R_01);

%% Djelovi J1
A1 = [diff(c1,q1), diff(c1,q2)]; % bilo [0 0 ; 0 0 ; 1/2 0]
B1 = [0 0 ; 0 0 ; 0 0];

D =  transpose(A1)*m1*A1+transpose(B1)*D1*B1;

%% Definiranje vektora z1
z1 = R_01*transpose([0 0 1]);

%% Izracun D2

D2 = R_02*D_2_cm*transpose(R_02);

%% Clanovi J2
A2 = [diff(c2,q1), diff(c2,q2) ];
B2 = [0 0 ; 0 0 ; 0 1];

%% Izracun krajnjeg D
D =D + transpose(A2)*m2*A2+transpose(B2)*D2*B2;

disp('Tenzor inercije manipulatora D(q):')
pretty(simple(D))