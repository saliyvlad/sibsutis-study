%% Лабораторная работа №6. Формирование управляющих случайных последовательностей
% ИКС-431 Салий Владислав, вариант 18 (Гамма-распределение)
clear; clc; close all;


lambda = 0.8;   % интенсивность входного потока
mu = 1.0;       % интенсивность обслуживания
N = 10000;      % длина последовательности

fprintf('=== Лабораторная работа №6 ===\n');
fprintf('Вариант 18: Гамма-распределение\n');
fprintf('Параметры: lambda = %.2f, mu = %.2f, N = %d\n\n', lambda, mu, N);



E_tau_exp = 1 / lambda;
D_tau_exp = 1 / lambda^2;
E_nu_exp = 1 / mu;
D_nu_exp = 1 / mu^2;

fprintf('Аналитические характеристики (показательное):\n');
fprintf('  tau: E = %.4f, D = %.4f\n', E_tau_exp, D_tau_exp);
fprintf('  nu:  E = %.4f, D = %.4f\n\n', E_nu_exp, D_nu_exp);

%% 3. Генерация показательных последовательностей
tau_exp = -log(rand(N, 1)) / lambda;
nu_exp  = -log(rand(N, 1)) / mu;

%% 4. Параметры гамма-распределения (G/G/1)
% Система уравнений: b*c = E, b^2*c = D_target
% Примечание: Если D_target = D_exp, то c = 1, и гамма совпадает с показательным.
% Чтобы получить истинное гамма-распределение (c != 1), уменьшим целевую дисперсию в 2 раза.
D_target_tau = D_tau_exp / 2;
D_target_nu  = D_nu_exp / 2;

b_tau = D_target_tau / E_tau_exp;
c_tau = E_tau_exp^2 / D_target_tau;

b_nu = D_target_nu / E_nu_exp;
c_nu = E_nu_exp^2 / D_target_nu;

fprintf('Параметры гамма-распределения (c - форма, b - масштаб):\n');
fprintf('  tau_1: b = %.4f, c = %.4f\n', b_tau, c_tau);
fprintf('  nu_1:  b = %.4f, c = %.4f\n\n', b_nu, c_nu);




tau_gamma = my_gamrnd(c_tau, b_tau, N);
nu_gamma  = my_gamrnd(c_nu, b_nu, N);


calc_stats = @(x) [mean(x), var(x)];

stats_tau_exp = calc_stats(tau_exp);
stats_nu_exp  = calc_stats(nu_exp);
stats_tau_gam = calc_stats(tau_gamma);
stats_nu_gam  = calc_stats(nu_gamma);

fprintf('=== Статистические (эмпирические) характеристики ===\n');
fprintf('  tau (Exp):   E = %.4f, D = %.4f\n', stats_tau_exp(1), stats_tau_exp(2));
fprintf('  nu  (Exp):   E = %.4f, D = %.4f\n', stats_nu_exp(1), stats_nu_exp(2));
fprintf('  tau (Gamma): E = %.4f, D = %.4f\n', stats_tau_gam(1), stats_tau_gam(2));
fprintf('  nu  (Gamma): E = %.4f, D = %.4f\n\n', stats_nu_gam(1), stats_nu_gam(2));

%% 7. Визуализация
figure('Name', 'Гистограммы распределений', 'Position', [100 100 1100 700]);

x_vals = linspace(0, max([tau_exp; tau_gamma])*1.1, 200);

subplot(2,2,1);
histogram(tau_exp, 50, 'Normalization', 'pdf'); hold on;
plot(x_vals, lambda*exp(-lambda*x_vals), 'r-', 'LineWidth', 2);
title('Поток заявок \tau (M/M/1) - Экспоненциальное');
xlabel('Время'); ylabel('Плотность'); grid on;
legend('Эмпирическая', 'Теоретическая');

subplot(2,2,2);
histogram(tau_gamma, 50, 'Normalization', 'pdf'); hold on;
pdf_gam = (x_vals.^(c_tau-1) .* exp(-x_vals/b_tau)) / (b_tau^c_tau * gamma(c_tau));
plot(x_vals, pdf_gam, 'r-', 'LineWidth', 2);
title('Поток заявок \tau_1 (G/G/1) - Гамма');
xlabel('Время'); ylabel('Плотность'); grid on;
legend('Эмпирическая', 'Теоретическая');

subplot(2,2,3);
histogram(nu_exp, 50, 'Normalization', 'pdf'); hold on;
plot(x_vals, mu*exp(-mu*x_vals), 'r-', 'LineWidth', 2);
title('Время обслуживания \nu (M/M/1) - Экспоненциальное');
xlabel('Время'); ylabel('Плотность'); grid on;
legend('Эмпирическая', 'Теоретическая');

subplot(2,2,4);
histogram(nu_gamma, 50, 'Normalization', 'pdf'); hold on;
pdf_gam_nu = (x_vals.^(c_nu-1) .* exp(-x_vals/b_nu)) / (b_nu^c_nu * gamma(c_nu));
plot(x_vals, pdf_gam_nu, 'r-', 'LineWidth', 2);
title('Время обслуживания \nu_1 (G/G/1) - Гамма');
xlabel('Время'); ylabel('Плотность'); grid on;
legend('Эмпирическая', 'Теоретическая');

fprintf('=== ЛАБОРАТОРНАЯ РАБОТА №6 ЗАВЕРШЕНА ===\n');

%% Собственный генератор гамма-распределения (метод Маршаглии-Цанга)
function X = my_gamrnd(c, b, N)
    if c < 1
        X = my_gamrnd(c + 1, b, N) .* (rand(N, 1)).^(1/c);
        return;
    end
    d = c - 1/3;
    c_var = 1 / sqrt(9*d);
    X = zeros(N, 1);
    for i = 1:N
        while true
            x = randn;
            v = (1 + c_var*x)^3;
            if v > 0
                u = rand;
                if log(u) < 0.5*x^2 + d - d*v + d*log(v)
                    X(i) = d * v * b;
                    break;
                end
            end
        end
    end
end