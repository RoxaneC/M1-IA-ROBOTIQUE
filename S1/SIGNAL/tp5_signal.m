%% Compte rendu n°5

% initialisation des variables
Op = 0.2*pi;    Os = 0.3*pi;
Oc = (Op + Os)/2;

%% Filtre Rectangulaire

% Question 2 :
% calcul de l'ordre du filtre (en suivant le tableau des fenêtres)
M = 1.8*pi / (Os - Op);

% Question 3 :
% calcul et affichage des coefficients du filtre en fonction de n
n = -(M-1)/2 : 1 : (M-1)/2;
h_d = sin(n .* Oc)./(n .* pi + eps);

w = ones(1,M);
h_n = h_d .* w;

figure
subplot(311)
stem(n,h_n)
xlabel('n')
ylabel('h_n[n]')
title('Filtre Rectangulaire')
grid

% Question 4 :
% calcul de H[Z] et affichage de son module et de sa phase
[H,W] = freqz(h_n, 1, 1024);
module = 20*log10(abs(H/max(H)));
phase = angle(H);

subplot(312)
plot(W./pi,module)
xlabel('w/pi')
ylabel('|H(w)|')
title('Module de H (normalisé)')
grid

subplot(313)
plot(W./pi,unwrap(phase*180/pi))
xlabel('w/pi')
ylabel('phase*180/pi de H')
title('Phase de H')
grid

%% Filtre Bartlett

M = 6.1*pi / (Os - Op);

n = -(M-1)/2 : 1 : (M-1)/2;
h_d = sin(n .* Oc)./(n .* pi + eps);

w = bartlett(M)';
h_n = h_d .* w;

figure
subplot(311)
stem(n,h_n)
xlabel('n')
ylabel('h_n[n]')
title('Filtre Bartlett')
grid

[H,W] = freqz(h_n, 1, 1024);
module = 20*log10(abs(H/max(H)));
phase = angle(H);

subplot(312)
plot(W./pi,module)
xlabel('w/pi')
ylabel('|H(w)|')
title('Module de H (normalisé)')
grid

subplot(313)
plot(W./pi,unwrap(phase*180/pi))
xlabel('w/pi')
ylabel('phase*180/pi de H')
title('Phase de H')
grid

%% Filtre hanning

M = 6.2*pi / (Os - Op);

n = -(M-1)/2 : 1 : (M-1)/2;
h_d = sin(n .* Oc)./(n .* pi + eps);

w = hanning(M)';
h_n = h_d .* w;

figure
subplot(311)
stem(n,h_n)
xlabel('n')
ylabel('h_n[n]')
title('Filtre hanning')
grid

[H,W] = freqz(h_n, 1, 1024);
module = 20*log10(abs(H/max(H)));
phase = angle(H);

subplot(312)
plot(W./pi,module)
xlabel('w/pi')
ylabel('|H(w)|')
title('Module de H (normalisé)')
grid

subplot(313)
plot(W./pi,unwrap(phase*180/pi))
xlabel('w/pi')
ylabel('phase*180/pi de H')
title('Phase de H')
grid


%% Filtre hamming

M = 6.6*pi / (Os - Op);

n = -(M-1)/2 : 1 : (M-1)/2;
h_d = sin(n .* Oc)./(n .* pi + eps);

w = hamming(M)';
h_n = h_d .* w;

figure
subplot(311)
stem(n,h_n)
xlabel('n')
ylabel('h_n[n]')
title('Filtre hamming')
grid

[H,W] = freqz(h_n, 1, 1024);
module = 20*log10(abs(H/max(H)));
phase = angle(H);

subplot(312)
plot(W./pi,module)
xlabel('w/pi')
ylabel('|H(w)|')
title('Module de H (normalisé)')
grid

subplot(313)
plot(W./pi,unwrap(phase*180/pi))
xlabel('w/pi')
ylabel('phase*180/pi de H')
title('Phase de H')
grid

%% Filtre Blackman

M = 11*pi / (Os - Op);

n = -(M-1)/2 : 1 : (M-1)/2;
h_d = sin(n .* Oc)./(n .* pi + eps);

w = blackman(M)';
h_n = h_d .* w;

figure
subplot(311)
stem(n,h_n)
xlabel('n')
ylabel('h_n[n]')
title('Filtre Blackman')
grid

[H,W] = freqz(h_n, 1, 1024);
module = 20*log10(abs(H/max(H)));
phase = angle(H);

subplot(312)
plot(W./pi,module)
xlabel('w/pi')
ylabel('|H(w)|')
title('Module de H (normalisé)')
grid

subplot(313)
plot(W./pi,unwrap(phase*180/pi))
xlabel('w/pi')
ylabel('phase*180/pi de H')
title('Phase de H')
grid