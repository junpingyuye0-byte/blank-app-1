# -*- coding: utf-8 -*-
"""
化学クイズゲーム
----------------
・4段階の難易度モード（初級／中級／上級／超級）
・各モード多数の問題（合計60問以上）
・連続正解するほど背景がだんだん明るくなる
・使用ライブラリは Python標準の tkinter と random のみ（AI・通信なし）
"""

import tkinter as tk
from tkinter import font as tkfont
import random

# =========================================================
# 問題データ（4段階）
# =========================================================

LEVEL1_QUESTIONS = [
    ("水素の元素記号は？", ["H", "He", "Hg", "N"], "H"),
    ("酸素の元素記号は？", ["O", "Os", "Ox", "On"], "O"),
    ("水の化学式は？", ["H2O", "CO2", "NaCl", "O2"], "H2O"),
    ("二酸化炭素の化学式は？", ["CO2", "CO", "O2", "H2O"], "CO2"),
    ("食塩（塩化ナトリウム）の化学式は？", ["NaCl", "NaOH", "KCl", "CaCl2"], "NaCl"),
    ("ヘリウムの元素記号は？", ["He", "H", "Ne", "Li"], "He"),
    ("炭素の元素記号は？", ["C", "Ca", "Cl", "Co"], "C"),
    ("窒素の元素記号は？", ["N", "Na", "Ne", "Ni"], "N"),
    ("ナトリウムの元素記号は？", ["Na", "N", "Ni", "Ne"], "Na"),
    ("鉄の元素記号は？", ["Fe", "F", "Ir", "Fr"], "Fe"),
    ("金の元素記号は？", ["Au", "Ag", "Al", "Ar"], "Au"),
    ("銀の元素記号は？", ["Ag", "Au", "Al", "As"], "Ag"),
    ("銅の元素記号は？", ["Cu", "Co", "Ca", "Cr"], "Cu"),
    ("カルシウムの元素記号は？", ["Ca", "Cu", "Cl", "C"], "Ca"),
    ("塩素の元素記号は？", ["Cl", "C", "Ca", "Co"], "Cl"),
    ("アルミニウムの元素記号は？", ["Al", "Ar", "Au", "As"], "Al"),
    ("硫黄の元素記号は？", ["S", "Si", "Sn", "Sr"], "S"),
    ("カリウムの元素記号は？", ["K", "Ca", "Kr", "Co"], "K"),
    ("亜鉛の元素記号は？", ["Zn", "Ni", "Sn", "Pb"], "Zn"),
    ("物質を構成する最小単位を何という？", ["原子", "分子", "細胞", "元素記号"], "原子"),
]

LEVEL2_QUESTIONS = [
    ("メタンの化学式は？", ["CH4", "C2H6", "CO2", "NH3"], "CH4"),
    ("アンモニアの化学式は？", ["NH3", "NO2", "N2O", "HN3"], "NH3"),
    ("硫酸の化学式は？", ["H2SO4", "HCl", "HNO3", "H2SO3"], "H2SO4"),
    ("塩酸の主成分は？", ["HCl", "H2SO4", "NaOH", "HNO3"], "HCl"),
    ("水酸化ナトリウムの化学式は？", ["NaOH", "NaCl", "Na2O", "NaHCO3"], "NaOH"),
    ("酸とアルカリが反応することを何という？", ["中和", "酸化", "還元", "電離"], "中和"),
    ("ものが燃える（完全燃焼）と主に発生する気体は？", ["二酸化炭素", "酸素", "水素", "窒素"], "二酸化炭素"),
    ("pHが7のとき溶液は？", ["中性", "酸性", "アルカリ性", "不明"], "中性"),
    ("pHが7より小さいと溶液は？", ["酸性", "アルカリ性", "中性", "中和"], "酸性"),
    ("pHが7より大きいと溶液は？", ["アルカリ性", "酸性", "中性", "中和"], "アルカリ性"),
    ("原子核を構成する粒子は陽子と何？", ["中性子", "電子", "イオン", "分子"], "中性子"),
    ("電子が持つ電荷は？", ["負（マイナス）", "正（プラス）", "電荷なし", "不定"], "負（マイナス）"),
    ("陽子が持つ電荷は？", ["正（プラス）", "負（マイナス）", "電荷なし", "不定"], "正（プラス）"),
    ("原子番号は何の数を表す？", ["陽子の数", "中性子の数", "電子殻の数", "分子の数"], "陽子の数"),
    ("陽子の数が同じで中性子の数が異なる原子どうしを何という？", ["同位体", "同素体", "異性体", "同族体"], "同位体"),
    ("炭素の同素体でないものは？", ["食塩", "ダイヤモンド", "黒鉛", "フラーレン"], "食塩"),
    ("金属が電子を放出してできるイオンを何という？", ["陽イオン", "陰イオン", "中性子", "分子イオン"], "陽イオン"),
    ("塩素原子が電子を受け取ってできるイオンを何という？", ["陰イオン", "陽イオン", "中性子", "同位体"], "陰イオン"),
    ("水溶液に電流が流れる物質を何という？", ["電解質", "非電解質", "触媒", "同位体"], "電解質"),
    ("砂糖水のように電流が流れない物質を何という？", ["非電解質", "電解質", "酸", "塩基"], "非電解質"),
]

