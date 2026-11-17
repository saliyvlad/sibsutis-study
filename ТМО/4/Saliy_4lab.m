clear; clc; close all;

fprintf('=== ЧАСТЬ 1: ЦЕПИ МАРКОВА ===\n\n');

P_raw = [5 5 1 0;
         5 5 2 0;
         2 5 5 2;
         0 0 3 3];

P = P_raw ./ sum(P_raw, 2);

fprintf('Исходная матрица (коэффициенты варианта 18):\n');
disp(P_raw);

fprintf('Нормированная матрица переходов P:\n');
disp(P);

fprintf('Проверка нормировки (суммы по строкам, должны быть = 1):\n');
disp(sum(P, 2));

states = {'Healthy', 'Unwell', 'Sick', 'Very sick'};
MC = dtmc(P, 'StateNames', states);

fprintf('Матрица переходов цепи Маркова MC.P:\n');
disp(MC.P);

figure('Name', 'Граф цепи Маркова', 'Position', [100 100 800 600]);
graphplot(MC);
title('Граф цепи Маркова (вероятности переходов)');

P_cum = cumsum(P, 2);
fprintf('Кумулятивная матрица переходов P_cum:\n');
disp(P_cum);

iterations = [200, 1000, 10000];
trajectories = cell(length(iterations), 1);
P_obs = cell(length(iterations), 1);

for idx = 1:length(iterations)
    T = iterations(idx);
    z = zeros(T, 1);
    z(1) = 1;
    
    for t = 1:T-1
        r = rand();
        z(t+1) = sum(r > P_cum(z(t), :)) + 1;
    end
    trajectories{idx} = z;
    
    P_obs_raw = zeros(4, 4);
    for t = 1:T-1
        i = z(t);
        j = z(t+1);
        P_obs_raw(i, j) = P_obs_raw(i, j) + 1;
    end
    row_sums = sum(P_obs_raw, 2);
    row_sums(row_sums == 0) = 1;
    P_obs{idx} = P_obs_raw ./ row_sums;
    
    figure('Name', sprintf('Траектория цепи Маркова (T=%d)', T), ...
           'Position', [100+idx*50 100+idx*50 900 400]);
    plot(1:T, z, 'b-', 'LineWidth', 1);
    title(sprintf('Изменение состояния цепи Маркова (T=%d итераций)', T));
    xlabel('Номер итерации');
    ylabel('Состояние');
    set(gca, 'YTick', 1:4, 'YTickLabel', states);
    grid on;
    ylim([0.5 4.5]);
end

for idx = 1:length(iterations)
    T = iterations(idx);
    fprintf('\n--- Оценённая матрица переходов для T=%d ---\n', T);
    disp(P_obs{idx});
    
    figure('Name', sprintf('Граф оценённой цепи (T=%d)', T), ...
           'Position', [150+idx*50 150+idx*50 700 500]);
    MC_obs = dtmc(P_obs{idx}, 'StateNames', states);
    graphplot(MC_obs);
    title(sprintf('Оценённый граф цепи Маркова (T=%d)', T));
end

fprintf('\n--- Повторное моделирование для T=200 ---\n');
T = 200;
z2 = zeros(T, 1);
z2(1) = 1;
for t = 1:T-1
    r = rand();
    z2(t+1) = sum(r > P_cum(z2(t), :)) + 1;
end

figure('Name', 'Сравнение траекторий T=200', 'Position', [200 200 1000 500]);
subplot(1,2,1);
plot(1:T, trajectories{1}, 'b-', 'LineWidth', 1);
title('Первая траектория (T=200)');
xlabel('Итерация'); ylabel('Состояние');
set(gca, 'YTick', 1:4, 'YTickLabel', states);
grid on; ylim([0.5 4.5]);

subplot(1,2,2);
plot(1:T, z2, 'r-', 'LineWidth', 1);
title('Вторая траектория (T=200)');
xlabel('Итерация'); ylabel('Состояние');
set(gca, 'YTick', 1:4, 'YTickLabel', states);
grid on; ylim([0.5 4.5]);

fprintf('\n\n=== ЧАСТЬ 2: СИСТЕМА МАССОВОГО ОБСЛУЖИВАНИЯ ===\n');

lambda = 40;
mu = 30;
n = 8;
m = 10;

fprintf('Параметры СМО:\n');
fprintf('  lambda = %.2f (интенсивность входного потока)\n', lambda);
fprintf('  mu = %.2f (интенсивность обслуживания)\n', mu);
fprintf('  n = %d (количество каналов)\n', n);
fprintf('  m = %d (длина очереди)\n', m);

rho = lambda / mu;
fprintf('  rho = lambda/mu = %.4f\n', rho);

if rho >= n
    fprintf('ВНИМАНИЕ: rho >= n, система перегружена!\n');
end

sum1 = 0;
for k = 0:n
    sum1 = sum1 + rho^k / factorial(k);
end

sum2 = 0;
for k = 1:m
    sum2 = sum2 + (rho/n)^k;
end

p0 = 1 / (sum1 + (rho^n / factorial(n)) * sum2);
fprintf('  p0 = %.6f (вероятность простоя системы)\n', p0);

