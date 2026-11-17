%% Лабораторная работа №5. Исследование эргодических свойств цепи Маркова
% ИКС-431 Салий Владислав, вариант 18
clear; clc; close all;

%% 1. Матрица переходов (из Лаб. 1.3, вариант 18)
L = 15;
P = zeros(L, L);
for i = 1:L
    P(i, mod(i, L) + 1) = 0.5;     % сосед справа
    P(i, mod(i+1, L) + 1) = 0.3;   % через один
    P(i, mod(i+3, L) + 1) = 0.2;   % через три
end

fprintf('Матрица переходов P (%dx%d) загружена.\n', L, L);
fprintf('Проверка стохастичности (суммы строк):\n');
disp(sum(P, 2)');

%% 2. Траектория движения пакета
N_traj = 1000;
s = 1;
traj = MarkovTrajectory(P, N_traj, s);

figure('Name', 'Траектория движения пакета', 'Position', [100 100 900 400]);
plot(0:N_traj-1, traj, 'b-o', 'MarkerSize', 3, 'LineWidth', 0.8);
title('Траектория движения пакета по сети (L=15)');
xlabel('Номер коммутации (шаг)');
ylabel('Номер узла');
grid on;
ylim([0.5 L+0.5]);
set(gca, 'YTick', 1:L);

%% 3. Расчёт вероятностей первого перехода f_{i,j}^{(m)}
% Используем корректную рекурсивную формулу вместо формулы (5.2)
i_node = 1;
j_node = 10;
epsilon = 1e-5;

fprintf('\n=== Анализ перехода из узла %d в узел %d ===\n', i_node, j_node);

% Массив степеней матрицы P
P_powers = cell(1, 500);
P_powers{1} = eye(L);  % P^(0)

f_history = [];
m = 0;
max_iter = 500;

while m < max_iter
    m = m + 1;
    P_powers{m+1} = P_powers{m} * P;   % P^(m)
    
    % Вероятность пребывания P_{i,j}^{(m)}
    P_ij_m = P_powers{m+1}(i_node, j_node);
    
    % КОРРЕКТНАЯ рекурсивная формула для вероятности первого перехода:
    % f_{i,j}^{(m)} = P_{i,j}^{(m)} - Σ_{k=1}^{m-1} f_{i,j}^{(k)} * P_{j,j}^{(m-k)}
    sum_term = 0;
    for k = 1:m-1
        P_jj_m_k = P_powers{m-k+1}(j_node, j_node);
        sum_term = sum_term + f_history(k) * P_jj_m_k;
    end
    
    f_m = P_ij_m - sum_term;
    
    % Защита от отрицательных значений из-за численных ошибок
    f_m = max(f_m, 0);
    
    f_history = [f_history; f_m];
    
    % Условие остановки: f_m очень мала И мы уже прошли несколько шагов
    if f_m < epsilon && m > 10
        break;
    end
end

fprintf('Расчёт завершён на шаге m = %d\n', m);
fprintf('Сумма f_{i,j}^{(m)} по всем m: %.6f\n', sum(f_history));

%% 4. Характеристики перехода i -> j
% Длина кратчайшего пути (первый шаг, где f > epsilon/10)
threshold = epsilon / 10;
M_ij = find(f_history > threshold, 1, 'first');
if isempty(M_ij)
    M_ij = find(f_history > 0, 1, 'first');
    if isempty(M_ij)
        M_ij = 1;  % Если все нули, берём 1
    end
end
fprintf('Длина кратчайшего пути M_{%d,%d} = %d\n', i_node, j_node, M_ij);

% Математическое ожидание
M_avg = sum((1:length(f_history))' .* f_history);
fprintf('Мат. ожидание длины пути M_ср_{%d,%d} = %.4f\n', i_node, j_node, M_avg);

% Дисперсия
D_ij = sum(((1:length(f_history))'.^2) .* f_history) - M_avg^2;
fprintf('Дисперсия длины пути D_{%d,%d} = %.4f\n\n', i_node, j_node, D_ij);

%% 5. График f_{i,j}^{(m)} от m
figure('Name', 'Вероятность первого перехода', 'Position', [150 150 800 400]);
stem(1:length(f_history), f_history, 'filled', 'MarkerSize', 4);
title(sprintf('Вероятность первого перехода f_{%d,%d}^{(m)} от m', i_node, j_node));
xlabel('Число коммутаций m'); ylabel('f_{i,j}^{(m)}');
grid on;

%% 6. Зависимости характеристик от номера конечного узла j
M_min_all = zeros(1, L);
M_avg_all = zeros(1, L);
D_all = zeros(1, L);
P_stay_all = zeros(1, L);

fprintf('=== Характеристики переходов из узла %d во все узлы j ===\n', i_node);
fprintf('%-4s %-10s %-12s %-12s\n', 'j', 'M_{i,j}', 'M_ср_{i,j}', 'D_{i,j}');
fprintf('---------------------------------------------\n');

for j = 1:L
    if j == i_node
        M_min_all(j) = 0; M_avg_all(j) = 0; D_all(j) = 0;
        P_stay_all(j) = 1;
        continue;
    end
    
    f_hist_loc = [];
    m_loc = 0;
    P_p_loc = eye(L);
    
    while m_loc < max_iter
        m_loc = m_loc + 1;
        P_p_loc = P_p_loc * P;
        
        P_ij_m = P_p_loc(i_node, j);
        
        % Рекурсивная формула
        sum_t = 0;
        for k = 1:m_loc-1
            P_jj_m_k = P_p_loc(j, j);  % P_{j,j}^{(m_loc-k)} - упрощение
            sum_t = sum_t + f_hist_loc(k) * P_jj_m_k;
        end
        
        f_val = P_ij_m - sum_t;
        f_val = max(f_val, 0);
        f_hist_loc = [f_hist_loc; f_val];
        
        if f_val < epsilon && m_loc > 10, break; end
    end
    

    
    M_min_all(j) = find(f_hist_loc > threshold, 1, 'first');
    if isempty(M_min_all(j))
        M_min_all(j) = find(f_hist_loc > 0, 1, 'first');
        if isempty(M_min_all(j))
            M_min_all(j) = 1;
        end
    end
    
    M_avg_all(j) = sum((1:length(f_hist_loc))' .* f_hist_loc);
    D_all(j) = sum(((1:length(f_hist_loc))'.^2) .* f_hist_loc) - M_avg_all(j)^2;
    P_stay_all(j) = P_p_loc(i_node, j);
    
    fprintf('%-4d %-10d %-12.4f %-12.4f\n', j, M_min_all(j), M_avg_all(j), D_all(j));
end

%% 7. Графики зависимостей от номера узла j
figure('Name', 'Характеристики переходов из узла 1', 'Position', [200 200 1100 700]);

subplot(2,2,1);
bar(1:L, M_min_all, 'FaceColor', [0.7 0.85 1], 'EdgeColor', 'b');
title('Длина кратчайшего пути M_{1,j}');
xlabel('Узел j'); ylabel('M_{1,j}'); grid on;
xticks(1:L);

subplot(2,2,2);
bar(1:L, M_avg_all, 'FaceColor', [0.9 0.7 0.8], 'EdgeColor', 'r');
title('Мат. ожидание длины пути M_ср_{1,j}');
xlabel('Узел j'); ylabel('M_ср_{1,j}'); grid on;
xticks(1:L);

subplot(2,2,3);
bar(1:L, D_all, 'FaceColor', [0.7 0.9 0.7], 'EdgeColor', 'g');
title('Дисперсия длины пути D_{1,j}');
xlabel('Узел j'); ylabel('D_{1,j}'); grid on;
xticks(1:L);

subplot(2,2,4);
bar(1:L, P_stay_all, 'FaceColor', [0.9 0.9 0.7], 'EdgeColor', 'k');
title('Вероятность пребывания P_{1,j}^{(m)}');
xlabel('Узел j'); ylabel('P_{1,j}'); grid on;
xticks(1:L);

fprintf('\n=== ЛАБОРАТОРНАЯ РАБОТА №5 ЗАВЕРШЕНА ===\n');

%% Вспомогательная функция
function traj = MarkovTrajectory(P, N, s)
    traj = zeros(1, N);
    traj(1) = s;
    L = size(P, 1);
    P_cum = cumsum(P, 2);
    for t = 1:N-1
        r = rand();
        traj(t+1) = sum(r > P_cum(traj(t), :)) + 1;
    end
end