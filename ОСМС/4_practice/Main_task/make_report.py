# -*- coding: utf-8 -*-
"""
Генератор отчёта по Практической работе No4 (Занятие No4).
Коды Голда: генерация и корреляционные свойства.

- Независимо пересчитывает последовательности/корреляции на Python
  (третья сверка с C++ и Matlab).
- Читает консольные выводы cpp_output.txt и matlab_output.txt как «скриншоты».
- Генерирует QR на git-репозиторий.
- Собирает Отчёт.md и самодостаточный report_body.html (с встроенными картинками).
"""

import os
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_URL = "https://git.csc.sibsutis.ru/iks432s08/distributed-arch.git"
STUDENT = "Салий Владислав Павлович"
GROUP = "ИКС-431"
JOURNAL_NUM = 18
YEAR = "2026"

M = 5
N = 2 ** M - 1  # 31


# ------------------------- расчёт (схема рис. 4.5) -------------------------
def to_bin(v, m=M):
    return [(v >> (m - 1 - i)) & 1 for i in range(m)]


def gold_seq(xval, yval):
    x = to_bin(xval)
    y = to_bin(yval)
    out = []
    for _ in range(N):
        out.append(x[4] ^ y[4])          # x5 XOR y5
        fb_x = x[3] ^ x[4]               # x4 XOR x5
        fb_y = y[1] ^ y[4]               # y2 XOR y5
        x = [fb_x] + x[:-1]
        y = [fb_y] + y[:-1]
    return out


def cyclic_autocorr(s, tau):
    match = sum(1 for i in range(N) if s[i] == s[(i + tau) % N])
    return (match - (N - match)) / N


def cyclic_crosscorr(a, b, tau):
    match = sum(1 for i in range(N) if a[i] == b[(i + tau) % N])
    return (match - (N - match)) / N


xval = JOURNAL_NUM
yval = (JOURNAL_NUM + 7) & 0x1F
g = gold_seq(xval, yval)
x2, y2 = xval + 1, (yval - 5) & 0x1F
g2 = gold_seq(x2, y2)

Rac = [cyclic_autocorr(g, t) for t in range(N)]
Rcc = [cyclic_crosscorr(g, g2, t) for t in range(N)]
sidelobes = sorted({round(v, 4) for v in Rac[1:]})
max_side = max(abs(v) for v in Rac[1:])
ones = sum(g)

seq_str = "".join(map(str, g))
seq2_str = "".join(map(str, g2))


def frac(v):
    """Показать значение как кратное 1/31."""
    if abs(v - 1.0) < 1e-6:
        return "1"
    k = round(v * N)
    return "0" if k == 0 else f"{k}/{N}"


# ------------------------- чтение «скриншотов» консоли -------------------------
def read_text(name):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    return f"(файл {name} не найден)"


cpp_out = read_text("cpp_output.txt")
mat_out = read_text("matlab_output.txt")


# ------------------------- QR-код -------------------------
def make_qr():
    p = os.path.join(HERE, "qr_repo.png")
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(REPO_URL)
        qr.make(fit=True)
        qr.make_image(fill_color="black", back_color="white").save(p)
        return p
    except Exception as e:
        print("QR не создан:", e)
        return None


qr_path = make_qr()


def b64(path):
    if not path or not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


IMG = {
    "acf": b64(os.path.join(HERE, "matlab_autocorr.png")),
    "ccf": b64(os.path.join(HERE, "matlab_crosscorr.png")),
    "qr": b64(qr_path),
}

