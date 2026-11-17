clear; clc; close all;

N = 800;    
K = 600;    
mu_wn = 16; sigma_wn = 4;   
mu_rw = 0;  sigma_rw = 1;   
l1 = 8; l2 = 80;            

%% ЧАСТЬ 1: Белый гауссовский шум
fprintf('=== ЧАСТЬ 1: Белый гауссовский шум ===\n');
fprintf('Параметры: N=%d, K=%d, mu=%.1f, sigma=%.1f\n\n', N, K, mu_wn, sigma_wn);

X_wn = mu_wn + sigma_wn * randn(N, K);

mean_ensemble = mean(X_wn, 2);

mean_time = mean(X_wn, 1);

figure('Name', 'Белый шум: среднее', 'Position', [100 100 900 400]);
plot(1:N, mean_ensemble, 'b', 'LineWidth', 1.5); hold on;
plot(1:N, mean_time(ones(N,1)), 'r--', 'LineWidth', 1.5);
yline(mu_wn, 'g:', 'LineWidth', 1.5);
title('Среднее по ансамблю и по реализации белого шума');
xlabel('n'); ylabel('Значение');
legend('По ансамблю', 'По реализации', 'Теор. mu=16');
grid on;

fprintf('Среднее по ансамблю (последнее значение): %.4f\n', mean_ensemble(end));
fprintf('Среднее по времени (первая реализация): %.4f\n\n', mean_time(1));

%% Скаттерограммы белого шума
fprintf('Выборочные корреляции белого шума:\n');
pairs = [100 101; 400 401; 700 701];

figure('Name', 'Белый шум: диаграммы рассеяния', 'Position', [100 100 1200 400]);
for p = 1:3
    ni = pairs(p,1); nj = pairs(p,2);
    subplot(1,3,p);
    scatter(X_wn(ni,:), X_wn(nj,:), 5, 'filled');
    
    x_i = X_wn(ni,:);
    x_j = X_wn(nj,:);
    r_hat = (mean(x_i.*x_j) - mean(x_i)*mean(x_j)) / (std(x_i)*std(x_j));
    
    title(sprintf('(%d,%d), r=%.4f', ni, nj, r_hat));
    xlabel(sprintf('xi[%d]', ni));
    ylabel(sprintf('xi[%d]', nj));
    grid on;
    
    fprintf('  (%d,%d): r = %.4f (теор. 0)\n', ni, nj, r_hat);
end

%% ЧАСТЬ 2: Случайные блуждания
fprintf('\n=== ЧАСТЬ 2: Случайные блуждания ===\n');
fprintf('Теоретически: M[xi[n]] = n*mu = 0\n');
fprintf('Теоретически: sigma_xi[n] = sqrt(n)\n');
fprintf('Теоретически: r_xi(n,n-l) = (n-l)*sigma^2\n\n');

X_rw = zeros(N, K);
for k = 1:K
    omega = mu_rw + sigma_rw * randn(N, 1);
    X_rw(:, k) = cumsum(omega);
end

figure('Name', 'Случайные блуждания', 'Position', [100 100 900 400]);
plot(1:N, X_rw, 'Color', [0.7 0.7 0.9], 'LineWidth', 0.3);
title('Реализации случайного блуждания (N=800, K=600)');
xlabel('n'); ylabel('xi[n]'); grid on;

figure('Name', 'Случайные блуждания: скаттерограммы', 'Position', [100 100 1200 400]);

pairs_rw1 = [10 9; 50 49; 100 99; 200 199];
subplot(1,2,1); hold on;
colors1 = lines(4);
for p = 1:4
    ni = pairs_rw1(p,1); nj = pairs_rw1(p,2);
    scatter(X_rw(ni,:), X_rw(nj,:), 10, colors1(p,:), 'filled');
end
title('Соседние отсчёты (лаг=1)');
xlabel('xi[n_i]'); ylabel('xi[n_j]'); grid on;
legend('(10,9)','(50,49)','(100,99)','(200,199)');

pairs_rw2 = [50 40; 100 90; 200 190];
subplot(1,2,2); hold on;
colors2 = lines(3);
for p = 1:3
    ni = pairs_rw2(p,1); nj = pairs_rw2(p,2);
    scatter(X_rw(ni,:), X_rw(nj,:), 10, colors2(p,:), 'filled');
end
title('Разные лаги (l=10)');
xlabel('xi[n_i]'); ylabel('xi[n_j]'); grid on;
legend('(50,40)','(100,90)','(200,190)');

fprintf('Выборочная автокорреляция случайного блуждания:\n');
r_emp = zeros(N-1, 1);
for l = 1:N-1
    temp = X_rw(1:end-l,:) .* X_rw(l+1:end,:);
    r_emp(l) = mean(temp(:));
end

r_theor = (N-1:-1:1)' * sigma_rw^2;

