clear; clc; close all;

syms x t;

f = sin(x)^2 - cos(x)^2;
df = diff(f, x);
F_int = int(f, t, 0, x);

fprintf('f(x)  = %s\n', char(f));
fprintf('f''(x) = %s\n', char(df));
fprintf('F(x)  = %s\n\n', char(F_int));

f_num  = matlabFunction(f);
df_num = matlabFunction(df);
F_num  = matlabFunction(F_int);

x_vals = linspace(-2, 2, 1000);

a = 1; b = 0;
equation = @(x) a*x + b - f_num(x);

figure('Name','Лабораторная работа 1.1','Position',[100 100 900 700]);

subplot(2,2,1);
plot(x_vals, f_num(x_vals), 'b', 'LineWidth', 1.5); hold on;
plot(x_vals, a*x_vals + b, 'r--', 'LineWidth', 1.5);
grid on; xlabel('x'); ylabel('y');
title('Графическое решение: f(x) и a*x+b');
legend('f(x)', 'a*x+b', 'Location','best');

x_sol = fsolve(equation, -0.5);
fprintf('Решение уравнения a*x+b = f(x):  x = %.6f\n', x_sol);

subplot(2,2,2);
plot(x_vals, f_num(x_vals), 'b', 'LineWidth', 1.5); grid on;
xlabel('x'); ylabel('f(x)'); title('График функции f(x)');

subplot(2,2,3);
plot(x_vals, df_num(x_vals), 'm', 'LineWidth', 1.5); grid on;
xlabel('x'); ylabel('f''(x)'); title('График производной f''(x)');

subplot(2,2,4);
plot(x_vals, F_num(x_vals), 'g', 'LineWidth', 1.5); grid on;
xlabel('x'); ylabel('F(x)'); title('График интеграла F(x)');

[X, Y] = meshgrid(linspace(-2, 2, 100), linspace(-2, 2, 100));
Z = (X.^2 + Y.^2) ./ (X.*Y + eps);

figure('Name','3D график F(x,y)','Position',[200 200 700 600]);
surf(X, Y, Z, 'EdgeColor', 'none');
colormap(parula);
shading interp;
xlabel('x'); ylabel('y'); zlabel('F(x,y)');
title('Трёхмерный график F(x,y) = (x^2 + y^2)/(x*y)');
colorbar;

fprintf('\nЛабораторная работа 1.1 выполнена.\n');