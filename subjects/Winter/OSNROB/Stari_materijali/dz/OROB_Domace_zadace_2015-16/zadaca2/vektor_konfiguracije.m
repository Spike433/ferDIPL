function w=vektor_kofniguracije(q,l)
w(1)=cos(q(1))*(l(1)*sin(q(2))+l(2)*cos(q(2))+(l(3)+l(4))*sin(q(2)+q(4)));
w(2)=sin(q(1))*(l(1)*sin(q(2))+l(2)*cos(q(2))+(l(3)+l(4))*sin(q(2)+q(4)));
w(3)=-l(1)*cos(q(2))+l(2)*sin(q(2))-(l(3)+l(4))*cos(q(2)+q(4));
w(4)=cos(q(1))*sin(q(5))*cos(q(2)+q(4))-sin(q(1))*cos(q(5));
w(5)=sin(q(1))*sin(q(5))*cos(q(2)+q(4))+cos(q(1))*cos(q(5));
w(6)=sin(q(5))*sin(q(2)+q(4));
end
    