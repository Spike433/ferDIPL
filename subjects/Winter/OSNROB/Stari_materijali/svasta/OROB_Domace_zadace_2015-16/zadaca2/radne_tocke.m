clc
l = [105 15 55.95 57.50];
    fprintf('Radna tocka %d:', i);
    q=[rand rand 0 rand rand]
    fprintf('Vektor konfiguracije:')
    w = vektor_konfiguracije(q, l)
    fprintf('Inverzna kinematika:')

    q = ik_nao_larm(w, l)
       if q(1,:) == zeros(1,5)
           return
       end
    fprintf('Direktna kinematika:')
    w1 = vektor_konfiguracije(q(1,:), l)
    if size(q, 1) == 2
        w2 = vektor_konfiguracije(q(2,:), l)
    end