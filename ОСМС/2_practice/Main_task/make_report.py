# -*- coding: utf-8 -*-
"""
Генератор отчёта по Практической работе №2 (Занятие №2).
Читает results.json и PNG-графики, собирает:
  - Отчёт.md   (редактируемый, для вставки в шаблон Word)
  - report_body.html (самодостаточный HTML-фрагмент с встроенными картинками)
"""

import os
import json
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "results.json"), encoding="utf-8") as f:
    R = json.load(f)

inp = R["inputs"]
lb = R["link_budget"]
c231 = R["cost231_params"]
mac = R["macro"]
mic = R["micro"]


def b64(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as fp:
        return "data:image/png;base64," + base64.b64encode(fp.read()).decode()


IMG = {
    "indoor": b64("task3_indoor_models.png"),
    "compare": b64("task3_models_comparison.png"),
    "micro": b64("task4_radius_micro_uminos.png"),
    "macro": b64("task4_radius_macro_cost231.png"),
    "qr": b64("qr_repo.png"),
}

REPO_URL = "https://git.csc.sibsutis.ru/iks432s08/distributed-arch.git"
STUDENT = "Салий Владислав Павлович"
GROUP = "ИКС-431"
YEAR = "2026"

# ---------------------------- ТЕКСТ ОТЧЁТА ----------------------------
# Формулы подстановки (для прозрачности вычислений)
formulas = {
    "TN_DL": f"-174 + 10·log10({inp['BW_DL_MHz']:.0f}·10⁶) = {lb['ThermalNoise_DL']:.2f} дБм",
    "TN_UL": f"-174 + 10·log10({inp['BW_UL_MHz']:.0f}·10⁶) = {lb['ThermalNoise_UL']:.2f} дБм",
    "RS_UE": f"{inp['NF_UE']} + ({lb['ThermalNoise_DL']:.2f}) + {inp['SINR_DL']:.0f} = {lb['RxSensUE']:.2f} дБм",
    "RS_BS": f"{inp['NF_BS']} + ({lb['ThermalNoise_UL']:.2f}) + {inp['SINR_UL']:.0f} = {lb['RxSensBS']:.2f} дБм",
    "MAPL_DL": (f"{inp['TxPowerBS']:.0f} − {inp['FeederLoss']:.1f} + {inp['AntGainBS']:.0f} + "
                f"{inp['MIMOGain']:.0f} − {inp['IM']:.0f} − {inp['PenetrationM']:.0f} − "
                f"({lb['RxSensUE']:.2f}) = {lb['MAPL_DL']:.2f} дБ"),
    "MAPL_UL": (f"{inp['TxPowerUE']:.0f} − {inp['FeederLoss']:.1f} + {inp['AntGainBS']:.0f} + "
                f"{inp['MIMOGain']:.0f} − {inp['IM']:.0f} − {inp['PenetrationM']:.0f} − "
                f"({lb['RxSensBS']:.2f}) = {lb['MAPL_UL']:.2f} дБ"),
}

qa = [
    ("Какие модели распространения сигналов используются для расчёта радиопокрытия сетей мобильной связи?",
     "Аналитическая модель распространения в свободном пространстве FSM/FSPM (формулы 2.1–2.2) — "
     "базовая, учитывает только частоту и расстояние. Эмпирические модели: UMiNLOS (городская "
     "микросота / помещение, формула 2.3), Okumura‑Hata и её модификация COST 231 Hata (макросоты, "
     "формулы 2.4–2.7), Walfish‑Ikegami (макросота в городской grid‑застройке, формулы 2.8–2.16), "
     "а также Knife‑Edge, Hata и др."),
    ("Какие основные составляющие бюджета восходящего (UL) и нисходящего (DL) каналов в радиосетях?",
     "Мощность передатчика (TxPowerBS для DL, TxPowerUE для UL), потери в антенно‑фидерном тракте "
     "(FeederLoss), усиление антенны БС (AntGainBS), выигрыш MIMO (MIMOGain), максимально допустимые "
     "потери MAPL, запас на интерференцию (IM), запас на проникновение сквозь стены (PenetrationM) и "
     "чувствительность приёмника (RxSensUE для DL, RxSensBS для UL)."),
    ("Чем отличается чувствительность приёмника базовой станции BS и пользовательского терминала UE?",
     "Чувствительность считается по формуле 2.17: RxSens = NoiseFigure + ThermalNoise + RequiredSINR. "
     "Различаются коэффициент шума (у БС ниже — %.1f дБ, у UE выше — %.1f дБ), полоса приёма и требуемое "
     "SINR, которые зависят от направления. В UL сигнал принимает БС (RxSensBS = %.2f дБм), в DL — "
     "терминал UE (RxSensUE = %.2f дБм). Из‑за более высокого шума приёмник UE менее чувствителен." %
     (inp["NF_BS"], inp["NF_UE"], lb["RxSensBS"], lb["RxSensUE"])),
    ("Что такое тепловой шум и как он определяется?",
     "Тепловой (джонсоновский) шум — собственный шум резистивных элементов приёмника при температуре T. "
     "Плотность шума на 1 Гц при 20 °C ≈ −174 дБм/Гц. Уровень: ThermalNoise = −174 + 10·log10(BW[Гц]) "
     "(формула 2.18). Чем шире полоса приёма, тем выше шум и хуже чувствительность."),
    ("Что ограничивает радиус соты мобильных сетей в нисходящем и восходящем каналах?",
     "Радиус — это расстояние, на котором потери PL(d) достигают MAPL выбранной модели. В DL его "
     "определяют мощность передатчика БС (%.0f дБм) и чувствительность UE; в UL — малая мощность "
     "терминала (%.0f дБм) и чувствительность БС. Итоговый радиус соты берут по меньшему из d_UL и d_DL: "
     "в обоих сценариях ограничивает восходящий канал (маломощный терминал)." %
     (inp["TxPowerBS"], inp["TxPowerUE"])),
    ("Из чего состоят потери сигнала в антенно‑фидерном тракте базовой станции BS?",
     "Потери в фидере (≈ 2 дБ), потери в малошумящем усилителе МШУ (≈ 0.4 дБ) и потери в соединительном "
     "джампере до антенны (≈ 0.5 дБ). Если БС развёрнута без фидера (приёмо‑передатчик рядом с антенной), "
     "учитывают только потери джампера 0.5 дБ."),
]

# ---------------------------- MARKDOWN ----------------------------
md = []
md.append(f"# Практическая работа №2. {STUDENT}, гр. {GROUP}\n")
md.append("**Занятие №2. Проектирование радиопокрытия мобильных сетей. "
          "Модели распространения сигналов. Бюджеты каналов.**\n")
md.append(f"*Учебное пособие: Дроздова В. Г. «Основы мобильных сетей LTE», СибГУТИ.*\n")

md.append("\n## 1. Цель работы\n")
md.append("Получить представление о проектировании покрытия сетей мобильной связи и научиться "
          "рассчитывать радиус действия (радиопокрытие) отдельных базовых станций (сот).")

md.append("\n## 2. Исходные данные\n")
md.append("| Параметр | Значение |")
md.append("|---|---|")
md.append(f"| Мощность передатчика БС (TxPowerBS) | {inp['TxPowerBS']:.0f} дБм |")
md.append(f"| Мощность передатчика UE (TxPowerUE) | {inp['TxPowerUE']:.0f} дБм |")
md.append(f"| Усиление антенны БС (AntGainBS) | {inp['AntGainBS']:.0f} дБи |")
md.append(f"| Число секторов на БС | {inp['N_sectors']} |")
md.append(f"| Число антенн MIMO (MIMOGain) | {inp['MIMO']} ({inp['MIMOGain']:.0f} дБ) |")
md.append(f"| Запас на проникновение (PenetrationM) | {inp['PenetrationM']:.0f} дБ |")
md.append(f"| Запас на интерференцию (IM) | {inp['IM']:.0f} дБ |")
md.append(f"| Потери фидерного тракта (FeederLoss) | {inp['FeederLoss']:.1f} дБ |")
md.append(f"| Диапазон частот (f) | {inp['f_GHz']} ГГц ({inp['f_MHz']:.0f} МГц) |")
md.append(f"| Полоса UL / DL | {inp['BW_UL_MHz']:.0f} / {inp['BW_DL_MHz']:.0f} МГц (FDD) |")
md.append(f"| Коэфф. шума BS / UE | {inp['NF_BS']} / {inp['NF_UE']} дБ |")
md.append(f"| Требуемое SINR DL / UL | {inp['SINR_DL']:.0f} / {inp['SINR_UL']:.0f} дБ |")
md.append(f"| Модель макросот | COST 231 Hata (hBS={inp['hBS']:.0f} м, hms={inp['hms']} м, тип {inp['terrain']}) |")
md.append(f"| Модель микро/фемтосот | UMiNLOS |")
md.append(f"| Площадь под макросоты | {inp['Area_macro']:.0f} кв.км |")
md.append(f"| Площадь под микро/фемтосоты | {inp['Area_micro']:.0f} кв.км |")

md.append("\n> **Допущения.** В исходных данных не заданы высоты антенн и тип местности для "
          "COST 231 Hata — приняты типовые: hBS = 30 м, hms = 1.5 м, местность U (город). "
          "FeederLoss для БС «с фидерами» = 2 + 0.4 + 0.5 = 2.9 дБ (по тексту методички).")

md.append("\n## 3. Ход работы\n")
md.append("### Задание 1. Бюджет восходящего канала (UL) → MAPL_UL\n")
md.append(f"- Тепловой шум (BW_UL): {formulas['TN_UL']}")
md.append(f"- Чувствительность RxSensBS = NF_BS + ThermalNoise + SINR_UL = {formulas['RS_BS']}")
md.append(f"- MAPL_UL = TxPowerUE − FeederLoss + AntGainBS + MIMOGain − IM − PenetrationM − RxSensBS")
md.append(f"  = {formulas['MAPL_UL']}")

md.append("\n### Задание 2. Бюджет нисходящего канала (DL) → MAPL_DL\n")
md.append(f"- Тепловой шум (BW_DL): {formulas['TN_DL']}")
md.append(f"- Чувствительность RxSensUE = NF_UE + ThermalNoise + SINR_DL = {formulas['RS_UE']}")
md.append(f"- MAPL_DL = TxPowerBS − FeederLoss + AntGainBS + MIMOGain − IM − PenetrationM − RxSensUE")
md.append(f"  = {formulas['MAPL_DL']}")

md.append("\n### Задание 3. Модели распространения и выбор модели\n")
md.append(f"Параметры COST 231 Hata (f={inp['f_MHz']:.0f} МГц → табл. 2.1): A={c231['A']}, "
          f"B={c231['B']}, a(hms)={c231['a_hms']}, Lclutter={c231['Lclutter']}.")
md.append("- **FSM** — свободное пространство (эталон, без учёта среды).")
md.append("- **UMiNLOS** — городская микросота / помещение → применяем для микро/фемтосот.")
md.append("- **COST 231 Hata** — макросоты → применяем для макросот.")
md.append("\n![Модели в помещении](task3_indoor_models.png)\n")
md.append("![Сравнение моделей](task3_models_comparison.png)\n")

md.append("\n### Задание 4. Радиусы сот, площадь и число БС\n")
md.append("Радиус — пересечение MAPL_UL/MAPL_DL с кривой PL(d); берём меньший из d_UL и d_DL. "
          "Площадь сайта с 3 секторами: S = 1.95·R² (рис. 2.7).\n")
md.append("| Сценарий | Модель | d_DL | d_UL | Радиус R | S сайта | Число БС |")
md.append("|---|---|---|---|---|---|---|")
md.append(f"| Макросоты ({inp['Area_macro']:.0f} км²) | COST 231 Hata | {mac['d_DL_km']} км | "
          f"{mac['d_UL_km']} км | **{mac['R_km']} км** | {mac['S_site_km2']} км² | "
          f"{mac['N_BS_raw']} → **{mac['N_BS']}** |")
md.append(f"| Микро/фемтосоты ({inp['Area_micro']:.0f} км²) | UMiNLOS | {mic['d_DL_m']:.0f} м | "
          f"{mic['d_UL_m']:.0f} м | **{mic['R_m']:.0f} м** | {mic['S_site_km2']} км² | "
          f"{mic['N_BS_raw']} → **{mic['N_BS']}** |")
md.append("\n![Радиус макросоты](task4_radius_macro_cost231.png)\n")
md.append("![Радиус микро/фемтосоты](task4_radius_micro_uminos.png)\n")

md.append("\n## 4. Ответы на контрольные вопросы\n")
for i, (q, a) in enumerate(qa, 1):
    md.append(f"\n**{i}) {q}**\n\n{a}")

md.append("\n## 5. Вывод\n")
md.append(f"Рассчитаны бюджеты каналов: MAPL_UL = {lb['MAPL_UL']:.2f} дБ, MAPL_DL = {lb['MAPL_DL']:.2f} дБ. "
          f"Построены кривые потерь по моделям FSM, UMiNLOS и COST 231 Hata и выбраны соответствующие "
          f"условиям модели. Для макросот радиус соты ограничен восходящим каналом и составляет "
          f"{mac['R_km']} км, что требует ≈{mac['N_BS']} базовых станций на {inp['Area_macro']:.0f} км². "
          f"Для микро/фемтосот радиус {mic['R_m']:.0f} м и ≈{mic['N_BS']} станций на {inp['Area_micro']:.0f} км². "
          f"Во всех случаях покрытие определяет более «слабый» восходящий канал из‑за малой мощности "
          f"терминала пользователя.")

md.append(f"\n---\n**Репозиторий с кодом:** {REPO_URL}\n")
md.append("![QR на репозиторий](qr_repo.png)\n")

with open(os.path.join(HERE, "Отчёт.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("Создан Отчёт.md")

# ---------------------------- HTML (body-only fragment) ----------------------------
def img_block(key, alt):
    if not IMG[key]:
        return f"<p class='warn'>Не найден график: {alt}</p>"
    return f"<figure><img src='{IMG[key]}' alt='{alt}'/><figcaption>{alt}</figcaption></figure>"


def qa_html():
    out = []
    for i, (q, a) in enumerate(qa, 1):
        out.append(f"<li><b>{i}) {q}</b><p>{a}</p></li>")
    return "\n".join(out)


html = f"""
<style>
  .rep {{ max-width: 960px; margin: 0 auto; padding: 24px; font-family: system-ui, "Segoe UI", Roboto, sans-serif;
          color: #1a1a1a; line-height: 1.55; background: #fff; }}
  .rep h1 {{ font-size: 1.7rem; border-bottom: 3px solid #2b6cb0; padding-bottom: 8px; }}
  .rep h2 {{ font-size: 1.3rem; color: #2b6cb0; margin-top: 32px; border-left: 5px solid #2b6cb0; padding-left: 10px; }}
  .rep h3 {{ font-size: 1.1rem; margin-top: 22px; }}
  .rep .meta {{ color: #555; font-size: 0.95rem; }}
  .rep table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 0.92rem; }}
  .rep th, .rep td {{ border: 1px solid #cbd5e0; padding: 7px 10px; text-align: left; }}
  .rep th {{ background: #edf2f7; }}
  .rep tr:nth-child(even) td {{ background: #f7fafc; }}
  .rep code, .rep .mono {{ font-family: ui-monospace, Consolas, monospace; background: #f1f5f9; padding: 1px 5px; border-radius: 4px; }}
  .rep .formula {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; margin: 8px 0;
                   font-family: ui-monospace, Consolas, monospace; overflow-x: auto; }}
  .rep figure {{ margin: 16px 0; text-align: center; }}
  .rep figure img {{ max-width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 8px; }}
  .rep figcaption {{ color: #666; font-size: 0.85rem; margin-top: 6px; }}
  .rep .note {{ background: #fffbea; border: 1px solid #f6e05e; border-radius: 8px; padding: 10px 14px; font-size: 0.9rem; }}
  .rep ol.qa li {{ margin-bottom: 14px; }}
  .rep ol.qa p {{ margin: 4px 0 0; color: #333; }}
  .rep .result {{ background: #ebf8ff; border: 1px solid #90cdf4; border-radius: 8px; padding: 12px 16px; }}
  .rep .qr {{ max-width: 220px; }}
  @media (max-width: 600px) {{ .rep {{ padding: 14px; }} .rep table {{ font-size: 0.8rem; }} }}
</style>
<div class="rep">
  <h1>Практическая работа №2 — Проектирование радиопокрытия мобильных сетей</h1>
  <p class="meta"><b>{STUDENT}</b>, группа {GROUP} · Курс «Основы мобильных сетей» (ОСМС) · СибГУТИ, {YEAR}<br>
  Занятие №2. Модели распространения сигналов. Бюджеты каналов (UL/DL).</p>

  <h2>1. Цель работы</h2>
  <p>Получить представление о проектировании покрытия сетей мобильной связи и научиться рассчитывать
  радиус действия (радиопокрытие) отдельных базовых станций (сот).</p>

  <h2>2. Исходные данные</h2>
  <table>
    <tr><th>Параметр</th><th>Значение</th></tr>
    <tr><td>Мощность передатчика БС / UE</td><td>{inp['TxPowerBS']:.0f} дБм / {inp['TxPowerUE']:.0f} дБм</td></tr>
    <tr><td>Усиление антенны БС (AntGainBS)</td><td>{inp['AntGainBS']:.0f} дБи</td></tr>
    <tr><td>Секторов на БС / антенн MIMO</td><td>{inp['N_sectors']} / {inp['MIMO']} (MIMOGain {inp['MIMOGain']:.0f} дБ)</td></tr>
    <tr><td>Запас проникновение / интерференция</td><td>{inp['PenetrationM']:.0f} дБ / {inp['IM']:.0f} дБ</td></tr>
    <tr><td>Потери фидерного тракта (FeederLoss)</td><td>{inp['FeederLoss']:.1f} дБ</td></tr>
    <tr><td>Частота f</td><td>{inp['f_GHz']} ГГц ({inp['f_MHz']:.0f} МГц)</td></tr>
    <tr><td>Полоса UL / DL (FDD)</td><td>{inp['BW_UL_MHz']:.0f} / {inp['BW_DL_MHz']:.0f} МГц</td></tr>
    <tr><td>Коэффициент шума BS / UE</td><td>{inp['NF_BS']} дБ / {inp['NF_UE']} дБ</td></tr>
    <tr><td>Требуемое SINR DL / UL</td><td>{inp['SINR_DL']:.0f} дБ / {inp['SINR_UL']:.0f} дБ</td></tr>
    <tr><td>Модели</td><td>COST 231 Hata (макро), UMiNLOS (микро/фемто)</td></tr>
    <tr><td>Площадь: макросоты / микро-фемто</td><td>{inp['Area_macro']:.0f} км² / {inp['Area_micro']:.0f} км²</td></tr>
  </table>
  <p class="note"><b>Допущения.</b> Высоты антенн и тип местности для COST 231 Hata в задании не заданы —
  приняты типовые hBS = {inp['hBS']:.0f} м, hms = {inp['hms']} м, местность «{inp['terrain']}» (город).
  FeederLoss для БС «с фидерами» = 2 + 0.4 + 0.5 = {inp['FeederLoss']:.1f} дБ.</p>

  <h2>3. Ход работы</h2>

  <h3>Задание 1 — бюджет восходящего канала (UL) → MAPL_UL</h3>
  <div class="formula">ThermalNoise_UL = {formulas['TN_UL']}</div>
  <div class="formula">RxSensBS = {formulas['RS_BS']}</div>
  <div class="formula">MAPL_UL = {formulas['MAPL_UL']}</div>

  <h3>Задание 2 — бюджет нисходящего канала (DL) → MAPL_DL</h3>
  <div class="formula">ThermalNoise_DL = {formulas['TN_DL']}</div>
  <div class="formula">RxSensUE = {formulas['RS_UE']}</div>
  <div class="formula">MAPL_DL = {formulas['MAPL_DL']}</div>

  <h3>Задание 3 — модели распространения и выбор модели</h3>
  <p>Параметры COST 231 Hata при f = {inp['f_MHz']:.0f} МГц (табл. 2.1): A = {c231['A']}, B = {c231['B']},
  a(hms) = {c231['a_hms']}, Lclutter = {c231['Lclutter']}. Модель <b>UMiNLOS</b> выбрана для микро/фемтосот
  (помещение), <b>COST 231 Hata</b> — для макросот.</p>
  {img_block('indoor', 'Рис. 2.1. Потери в помещении: UMiNLOS против FSM')}
  {img_block('compare', 'Рис. 3. Сравнение моделей FSM / UMiNLOS / COST 231 Hata')}

  <h3>Задание 4 — радиусы сот, площадь сайта и число БС</h3>
  <p>Радиус определяется пересечением MAPL_UL и MAPL_DL с кривой PL(d); для проекта берут меньший.
  Площадь сайта с 3 секторами: S = 1.95·R² (рис. 2.7).</p>
  <table>
    <tr><th>Сценарий</th><th>Модель</th><th>d_DL</th><th>d_UL</th><th>Радиус R</th><th>S сайта</th><th>Число БС</th></tr>
    <tr><td>Макросоты, {inp['Area_macro']:.0f} км²</td><td>COST 231 Hata</td>
        <td>{mac['d_DL_km']} км</td><td>{mac['d_UL_km']} км</td><td><b>{mac['R_km']} км</b></td>
        <td>{mac['S_site_km2']} км²</td><td>{mac['N_BS_raw']} → <b>{mac['N_BS']}</b></td></tr>
    <tr><td>Микро/фемто, {inp['Area_micro']:.0f} км²</td><td>UMiNLOS</td>
        <td>{mic['d_DL_m']:.0f} м</td><td>{mic['d_UL_m']:.0f} м</td><td><b>{mic['R_m']:.0f} м</b></td>
        <td>{mic['S_site_km2']} км²</td><td>{mic['N_BS_raw']} → <b>{mic['N_BS']}</b></td></tr>
  </table>
  {img_block('macro', 'Рис. 2.6/4. Радиус макросоты (COST 231 Hata)')}
  {img_block('micro', 'Рис. 2.6/4. Радиус микро/фемтосоты (UMiNLOS)')}

  <h2>4. Ответы на контрольные вопросы</h2>
  <ol class="qa">
  {qa_html()}
  </ol>

  <h2>5. Вывод</h2>
  <div class="result">
  Рассчитаны бюджеты каналов: <b>MAPL_UL = {lb['MAPL_UL']:.2f} дБ</b>, <b>MAPL_DL = {lb['MAPL_DL']:.2f} дБ</b>.
  Для макросот радиус ограничен восходящим каналом — <b>{mac['R_km']} км</b>, требуется ≈<b>{mac['N_BS']}</b> БС
  на {inp['Area_macro']:.0f} км². Для микро/фемтосот радиус <b>{mic['R_m']:.0f} м</b>, ≈<b>{mic['N_BS']}</b> БС
  на {inp['Area_micro']:.0f} км². Во всех случаях покрытие определяет более «слабый» восходящий канал
  из‑за малой мощности терминала пользователя.
  </div>

  <h2>Репозиторий с кодом</h2>
  <p class="mono">{REPO_URL}</p>
  <figure><img class="qr" src='{IMG['qr']}' alt='QR на репозиторий'/><figcaption>Ссылка на git‑репозиторий</figcaption></figure>
</div>
"""

with open(os.path.join(HERE, "report_body.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Создан report_body.html")
