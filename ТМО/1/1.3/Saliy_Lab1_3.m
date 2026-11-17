clear; clc;

L = 15;
T = zeros(L, L);

for i = 1:L
    next1 = mod(i, L) + 1;
    next2 = mod(i+1, L) + 1;
    next3 = mod(i+3, L) + 1;
    
    T(i, next1) = 0.5;
    T(i, next2) = 0.3;
    T(i, next3) = 0.2;
end

fprintf('Матрица переходов %d на %d задана ВРУЧНУЮ с точностью до 10го знака\n', L, L);

if stochastic(T)
    disp('Матрица стохастичная.');
else
    disp('ОШИБКА: Матрица НЕ является стохастической!');
end

if ergodic(T, 1e-5)
    disp('Цепь эргодическая.');
else
    disp('Цепь НЕ является эргодической.');
end

function is_stoch = stochastic(matrix)
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
    m = 200;
    T_pow = matrix^m;
    if min(T_pow(:)) > epsilon
        is_erg = true;
    else
        is_erg = false;
    end
end