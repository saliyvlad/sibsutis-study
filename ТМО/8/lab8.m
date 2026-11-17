%% Лабораторная работа №8. СМО M/G/1. Формула Хинчина - Поллячека
% Проверка корректности формулы Хинчина-Поллячека на примерах M/M/1 и M/D/1.
% ИКС-431 Салий Владислав, вариант 18
clear; clc; close all;

%% Параметры
xbar = 1;                       % среднее время обслуживания (по усмотрению)
rho  = linspace(0.05, 0.95, 200);  % коэффициент загрузки
Cb2_g = 10;                     % нормированная дисперсия для M/G/1 на общих графиках
Cb2_list = [0 1 10 20 30 40 50 60 70 80 90 100];  % по заданию п.3

fprintf('=== Лабораторная работа №8 (M/G/1, формула Хинчина-Поллячека) ===\n');
fprintf('Среднее время обслуживания x̄ = %.2f\n\n', xbar);

%% Формулы Хинчина-Поллячека для M/G/1 (8.1 - 8.4)
% Nq = rho^2 (1+Cb^2) / (2(1-rho));  N = rho + Nq;
% W  = rho*xbar(1+Cb^2) / (2(1-rho)); T = xbar + W
MG1_Nq = @(r,c) r.^2 .* (1+c) ./ (2*(1-r));
MG1_N  = @(r,c) r + MG1_Nq(r,c);
MG1_W  = @(r,c) r .* xbar .* (1+c) ./ (2*(1-r));
MG1_T  = @(r,c) xbar + MG1_W(r,c);

%% Проверка: M/M/1 (Cb^2=1) и M/D/1 (Cb^2=0) как частные случаи PK
% M/M/1 (8.9-8.12):  Nq=rho^2/(1-rho), N=rho/(1-rho), W=rho*xbar/(1-rho), T=xbar/(1-rho)
% M/D/1 (8.5-8.8):   Nq=rho^2/(2(1-rho)), N=rho+Nq, W=rho*xbar/(2(1-rho)), T=xbar+W
r_chk = 0.7;
err_MM  = abs(MG1_Nq(r_chk,1) - r_chk^2/(1-r_chk));
err_MD  = abs(MG1_Nq(r_chk,0) - r_chk^2/(2*(1-r_chk)));
fprintf('Проверка (rho=%.2f): |Nq_PK(Cb2=1)-Nq_M/M/1| = %.2e ; |Nq_PK(Cb2=0)-Nq_M/D/1| = %.2e\n', ...
        r_chk, err_MM, err_MD);
fprintf('Формула Хинчина-Поллячека подтверждена (погрешность ~0).\n\n');

%% Кривые для трёх СМО (зависимость от rho)
Nq_MD = MG1_Nq(rho, 0);   N_MD = MG1_N(rho, 0);   W_MD = MG1_W(rho, 0);   T_MD = MG1_T(rho, 0);
Nq_MM = MG1_Nq(rho, 1);   N_MM = MG1_N(rho, 1);   W_MM = MG1_W(rho, 1);   T_MM = MG1_T(rho, 1);
Nq_MG = MG1_Nq(rho, Cb2_g); N_MG = MG1_N(rho, Cb2_g); W_MG = MG1_W(rho, Cb2_g); T_MG = MG1_T(rho, Cb2_g);

leg = {'M/D/1 (C_b^2=0)', 'M/M/1 (C_b^2=1)', sprintf('M/G/1 (C_b^2=%d)', Cb2_g)};

%% Рисунок 1: средняя длина очереди N_q(rho)
figure('Name','Рис.8.1 N_q(rho)','Color','w');
plot(rho, Nq_MD,'b-', rho, Nq_MM,'r-', rho, Nq_MG,'m-', 'LineWidth',1.6); grid on;
xlabel('\rho'); ylabel('N_q'); title('Средняя длина очереди');
legend(leg,'Location','northwest');

%% Рисунок 2: среднее число заявок в СМО N(rho)
figure('Name','Рис.8.2 N(rho)','Color','w');
plot(rho, N_MD,'b-', rho, N_MM,'r-', rho, N_MG,'m-', 'LineWidth',1.6); grid on;
xlabel('\rho'); ylabel('N'); title('Среднее число заявок в СМО');
legend(leg,'Location','northwest');

%% Рисунок 3: среднее время ожидания W(rho)
figure('Name','Рис.8.3 W(rho)','Color','w');
plot(rho, W_MD,'b-', rho, W_MM,'r-', rho, W_MG,'m-', 'LineWidth',1.6); grid on;
xlabel('\rho'); ylabel('W'); title('Среднее время ожидания в очереди');
legend(leg,'Location','northwest');

%% Рисунок 4: среднее время пребывания в СМО T(rho)
figure('Name','Рис.8.4 T(rho)','Color','w');
plot(rho, T_MD,'b-', rho, T_MM,'r-', rho, T_MG,'m-', 'LineWidth',1.6); grid on;
xlabel('\rho'); ylabel('T'); title('Среднее время пребывания в СМО');
legend(leg,'Location','northwest');

%% Рисунок 5: зависимость характеристик M/G/1 от нормированной дисперсии C_b^2
rho_fix = [0.3 0.5 0.7 0.9];
Cb2_axis = linspace(0, 100, 200);
figure('Name','Рис.8.5 M/G/1 от C_b^2','Color','w');
subplot(2,2,1); hold on; grid on;
for k=1:numel(rho_fix)
    plot(Cb2_axis, MG1_Nq(Cb2_axis, rho_fix(k)), 'LineWidth',1.4);
end
xlabel('C_b^2'); ylabel('N_q'); title('N_q от C_b^2');
legend(arrayfun(@(r) sprintf('\\rho=%.1f',r), rho_fix, 'UniformOutput',false),'Location','northwest');
subplot(2,2,2); hold on; grid on;
for k=1:numel(rho_fix)
    plot(Cb2_axis, MG1_N(Cb2_axis, rho_fix(k)), 'LineWidth',1.4);
end
xlabel('C_b^2'); ylabel('N'); title('N от C_b^2');
subplot(2,2,3); hold on; grid on;
for k=1:numel(rho_fix)
    plot(Cb2_axis, MG1_W(Cb2_axis, rho_fix(k)), 'LineWidth',1.4);
end
xlabel('C_b^2'); ylabel('W'); title('W от C_b^2');
subplot(2,2,4); hold on; grid on;
for k=1:numel(rho_fix)
    plot(Cb2_axis, MG1_T(Cb2_axis, rho_fix(k)), 'LineWidth',1.4);
end
xlabel('C_b^2'); ylabel('T'); title('T от C_b^2');

%% Таблица значений M/G/1 при C_b^2 = 0,1,10,...,100 и rho = 0.7
fprintf('=== M/G/1: характеристики от C_b^2 (rho=0.7, x̄=%.1f) ===\n', xbar);
fprintf(' C_b^2 |   N_q      N       W       T\n');
fprintf('--------------------------------------\n');
for c = Cb2_list
    fprintf('%5d | %7.3f %7.3f %7.3f %7.3f\n', c, ...
        MG1_Nq(0.7,c), MG1_N(0.7,c), MG1_W(0.7,c), MG1_T(0.7,c));
end
fprintf('\n=== ЛАБОРАТОРНАЯ РАБОТА №8 ЗАВЕРШЕНА ===\n');