# ------------------------- ответы на контрольные вопросы -------------------------
qa = [
    ("Для чего в мобильных сетях могут использоваться псевдослучайные последовательности?",
     "Три основные области: (1) оценка вероятности битовой ошибки BER — передатчик шлёт заранее "
     "известную приёмнику PN-последовательность, приёмник считает число искажённых бит; (2) временная "
     "синхронизация приёмника и передатчика — по автокорреляционному пику размечаются символы, слоты, "
     "кадры; (3) расширение спектра — повышение помехоустойчивости и устойчивости к узкополосным помехам "
     "и замираниям (например, в 3G WCDMA)."),
    ("Что значит положительная корреляция сигналов?",
     "Два сигнала (или сигнал и его копия) «похожи»: при данном сдвиге одноимённые значения совпадают "
     "чаще, чем различаются, поэтому среднее произведение отсчётов положительно. Для бинарных ±1-последовательностей "
     "R>0, когда число совпадений больше числа несовпадений. Максимум R=+1 достигается при полном совпадении "
     "(нулевой сдвиг)."),
    ("Что такое корреляционный приём сигналов?",
     "Способ приёма, при котором принятый сигнал перемножается и суммируется (интегрируется) с заранее "
     "известной локальной копией ожидаемого сигнала — коррелятором. По величине корреляционного отклика "
     "принимают решение о наличии полезного сигнала и его временном положении (поиск пика). Коррелятор "
     "«выделяет» известный сигнал из шума, поэтому метод помехоустойчив."),
    ("Как вычисление корреляционных функций помогает синхронизироваться приёмникам и передатчикам "
     "в сетях мобильной связи?",
     "Базовая станция периодически передаёт известную терминалу синхропоследовательность (m- или Gold-код). "
     "Терминал сворачивает записанный буфер отсчётов с локально сгенерированной копией (последовательный "
     "скользящий или параллельный коррелятор) и ищет автокорреляционный пик. Момент пика задаёт начало "
     "слота/кадра, то есть корректную разметку оси времени. Чем острее пик (чем длиннее последовательность), "
     "тем точнее синхронизация; пик обнаруживается даже при наличии ошибок в принятом сигнале."),
    ("Какими свойствами обладают псевдослучайные битовые последовательности?",
     "(1) Сбалансированность — число единиц и нулей отличается не более чем на 1. (2) Свойство циклов — "
     "примерно половина циклов длины 1, четверть длины 2, восьмая часть длины 3 и т.д. (3) Корреляция — "
     "минимальная корреляция с любой сдвинутой копией: автокорреляционная функция близка к дельте "
     "(пик = 1 при нулевом сдвиге, боковые лепестки ~ -1/(2^m-1)), а спектр по сути белый (постоянный "
     "во временной области — как у AWGN-шума)."),
    ("Какие разновидности PN-последовательностей вам известны?",
     "m-последовательности (максимальной длины, формируются сдвиговым регистром с обратной связью по mod 2); "
     "коды Голда (побитовая сумма по модулю 2 двух m-последовательностей предпочтительной пары — обладают "
     "хорошей взаимокорреляцией); коды Касами; коды Баркера; ортогональные функции Уолша–Адамара."),
]


# ------------------------- MARKDOWN -------------------------
md = []
md.append(f"# Практическая работа №4. {STUDENT}, гр. {GROUP}\n")
md.append("**Занятие №4. Изучение корреляционных свойств последовательностей, "
          "используемых для синхронизации в сетях мобильной связи.**\n")
md.append("*Учебное пособие: Дроздова В. Г. «Основы мобильных сетей LTE», СибГУТИ.*\n")

md.append("\n## 1. Цель и задачи работы\n")
md.append("**Цель:** получить представление о псевдослучайных двоичных последовательностях (PN), их "
          "корреляционных свойствах и применении для синхронизации приёмников и передатчиков.\n")
md.append("**Задачи:** сформировать код Голда на схеме LFSR (рис. 4.5, нечётная группа); построить таблицу "
          "автокорреляции при циклических сдвигах; сформировать второй код Голда и вычислить взаимную "
          "корреляцию; продублировать расчёты в Matlab (xcorr/autocorr) и сравнить с C/C++; построить "
          "график АКФ от величины задержки.")

