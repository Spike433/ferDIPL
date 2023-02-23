%% 1. Domaca zadaca, Osnove robotike, Miha the mighty, 1.D_AUT, 4/11/2012
clear
clc
%% Inicijalizacija potrebnih varijabli 
syms theta_k alpha_k a_k d_k q30

syms q1 q2 q3 q4                % varijable zglobova
alpha = [pi/2, pi/2, 0, 0];     % DH parametri alpha
syms d1 d2 d3 d4                % DH parametri d
syms a1 a2 a3 a4;               % DH parametri a

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

T_01 = subs(T_k, [theta_k, d_k, a_k, alpha_k], [q1, d1, 0, alpha(1)]);
T_12 = subs(T_k, [theta_k, d_k, a_k, alpha_k], [q2, 0, 0, alpha(2)]);
T_23 = subs(T_k, [theta_k, d_k, a_k, alpha_k], [pi/2, q3, 0, alpha(3)]);
T_34 = subs(T_k, [theta_k, d_k, a_k, alpha_k], [q4, d4, 0, alpha(4)]);

% Izracun matrice koja povezuje koordinatne sustave baze i alata

T_04 = simple(T_01*T_12*T_23*T_34)

% Iz matrice T_04 uzimamo vektor polozaja p

p = T_04(1:3,4);

% Racunamo koordinate vrha alata u odnosu na koordinatni sustav baze
% manipulatora za pocetne uvijete 

xyz_alat = subs(p, {q1,q2,q3,q4}, {pi/2, pi/2, q30, 0})

% Iz matrice T_04 uzimamo matricu rotacije R

R = T_04(1:3,1:3);

% Raèunamo orijentaciju alata u odnosu na koordinatni sustav baze
% manipulatora

alat_orijentacija = subs(R, {q1,q2,q3,q4}, {pi/2, pi/2, q30, 0})


