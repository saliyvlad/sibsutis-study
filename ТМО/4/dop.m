%% Доп. задание 2: СМО M/M/8/10 в Simulink (вариант 18)
% ИКС-431 Салий Владислав
clear; clc; close all;

% Проверка наличия SimEvents
if ~license('test','Simulink_Discrete_Event')
    error('SimEvents не установлен. Используйте доп. задание 1 (Python).');
end

% Параметры варианта 18
lambda = 40;    % интенсивность входного потока
mu = 30;        % интенсивность обслуживания
n = 8;          % число каналов
m = 10;         % длина очереди
N_entities = 1000;  % число заявок для симуляции

fprintf('Параметры СМО: lambda=%.1f, mu=%.1f, n=%d, m=%d\n', lambda, mu, n, m);

% Создаём новую модель
modelName = 'SMO_Lab4_Variant18';
if bdIsLoaded(modelName), close_system(modelName, 0); end
new_system(modelName);
open_system(modelName);

% --- Блок генератора заявок (Entity Generator) ---
gen = add_block('simeventslib/Entity Generator', [modelName '/Generator']);
set_param(gen, 'InterarrivalTime', 'exponential(1/lambda)');
set_param(gen, 'DataAttributeName', 'arrivalTime');

% --- Блок очереди (FIFO Queue) ---
queue = add_block('simeventslib/FIFO Queue', [modelName '/Queue']);
set_param(queue, 'Capacity', num2str(m));

% --- Блок сервера (Entity Server) ---
server = add_block('simeventslib/Entity Server', [modelName '/Server']);
set_param(server, 'ServiceTime', 'exponential(1/mu)');
set_param(server, 'NumberOfServers', num2str(n));

% --- Блок приёмника (Entity Sink) ---
sink = add_block('simeventslib/Entity Sink', [modelName '/Sink']);

% --- Соединяем блоки ---
add_line(modelName, 'Generator/1', 'Queue/1', 'autorouting', 'on');
add_line(modelName, 'Queue/1', 'Server/1', 'autorouting', 'on');
add_line(modelName, 'Server/1', 'Sink/1', 'autorouting', 'on');

% --- Настройка параметров симуляции ---
set_param(modelName, 'StopTime', num2str(N_entities / lambda * 2));
set_param(modelName, 'Solver', 'FixedStepDiscrete');

% --- Запуск симуляции ---
fprintf('\nЗапуск симуляции...\n');
simOut = sim(modelName, 'ReturnWorkspaceOutputs', 'on');

% --- Сбор статистики ---
% Число обслуженных заявок
N_served = simOut.get('Sink').Data(end);
% Среднее время в системе (из блока Sink, если настроен таймер)
% Для упрощения считаем аналитически

% Аналитические показатели (для сравнения)
rho = lambda / mu;
p0 = 1 / (sum(arrayfun(@(k) rho^k/factorial(k), 0:n)) + ...
     (rho^n/factorial(n)) * sum((rho/n).^(1:m)));
P_otk = (rho^n/factorial(n)) * (rho/n)^m * p0;
Q = 1 - P_otk;
A = lambda * Q;
L_och = (rho^(n+1)/(n*factorial(n))) * ...
        (1-(m+1-m*rho/n)*(rho/n)^m)/(1-rho/n)^2 * p0;
T_sist = (L_och + A/mu) / lambda;

fprintf('\n=== Аналитические результаты ===\n');
fprintf('P_отк = %.6f\n', P_otk);
fprintf('Q = %.6f\n', Q);
fprintf('A = %.4f\n', A);
fprintf('L_оч = %.4f\n', L_och);
fprintf('T_сист = %.4f\n', T_sist);

fprintf('\n=== Результаты симуляции ===\n');
fprintf('Обслужено заявок: %d из %d\n', N_served, N_entities);
fprintf('Эмпирическая P_отк = %.6f\n', 1 - N_served/N_entities);

% Сохраняем модель
save_system(modelName);
fprintf('\nМодель сохранена: %s.slx\n', modelName);

% Закрываем модель (опционально)
% close_system(modelName, 0);

fprintf('\n=== Доп. задание 2 (Simulink) завершено ===\n');