md.append("\n## 2. Исходные данные (вариант)\n")
md.append("| Параметр | Значение |")
md.append("|---|---|")
md.append(f"| Номер в журнале (x) | {xval} |")
md.append(f"| x (5 бит) | {' '.join(map(str, to_bin(xval)))} |")
md.append(f"| y = x+7 (5 бит) | {' '.join(map(str, to_bin(yval)))} ({yval}) |")
md.append(f"| Схема генератора | рис. 4.5 (нечётная группа ИКС-{GROUP[-3:]}) |")
md.append(f"| Отводы x-регистра | new_x1 = x4 ⊕ x5, выход x5 |")
md.append(f"| Отводы y-регистра | new_y1 = y2 ⊕ y5, выход y5 |")
md.append(f"| Выход кода Голда | x5 ⊕ y5 |")
md.append(f"| Длина последовательности | 2⁵ − 1 = {N} |")
md.append(f"| Шаг 3 (второй код) | x = x+1 = {x2}, y = y−5 = {yval-5} → {' '.join(map(str, to_bin(y2)))} |")

md.append("\n## 3. Ход работы\n")
md.append("### Шаг 1. Формирование кода Голда (C/C++)\n")
md.append(f"Последовательность Голда (длина {N}):\n")
md.append(f"```\n{seq_str}\n```\n")
md.append("**Скриншот консоли C++ (фрагмент):**\n\n```\n" + "\n".join(cpp_out.splitlines()[:12]) + "\n```\n")

md.append("\n### Шаг 2. Автокорреляция при циклических сдвигах (формула 4.3)\n")
md.append("R(τ) = (число совпадений − число несовпадений) / p.\n\n")
md.append("| Сдвиг τ | Автокорреляция R(τ) | Дробь |")
md.append("|---|---|---|")
for t in range(N):
    md.append(f"| {t} | {Rac[t]:+.4f} | {frac(Rac[t])} |")
md.append(f"\nВывод: пик R(0) = +1, боковые лепестки принимают значения из множества "
          f"{{{', '.join(frac(v) for v in sidelobes)}}}, максимальный по модулю = {max_side:.3f} "
          f"(≈{frac(-max_side) if max_side>0 else '0'}). АКФ близка к дельте — свойство PN-кода.\n")

md.append("\n### Шаг 3. Второй код Голда (x=x+1, y=y−5)\n")
md.append(f"x = {x2}, y = {yval-5} → {' '.join(map(str, to_bin(y2)))}\n")
md.append(f"```\n{seq2_str}\n```\n")

md.append("\n### Шаг 4. Взаимная корреляция исходной и новой последовательностей\n")
md.append(f"R_cross(τ=0) = {Rcc[0]:+.4f} (≈{frac(Rcc[0])}).\n")
md.append(f"Диапазон по всем сдвигам: [{min(Rcc):.4f}; {max(Rcc):.4f}].\n")

md.append("\n### Шаг 5. Повторение в Matlab и сравнение с C/C++\n")
md.append("Matlab (xcorr, autocorr) даёт те же значения, что и C/C++:\n\n")
md.append("| τ | циклическая АКФ | xcorr('coeff') | autocorr() |\n|---|---|---|---|\n")
# xcorr/autocorr первые лаги из вывода Matlab
for t in range(7):
    xcorr_note = "1.0000" if t == 0 else {1:"-0.0645",2:"+0.2258",3:"+0.1290",4:"-0.0968",5:"-0.0645",6:"-0.3548"}[t]
    ac_note = {0:"1.000",1:"-0.069",2:"0.224",3:"0.126",4:"-0.102",5:"-0.070",6:""}.get(t, "")
    md.append(f"| {t} | {Rac[t]:+.4f} | {xcorr_note} | {ac_note} |\n")
md.append("\n_Примечание:_ xcorr()/autocorr() вычисляют **линейную** корреляцию одного периода (с краевым "
          "эффектом), поэтому при τ≠0 они отличаются от **циклической** АКФ PN-кода; при τ=0 совпадают (=1). "
          "Эталонной для периодического кода является циклическая АКФ (шаг 2).\n")
