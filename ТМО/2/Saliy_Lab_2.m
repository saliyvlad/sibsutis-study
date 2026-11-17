%% Лабораторная работа №2. Моделирование непрерывных и дискретных СВ
% ИКС-431 Салий Владислав (pointCreator), вариант 18
% Работает БЕЗ Statistics and Machine Learning Toolbox
clear; clc; close all;

sizes = [50, 200, 1000];
alphas = [0.1, 0.05, 0.01];

%% ЧАСТЬ 1: НЕПРЕРЫВНАЯ СЛУЧАЙНАЯ ВЕЛИЧИНА
% f(x) = 2/x^3, x >= 1
% F(x) = 1 - 1/x^2 => x = 1/sqrt(1-z)
fprintf('=== ЧАСТЬ 1: Непрерывная СВ f(x)=2/x^3, x>=1 ===\n');
theoretical_mean_cont = 2;
% Дисперсия бесконечна! Интервальные оценки для дисперсии не строятся.

for n_idx = 1:length(sizes)
    N = sizes(n_idx);
    
    % Генерация выборки методом обратной функции
    z = rand(N, 1);
    X = 1 ./ sqrt(1 - z);
    
    % Точечные оценки
    m_est = mean(X);
    d_est = var(X); 
    s_est = std(X);
    
    fprintf('\nРазмер выборки N=%d:\n', N);
    fprintf('  Выборочное среднее: %.4f (теор. 2)\n', m_est);
    fprintf('  Выборочная дисперсия: %.4f (теор. Inf)\n', d_est);
    fprintf('  СКО: %.4f\n', s_est);
    
    % Интервальные оценки ТОЛЬКО для среднего
    if N == 50
        t_vals = [1.676, 2.009, 2.678];
    elseif N == 200
        t_vals = [1.653, 1.972, 2.601];
    else % N == 1000
        t_vals = [1.646, 1.962, 2.581];
    end
    
    for a_idx = 1:length(alphas)
        delta = t_vals(a_idx) * s_est / sqrt(N);
        ci_low = m_est - delta;
        ci_high = m_est + delta;
        fprintf('  ДИ для среднего (alpha=%.2f): [%.4f; %.4f]\n', alphas(a_idx), ci_low, ci_high);
    end
    
    % Гистограмма и теоретическая плотность
    k_bins = floor(1 + 3.2*log10(N));
    figure('Name', ['Непрерывная СВ N=' num2str(N)]);
    subplot(2,1,1);
    [counts, edges] = histcounts(X, k_bins);
    bin_width = edges(2)-edges(1);
    bar(edges(1:end-1)+bin_width/2, counts/bin_width/N, 'hist'); hold on;
    x_plot = linspace(1, max(X)*1.1, 500);
    f_theor_pdf = 2 ./ x_plot.^3;
    plot(x_plot, f_theor_pdf, 'r-', 'LineWidth', 2);
    title(['Гистограмма и плотность f(x)=2/x^3, N=' num2str(N)]);
    xlabel('x'); ylabel('Частота / Плотность');
    legend('Эмпирическая', 'Теоретическая'); grid on;
    
    % График функции распределения и плотности (РУЧНАЯ РЕАЛИЗАЦИЯ ECDF)
    subplot(2,1,2);
    X_sorted = sort(X);
    N_pts = length(X_sorted);
    x_ecdf = [X_sorted(1); X_sorted; X_sorted(end)]; 
    f_emp_cdf = [0; (1:N_pts)'/N_pts; 1];
    
    plot(x_ecdf, f_emp_cdf, 'b-', 'LineWidth', 1.5); hold on;
    f_theor_cdf = 1 - 1./x_plot.^2;
    plot(x_plot, f_theor_cdf, 'r--', 'LineWidth', 2);
    
    yyaxis right;
    plot(x_plot, f_theor_pdf, 'g:', 'LineWidth', 1.5);
    title('Функция распределения и плотность');
    xlabel('x'); ylabel('F(x)');
    yyaxis right; ylabel('f(x)');
    legend('F_{emp}(x)', 'F_{theor}(x)', 'f_{theor}(x)'); 
    grid on;
end

% Проверка гипотезы (Колмогоров-Смирнов) - ручная реализация
try
    fprintf('\n--- Проверка гипотезы (непрерывная) ---\n');
    N_test = 1000;
    z_test = rand(N_test, 1);
    X_test = 1 ./ sqrt(1 - z_test);
    
    X_s = sort(X_test);
    F_emp_manual = (1:N_test)' / N_test;
    F_theor_manual = 1 - 1./X_s.^2;
    D_stat = max(abs(F_emp_manual - F_theor_manual));
    
    crit_val = 1.36 / sqrt(N_test); 
    
    fprintf('KS-statistic (N=1000): %.4f\n', D_stat);
    fprintf('Критическое значение (alpha=0.05): %.4f\n', crit_val);
    if D_stat < crit_val
        fprintf('Гипотеза о соответствии закону f(x)=2/x^3 НЕ отвергается.\n');
    else
        fprintf('Гипотеза ОТВЕРГАЕТСЯ.\n');
    end
catch
    fprintf('Проверка гипотезы пропущена из-за ошибки.\n');
end

%% ЧАСТЬ 2: ДИСКРЕТНАЯ СЛУЧАЙНАЯ ВЕЛИЧИНА
% P(X=k) = 2^(-k-1), k=0,1,2,...
fprintf('\n\n=== ЧАСТЬ 2: Дискретная СВ P(X=k)=2^(-k-1) ===\n');

theoretical_mean_disc = 1;
theoretical_var_disc = 2;

for n_idx = 1:length(sizes)
    N = sizes(n_idx);
    
    % Генерация дискретной СВ (метод интервалов)
    z = rand(N, 1);
    K = zeros(N, 1);
    
    max_k_needed = 50; 
    probs = 2.^(-(0:max_k_needed));
    cum_probs = cumsum(probs);
    
    for i = 1:N
        idx = find(cum_probs >= z(i), 1, 'first');
        K(i) = idx - 1;
    end
    
    % Точечные оценки
    m_est = mean(K);
    d_est = var(K);
    s_est = std(K);
    
    fprintf('\nРазмер выборки N=%d:\n', N);
    fprintf('  Выборочное среднее: %.4f (теор. 1)\n', m_est);
    fprintf('  Выборочная дисперсия: %.4f (теор. 2)\n', d_est);
    fprintf('  СКО: %.4f\n', s_est);
    
    % Интервальные оценки с табличными значениями
    if N == 50
        t_vals_d = [1.676, 2.009, 2.678];
        chi2_low_vals = [36.42, 32.36, 27.99];
        chi2_high_vals = [66.34, 71.42, 79.49];
    elseif N == 200
        t_vals_d = [1.653, 1.972, 2.601];
        chi2_low_vals = [168.3, 158.7, 147.6];
        chi2_high_vals = [233.9, 244.3, 257.7];
    else % N == 1000
        t_vals_d = [1.646, 1.962, 2.581];
        chi2_low_vals = [923.0, 905.3, 875.2];
        chi2_high_vals = [1078.7, 1100.3, 1138.5];
    end
    
    for a_idx = 1:length(alphas)
        delta_m = t_vals_d(a_idx) * s_est / sqrt(N);
        ci_m_low = m_est - delta_m;
        ci_m_high = m_est + delta_m;
        
        ci_v_low = (N-1)*d_est / chi2_high_vals(a_idx);
        ci_v_high = (N-1)*d_est / chi2_low_vals(a_idx);
        
        fprintf('  ДИ ср. (a=%.2f): [%.4f; %.4f]\n', alphas(a_idx), ci_m_low, ci_m_high);
        fprintf('  ДИ дисп. (a=%.2f): [%.4f; %.4f]\n', alphas(a_idx), ci_v_low, ci_v_high);
    end
    
    % Гистограмма и теоретический закон (ИСПРАВЛЕННЫЙ ПОДСЧЕТ И ОТОБРАЖЕНИЕ)
    max_k_plot = min(max(K), 20);
    k_range = 0:max_k_plot;
    
    % Надежный подсчет частот без histcounts
    counts = zeros(size(k_range));
    for val = k_range
        counts(val + 1) = sum(K == val);
    end
    
    emp_probs = counts / N;
    theor_probs = 2.^(-(k_range+1));
    
    figure('Name', ['Дискретная СВ N=' num2str(N)]);
    
    % BarWidth = 0.4 предотвращает сливание столбиков
    b = bar(k_range, emp_probs, 'FaceColor', [0.7 0.85 1], 'EdgeColor', 'b', 'BarWidth', 0.4); 
    hold on;
    
    stem(k_range, theor_probs, 'r', 'LineWidth', 1.5, 'MarkerFaceColor', 'r', 'DisplayName', 'Теоретическое');
    
    title(['Распределение P(X=k)=2^{-(k+1)}, N=' num2str(N)]);
    xlabel('k'); ylabel('Вероятность');
    legend('Эмпирическое', 'Теоретическое'); 
    grid on;
    
    % Фиксируем границы оси X и добавляем метки для каждого k
    xlim([-0.5, max_k_plot + 0.5]);
    xticks(k_range);
end

% Проверка гипотезы (Хи-квадрат) - ручная реализация
try
    fprintf('\n--- Проверка гипотезы (дискретная) ---\n');
    N_test = 1000;
    z_test = rand(N_test, 1);
    K_test = zeros(N_test, 1);
    cum_probs_full = cumsum(2.^(-(0:50)));
    for i = 1:N_test
        idx = find(cum_probs_full >= z_test(i), 1, 'first');
        K_test(i) = idx - 1;
    end

    max_bin = 15;
    observed = zeros(1, max_bin+1);
    for val = 0:max_bin
        observed(val+1) = sum(K_test == val);
    end
    expected = N_test * 2.^(-(0:max_bin+1));
    
    while expected(end) < 5 && length(expected) > 3
        observed(end-1) = observed(end-1) + observed(end);
        expected(end-1) = expected(end-1) + expected(end);
        observed(end) = [];
        expected(end) = [];
    end

    chi2_stat = sum((observed - expected).^2 ./ expected);
    df = length(observed) - 1; 
    crit_chi2 = df + 2*sqrt(2*df); 
    
    fprintf('Chi2-statistic (N=1000): %.4f, df=%d\n', chi2_stat, df);
    fprintf('Приближенное критическое значение (alpha=0.05): %.2f\n', crit_chi2);
    if chi2_stat < crit_chi2
        fprintf('Гипотеза НЕ отвергается (приближенная оценка).\n');
    else
        fprintf('Гипотеза ОТВЕРГАЕТСЯ (приближенная оценка).\n');
    end
catch
    fprintf('Проверка гипотезы пропущена.\n');
end

fprintf('\n=== ЛАБОРАТОРНАЯ РАБОТА №2 ЗАВЕРШЕНА ===\n');