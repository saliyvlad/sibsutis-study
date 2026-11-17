import numpy as np
import matplotlib.pyplot as plt

# Параметры по заданию: RC в интервале 0.001 - 0.01, частота сигнала 800 - 2000 Гц
RC = 0.001        # постоянная времени RC-цепи, с
f_sig = 1000.0    # частота входного гармонического колебания, Гц
Ts = 2e-5         # шаг дискретизации при численной свертке, с

# =========================================================
# 1.1 Вычисление интеграла свертки сигнала и импульсной характеристики
# =========================================================
print("=== 1.1 Свертка входного сигнала и ИХ RC-цепи ===")
t = np.arange(0, 0.02, Ts)                     # отрезок 20 мс = 20 периодов сигнала
s1 = np.cos(2 * np.pi * f_sig * t)             # входной сигнал
h = (1 / RC) * np.exp(-t / RC)                 # импульсная характеристика h(t)=1/RC*exp(-t/RC)

print(f"RC = {RC} с, начальное значение ИХ h(0) = {h[0]:.0f}, "
      f"длительность ИХ (5*RC) = {5 * RC * 1000:.1f} мс")

# Численная свертка интегралом: y(t) = integral s1(t-u) h(u) du
# выполняется сверткой отсчетов с множителем Ts (метод прямоугольников/трапеций)
y = np.convolve(s1, h)[:len(s1)] * Ts          # y[n] ~ integral s1(t-u)h(u)du

plt.figure(figsize=(12, 7))
plt.subplot(2, 1, 1)
plt.stem(t[:200] * 1000, h[:200], basefmt=' ')
plt.title(f'Импульсная характеристика RC-цепи, RC = {RC} с')
plt.xlabel('t, мс')
plt.ylabel('h(t)')
plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(t * 1000, s1, label='вход s1(t)', alpha=0.7)
plt.plot(t * 1000, y, 'r', linewidth=2, label='выход y(t) — свертка')
plt.title('Преобразование сигнала в линейной цепи (свертка с ИХ)')
plt.xlabel('t, мс')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()
plt.tight_layout()

print(f"Амплитуда выхода в установившемся режиме (t > 10 мс): "
      f"{np.max(np.abs(y[t > 0.01])):.4f}")
print("Вывод: высокочастотный входной сигнал (1000 Гц >> 1/(2*pi*RC) = 159 Гц) "
      "сильно ослаблен и сдвинут по фазе — цепь работает как ФНЧ.")

# =========================================================
# 1.2 Вычисление частотной характеристики RC цепи
# =========================================================
print("\n=== 1.2 Частотная характеристика RC-цепи ===")
f = np.linspace(0, 3 / RC, 3000)               # интервал частот 0 ... 3/RC Гц
w = 2 * np.pi * f

H = 1 / (1 + 1j * w * RC)                       # комплексная ЧХ
abs_H_formula = 1 / np.sqrt(1 + (w * RC) ** 2)  # АЧХ по формуле
phi_formula = -np.arctan(w * RC)                # ФЧХ по формуле

err_abs = np.max(np.abs(np.abs(H) - abs_H_formula))
err_phi = np.max(np.abs(np.angle(H) - phi_formula))
print(f"Контроль совпадения комплексной ЧХ и формул: "
      f"по модулю {err_abs:.2e}, по аргументу {err_phi:.2e}")

f_c = 1 / (2 * np.pi * RC)
print(f"Частота среза f_c = 1/(2*pi*RC) = {f_c:.1f} Гц, "
      f"на ней |H| = 1/sqrt(2) = {1 / np.sqrt(2):.3f} (-3 дБ)")

plt.figure(figsize=(12, 7))
plt.subplot(2, 1, 1)
plt.plot(f, abs_H_formula, 'b', linewidth=2)
plt.axvline(f_c, color='g', linestyle='--', label=f'f_c = {f_c:.0f} Гц')
plt.axhline(1 / np.sqrt(2), color='r', linestyle=':', label='-3 дБ')
plt.title(f'АЧХ RC-цепи, |H(jw)| = 1/sqrt(1+(wRC)^2), RC = {RC}')
plt.xlabel('Частота f, Гц')
plt.ylabel('|H|')
plt.grid(True)
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(f, phi_formula, 'b', linewidth=2)
plt.axvline(f_c, color='g', linestyle='--', label=f'f_c = {f_c:.0f} Гц')
plt.axvline(3 * f_c, color='k', linestyle=':', label='3*f_c')
plt.title(f'ФЧХ RC-цепи, phi(f) = -arctg(2*pi*f*RC)')
plt.xlabel('Частота f, Гц')
plt.ylabel('phi, рад')
plt.grid(True)
plt.legend()
plt.tight_layout()

# =========================================================
# 1.3 Вычисление сигнала на выходе по частотной характеристике
# =========================================================
print("\n=== 1.3 Выходной сигнал по комплексному коэффициенту передачи ===")
f0 = f_sig                                   # выбранная частота входного колебания
w0 = 2 * np.pi * f0
H0 = 1 / (1 + 1j * w0 * RC)                  # комплексный коэффициент передачи
A0 = np.abs(H0)
phi0 = np.angle(H0)

print(f"Входной сигнал:  s1(t) = cos(2*pi*{f0:.0f}*t)")
print(f"H(j*w0) = 1/(1+j*w0*RC) = {H0:.4f}")
print(f"Модуль ЧХ  |H(jw0)| = {A0:.4f},  аргумент phi(w0) = {phi0:.4f} рад "
      f"({np.degrees(phi0):.1f} град)")
print(f"Выходной сигнал: y(t) = {A0:.4f} * cos(2*pi*{f0:.0f}*t {phi0:+.4f})")

y_analytic = A0 * np.cos(2 * np.pi * f0 * t + phi0)

# Сравнение аналитического установившегося сигнала и численной свертки из 1.1
mask = t > 0.01                              # после переходного процесса (>5*RC)
err = np.max(np.abs(y[mask] - y_analytic[mask]))
print(f"Макс. отклонение численной свертки от аналитического выхода "
      f"в установившемся режиме: {err:.4f}")

plt.figure(figsize=(12, 5))
plt.plot(t * 1000, s1, label='вход s1(t)', alpha=0.7)
plt.plot(t * 1000, y_analytic, 'g', linewidth=2, label='выход по ЧХ (аналитически)')
plt.plot(t * 1000, y, 'r', linestyle=':', label='выход по свертке (численно)')
plt.title(f'Вход и выход RC-цепи: |H| = {A0:.3f}, сдвиг фаз {np.degrees(phi0):.1f}°')
plt.xlabel('t, мс')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()
plt.tight_layout()

print("\nВывод по работе: свертка с ИХ и умножение спектра на ЧХ дают один и тот же "
      "выходной сигнал; на 1000 Гц RC-цепь (f_c = 159 Гц) ослабляет сигнал в ~6.3 раз "
      "и сдвигает фазу почти на -81 град — свойства ФНЧ.")

plt.show()