P_otk = (rho^n / factorial(n)) * (rho/n)^m * p0;
fprintf('  P_otk = %.6f (вероятность отказа)\n', P_otk);

Q = 1 - P_otk;
fprintf('  Q = %.6f (относительная пропускная способность)\n', Q);

A = lambda * Q;
fprintf('  A = %.4f (абсолютная пропускная способность, заявок/ед.вр.)\n', A);

k_zan = A / mu;
fprintf('  k_zan = %.4f (среднее число занятых каналов)\n', k_zan);

if abs(rho/n - 1) > 1e-10
    L_och = (rho^(n+1) / (n * factorial(n))) * ...
            (1 - (m + 1 - m*rho/n) * (rho/n)^m) / (1 - rho/n)^2 * p0;
else
    L_och = (rho^(n+1) / (n * factorial(n))) * m * (m+1) / 2 * p0;
end
fprintf('  L_och = %.4f (средняя длина очереди)\n', L_och);

T_och = L_och / lambda;
fprintf('  T_och = %.4f (среднее время ожидания в очереди)\n', T_och);

L_sist = L_och + k_zan;
fprintf('  L_sist = %.4f (среднее число заявок в системе)\n', L_sist);

T_sist = L_sist / lambda;
fprintf('  T_sist = %.4f (среднее время пребывания в системе)\n', T_sist);

rho_zag = A / (n * mu);
fprintf('  rho_zag = %.4f (коэффициент загрузки системы)\n', rho_zag);

fprintf('\n=== ИТОГОВАЯ ТАБЛИЦА ПОКАЗАТЕЛЕЙ СМО ===\n');
fprintf('--------------------------------------------------\n');
fprintf('Показатель                          | Значение    \n');
fprintf('--------------------------------------------------\n');
fprintf('Вероятность отказа P_otk            | %.6f\n', P_otk);
fprintf('Относительная пропускная sp-st Q    | %.6f\n', Q);
fprintf('Абсолютная пропускная sp-st A       | %.4f\n', A);
fprintf('Среднее число занятых каналов k_zan | %.4f\n', k_zan);
fprintf('Средняя длина очереди L_och         | %.4f\n', L_och);
fprintf('Среднее время ожидания T_och        | %.4f\n', T_och);
fprintf('Среднее число заявок v sisteme L_sist| %.4f\n', L_sist);
fprintf('Среднее время v sisteme T_sist      | %.4f\n', T_sist);
fprintf('Koeffitsient zagruzki rho_zag       | %.4f\n', rho_zag);
fprintf('--------------------------------------------------\n');

figure('Name', 'Зависимости pokazateley SMO ot rho', 'Position', [100 100 1000 700]);

rho_range = linspace(0.1, n-0.1, 100);
P_otk_arr = zeros(size(rho_range));
Q_arr = zeros(size(rho_range));
L_och_arr = zeros(size(rho_range));
T_sist_arr = zeros(size(rho_range));

for i = 1:length(rho_range)
    r = rho_range(i);
    
    s1 = 0;
    for k = 0:n
        s1 = s1 + r^k / factorial(k);
    end
    s2 = 0;
    for k = 1:m
        s2 = s2 + (r/n)^k;
    end
    pp0 = 1 / (s1 + (r^n / factorial(n)) * s2);
    
    P_otk_arr(i) = (r^n / factorial(n)) * (r/n)^m * pp0;
    Q_arr(i) = 1 - P_otk_arr(i);
    
    if abs(r/n - 1) > 1e-10
        L_och_arr(i) = (r^(n+1) / (n * factorial(n))) * ...
                       (1 - (m + 1 - m*r/n) * (r/n)^m) / (1 - r/n)^2 * pp0;
    else
        L_och_arr(i) = (r^(n+1) / (n * factorial(n))) * m * (m+1) / 2 * pp0;
    end
    
    k_z = lambda * Q_arr(i) / mu;
    L_s = L_och_arr(i) + k_z;
    T_sist_arr(i) = L_s / lambda;
end

subplot(2,2,1);
plot(rho_range, P_otk_arr, 'b-', 'LineWidth', 2);
title('Вероятность отказа P_otk от rho');
xlabel('rho = lambda/mu'); ylabel('P_otk');
grid on; xline(rho, 'r--', 'LineWidth', 1.5);

subplot(2,2,2);
plot(rho_range, Q_arr, 'g-', 'LineWidth', 2);
title('Относительная пропускная способность Q от rho');
xlabel('rho = lambda/mu'); ylabel('Q');
grid on; xline(rho, 'r--', 'LineWidth', 1.5);

subplot(2,2,3);
plot(rho_range, L_och_arr, 'm-', 'LineWidth', 2);
title('Средняя длина очереди L_och от rho');
xlabel('rho = lambda/mu'); ylabel('L_och');
grid on; xline(rho, 'r--', 'LineWidth', 1.5);

subplot(2,2,4);
plot(rho_range, T_sist_arr, 'k-', 'LineWidth', 2);
title('Среднее время в системе T_sist от rho');
xlabel('rho = lambda/mu'); ylabel('T_sist');
grid on; xline(rho, 'r--', 'LineWidth', 1.5);
