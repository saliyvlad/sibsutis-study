# -*- coding: utf-8 -*-
"""
Практическая работа №2 (Занятие №2).
Проектирование радиопокрытия мобильных сетей.
Модели распространения сигналов. Бюджеты каналов (Link Budget).

Выполняются задания 1-4 из раздела "Порядок выполнения работы":
  1) Бюджет восходящего канала (UL) -> MAPL_UL
  2) Бюджет нисходящего канала (DL) -> MAPL_DL
  3) Зависимость потерь радиосигнала от расстояния по моделям
     FSM (Free Space), UMiNLOS, COST 231 Hata + выбор модели
  4) Радиус сот в UL и DL, площадь одной БС, число БС для покрытия
     заданной территории (макросоты и микро/фемтосоты)

Поиск радиуса выполнен двумя способами: графически (пересечение MAPL
с кривой PL(d)) и аналитически (обратная функция PL(d)) — результаты
совпадают.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")  # сохраняем графики в файлы без открытия окна
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 1. ИСХОДНЫЕ ДАННЫЕ (раздел 3 задания)
# ----------------------------------------------------------------------
TxPowerBS = 46.0        # мощность передатчика базовой станции, дБм
N_sectors = 3           # число секторов на одной БС
TxPowerUE = 24.0        # мощность передатчика терминала пользователя, дБм
AntGainBS = 21.0        # коэффициент усиления антенны БС, дБи
PenetrationM = 15.0     # запас на проникновение сквозь стены, дБ
IM = 1.0                # запас на интерференцию (Interference Margin), дБ
f_GHz = 1.8             # диапазон частот, ГГц
f_MHz = f_GHz * 1000    # диапазон частот, МГц
BW_UL_MHz = 10.0        # полоса частот UL, МГц
BW_DL_MHz = 20.0        # полоса частот DL, МГц
NF_BS = 2.4             # коэффициент шума приёмника БС, дБ
NF_UE = 6.0             # коэффициент шума приёмника пользователя, дБ
SINR_DL = 2.0           # требуемое SINR для DL, дБ
SINR_UL = 4.0           # требуемое SINR для UL, дБ
MIMO = 2                # число приёмо-передающих антенн БС (MIMO 2x2)

Area_macro = 100.0      # площадь территории под макросоты, кв.км
Area_micro = 4.0        # площадь ТЦ/БЦ под микро/фемтосоты, кв.км

# --- Допущения, не заданные в исходных данных (для COST 231 Hata) ------
hBS = 30.0              # высота подвеса антенны БС, м (диапазон модели 30..200 м)
hms = 1.5               # высота антенны мобильного устройства, м (1..10 м)
terrain = "U"           # тип местности: U = urban (городская застройка)
# FeederLoss: БС "с фидерами" -> фидер 2 дБ + МШУ 0.4 дБ + джампер 0.5 дБ
FeederLoss = 2.0 + 0.4 + 0.5
MIMOGain = 3.0          # выигрыш MIMO 2x2 = 10*log10(2) ~ 3 дБ

# ----------------------------------------------------------------------
# 2. ЧУВСТВИТЕЛЬНОСТЬ ПРИЁМНИКА (формулы 2.17, 2.18)
# ----------------------------------------------------------------------
def thermal_noise(bw_mhz):
    """Тепловой шум приёмника, дБм: -174 + 10*log10(BW[Гц])."""
    bw_hz = bw_mhz * 1e6
    return -174.0 + 10.0 * np.log10(bw_hz)


# В DL принимает UE -> чувствительность UE и тепловой шум в полосе DL
ThermalNoise_DL = thermal_noise(BW_DL_MHz)
RxSensUE = NF_UE + ThermalNoise_DL + SINR_DL

# В UL принимает БС -> чувствительность БС и тепловой шум в полосе UL
ThermalNoise_UL = thermal_noise(BW_UL_MHz)
RxSensBS = NF_BS + ThermalNoise_UL + SINR_UL

# ----------------------------------------------------------------------
# 3. БЮДЖЕТЫ КАНАЛОВ -> MAPL (формулы 2.19, 2.20)
# ----------------------------------------------------------------------
# TxPowerBS - FeederLoss + AntGainBS + MIMOGain - MAPL_DL - IM - PenetrationM = RxSensUE
MAPL_DL = TxPowerBS - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM - RxSensUE
# TxPowerUE - FeederLoss + AntGainBS + MIMOGain - MAPL_UL - IM - PenetrationM = RxSensBS
MAPL_UL = TxPowerUE - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM - RxSensBS

# ----------------------------------------------------------------------
# 4. МОДЕЛИ РАСПРОСТРАНЕНИЯ (раздел 2.2)
# ----------------------------------------------------------------------
def PL_fsm(d_m):
    """Free Space Model, формула (2.2): PL = 20*log10(4*pi*d*f/c), дБ."""
    c = 3e8
    d = np.asarray(d_m, dtype=float)
    return 20.0 * np.log10(4.0 * np.pi * d * (f_GHz * 1e9) / c)


def PL_uminlos(d_m):
    """UMiNLOS, формула (2.3): PL = 26*log10(f[ГГц]) + 22.7 + 36.7*log10(d[м])."""
    d = np.asarray(d_m, dtype=float)
    return 26.0 * np.log10(f_GHz) + 22.7 + 36.7 * np.log10(d)


def cost231_params():
    """Константы A, B (табл. 2.1), a(hms), Lclutter, s для COST 231 Hata."""
    if 150 <= f_MHz <= 1500:
        A, B = 69.55, 26.16
    else:  # 1500..2000 МГц
        A, B = 46.3, 33.9

    lf = np.log10(f_MHz)
    # a(hms), формула (2.5)
    if terrain in ("DU", "U"):
        a = 3.2 * (np.log10(11.75 * hms)) ** 2 - 4.97
    else:  # SU, RURAL, ROAD
        a = (1.1 * lf) * hms - (1.56 * lf - 0.8)

    # Lclutter, формула (2.6)
    if terrain == "DU":
        Lclutter = 3.0
    elif terrain == "U":
        Lclutter = 0.0
    elif terrain == "SU":
        Lclutter = -((2.0 * np.log10(f_MHz / 28.0)) ** 2 + 5.4)
    elif terrain == "RURAL":
        Lclutter = -(4.78 * lf ** 2 - 18.33 * lf + 40.94)
    else:  # ROAD
        Lclutter = -(4.78 * lf ** 2 - 18.33 * lf + 35.94)

    return A, B, a, Lclutter, lf


def PL_cost231(d_km):
    """COST 231 Hata, формула (2.4). d в км, f в МГц."""
    A, B, a, Lclutter, lf = cost231_params()
    d = np.asarray(d_km, dtype=float)
    const = A + B * lf - 13.82 * np.log10(hBS) - a + Lclutter
    # s зависит от расстояния (формула 2.7): при d>=1 км и d<1 км разные ветки
    s_far = 44.9 - 6.55 * lf
    s_near = (47.88 + 13.9 * lf - 13.9 * np.log10(hBS)) / np.log10(50.0)
    s = np.where(d >= 1.0, s_far, s_near)
    return const + s * np.log10(d)


def radius_cost231(mapl):
    """Аналитический радиус COST 231 Hata для заданного MAPL (км)."""
    A, B, a, Lclutter, lf = cost231_params()
    const = A + B * lf - 13.82 * np.log10(hBS) - a + Lclutter
    s_far = 44.9 - 6.55 * lf
    # ветка d >= 1 км
    d_far = 10 ** ((mapl - const) / s_far)
    if d_far >= 1.0:
        return d_far
    # ветка d < 1 км
    s_near = (47.88 + 13.9 * lf - 13.9 * np.log10(hBS)) / np.log10(50.0)
    return 10 ** ((mapl - const) / s_near)


def radius_linear_model(mapl, kind):
    """Аналитический радиус для моделей вида PL = C + n*log10(d)."""
    if kind == "uminlos":
        C = 26.0 * np.log10(f_GHz) + 22.7
        n = 36.7
        return 10 ** ((mapl - C) / n)          # метры
    # fsm: PL = 20*log10(4*pi*f/c) + 20*log10(d)
    C = 20.0 * np.log10(4.0 * np.pi * f_GHz * 1e9 / 3e8)
    n = 20.0
    return 10 ** ((mapl - C) / n)              # метры


# ----------------------------------------------------------------------
# 5. РАДИУСЫ СОТ (задание 4)
# ----------------------------------------------------------------------
# Макросоты: модель COST 231 Hata (d в км)
d_DL_macro_km = radius_cost231(MAPL_DL)
d_UL_macro_km = radius_cost231(MAPL_UL)
d_macro_km = min(d_DL_macro_km, d_UL_macro_km)   # берём меньший радиус

# Микро/фемтосоты: модель UMiNLOS (d в метрах)
d_DL_micro_m = radius_linear_model(MAPL_DL, "uminlos")
d_UL_micro_m = radius_linear_model(MAPL_UL, "uminlos")
d_micro_m = min(d_DL_micro_m, d_UL_micro_m)

# Площадь одной БС (3 сектора): S = 1.95 * R^2 (рис. 2.7)
S_sector_coeff = 1.95
S_macro_site = S_sector_coeff * d_macro_km ** 2                 # кв.км
S_micro_site = S_sector_coeff * (d_micro_m / 1000.0) ** 2       # кв.км

# Число БС (округление вверх до целого)
N_BS_macro = int(np.ceil(Area_macro / S_macro_site))
N_BS_micro = int(np.ceil(Area_micro / S_micro_site))

# ----------------------------------------------------------------------
# 6. КОНСОЛЬНЫЙ ОТЧЁТ
# ----------------------------------------------------------------------
print("=" * 64)
print(" ПРАКТИЧЕСКАЯ РАБОТА №2. Радиопокрытие. Бюджеты каналов.")
print("=" * 64)

print("\n[Задание 1] Бюджет восходящего канала (UL), приёмник = БС:")
print(f"  Тепловой шум (BW_UL={BW_UL_MHz:.0f} МГц): {ThermalNoise_UL:.2f} дБм")
print(f"  Чувствительность RxSensBS = {NF_BS} + ({ThermalNoise_UL:.2f}) + {SINR_UL}"
      f" = {RxSensBS:.2f} дБм")
print(f"  MAPL_UL = {MAPL_UL:.2f} дБ")

print("\n[Задание 2] Бюджет нисходящего канала (DL), приёмник = UE:")
print(f"  Тепловой шум (BW_DL={BW_DL_MHz:.0f} МГц): {ThermalNoise_DL:.2f} дБм")
print(f"  Чувствительность RxSensUE = {NF_UE} + ({ThermalNoise_DL:.2f}) + {SINR_DL}"
      f" = {RxSensUE:.2f} дБм")
print(f"  MAPL_DL = {MAPL_DL:.2f} дБ")

print("\n[Задание 3] Модели распространения (f = %.1f ГГц, hBS = %.0f м, "
      "hms = %.1f м, тип местности = %s):" % (f_GHz, hBS, hms, terrain))
A, B, a_par, Lcl, lf = cost231_params()
print(f"  COST 231 Hata: A={A}, B={B}, a(hms)={a_par:.3f}, Lclutter={Lcl:.3f}")
print("  Для макросот (макропокрытие) -> COST 231 Hata")
print("  Для микро/фемтосот (помещения) -> UMiNLOS")

print("\n[Задание 4] Радиусы сот (пересечение MAPL с кривой PL(d)):")
print("  --- Макросоты (COST 231 Hata) ---")
print(f"    d_DL = {d_DL_macro_km:.3f} км,  d_UL = {d_UL_macro_km:.3f} км")
print(f"    Радиус БС (минимум) R = {d_macro_km:.3f} км")
print(f"    Площадь 1 сайта (3 сектора, S=1.95*R^2) = {S_macro_site:.3f} кв.км")
print(f"    Требуется БС для {Area_macro:.0f} кв.км: {Area_macro/S_macro_site:.2f}"
      f" -> {N_BS_macro} шт.")
print("  --- Микро/фемтосоты (UMiNLOS) ---")
print(f"    d_DL = {d_DL_micro_m:.1f} м,  d_UL = {d_UL_micro_m:.1f} м")
print(f"    Радиус БС (минимум) R = {d_micro_m:.1f} м")
print(f"    Площадь 1 сайта (3 сектора, S=1.95*R^2) = {S_micro_site*1e6:.1f} кв.м")
print(f"    Требуется БС для {Area_micro:.0f} кв.км: {Area_micro/S_micro_site:.2f}"
      f" -> {N_BS_micro} шт.")

# ----------------------------------------------------------------------
# 7. ГРАФИКИ
# ----------------------------------------------------------------------
out_dir = os.path.dirname(os.path.abspath(__file__))

# --- Рис.1: кривые потерь (как рис. 2.1) ---
d1 = np.logspace(0, 2.3, 400)  # 1 .. ~200 м
plt.figure(figsize=(9, 5.5))
plt.plot(d1, PL_uminlos(d1), "r-", lw=2, label=f"UMiNLOS ({f_GHz} ГГц)")
plt.plot(d1, PL_fsm(d1), "b--", lw=2, label=f"FSM ({f_GHz} ГГц)")
plt.title("Задание 3: Потери сигнала в помещении (UMiNLOS vs FSM)")
plt.xlabel("Расстояние между приёмником и передатчиком, м")
plt.ylabel("Потери сигнала, дБ")
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
p = os.path.join(out_dir, "task3_indoor_models.png")
plt.savefig(p, dpi=150)
plt.close()
print("\nГрафик сохранён:", p)

# --- Рис.2: радиус микро/фемтосот (как рис. 2.6) ---
d2 = np.logspace(0, 3.3, 600)  # 1 .. ~2000 м (чтобы показать пересечение с MAPL_DL)
plt.figure(figsize=(9, 5.5))
plt.plot(d2, PL_uminlos(d2), "r.-", lw=2, ms=3, label=f"UMiNLOS ({f_GHz} ГГц)")
plt.axhline(MAPL_UL, color="b", lw=2, label=f"MAPL_UL = {MAPL_UL:.1f} дБ")
plt.axhline(MAPL_DL, color="g", ls="--", lw=2, label=f"MAPL_DL = {MAPL_DL:.1f} дБ")
plt.axvline(d_UL_micro_m, color="b", ls=":", alpha=0.7)
plt.axvline(d_DL_micro_m, color="g", ls=":", alpha=0.7)
plt.annotate(f"d_UL={d_UL_micro_m:.0f} м", (d_UL_micro_m, MAPL_UL),
             xytext=(d_UL_micro_m * 1.15, MAPL_UL - 15), color="b")
plt.annotate(f"d_DL={d_DL_micro_m:.0f} м", (d_DL_micro_m, MAPL_DL),
             xytext=(d_DL_micro_m * 0.55, MAPL_DL - 15), color="g")
plt.title("Задание 4: Радиус микро/фемтосоты (модель UMiNLOS)")
plt.xlabel("Расстояние, м")
plt.ylabel("Потери сигнала, дБ")
plt.xlim(0, d_DL_micro_m * 1.1)
plt.ylim(40, MAPL_DL + 8)
plt.grid(True, alpha=0.4)
plt.legend(loc="lower right")
plt.tight_layout()
p = os.path.join(out_dir, "task4_radius_micro_uminos.png")
plt.savefig(p, dpi=150)
plt.close()
print("График сохранён:", p)

# --- Рис.3: радиус макросоты (COST 231 Hata) ---
d3 = np.logspace(-2, 1, 600)  # 0.01 .. 10 км
plt.figure(figsize=(9, 5.5))
plt.plot(d3, PL_cost231(d3), "m-", lw=2, label=f"COST 231 Hata ({f_MHz:.0f} МГц)")
plt.axhline(MAPL_UL, color="b", lw=2, label=f"MAPL_UL = {MAPL_UL:.1f} дБ")
plt.axhline(MAPL_DL, color="g", ls="--", lw=2, label=f"MAPL_DL = {MAPL_DL:.1f} дБ")
plt.axvline(d_UL_macro_km, color="b", ls=":", alpha=0.7)
plt.axvline(d_DL_macro_km, color="g", ls=":", alpha=0.7)
plt.annotate(f"d_UL={d_UL_macro_km:.2f} км", (d_UL_macro_km, MAPL_UL),
             xytext=(d_UL_macro_km * 1.1, MAPL_UL - 5), color="b")
plt.annotate(f"d_DL={d_DL_macro_km:.2f} км", (d_DL_macro_km, MAPL_DL),
             xytext=(d_DL_macro_km * 1.1, MAPL_DL - 5), color="g")
plt.title("Задание 4: Радиус макросоты (COST 231 Hata, тип U)")
plt.xlabel("Расстояние, км")
plt.ylabel("Потери сигнала, дБ")
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
p = os.path.join(out_dir, "task4_radius_macro_cost231.png")
plt.savefig(p, dpi=150)
plt.close()
print("График сохранён:", p)

# --- Рис.4: сравнение всех трёх моделей на одном графике ---
d4 = np.logspace(0, 3, 500)  # 1 м .. 1 км (по оси X — метры)
plt.figure(figsize=(9, 5.5))
plt.plot(d4, PL_fsm(d4), "b--", lw=2, label="FSM (свободное пространство)")
plt.plot(d4, PL_uminlos(d4), "r-", lw=2, label="UMiNLOS (помещение)")
plt.plot(d4, PL_cost231(d4 / 1000.0), "g-.", lw=2,
         label="COST 231 Hata (макро, U)")
plt.title(f"Задание 3: Сравнение моделей распространения (f = {f_GHz} ГГц)")
plt.xlabel("Расстояние, м")
plt.ylabel("Потери сигнала, дБ")
plt.xscale("log")
plt.grid(True, alpha=0.4, which="both")
plt.legend()
plt.tight_layout()
p = os.path.join(out_dir, "task3_models_comparison.png")
plt.savefig(p, dpi=150)
plt.close()
print("График сохранён:", p)

# ----------------------------------------------------------------------
# 8. QR-код на git-репозиторий (требование к отчёту)
# ----------------------------------------------------------------------
REPO_URL = "https://git.csc.sibsutis.ru/iks432s08/distributed-arch.git"
try:
    import qrcode
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(REPO_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    p = os.path.join(out_dir, "qr_repo.png")
    img.save(p)
    print("QR-код сохранён:", p, "->", REPO_URL)
except Exception as e:
    print("Не удалось сгенерировать QR-код:", e)

print("\n" + "=" * 64)
print(" ВСЕ ЗАДАНИЯ (1-4) ВЫПОЛНЕНЫ. Проверьте PNG-файлы в папке скрипта.")
print("=" * 64)

# ----------------------------------------------------------------------
# 9. Выгрузка результатов в JSON (единый источник данных для отчёта)
# ----------------------------------------------------------------------
results = {
    "inputs": {
        "f_GHz": f_GHz, "f_MHz": f_MHz, "N_sectors": N_sectors,
        "TxPowerBS": TxPowerBS, "TxPowerUE": TxPowerUE, "AntGainBS": AntGainBS,
        "PenetrationM": PenetrationM, "IM": IM,
        "BW_UL_MHz": BW_UL_MHz, "BW_DL_MHz": BW_DL_MHz,
        "NF_BS": NF_BS, "NF_UE": NF_UE, "SINR_DL": SINR_DL, "SINR_UL": SINR_UL,
        "MIMO": MIMO, "MIMOGain": MIMOGain, "FeederLoss": FeederLoss,
        "hBS": hBS, "hms": hms, "terrain": terrain,
        "Area_macro": Area_macro, "Area_micro": Area_micro,
    },
    "link_budget": {
        "ThermalNoise_UL": round(ThermalNoise_UL, 2),
        "ThermalNoise_DL": round(ThermalNoise_DL, 2),
        "RxSensBS": round(RxSensBS, 2), "RxSensUE": round(RxSensUE, 2),
        "MAPL_UL": round(MAPL_UL, 2), "MAPL_DL": round(MAPL_DL, 2),
    },
    "cost231_params": {
        "A": A, "B": B, "a_hms": round(a_par, 3), "Lclutter": round(Lcl, 3),
    },
    "macro": {
        "d_DL_km": round(d_DL_macro_km, 3), "d_UL_km": round(d_UL_macro_km, 3),
        "R_km": round(d_macro_km, 3), "S_site_km2": round(S_macro_site, 3),
        "N_BS_raw": round(Area_macro / S_macro_site, 2), "N_BS": N_BS_macro,
    },
    "micro": {
        "d_DL_m": round(d_DL_micro_m, 1), "d_UL_m": round(d_UL_micro_m, 1),
        "R_m": round(d_micro_m, 1), "S_site_km2": round(S_micro_site, 3),
        "N_BS_raw": round(Area_micro / S_micro_site, 2), "N_BS": N_BS_micro,
    },
}
json_path = os.path.join(out_dir, "results.json")
with open(json_path, "w", encoding="utf-8") as fp:
    json.dump(results, fp, ensure_ascii=False, indent=2)
print("Результаты выгружены:", json_path)
