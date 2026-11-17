%% Лабораторная работа 1.3. Марковские цепи. Вариант 18.
% ИКС-431 Салий Владислав
clear; clc;

L = 15;
T = zeros(L, L);

% Формирование матрицы переходов вручную
% Каждый узел имеет >= 3 исходящих связи с вероятностями 0.5, 0.3, 0.2
for i = 1:L
    next1 = mod(i, L) + 1;      % Сосед справа
    next2 = mod(i+1, L) + 1;    % Следующий сосед  
    next3 = mod(i+3, L) + 1;    % Узел через один
    
    T(i, next1) = 0.5;
    T(i, next2) = 0.3;
    T(i, next3) = 0.2;
end

% Вывод информации о матрице
fprintf('Матрица переходов %d на %d задана ВРУЧНУЮ с точностью до 10го знака\n', L, L);

% Проверка стохастичности
if stochastic(T)
    disp('Матрица стохастичная.');
else
    disp('ОШИБКА: Матрица НЕ является стохастической!');
end

% Проверка эргодичности
if ergodic(T, 1e-5)
    disp('Цепь эргодическая.');
else
    disp('Цепь НЕ является эргодической.');
end

% --- Функции проверки ---

function is_stoch = stochastic(matrix)
    % Проверка на стохастичность: суммы строк == 1 и элементы >= 0
    [rows, ~] = size(matrix);
    is_stoch = true;
    for i = 1:rows
        row_sum = sum(matrix(i, :));
        if abs(row_sum - 1) > 1e-6 || any(matrix(i, :) < 0)
            is_stoch = false;
            return;
        end
    end
end

function is_erg = ergodic(matrix, epsilon)
    % Проверка на эргодичность через возведение в степень m=200
    m = 200;
    T_pow = matrix^m;
    % Если минимальный элемент предельной матрицы > epsilon, цепь эргодична
    if min(T_pow(:)) > epsilon
        is_erg = true;
    else
        is_erg = false;
    end
end