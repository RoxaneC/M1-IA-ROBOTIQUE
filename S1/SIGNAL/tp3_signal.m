% initialisation des variables
f_0 = 50;
w_0 = 2*pi*f_0;

f = 0:0.01:100;
w = 2*pi.*f;
S = 1i.*w;
theta = [60 80 87];

for t = theta
    % calcul de H(S)
    H = (S.^2 + w_0^2) ./ (S.^2 + 2*w_0*cos(t).*S + w_0^2);
    
    % visualisation des pôles et des zéros
    p1 = -w_0*exp(1i*t);
    p2 = -w_0*exp(-1i*t);
    z1 = 1i*w_0;
    z2 = -1i*w_0;
    
    figure; hold on
    plot(real([p1, p2]), imag([p1, p2]), 'r+')
    plot(real([z1, z2]), imag([z1, z2]), 'go')
    grid
    xlabel('Partie Réelle');        ylabel('Partie Imaginaire')
    title(['Position des pôles et des zéros sur le plan S pour theta = ' num2str(t)])
    axis equal;

    % visualisation du module et de la phase
    module = 20*log10(abs(H));
    phase = angle(H);

    figure;
    plot(w/pi,module)
    grid
    xlabel('w/pi');     ylabel('|H(iw)|')
    title(['Module de H(S) pour theta = ' num2str(t)])
    
    figure;
    plot(w/pi,unwrap(phase*180/pi))
    grid
    xlabel('w/pi');     ylabel('Phase')
    title(['Phase de H(S) pour theta = ' num2str(t)])
end