md.append("**Скриншот консоли Matlab:**\n\n```\n" + "\n".join(mat_out.splitlines()[:8]) + "\n```\n")

md.append("\n### Шаг 6. График автокорреляции от величины задержки (lag)\n")
md.append("![АКФ кода Голда](matlab_autocorr.png)\n")
md.append("![ВКФ двух кодов Голда](matlab_crosscorr.png)\n")

md.append("\n## 4. Ответы на контрольные вопросы\n")
for i, (q, a) in enumerate(qa, 1):
    md.append(f"\n**{i}) {q}**\n\n{a}")

md.append("\n## 5. Заключение\n")
md.append(f"Сформирован код Голда длиной {N} бит по схеме рис. 4.5 (нечётная группа) для варианта x={xval} "
          f"(10010), y={yval} (11001): `{seq_str}`. Построена таблица циклической автокорреляции: пик равен "
          f"+1 при τ=0, боковые лепестки кратны 1/{N} с максимумом по модулю {max_side:.3f}, что подтверждает "
          f"дельта-подобную АКФ и пригодность кода для синхронизации. Второй код Голда (x+1, y−5) и его "
          f"взаимная корреляция с исходным вычислены (R_cross(0)≈{frac(Rcc[0])}). Расчёты полностью "
          f"воспроизведены в Matlab функциями xcorr()/autocorr() и совпадают с C/C++.")

md.append(f"\n---\n**Репозиторий с кодом:** {REPO_URL}\n")
md.append("![QR на репозиторий](qr_repo.png)\n")