LEVEL3_QUESTIONS = [
    ("水の生成反応式は？ 2H2 + O2 →", ["2H2O", "H2O2", "2H2O2", "HO2"], "2H2O"),
    ("物質量（molの単位）が表すものは？", ["粒子の数の集まり", "重さ", "体積", "温度"], "粒子の数の集まり"),
    ("1molに含まれる粒子の数（アボガドロ数）は約？", ["6.02×10の23乗", "3.14×10の8乗", "9.8×10の10乗", "1.0×10の6乗"], "6.02×10の23乗"),
    ("酸素と結びつく化学変化を何という？", ["酸化", "還元", "中和", "電離"], "酸化"),
    ("酸化物から酸素を奪う化学変化を何という？", ["還元", "酸化", "中和", "電離"], "還元"),
    ("塩化ナトリウムの結晶を作る結合は？", ["イオン結合", "共有結合", "金属結合", "水素結合"], "イオン結合"),
    ("水分子（H2O）を作る結合は？", ["共有結合", "イオン結合", "金属結合", "配位結合のみ"], "共有結合"),
    ("周期表で縦の列（同じ族）の元素は性質が？", ["似ている", "全く異なる", "関係ない", "反応しない"], "似ている"),
    ("ヘリウムやネオンなど反応しにくい気体を何という？", ["貴ガス（希ガス）", "ハロゲン", "アルカリ金属", "遷移金属"], "貴ガス（希ガス）"),
    ("化学反応の速さを変えるが自身は変化しない物質は？", ["触媒", "溶媒", "溶質", "指示薬"], "触媒"),
    ("塩酸と水酸化ナトリウム水溶液を混ぜると生じる塩は？", ["塩化ナトリウム", "硫酸ナトリウム", "炭酸ナトリウム", "硝酸ナトリウム"], "塩化ナトリウム"),
    ("酸化銀を加熱すると発生する気体は？", ["酸素", "水素", "二酸化炭素", "窒素"], "酸素"),
    ("塩酸に亜鉛を入れると発生する気体は？", ["水素", "酸素", "二酸化炭素", "塩素"], "水素"),
    ("炭酸水素ナトリウムを加熱すると発生する気体は？", ["二酸化炭素", "酸素", "水素", "アンモニア"], "二酸化炭素"),
    ("BTB溶液が酸性で示す色は？", ["黄色", "青色", "緑色", "赤色"], "黄色"),
]

