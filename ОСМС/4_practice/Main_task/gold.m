% =====================================================================
%  Практическая работа No4 (Занятие No4). Коды Голда - часть Matlab.
%  Схема рис. 4.5 (нечётная группа, ИКС-431).
%  Шаги 5-6: повторить генерацию и корреляции, используя xcorr() и
%  autocorr(); сравнить с C/C++; построить АКФ от величины задержки (lag).
% =====================================================================
clear; clc; close all;

% Светлая тема, чтобы графики в отчёте были на белом фоне (R2024a+).
try
    matlab.appearance.set('Preferences', 'Color', 'Theme', 'light');
catch
end

JOURNAL_NUM = 18;          % <<< порядковый номер в журнале (x); y = x+7
M  = 5;                    % разрядов регистра
N  = 2^M - 1;              % длина последовательности = 31

fprintf('================================================================\n');
fprintf(' ПР No4. Код Голда (Matlab, схема рис. 4.5, нечётная группа).\n');
fprintf(' Номер в журнале x = %d, y = x+7 = %d\n', JOURNAL_NUM, JOURNAL_NUM+7);

xval = JOURNAL_NUM;
yval = mod(JOURNAL_NUM + 7, 32);
g = gold_seq(xval, yval);

% ---- Шаг 1: вывод последовательности ----
fprintf('\n[Шаг 1] Последовательность Голда (длина %d):\n  ', N);
fprintf('%d', g); fprintf('\n');

% ---- Шаг 2: таблица автокорреляции по циклическим сдвигам ----
fprintf('\n[Шаг 2] Автокорреляция (циклическая, формула 4.3):\n');
fprintf('  Сдвиг | Автокорр.\n');
Rcyc = zeros(1, N);
for tau = 0:N-1
    Rcyc(tau+1) = cyclic_autocorr(g, tau);
    fprintf('  %5d | %+.4f\n', tau, Rcyc(tau+1));
end

% ---- Шаг 5a: сравнение с xcorr() ----
a = 1 - 2*g;                              % bits -> +/-1 (0 -> +1, 1 -> -1)
[rx, lags] = xcorr(a, a, 'coeff');        % линейная нормированная АКФ
fprintf('\n[Шаг 5] Сравнение циклической АКФ и xcorr() (несколько лагов):\n');
fprintf('  lag | циклич. | xcorr(coeff)\n');
for tau = 0:min(6, N-1)
    idx = find(lags == tau, 1);
    fprintf('  %3d | %+.4f  | %+.4f\n', tau, Rcyc(tau+1), rx(idx));
end

% ---- Шаг 5b: autocorr() (если доступна), сравнение с циклической АКФ ----
try
    [ac, lags_ac] = autocorr(a);          % выборочная (линейная) АКФ по умолчанию
    fprintf('\n[Шаг 5] autocorr() (первые 6 лагов): ');
    fprintf('%.3f ', ac(1:min(6,numel(ac))));
    fprintf('\n  (autocorr - выборочная линейная АКФ; для периодического PN-кода\n');
    fprintf('   эталонна циклическая АКФ из шага 2 - пик = 1 при tau=0.)\n');
catch ME
    fprintf('\n[Шаг 5] autocorr() недоступна (%s) - используем xcorr().\n', ME.message);
end

% ---- Шаг 3: второй код Голда (x=x+1, y=y-5) ----
x2 = xval + 1;
y2 = mod(yval - 5, 32);
g2 = gold_seq(x2, y2);
fprintf('\n[Шаг 3] Второй код Голда: x=x+1=%d, y=y-5=%d\n  ', x2, yval-5);
fprintf('%d', g2); fprintf('\n');