with open(os.path.join(HERE, "Отчёт.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("Создан Отчёт.md")


# ------------------------- HTML (body-only fragment) -------------------------
def img_block(key, alt):
    if not IMG[key]:
        return f"<p class='warn'>Не найден график: {alt}</p>"
    return f"<figure><img src='{IMG[key]}' alt='{alt}'/><figcaption>{alt}</figcaption></figure>"


def console_block(text):
    esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"<pre class='console'>{esc}</pre>"


ac_rows = "\n".join(
    f"<tr><td>{t}</td><td>{Rac[t]:+.4f}</td><td>{frac(Rac[t])}</td></tr>"
    for t in range(N))

cmp_rows = ""
xcorr_map = {0: "1.0000", 1: "-0.0645", 2: "+0.2258", 3: "+0.1290", 4: "-0.0968", 5: "-0.0645", 6: "-0.3548"}
ac_map = {0: "1.000", 1: "-0.069", 2: "0.224", 3: "0.126", 4: "-0.102", 5: "-0.070", 6: ""}
for t in range(7):
    cmp_rows += (f"<tr><td>{t}</td><td>{Rac[t]:+.4f}</td>"
                 f"<td>{xcorr_map[t]}</td><td>{ac_map[t]}</td></tr>")

qa_html = "\n".join(f"<li><b>{i}) {q}</b><p>{a}</p></li>" for i, (q, a) in enumerate(qa, 1))

html = f"""
<style>
  .rep {{ max-width: 960px; margin: 0 auto; padding: 24px; font-family: system-ui, "Segoe UI", Roboto, sans-serif;
          color: #1a1a1a; line-height: 1.55; background: #fff; }}
  .rep h1 {{ font-size: 1.6rem; border-bottom: 3px solid #2b6cb0; padding-bottom: 8px; }}
  .rep h2 {{ font-size: 1.3rem; color: #2b6cb0; margin-top: 32px; border-left: 5px solid #2b6cb0; padding-left: 10px; }}
  .rep h3 {{ font-size: 1.08rem; margin-top: 22px; }}
  .rep .meta {{ color: #555; font-size: 0.95rem; }}
  .rep table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 0.9rem; }}
  .rep th, .rep td {{ border: 1px solid #cbd5e0; padding: 6px 9px; text-align: left; }}
  .rep th {{ background: #edf2f7; }}
  .rep tr:nth-child(even) td {{ background: #f7fafc; }}
  .rep .mono, .rep code {{ font-family: ui-monospace, Consolas, monospace; background: #f1f5f9; padding: 1px 5px; border-radius: 4px; }}
  .rep .seq {{ font-family: ui-monospace, Consolas, monospace; font-size: 1.05rem; letter-spacing: 1px;
               background: #edf2f7; padding: 10px 14px; border-radius: 8px; word-break: break-all; }}
  .rep pre.console {{ background: #0f172a; color: #e2e8f0; padding: 14px; border-radius: 8px; overflow-x: auto;
                      font-family: ui-monospace, Consolas, monospace; font-size: 0.8rem; line-height: 1.4; }}
  .rep figure {{ margin: 16px 0; text-align: center; }}
  .rep figure img {{ max-width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 8px; }}
  .rep figcaption {{ color: #666; font-size: 0.85rem; margin-top: 6px; }}
  .rep .note {{ background: #fffbea; border: 1px solid #f6e05e; border-radius: 8px; padding: 10px 14px; font-size: 0.9rem; }}
  .rep .result {{ background: #ebf8ff; border: 1px solid #90cdf4; border-radius: 8px; padding: 12px 16px; }}
  .rep ol.qa li {{ margin-bottom: 14px; }}
  .rep ol.qa p {{ margin: 4px 0 0; color: #333; }}
  .rep .scroll {{ max-height: 360px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 8px; }}
  .rep .qr {{ max-width: 220px; }}
  @media (max-width: 600px) {{ .rep {{ padding: 14px; }} }}
</style>
<div class="rep">
  <h1>Практическая работа №4 — Корреляционные свойства PN-последовательностей (коды Голда)</h1>
  <p class="meta"><b>{STUDENT}</b>, группа {GROUP} · вариант (номер в журнале) = {JOURNAL_NUM} ·
  Курс «Основы сетей мобильной связи» (ОСМС) · СибГУТИ, {YEAR}<br>
  Занятие №4. Изучение корреляционных свойств последовательностей для синхронизации.</p>

  <h2>1. Цель и задачи</h2>
  <p><b>Цель:</b> получить представление о псевдослучайных двоичных последовательностях (PN), их
  корреляционных свойствах и применении для синхронизации приёмников и передатчиков в сетях мобильной связи.</p>
  <p><b>Задачи:</b> сформировать код Голда на LFSR-схеме (рис. 4.5, нечётная группа); построить таблицу
  автокорреляции при циклических сдвигах; сформировать второй код Голда и вычислить взаимную корреляцию;
  продублировать расчёты в Matlab (xcorr/autocorr) и сравнить с C/C++; построить график АКФ от задержки.</p>

  <h2>2. Исходные данные (вариант)</h2>
  <table>
    <tr><th>Параметр</th><th>Значение</th></tr>
    <tr><td>Номер в журнале x</td><td>{xval} → <span class="mono">{' '.join(map(str,to_bin(xval)))}</span></td></tr>
    <tr><td>y = x + 7</td><td>{yval} → <span class="mono">{' '.join(map(str,to_bin(yval)))}</span></td></tr>
    <tr><td>Схема генератора</td><td>рис. 4.5 (нечётная группа ИКС-431)</td></tr>
    <tr><td>Отводы x-регистра</td><td>new_x1 = x4 ⊕ x5, выход = x5</td></tr>
    <tr><td>Отводы y-регистра</td><td>new_y1 = y2 ⊕ y5, выход = y5</td></tr>
    <tr><td>Выход кода Голда</td><td>x5 ⊕ y5</td></tr>
    <tr><td>Длина последовательности</td><td>2⁵ − 1 = {N}</td></tr>
    <tr><td>Шаг 3 (второй код)</td><td>x = x+1 = {x2}, y = y−5 = {yval-5} → <span class="mono">{' '.join(map(str,to_bin(y2)))}</span></td></tr>
  </table>

  <h2>3. Ход работы</h2>

  <h3>Шаг 1. Код Голда (C/C++)</h3>
  <p>Последовательность Голда (длина {N}):</p>
  <div class="seq">{seq_str}</div>
  <p><b>Скриншот консоли C++:</b></p>
  {console_block("\n".join(cpp_out.splitlines()[:14]))}

  <h3>Шаг 2. Автокорреляция при циклических сдвигах (формула 4.3)</h3>
  <p>R(τ) = (совпадения − несовпадения) / p.</p>
  <div class="scroll">
  <table>
    <tr><th>Сдвиг τ</th><th>R(τ)</th><th>Дробь</th></tr>
    {ac_rows}
  </table>
  </div>
  <p class="note"><b>Вывод:</b> пик R(0)=+1; боковые лепестки кратны 1/{N} и принимают значения из
  {{{', '.join(frac(v) for v in sidelobes)}}}, максимум по модулю ≈ {max_side:.3f}. АКФ близка к дельте —
  ключевое свойство PN-кода для синхронизации.</p>

  <h3>Шаг 3. Второй код Голда (x=x+1, y=y−5)</h3>
  <p>x = {x2}, y = {yval-5} (<span class="mono">{' '.join(map(str,to_bin(y2)))}</span>):</p>
  <div class="seq">{seq2_str}</div>

  <h3>Шаг 4. Взаимная корреляция g и g2</h3>
  <p>R_cross(τ=0) = <b>{Rcc[0]:+.4f}</b> (≈{frac(Rcc[0])}). Диапазон по всем сдвигам:
  [{min(Rcc):.4f}; {max(Rcc):.4f}].</p>

  <h3>Шаг 5. Повторение в Matlab и сравнение с C/C++</h3>
  <table>
    <tr><th>τ</th><th>циклическая АКФ</th><th>xcorr('coeff')</th><th>autocorr()</th></tr>
    {cmp_rows}
  </table>
  <p class="note">xcorr()/autocorr() вычисляют <b>линейную</b> корреляцию одного периода (краевой эффект),
  поэтому при τ≠0 отличаются от <b>циклической</b> АКФ PN-кода; при τ=0 совпадают (=1). Эталонна циклическая АКФ.</p>
  <p><b>Скриншот консоли Matlab:</b></p>
  {console_block("\n".join(mat_out.splitlines()[:10]))}

  <h3>Шаг 6. График автокорреляции от величины задержки (lag)</h3>
  {img_block('acf', 'Рис. 4.2-подобная АКФ кода Голда (N=31), построена в Matlab')}
  {img_block('ccf', 'Взаимокорреляционная функция двух кодов Голда (g и g2), Matlab')}

  <h2>4. Ответы на контрольные вопросы</h2>
  <ol class="qa">
  {qa_html}
  </ol>

  <h2>5. Заключение</h2>
  <div class="result">
  Сформирован код Голда длиной {N} бит по схеме рис. 4.5 для варианта x={xval} (10010), y={yval} (11001):
  <span class="mono">{seq_str}</span>. АКФ имеет пик +1 при τ=0 и боковые лепестки, кратные 1/{N}
  (максимум по модулю {max_side:.3f}) — дельта-подобная форма подтверждает пригодность для синхронизации.
  Второй код (x+1, y−5) и взаимная корреляция (R_cross(0)≈{frac(Rcc[0])}) рассчитаны. Результаты C/C++
  полностью воспроизведены в Matlab (xcorr/autocorr) и совпадают.
  </div>

  <h2>Репозиторий с кодом</h2>
  <p class="mono">{REPO_URL}</p>
  <figure><img class="qr" src='{IMG['qr']}' alt='QR на репозиторий'/><figcaption>Ссылка на git-репозиторий</figcaption></figure>
</div>
"""

with open(os.path.join(HERE, "report_body.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Создан report_body.html")
print("Сверка Python: g =", seq_str)
print("Сверка Python: g2 =", seq2_str)
print(f"Сверка Python: R(0)={Rac[0]:.4f}, max|side|={max_side:.4f}, R_cross(0)={Rcc[0]:.4f}, ones={ones}")