figure('Name', 'АКФ случайного блуждания', 'Position', [100 100 900 400]);
plot(1:100, r_emp(1:100), 'b', 'LineWidth', 1.5); hold on;
plot(1:100, r_theor(1:100), 'r--', 'LineWidth', 1.5);
title('Автокорреляционная функция случайного блуждания');
xlabel('Лаг l'); ylabel('r_xi(n,n-l)');
legend('Выборочная', 'Теоретическая'); grid on;

fprintf('  r(1) выборочная: %.2f, теоретическая: %.2f\n', r_emp(1), r_theor(1));
fprintf('  r(100) выборочная: %.2f, теоретическая: %.2f\n\n', r_emp(100), r_theor(100));

%% ЧАСТЬ 3: Случайные блуждания с затуханием
fprintf('=== ЧАСТЬ 3: Случайные блуждания с затуханием ===\n');
alpha = 0.9;
fprintf('Коэффициент затухания: alpha=%.1f\n', alpha);
fprintf('Теоретическая дисперсия (стационарная): %.4f\n\n', sigma_rw^2/(1-alpha^2));

X_rwd = zeros(N, K);
for k = 1:K
    omega = mu_rw + sigma_rw * randn(N, 1);
    for n = 2:N
        X_rwd(n, k) = alpha * X_rwd(n-1, k) + omega(n);
    end
end

figure('Name', 'Затухающие блуждания', 'Position', [100 100 900 400]);
plot(1:N, X_rwd, 'Color', [0.7 0.9 0.7], 'LineWidth', 0.3); hold on;
sigma_stationary = sqrt(sigma_rw^2/(1-alpha^2));
yline(sigma_stationary, 'r--', 'LineWidth', 1.5);
yline(-sigma_stationary, 'r--', 'LineWidth', 1.5);
title('Реализации случайного блуждания с затуханием (alpha=0.9)');
xlabel('n'); ylabel('xi[n]');
legend('Реализации', '+/-sigma_xi (стационар.)');
grid on;

figure('Name', 'Затухающие блуждания: скаттерограммы', 'Position', [100 100 1200 400]);

subplot(1,2,1); hold on;
for p = 1:4
    ni = pairs_rw1(p,1); nj = pairs_rw1(p,2);
    scatter(X_rwd(ni,:), X_rwd(nj,:), 10, colors1(p,:), 'filled');
end
title('Соседние отсчёты (лаг=1)');
xlabel('xi[n_i]'); ylabel('xi[n_j]'); grid on;

subplot(1,2,2); hold on;
for p = 1:3
    ni = pairs_rw2(p,1); nj = pairs_rw2(p,2);
    scatter(X_rwd(ni,:), X_rwd(nj,:), 10, colors2(p,:), 'filled');
end
title('Разные лаги (l=10)');
xlabel('xi[n_i]'); ylabel('xi[n_j]'); grid on;

r_emp_d = zeros(N-1, 1);
for l = 1:N-1
    temp_d = X_rwd(1:end-l,:) .* X_rwd(l+1:end,:);
    r_emp_d(l) = mean(temp_d(:));
end
r_theor_d = alpha.^(1:N-1)' * (sigma_rw^2/(1-alpha^2));

figure('Name', 'АКФ затухающих блужданий', 'Position', [100 100 900 400]);
plot(1:100, r_emp_d(1:100), 'g', 'LineWidth', 1.5); hold on;
plot(1:100, r_theor_d(1:100), 'r--', 'LineWidth', 1.5);
title('Автокорреляционная функция затухающего блуждания');
xlabel('Лаг l'); ylabel('r_xi(l)');
legend('Выборочная', 'Теоретическая (0.9^l * sigma^2)');
grid on;

%% ЧАСТЬ 4: Сравнение АКФ трёх процессов
figure('Name', 'Сравнение АКФ', 'Position', [100 100 900 600]);

subplot(3,1,1);
r_wn = zeros(50, 1);
for l = 1:50
    A = X_wn(1:end-l,:);
    B = X_wn(l+1:end,:);
    r_wn(l) = mean(A(:).*B(:)) - mean(A(:))*mean(B(:));
end
stem(1:50, r_wn, 'MarkerSize', 3);
title('АКФ белого шума'); xlabel('Лаг'); ylabel('r'); grid on;

subplot(3,1,2);
plot(1:100, r_emp(1:100), 'b', 'LineWidth', 1.5);
title('АКФ случайного блуждания'); xlabel('Лаг'); ylabel('r'); grid on;

subplot(3,1,3);
plot(1:100, r_emp_d(1:100), 'g', 'LineWidth', 1.5); hold on;
plot(1:100, r_theor_d(1:100), 'r--', 'LineWidth', 1.5);
title('АКФ затухающего блуждания');
xlabel('Лаг'); ylabel('r');
legend('Выборочная', 'Теоретическая'); grid on;
