clear; clc;

I = 33;
J = 10;

[E_M, D_M, M] = matrix_ops(I, J);

fprintf('Размерность матрицы: %dx%d\n', I, J);
fprintf('Среднее значение (E): %.4f\n', E_M);
fprintf('Дисперсия (D): %.4f\n', D_M);

function [E_val, D_val, Matrix] = matrix_ops(rows, cols)
    V_col = 10 * rand(rows, 1);
    V_row = 10 * rand(1, cols) - 5;
    Matrix = V_col * V_row;
    E_val = mean(Matrix(:));
    D_val = var(Matrix(:));
end