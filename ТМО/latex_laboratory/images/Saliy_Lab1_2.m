%% Лабораторная работа 1.2. Вариант 18.
% ИКС-431 Салий Владислав
clear; clc;

% Параметры варианта 18
I = 33;
J = 10;

% Вызов функции
[E_M, D_M, M] = matrix_ops(I, J);

fprintf('Размерность матрицы: %dx%d\n', I, J);
fprintf('Среднее значение (E): %.4f\n', E_M);
fprintf('Дисперсия (D): %.4f\n', D_M);

function [E_val, D_val, Matrix] = matrix_ops(rows, cols)
    % Генерация вектора-столбца [0, 10]
    V_col = 10 * rand(rows, 1);
    
    % Генерация вектора-строки [-5, 5]
    V_row = 10 * rand(1, cols) - 5;
    
    % Перемножение векторов (внешнее произведение)
    Matrix = V_col * V_row;
    
    % Вычисление среднего
    E_val = mean(Matrix(:));
    
    % Вычисление дисперсии
    D_val = var(Matrix(:));
end