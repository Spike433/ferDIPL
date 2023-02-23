function q=ik_nao_larm(w,l)
% Q = IK_NAO_LARM(W,L) racuna inverznu kinematku lijeve ruke Nao robota
% Za zadane vektore konfiguracije alata W i karakteristicnih duljina L,
% funkcija vraca matricu Q koja sadrzi sva moguca rjesenja inverznog
% kinematickog problema. Svaki redak matrice Q predstavlja jedno
% moguce rjesenje. U slucaju da je zadani W izvan radnog prostora,
% funkcija vraca praznu matricu Q.

q=zeros(1,5);
if sqrt(w(1)^2+w(2)^2+w(3)^2)>=(l(1)+l(3)+l(4))
    fprintf('w(q) se nalazi izvan radnog prostora robota')
else    
    mat(1,1)=atan2(w(2),w(1));
    mat(1,3)=0;
    mat(1,5)=acos(w(5)*cos(mat(1,1))-w(4)*sin(mat(1,1)));
    mat(1,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(1,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(1,5))+l(1)*(w(4)+sin(mat(1,1))*cos(mat(1,5)))/(sin(mat(1,5))*cos(mat(1,1))))-l(1)*w(3)));
    mat(1,4)=asin(w(6)/sin(mat(1,5)))-mat(1,2);
    
    mat(2,1)=atan2(w(2),w(1));
    mat(2,3)=0;
    mat(2,5)=-acos(w(5)*cos(mat(2,1))-w(4)*sin(mat(2,1)));
    mat(2,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(2,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(2,5))+l(1)*(w(4)+sin(mat(2,1))*cos(mat(2,5)))/(sin(mat(2,5))*cos(mat(2,1))))-l(1)*w(3)));
    mat(2,4)=asin(w(6)/sin(mat(2,5)))-mat(2,2);
    
    mat(3,1)=atan2(w(2),w(1));
    mat(3,3)=0;
    mat(3,5)=acos(w(5)*cos(mat(3,1))-w(4)*sin(mat(3,1)));
    mat(3,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(3,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(3,5))+l(1)*(w(4)+sin(mat(3,1))*cos(mat(3,5)))/(sin(mat(3,5))*cos(mat(3,1))))-l(1)*w(3)));
    mat(3,4)=pi-asin(w(6)/sin(mat(3,5)))-mat(3,2);
    
    mat(4,1)=atan2(w(2),w(1));
    mat(4,3)=0;
    mat(4,5)=-acos(w(5)*cos(mat(4,1))-w(4)*sin(mat(4,1)));
    mat(4,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(4,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(4,5))+l(1)*(w(4)+sin(mat(4,1))*cos(mat(4,5)))/(sin(mat(4,5))*cos(mat(4,1))))-l(1)*w(3)));
    mat(4,4)=pi-asin(w(6)/sin(mat(4,5)))-mat(4,2);
    
    mat(5,1)=atan2(w(2),w(1));
    mat(5,3)=0;
    mat(5,5)=acos(w(5)*cos(mat(5,1))-w(4)*sin(mat(5,1)));
    mat(5,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(5,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(5,5))+l(1)*(w(4)+sin(mat(5,1))*cos(mat(5,5)))/(sin(mat(5,5))*cos(mat(5,1))))-l(1)*w(3)));
    mat(5,4)=asin(w(6)/sin(mat(5,5)))-mat(5,2);
    
    mat(6,1)=atan2(w(2),w(1));
    mat(6,3)=0;
    mat(6,5)=-acos(w(5)*cos(mat(6,1))-w(4)*sin(mat(6,1)));
    mat(6,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(6,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(6,5))+l(1)*(w(4)+sin(mat(6,1))*cos(mat(6,5)))/(sin(mat(6,5))*cos(mat(6,1))))-l(1)*w(3)));
    mat(6,4)=asin(w(6)/sin(mat(6,5)))-mat(6,2);
    
    mat(7,1)=atan2(w(2),w(1));
    mat(7,3)=0;
    mat(7,5)=acos(w(5)*cos(mat(7,1))-w(4)*sin(mat(7,1)));
    mat(7,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(7,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(7,5))+l(1)*(w(4)+sin(mat(7,1))*cos(mat(7,5)))/(sin(mat(7,5))*cos(mat(7,1))))-l(1)*w(3)));
    mat(7,4)=pi-asin(w(6)/sin(mat(7,5)))-mat(7,2);
    
    mat(8,1)=atan2(w(2),w(1));
    mat(8,3)=0;
    mat(8,5)=-acos(w(5)*cos(mat(8,1))-w(4)*sin(mat(8,1)));
    mat(8,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(8,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(8,5))+l(1)*(w(4)+sin(mat(8,1))*cos(mat(8,5)))/(sin(mat(8,5))*cos(mat(8,1))))-l(1)*w(3)));
    mat(8,4)=pi-asin(w(6)/sin(mat(8,5)))-mat(8,2);
    
    mat(9,1)=pi+atan2(w(2),w(1));
    mat(9,3)=0;
    mat(9,5)=acos(w(5)*cos(mat(9,1))-w(4)*sin(mat(9,1)));
    mat(9,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(9,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(9,5))+l(1)*(w(4)+sin(mat(9,1))*cos(mat(9,5)))/(sin(mat(9,5))*cos(mat(9,1))))-l(1)*w(3)));
    mat(9,4)=asin(w(6)/sin(mat(9,5)))-mat(9,2);
    
    mat(10,1)=pi+atan2(w(2),w(1));
    mat(10,3)=0;
    mat(10,5)=-acos(w(5)*cos(mat(10,1))-w(4)*sin(mat(10,1)));
    mat(10,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(10,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(10,5))+l(1)*(w(4)+sin(mat(10,1))*cos(mat(10,5)))/(sin(mat(10,5))*cos(mat(10,1))))-l(1)*w(3)));
    mat(10,4)=asin(w(6)/sin(mat(10,5)))-mat(10,2);
    
    mat(11,1)=pi+atan2(w(2),w(1));
    mat(11,3)=0;
    mat(11,5)=acos(w(5)*cos(mat(11,1))-w(4)*sin(mat(11,1)));
    mat(11,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(11,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(11,5))+l(1)*(w(4)+sin(mat(11,1))*cos(mat(11,5)))/(sin(mat(11,5))*cos(mat(11,1))))-l(1)*w(3)));
    mat(11,4)=pi-asin(w(6)/sin(mat(11,5)))-mat(11,2);
    
    mat(12,1)=pi+atan2(w(2),w(1));
    mat(12,3)=0;
    mat(12,5)=-acos(w(5)*cos(mat(12,1))-w(4)*sin(mat(12,1)));
    mat(12,2)=acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(12,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(12,5))+l(1)*(w(4)+sin(mat(12,1))*cos(mat(12,5)))/(sin(mat(12,5))*cos(mat(12,1))))-l(1)*w(3)));
    mat(12,4)=pi-asin(w(6)/sin(mat(12,5)))-mat(12,2);
    
    mat(13,1)=pi+atan2(w(2),w(1));
    mat(13,3)=0;
    mat(13,5)=acos(w(5)*cos(mat(13,1))-w(4)*sin(mat(13,1)));
    mat(13,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(13,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(13,5))+l(1)*(w(4)+sin(mat(13,1))*cos(mat(13,5)))/(sin(mat(13,5))*cos(mat(13,1))))-l(1)*w(3)));
    mat(13,4)=asin(w(6)/sin(mat(13,5)))-mat(13,2);
    
    mat(14,1)=pi+atan2(w(2),w(1));
    mat(14,3)=0;
    mat(14,5)=-acos(w(5)*cos(mat(14,1))-w(4)*sin(mat(14,1)));
    mat(14,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(14,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(14,5))+l(1)*(w(4)+sin(mat(14,1))*cos(mat(14,5)))/(sin(mat(14,5))*cos(mat(14,1))))-l(1)*w(3)));
    mat(14,4)=asin(w(6)/sin(mat(14,5)))-mat(14,2);
    
    mat(15,1)=pi+atan2(w(2),w(1));
    mat(15,3)=0;
    mat(15,5)=acos(w(5)*cos(mat(15,1))-w(4)*sin(mat(15,1)));
    mat(15,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(15,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(15,5))+l(1)*(w(4)+sin(mat(15,1))*cos(mat(15,5)))/(sin(mat(15,5))*cos(mat(15,1))))-l(1)*w(3)));
    mat(15,4)=pi-asin(w(6)/sin(mat(15,5)))-mat(15,2);
    
    mat(16,1)=pi+atan2(w(2),w(1));
    mat(16,3)=0;
    mat(16,5)=-acos(w(5)*cos(mat(16,1))-w(4)*sin(mat(16,1)));
    mat(16,2)=-acos((1/(l(2)^2+l(1)^2))*(l(2)*w(1)/cos(mat(16,1))-(l(3)+l(4))*(l(2)*w(6)/sin(mat(16,5))+l(1)*(w(4)+sin(mat(16,1))*cos(mat(16,5)))/(sin(mat(16,5))*cos(mat(16,1))))-l(1)*w(3)));
    mat(16,4)=pi-asin(w(6)/sin(mat(16,5)))-mat(16,2);
    
    j=1;
    for i=1:16
        if round(vektor_konfiguracije(mat(i,:), l)*10000)/10000==round(w*10000)/10000   
            q(j,:)=mat(i,:);
            j=j+1;
        end
    end    
end
end
