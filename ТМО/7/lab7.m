%% Лабораторная работа №7. СМО G/G/1. Зависимость параметров от типа
% распределения управляющих последовательностей.
% Используются последовательности из лаб. 6: tau, tau1 (вход), nu, nu1 (обслуж.).
% ИКС-431 Салий Владислав, вариант 18
clear; clc; close all;

%% Параметры (как в лаб. 6)
lambda = 0.8;   % интенсивность входного потока
mu     = 1.0;   % интенсивность обслуживания
N      = 5000;  % число заявок

fprintf('=== Лабораторная работа №7 (G/G/1, влияние типа распределения) ===\n');
fprintf('lambda=%.2f, mu=%.2f, rho=%.3f (<1, стационарность), N=%d\n\n', lambda, mu, lambda/mu, N);

%% Формирование управляющих последовательностей (как в лаб. 6)
E_tau = 1/lambda;  D_tau_exp = 1/lambda^2;
E_nu  = 1/mu;      D_nu_exp  = 1/mu^2;

tau = -log(rand(N,1)) / lambda;        % показательный вход   (M)
nu  = -log(rand(N,1)) / mu;            % показательное обслуж.(M)

D_tau_t = D_tau_exp/2;  D_nu_t = D_nu_exp/2;   % гамма с меньшей дисперсией (G)
b_tau = D_tau_t/E_tau;  c_tau = E_tau^2/D_tau_t;
b_nu  = D_nu_t /E_nu ;  c_nu  = E_nu ^2/D_nu_t;
tau1 = my_gamrnd(c_tau, b_tau, N);     % гамма-вход
nu1  = my_gamrnd(c_nu,  b_nu,  N);     % гамма-обслуживание

%% Четыре модели СМО (по заданию): пары (вход, обслуживание)
types = {'M/M/1','M/G/1','G/M/1','G/G/1'};
ins   = {tau, tau, tau1, tau1};
svs   = {nu,  nu1, nu,   nu1};

res = cell(1,4);
for t = 1:4
    res{t} = sim_smo(ins{t}, svs{t});
    fprintf('--- %s ---\n', types{t});
    fprintf('  rho = %.4f | N = %.4f | W = %.4f | T = %.4f\n', ...
            res{t}.rho, res{t}.N, res{t}.W, res{t}.T);
    fprintf('  среднее число в очереди Nq = %.4f\n\n', res{t}.Nq);
end

%% Графики для каждого типа СМО: 3 зависимости на одном рисунке
for t = 1:4
    r = res{t};
    figure('Name', ['Рис.7 ' types{t}], 'Color','w', 'Position',[80 60 1200 380]);

    subplot(1,3,1);   % число пришедших и обслуженных заявок от времени
    stairs(r.arr, 1:N, 'b-','LineWidth',1.2); hold on;
    stairs(r.dep, 1:N, 'r-','LineWidth',1.2); grid on;
    xlabel('t, c'); ylabel('Кол-во заявок');
    title(sprintf('%s: приход и обслуживание', types{t}));
    legend('Пришло','Обслужено','Location','northwest');

    subplot(1,3,2);   % число заявок в СМО от времени
    stairs(r.evT, r.cnt, 'k-','LineWidth',1.0); grid on;
    xlabel('t, c'); ylabel('N(t)');
    title('Число заявок в СМО от времени');

    subplot(1,3,3);   % распределение числа заявок в СМО
    bar(r.levels, r.prob, 'FaceColor',[0.3 0.5 0.9]); grid on;
    xlabel('n'); ylabel('P\{N=n\}');
    title('Распределение числа заявок в СМО');
end

%% Сводное сравнение характеристик четырёх СМО
Nq_v = cell2mat(cellfun(@(x) x.Nq, res, 'UniformOutput',false));
N_v  = cell2mat(cellfun(@(x) x.N,  res, 'UniformOutput',false));
W_v  = cell2mat(cellfun(@(x) x.W,  res, 'UniformOutput',false));
T_v  = cell2mat(cellfun(@(x) x.T,  res, 'UniformOutput',false));

figure('Name','Рис.7 Сравнение','Color','w','Position',[100 100 1200 380]);
x = 1:4;
subplot(1,4,1); bar(x, Nq_v, 0.6,'FaceColor',[0.3 0.5 0.9]); set(gca,'XTick',x,'XTickLabel',types,'XTickLabelRotation',20); title('N_q'); grid on;
subplot(1,4,2); bar(x, N_v,  0.6,'FaceColor',[0.9 0.5 0.3]); set(gca,'XTick',x,'XTickLabel',types,'XTickLabelRotation',20); title('N');  grid on;
subplot(1,4,3); bar(x, W_v,  0.6,'FaceColor',[0.3 0.8 0.4]); set(gca,'XTick',x,'XTickLabel',types,'XTickLabelRotation',20); title('W');  grid on;
subplot(1,4,4); bar(x, T_v,  0.6,'FaceColor',[0.8 0.3 0.7]); set(gca,'XTick',x,'XTickLabel',types,'XTickLabelRotation',20); title('T');  grid on;

fprintf('=== ЛАБОРАТОРНАЯ РАБОТА №7 ЗАВЕРШЕНА ===\n');

%% ============ Функции ============
function out = sim_smo(tau, nu)
    % Имитация одноканальной СМО FIFO (неограниченная очередь).
    % tau - интервалы поступления, nu - времена обслуживания.
    N = numel(tau);
    arr = cumsum(tau);
    dep = zeros(N,1); wait = zeros(N,1);
    free = 0;
    for i = 1:N
        a = arr(i);
        if free <= a
            w_i = 0; free = a + nu(i);
        else
            w_i = free - a; free = free + nu(i);
        end
        wait(i) = w_i; dep(i) = free;
    end
    sojourn = dep - arr;
    out.arr = arr; out.dep = dep;
    out.T = mean(sojourn); out.W = mean(wait);
    Ttotal = dep(end);
    lam = N / Ttotal;
    out.N  = lam * out.T;          % Литтл
    out.Nq = lam * out.W;          % Литтл для очереди
    out.rho = lam * mean(nu);      % коэффициент загрузки

    % Число заявок в системе во времени (ступенчатая функция)
    evT = [arr; dep];
    evD = [ones(N,1); -ones(N,1)];
    [evT, idx] = sort(evT); evD = evD(idx);
    cnt = cumsum(evD);
    % длительности между событиями
    dur = diff([evT; Ttotal]);
    out.evT = evT; out.cnt = cnt;
    % распределение числа заявок (взвешенное по времени)
    levels = 0:max(cnt);
    tin = zeros(numel(levels),1);
    for i = 1:numel(cnt)
        tin(cnt(i)+1) = tin(cnt(i)+1) + dur(i);
    end
    out.levels = levels;
    out.prob = tin / sum(tin);
end

function X = my_gamrnd(c, b, N)
    % Гамма-распределение (метод Маршаглии-Цанга)
    if c < 1
        X = my_gamrnd(c + 1, b, N) .* (rand(N,1)).^(1/c);
        return;
    end
    d = c - 1/3; cm = 1/sqrt(9*d);
    X = zeros(N,1);
    for i = 1:N
        while true
            x = randn; v = (1 + cm*x)^3;
            if v > 0
                u = rand;
                if log(u) < 0.5*x^2 + d - d*v + d*log(v)
                    X(i) = d*v*b; break;
                end
            end
        end
    end
end