LEVEL4_QUESTIONS = [
    ("NaOH + HCl → NaCl + ？", ["H2O", "H2", "O2", "Cl2"], "H2O"),
    ("水（H2O）のモル質量は約18g/molである。0.5molの水の質量は？", ["9g", "18g", "36g", "4.5g"], "9g"),
    ("炭酸カルシウムの化学式は？", ["CaCO3", "CaO", "Ca(OH)2", "CaCl2"], "CaCO3"),
    ("硝酸の化学式は？", ["HNO3", "H2SO4", "HCl", "H2CO3"], "HNO3"),
    ("水を電気分解すると陰極（マイナス極）に発生する気体は？", ["水素", "酸素", "窒素", "二酸化炭素"], "水素"),
    ("pH2の溶液はpH5の溶液に比べて水素イオン濃度が？", ["1000倍高い", "1000倍低い", "3倍高い", "同じ"], "1000倍高い"),
    ("気体の状態方程式 PV=？ の右辺は？", ["nRT", "mgh", "F/A", "ρV"], "nRT"),
    ("標準状態（0℃・1気圧）で気体1molが占める体積は？", ["22.4L", "1L", "100L", "18mL"], "22.4L"),
    ("1Lの水にNaClを1mol溶かした水溶液のモル濃度は？", ["1mol/L", "0.5mol/L", "2mol/L", "10mol/L"], "1mol/L"),
    ("単体（例：O2やFeなど）を構成する原子の酸化数は？", ["0", "+1", "-1", "+2"], "0"),
    ("メタン(CH4)が完全燃焼すると生成する物質は？", ["CO2とH2O", "COとH2", "CとH2O", "CO2とH2"], "CO2とH2O"),
    ("エタノールの化学式は？", ["C2H5OH", "CH3OH", "C2H4", "C2H6"], "C2H5OH"),
    ("酢酸の化学式は？", ["CH3COOH", "HCOOH", "C2H5OH", "CH3OH"], "CH3COOH"),
    ("ダニエル電池で使われる2種類の金属は？", ["亜鉛と銅", "鉄と銅", "亜鉛と鉛", "銀と銅"], "亜鉛と銅"),
    ("イオン化傾向が最も大きい金属はどれ？", ["カリウム(K)", "金(Au)", "銀(Ag)", "銅(Cu)"], "カリウム(K)"),
]

LEVELS = {
    1: ("初級", LEVEL1_QUESTIONS, "#dbe9ff"),
    2: ("中級", LEVEL2_QUESTIONS, "#dbffe4"),
    3: ("上級", LEVEL3_QUESTIONS, "#fff3db"),
    4: ("超級", LEVEL4_QUESTIONS, "#ffdbdb"),
}

MAX_STREAK_FOR_BRIGHTNESS = 8  # このくらい連続正解すると最大の明るさになる


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)


def brighten_color(base_hex, streak):
    """連続正解数(streak)に応じて背景色を白に近づけて明るくする"""
    r, g, b = hex_to_rgb(base_hex)
    ratio = min(streak, MAX_STREAK_FOR_BRIGHTNESS) / MAX_STREAK_FOR_BRIGHTNESS
    r = r + (255 - r) * ratio
    g = g + (255 - g) * ratio
    b = b + (255 - b) * ratio
    return rgb_to_hex((r, g, b))


class ChemistryGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("化学クイズゲーム")
        self.geometry("700x520")
        self.resizable(False, False)

        self.title_font = tkfont.Font(size=22, weight="bold")
        self.normal_font = tkfont.Font(size=14)
        self.button_font = tkfont.Font(size=13)
        self.small_font = tkfont.Font(size=11)

        self.level = None
        self.base_color = "#ffffff"
        self.questions = []
        self.q_index = 0
        self.score = 0
        self.streak = 0

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_start_screen()

    # -----------------------------------------------------
    # 画面：スタート（レベル選択）
    # -----------------------------------------------------
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.configure(bg="#ffffff")
        self.container.configure(bg="#ffffff")
        self.clear_container()

        tk.Label(
            self.container, text="化学クイズゲーム",
            font=self.title_font, bg="#ffffff"
        ).pack(pady=(40, 10))

        tk.Label(
            self.container,
            text="モードを選んでください\n連続正解すると背景がどんどん明るくなります！",
            font=self.normal_font, bg="#ffffff", justify="center"
        ).pack(pady=(0, 30))

        for level_num, (name, questions, color) in LEVELS.items():
            btn = tk.Button(
                self.container,
                text=f"{level_num}. {name}　（全{len(questions)}問）",
                font=self.button_font,
                width=30, height=2,
                bg=color,
                activebackground=color,
                command=lambda n=level_num: self.start_level(n)
            )
            btn.pack(pady=6)

    # -----------------------------------------------------
    # ゲーム開始
    # -----------------------------------------------------
    def start_level(self, level_num):
        self.level = level_num
        name, questions, color = LEVELS[level_num]
        self.base_color = color
        self.questions = questions[:]
        random.shuffle(self.questions)

        self.q_index = 0
        self.score = 0
        self.streak = 0

        self.update_background()
        self.show_question_screen()

    def update_background(self):
        color = brighten_color(self.base_color, self.streak)
        self.configure(bg=color)
        self.container.configure(bg=color)

    # -----------------------------------------------------
    # 画面：問題
    # -----------------------------------------------------
    def show_question_screen(self):
        self.clear_container()

        if self.q_index >= len(self.questions):
            self.show_result_screen()
            return

        question, choices, answer = self.questions[self.q_index]
        bg = self.container["bg"]

        name, _, _ = LEVELS[self.level]
        header = tk.Label(
            self.container,
            text=f"【{name}】 第{self.q_index + 1}問 / 全{len(self.questions)}問"
                 f"　　得点: {self.score}　　連続正解: {self.streak}",
            font=self.small_font, bg=bg
        )
        header.pack(pady=(20, 10))

        q_label = tk.Label(
            self.container, text=question, font=self.normal_font,
            bg=bg, wraplength=600, justify="center"
        )
        q_label.pack(pady=(10, 30))

        shuffled_choices = choices[:]
        random.shuffle(shuffled_choices)

        self.feedback_label = tk.Label(
            self.container, text="", font=self.normal_font, bg=bg
        )
        self.feedback_label.pack(pady=(0, 10))

        btn_frame = tk.Frame(self.container, bg=bg)
        btn_frame.pack()

        self.choice_buttons = []
        for choice in shuffled_choices:
            btn = tk.Button(
                btn_frame, text=choice, font=self.button_font,
                width=25, height=2,
                command=lambda c=choice, a=answer: self.check_answer(c, a)
            )
            btn.pack(pady=5)
            self.choice_buttons.append(btn)

    def check_answer(self, chosen, answer):
        for btn in self.choice_buttons:
            btn.config(state="disabled")

        if chosen == answer:
            self.score += 1
            self.streak += 1
            self.feedback_label.config(text="○ 正解！", fg="#0a8a2f")
        else:
            self.streak = 0
            self.feedback_label.config(
                text=f"× 不正解…　正解は「{answer}」", fg="#c0392b"
            )

        self.update_background()
        self.container.configure(bg=self.container["bg"])
        self.feedback_label.configure(bg=self.container["bg"])

        # 少し待ってから次の問題へ
        self.after(900, self.next_question)

    def next_question(self):
        self.q_index += 1
        self.show_question_screen()

    # -----------------------------------------------------
    # 画面：結果
    # -----------------------------------------------------
    def show_result_screen(self):
        self.clear_container()
        bg = self.container["bg"]
        name, _, _ = LEVELS[self.level]

        tk.Label(
            self.container, text="結果発表",
            font=self.title_font, bg=bg
        ).pack(pady=(50, 20))

        total = len(self.questions)
        rate = 0 if total == 0 else round(self.score / total * 100)

        tk.Label(
            self.container,
            text=f"モード：{name}\n得点：{self.score} / {total}　（正答率 {rate}%）",
            font=self.normal_font, bg=bg, justify="center"
        ).pack(pady=(0, 30))

        tk.Button(
            self.container, text="もう一度このモードで挑戦",
            font=self.button_font, width=28, height=2,
            command=lambda: self.start_level(self.level)
        ).pack(pady=8)

        tk.Button(
            self.container, text="モード選択に戻る",
            font=self.button_font, width=28, height=2,
            command=self.show_start_screen
        ).pack(pady=8)


if __name__ == "__main__":
    app = ChemistryGame()
    app.mainloop()