% ---- Шаг 4: взаимная корреляция через xcorr() ----
b = 1 - 2*g2;
[rxy, lags_xy] = xcorr(a, b, 'coeff');
Rc0 = cyclic_crosscorr(g, g2, 0);
idx0 = find(lags_xy == 0, 1);
fprintf('\n[Шаг 4] Взаимная корреляция g и g2:\n');
fprintf('  циклическая R_cross(tau=0) = %+.4f\n', Rc0);
fprintf('  xcorr(coeff) при lag=0      = %+.4f\n', rxy(idx0));

% ---- Шаг 6: график АКФ от величины задержки (lag) ----
lags_full = 0:N-1;
figure('Color','w','Position',[100 100 820 460]);
set(gca, 'Color', 'w');
stem(lags_full, Rcyc, 'filled', 'MarkerSize', 5);
hold on; plot(lags_full, Rcyc, 'r-', 'LineWidth', 1);
title('Автокорреляционная функция кода Голда (N=31, схема рис. 4.5)');
xlabel('Величина задержки \tau (лаг, такт)');
ylabel('Нормированная автокорреляция R_x(\tau)');
ylim([-1 1.1]); grid on;
set(gca, 'XTick', 0:2:N-1);
lighten(gca);
saveas(gcf, 'matlab_autocorr.png');

% ---- Шаг 6b: график взаимной корреляции по всем сдвигам ----
Rxy = zeros(1, N);
for tau = 0:N-1
    Rxy(tau+1) = cyclic_crosscorr(g, g2, tau);
end
figure('Color','w','Position',[100 100 820 460]);
set(gca, 'Color', 'w');
stem(0:N-1, Rxy, 'filled', 'MarkerSize', 5, 'Color', [0 0.44 0.74]);
title('Взаимокорреляционная функция двух кодов Голда (g и g2)');
xlabel('Величина задержки \tau (лаг, такт)');
ylabel('R_{xy}(\tau)');
ylim([-1 1.1]); grid on;
lighten(gca);
saveas(gcf, 'matlab_crosscorr.png');

fprintf('\nГрафики сохранены: matlab_autocorr.png, matlab_crosscorr.png\n');
fprintf('================================================================\n');

% =========================== ЛОКАЛЬНЫЕ ФУНКЦИИ ======================
function g = gold_seq(xval, yval)
    % Код Голда по схеме рис. 4.5:
    %   x-регистр: new_x1 = x4 XOR x5, выход x5
    %   y-регистр: new_y1 = y2 XOR y5, выход y5
    %   выход Голда = x5 XOR y5
    M = 5; N = 2^M - 1;
    x = double(bitget(uint32(xval), M:-1:1));   % x(1)=x1 ... x(5)=x5
    y = double(bitget(uint32(yval), M:-1:1));
    g = zeros(1, N);
    for n = 1:N
        g(n) = bitxor(x(5), y(5));
        fb_x = bitxor(x(4), x(5));              % отводы 4,5
        fb_y = bitxor(y(2), y(5));              % отводы 2,5
        x = [fb_x, x(1:end-1)];                 % сдвиг вправо
        y = [fb_y, y(1:end-1)];
    end
end

function r = cyclic_autocorr(s, tau)
    N = numel(s);
    s2 = circshift(s, [0, -tau]);
    match = sum(s == s2);
    r = (match - (N - match)) / N;
end

function r = cyclic_crosscorr(s1, s2, tau)
    N = numel(s1);
    s2c = circshift(s2, [0, -tau]);
    match = sum(s1 == s2c);
    r = (match - (N - match)) / N;
end

function lighten(ax)
    % Принудительно светлое оформление осей (фон белый, текст/оси чёрные),
    % чтобы график корректно выглядел в отчёте независимо от темы Matlab.
    ax.Color = 'w';
    ax.XAxis.Color = 'k';
    ax.YAxis.Color = 'k';
    ax.Title.Color = 'k';
    ax.XLabel.Color = 'k';
    ax.YLabel.Color = 'k';
    ax.GridColor = [0.7 0.7 0.7];
    set(gcf, 'Color', 'w');
end
