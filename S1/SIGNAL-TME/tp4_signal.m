%% Exercice 1

% initialisation des variables de base
wp = 0.2*pi;    ws = 0.3*pi;
Rp = 7;         As = 16;
f = 0:0.001:1;
w =  2*pi .*f;
S = 1i*w;

% Question 1 :
% calcul de N et wc
N = ceil(log((10^(Rp/10) -1) / (10^(As/10) -1)) / (2*log(wp/ws)));
wcp = wp / (10^(Rp/10) -1)^(1/(2*N));
wcs = ws / (10^(As/10) -1)^(1/(2*N));
wc = (wcp + wcs)/2;

% Question 2 :
% calcul et affichage des pôles
p2 = wc * exp(1i*2*pi/3);
p3 = wc * exp(1i*pi);
p4 = wc * exp(1i*4*pi/3);

figure; hold on
plot(real([p2, p3, p4]), imag([p2, p3, p4]), 'r+')
grid
xlabel('Partie Réelle');        ylabel('Partie Imaginaire')
title('Position des pôles sur le plan S')
axis equal;

% Question 3 :
% calcul de H(S)
H = (wc^N) ./ ((S+p2) .* (S+p3) .* (S+p4));

% Question 4 :
% affichage du module et de la phase
module = 20* log10(abs(H));
phase = angle(H);

figure
subplot(211)
plot(w/pi,module)
xlabel('w/pi');         ylabel('|H(w)|')
title('Module de H')
grid

subplot(212)
plot(w/pi,unwrap(phase*180/pi))
xlabel('w/pi');         ylabel('phase*180/pi de H')
title('Phase de H')
grid


%% Exercice 2

% initialisation des variables de base supplémentaires
Op = 0.2*pi;    Os = 0.3*pi;

% Question 2&3 :
% calcul de H[Z]
Omega = 0:0.1:2*pi;
Z = exp(1j*Omega);
S = 2* (1-Z.^(-1))./(1+Z.^(-1));

H = (wc^N) ./ ((S+p2) .* (S+p3) .* (S+p4));

% affichage du module et de la phase
module = 20* log10(abs(H));
phase = angle(H);

figure
subplot(211)
plot(Omega/pi,module)
xlabel('Omega/pi');     ylabel('|H(w)|')
title('Module de H')
grid

subplot(212)
plot(Omega/pi,unwrap(phase*180/pi))
xlabel('Omega/pi');     ylabel('phase*180/pi de H')
title('Phase de H')
grid