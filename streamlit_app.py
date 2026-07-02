# -*- coding: utf-8 -*-
"""
化学クイズゲーム（コイン・アイテム対応版）
--------------------------------------------
・4段階の難易度モード（初級／中級／上級／超級）
・各モードたくさんの問題（合計110問）
・連続正解するほど背景がだんだん明るくなる
・正解するとコインがたまり、ショップでアイテムが買える
    - ヒント：はずれの選択肢を2つ消す
    - スキップ：この問題を飛ばす
    - シールド：1回だけ不正解を無効にして連続正解を守る
・コインとアイテムはファイルに保存され、次回起動時も引き継がれる
・使用ライブラリは Python標準の tkinter / random / json / os のみ
  （AI・ネット通信は一切なし）
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import json
import os

# =========================================================
# 問題データ（4段階・合計110問）
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
    ("リチウムの元素記号は？", ["Li", "La", "Lr", "Lv"], "Li"),
    ("マグネシウムの元素記号は？", ["Mg", "Mn", "Mo", "Md"], "Mg"),
    ("フッ素の元素記号は？", ["F", "Fe", "Fr", "Fm"], "F"),
    ("ネオンの元素記号は？", ["Ne", "N", "Na", "Ni"], "Ne"),
    ("臭素の元素記号は？", ["Br", "B", "Ba", "Bi"], "Br"),
    ("ヨウ素の元素記号は？", ["I", "In", "Ir", "Y"], "I"),
    ("ケイ素の元素記号は？", ["Si", "S", "Se", "Sn"], "Si"),
    ("リンの元素記号は？", ["P", "Pb", "Pt", "Po"], "P"),
    ("鉛の元素記号は？", ["Pb", "P", "Pt", "Po"], "Pb"),
    ("水銀の元素記号は？", ["Hg", "H", "He", "Ho"], "Hg"),
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
    ("過酸化水素の化学式は？", ["H2O2", "H2O", "HO2", "H3O2"], "H2O2"),
    ("二酸化硫黄の化学式は？", ["SO2", "SO3", "S2O", "H2SO3"], "SO2"),
    ("一酸化炭素の化学式は？", ["CO", "CO2", "C2O", "COOH"], "CO"),
    ("塩化水素が水に溶けたものを何という？", ["塩酸", "硫酸", "硝酸", "炭酸"], "塩酸"),
    ("酸化カルシウムの別名は？", ["生石灰", "消石灰", "石灰水", "炭酸カルシウム"], "生石灰"),
    ("水酸化カルシウムの別名は？", ["消石灰", "生石灰", "石灰石", "セッコウ"], "消石灰"),
    ("石灰水に二酸化炭素を通すとどうなる？", ["白く濁る", "赤くなる", "透明になる", "気体が消える"], "白く濁る"),
    ("金属が酸に溶けるとき多くの場合発生する気体は？", ["水素", "酸素", "窒素", "二酸化炭素"], "水素"),
    ("燃焼に必ず必要な気体は？", ["酸素", "窒素", "水素", "二酸化炭素"], "酸素"),
    ("空気中で体積の割合が最も多い気体は？", ["窒素", "酸素", "二酸化炭素", "アルゴン"], "窒素"),
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
    ("二酸化炭素の分子の形は？", ["直線形", "折れ線形", "三角形", "正四面体形"], "直線形"),
    ("メタン分子の形は？", ["正四面体形", "直線形", "折れ線形", "平面三角形"], "正四面体形"),
    ("イオン結晶の一般的な特徴は？", ["硬くてもろい", "やわらかくて伸びる", "電気を通しやすい液体状", "気体になりやすい"], "硬くてもろい"),
    ("金属特有の光沢や展延性のもとになる結合は？", ["金属結合", "イオン結合", "共有結合", "水素結合"], "金属結合"),
    ("電子親和力が大きい元素ほど？", ["陰イオンになりやすい", "陽イオンになりやすい", "反応しにくい", "金属になりやすい"], "陰イオンになりやすい"),
    ("イオン化エネルギーが小さい元素ほど？", ["陽イオンになりやすい", "陰イオンになりやすい", "反応しにくい", "非金属になりやすい"], "陽イオンになりやすい"),
    ("ハロゲンに分類される元素は？", ["塩素", "ナトリウム", "鉄", "ヘリウム"], "塩素"),
    ("アルカリ金属に分類される元素は？", ["ナトリウム", "塩素", "ヘリウム", "鉄"], "ナトリウム"),
    ("遷移元素に分類される元素は？", ["鉄", "ナトリウム", "塩素", "ヘリウム"], "鉄"),
    ("化学反応式の係数は何を表す？", ["物質の粒子（分子・イオン）の数の比", "反応にかかる時間", "物質の色", "反応の温度"], "物質の粒子（分子・イオン）の数の比"),
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
    ("質量パーセント濃度10%の食塩水100gに含まれる食塩は？", ["10g", "1g", "100g", "90g"], "10g"),
    ("0.1mol/Lの塩酸100mLに含まれるHClの物質量は？", ["0.01mol", "0.1mol", "1mol", "0.001mol"], "0.01mol"),
    ("中和滴定で使われる指示薬の一つは？", ["フェノールフタレイン", "リトマス紙のみ", "塩化コバルト紙", "でんぷん"], "フェノールフタレイン"),
    ("強酸と強塩基がちょうど中和すると生じる塩の水溶液は？", ["中性", "酸性", "アルカリ性", "不安定"], "中性"),
    ("平衡が移動する向きに関する原理を何という？", ["ルシャトリエの原理", "アボガドロの法則", "ボイルの法則", "質量保存の法則"], "ルシャトリエの原理"),
    ("反応が進むときに熱を放出する反応を何という？", ["発熱反応", "吸熱反応", "中和反応", "電離反応"], "発熱反応"),
    ("反応が進むときに熱を吸収する反応を何という？", ["吸熱反応", "発熱反応", "酸化反応", "還元反応"], "吸熱反応"),
    ("電池の負極で一般に起こる反応は？", ["酸化", "還元", "中和", "電離"], "酸化"),
    ("電池の正極で一般に起こる反応は？", ["還元", "酸化", "中和", "電離"], "還元"),
    ("炭素骨格が環状になっている有機化合物を何という？", ["環式化合物", "鎖式化合物", "無機化合物", "高分子化合物"], "環式化合物"),
]

LEVELS = {
    1: ("初級", LEVEL1_QUESTIONS, "#dbe9ff"),
    2: ("中級", LEVEL2_QUESTIONS, "#dbffe4"),
    3: ("上級", LEVEL3_QUESTIONS, "#fff3db"),
    4: ("超級", LEVEL4_QUESTIONS, "#ffdbdb"),
}

MAX_STREAK_FOR_BRIGHTNESS = 8  # このくらい連続正解すると最大の明るさになる

# =========================================================
# アイテム定義
# =========================================================
ITEMS = {
    "hint":   {"name": "ヒント（２択に絞る）", "cost": 8,  "desc": "はずれの選択肢を2つ消します"},
    "skip":   {"name": "スキップ",             "cost": 12, "desc": "この問題を飛ばします（コインは増えません）"},
    "shield": {"name": "シールド",             "cost": 15, "desc": "1回だけ不正解を無効にして連続正解を守ります"},
}

SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chemistry_save.json")


def load_save():
    default = {"coins": 0, "inventory": {"hint": 0, "skip": 0, "shield": 0}}
    if os.path.exists(SAVE_PATH):
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            default["coins"] = int(data.get("coins", 0))
            inv = data.get("inventory", {})
            for k in default["inventory"]:
                default["inventory"][k] = int(inv.get(k, 0))
        except Exception:
            pass
    return default


def write_save(coins, inventory):
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump({"coins": coins, "inventory": inventory}, f, ensure_ascii=False)
    except Exception:
        pass


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


def coins_for_streak(streak):
    """連続正解数に応じたコイン獲得量（連続するほどボーナスが増える）"""
    base = 2
    bonus = min(streak // 3, 5)
    return base + bonus


class ChemistryGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("化学クイズゲーム")
        self.geometry("720x580")
        self.resizable(False, False)

        self.title_font = tkfont.Font(size=22, weight="bold")
        self.normal_font = tkfont.Font(size=14)
        self.button_font = tkfont.Font(size=13)
        self.small_font = tkfont.Font(size=11)
        self.coin_font = tkfont.Font(size=12, weight="bold")

        save = load_save()
        self.coins = save["coins"]
        self.inventory = save["inventory"]

        self.level = None
        self.base_color = "#ffffff"
        self.questions = []
        self.q_index = 0
        self.score = 0
        self.streak = 0
        self.coins_earned_session = 0

        self.hint_used_this_q = False
        self.shield_active = False

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_start_screen()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        write_save(self.coins, self.inventory)
        self.destroy()

    # -----------------------------------------------------
    # 画面：スタート（レベル選択）
    # -----------------------------------------------------
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        write_save(self.coins, self.inventory)
        self.configure(bg="#ffffff")
        self.container.configure(bg="#ffffff")
        self.clear_container()

        tk.Label(
            self.container, text="化学クイズゲーム",
            font=self.title_font, bg="#ffffff"
        ).pack(pady=(30, 5))

        tk.Label(
            self.container,
            text=f"所持コイン：{self.coins} 枚",
            font=self.coin_font, fg="#b8860b", bg="#ffffff"
        ).pack(pady=(0, 10))

        tk.Label(
            self.container,
            text="モードを選んでください\n連続正解すると背景が明るくなり、コインもたまります！",
            font=self.normal_font, bg="#ffffff", justify="center"
        ).pack(pady=(0, 20))

        for level_num, (name, questions, color) in LEVELS.items():
            btn = tk.Button(
                self.container,
                text=f"{level_num}. {name}　（全{len(questions)}問）",
                font=self.button_font,
                width=32, height=2,
                bg=color,
                activebackground=color,
                command=lambda n=level_num: self.start_level(n)
            )
            btn.pack(pady=5)

        tk.Button(
            self.container, text="🛒 ショップ",
            font=self.button_font, width=32, height=2,
            bg="#f0e0ff", activebackground="#f0e0ff",
            command=self.show_shop_screen
        ).pack(pady=(15, 5))

    # -----------------------------------------------------
    # 画面：ショップ
    # -----------------------------------------------------
    def show_shop_screen(self):
        self.configure(bg="#ffffff")
        self.container.configure(bg="#ffffff")
        self.clear_container()

        tk.Label(
            self.container, text="ショップ",
            font=self.title_font, bg="#ffffff"
        ).pack(pady=(20, 5))

        tk.Label(
            self.container, text=f"所持コイン：{self.coins} 枚",
            font=self.coin_font, fg="#b8860b", bg="#ffffff"
        ).pack(pady=(0, 20))

        for item_id, info in ITEMS.items():
            frame = tk.Frame(self.container, bg="#f5f5f5", bd=1, relief="solid")
            frame.pack(pady=6, padx=30, fill="x")

            text = (
                f"{info['name']}　（{info['cost']}コイン）\n"
                f"{info['desc']}\n"
                f"所持数：{self.inventory.get(item_id, 0)} 個"
            )
            tk.Label(
                frame, text=text, font=self.small_font, bg="#f5f5f5",
                justify="left", anchor="w"
            ).pack(side="left", padx=10, pady=8, fill="x", expand=True)

            buy_btn = tk.Button(
                frame, text="購入する", font=self.button_font,
                command=lambda i=item_id: self.buy_item(i)
            )
            buy_btn.pack(side="right", padx=10)
            if self.coins < info["cost"]:
                buy_btn.config(state="disabled")

        tk.Button(
            self.container, text="戻る", font=self.button_font,
            width=20, height=2,
            command=self.show_start_screen
        ).pack(pady=20)

    def buy_item(self, item_id):
        cost = ITEMS[item_id]["cost"]
        if self.coins >= cost:
            self.coins -= cost
            self.inventory[item_id] = self.inventory.get(item_id, 0) + 1
            write_save(self.coins, self.inventory)
        self.show_shop_screen()

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
        self.coins_earned_session = 0
        self.shield_active = False

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
        self.hint_used_this_q = False

        if self.q_index >= len(self.questions):
            self.show_result_screen()
            return

        question, choices, answer = self.questions[self.q_index]
        bg = self.container["bg"]

        name, _, _ = LEVELS[self.level]
        header = tk.Label(
            self.container,
            text=f"【{name}】 第{self.q_index + 1}問 / 全{len(self.questions)}問"
                 f"　　得点: {self.score}　　連続正解: {self.streak}"
                 f"　　コイン: {self.coins}",
            font=self.small_font, bg=bg
        )
        header.pack(pady=(15, 10))

        q_label = tk.Label(
            self.container, text=question, font=self.normal_font,
            bg=bg, wraplength=620, justify="center"
        )
        q_label.pack(pady=(5, 20))

        self.shuffled_choices = choices[:]
        random.shuffle(self.shuffled_choices)
        self.current_answer = answer

        self.feedback_label = tk.Label(
            self.container, text="", font=self.normal_font, bg=bg
        )
        self.feedback_label.pack(pady=(0, 8))

        btn_frame = tk.Frame(self.container, bg=bg)
        btn_frame.pack()

        self.choice_buttons = {}
        for choice in self.shuffled_choices:
            btn = tk.Button(
                btn_frame, text=choice, font=self.button_font,
                width=25, height=2,
                command=lambda c=choice, a=answer: self.check_answer(c, a)
            )
            btn.pack(pady=4)
            self.choice_buttons[choice] = btn

        # ----- アイテム使用エリア -----
        item_frame = tk.Frame(self.container, bg=bg)
        item_frame.pack(pady=(15, 0))

        tk.Label(item_frame, text="アイテム：", font=self.small_font, bg=bg).pack(side="left")

        self.hint_btn = tk.Button(
            item_frame, text=f"ヒント({self.inventory.get('hint', 0)})",
            font=self.small_font, command=self.use_hint
        )
        self.hint_btn.pack(side="left", padx=4)
        if self.inventory.get("hint", 0) <= 0:
            self.hint_btn.config(state="disabled")

        self.skip_btn = tk.Button(
            item_frame, text=f"スキップ({self.inventory.get('skip', 0)})",
            font=self.small_font, command=self.use_skip
        )
        self.skip_btn.pack(side="left", padx=4)
        if self.inventory.get("skip", 0) <= 0:
            self.skip_btn.config(state="disabled")

        shield_label = "使用中" if self.shield_active else f"シールド({self.inventory.get('shield', 0)})"
        self.shield_btn = tk.Button(
            item_frame, text=shield_label,
            font=self.small_font, command=self.use_shield
        )
        self.shield_btn.pack(side="left", padx=4)
        if self.shield_active or self.inventory.get("shield", 0) <= 0:
            self.shield_btn.config(state="disabled")

    # -----------------------------------------------------
    # アイテム効果
    # -----------------------------------------------------
    def use_hint(self):
        if self.hint_used_this_q or self.inventory.get("hint", 0) <= 0:
            return
        wrong_choices = [c for c in self.shuffled_choices if c != self.current_answer]
        random.shuffle(wrong_choices)
        to_disable = wrong_choices[:2]
        for c in to_disable:
            self.choice_buttons[c].config(state="disabled", bg="#dddddd")

        self.inventory["hint"] -= 1
        self.hint_used_this_q = True
        write_save(self.coins, self.inventory)
        self.hint_btn.config(text=f"ヒント({self.inventory['hint']})", state="disabled")

    def use_skip(self):
        if self.inventory.get("skip", 0) <= 0:
            return
        self.inventory["skip"] -= 1
        write_save(self.coins, self.inventory)
        for btn in self.choice_buttons.values():
            btn.config(state="disabled")
        self.feedback_label.config(text="この問題はスキップしました", fg="#555555")
        self.after(500, self.next_question)

    def use_shield(self):
        if self.shield_active or self.inventory.get("shield", 0) <= 0:
            return
        self.inventory["shield"] -= 1
        self.shield_active = True
        write_save(self.coins, self.inventory)
        self.shield_btn.config(text="使用中", state="disabled")

    # -----------------------------------------------------
    # 解答チェック
    # -----------------------------------------------------
    def check_answer(self, chosen, answer):
        for btn in self.choice_buttons.values():
            btn.config(state="disabled")

        if chosen == answer:
            self.score += 1
            self.streak += 1
            earned = coins_for_streak(self.streak)
            self.coins += earned
            self.coins_earned_session += earned
            write_save(self.coins, self.inventory)
            self.feedback_label.config(
                text=f"○ 正解！　+{earned} コイン", fg="#0a8a2f"
            )
        else:
            if self.shield_active:
                self.shield_active = False
                self.feedback_label.config(
                    text=f"× 不正解…でもシールド発動！連続正解記録は守られた（正解：{answer}）",
                    fg="#8a5a0a"
                )
                # streak は維持（リセットしない）
            else:
                self.streak = 0
                self.feedback_label.config(
                    text=f"× 不正解…　正解は「{answer}」", fg="#c0392b"
                )

        self.update_background()
        self.feedback_label.configure(bg=self.container["bg"])

        self.after(1000, self.next_question)

    def next_question(self):
        self.q_index += 1
        self.show_question_screen()

    # -----------------------------------------------------
    # 画面：結果
    # -----------------------------------------------------
    def show_result_screen(self):
        write_save(self.coins, self.inventory)
        self.clear_container()
        bg = self.container["bg"]
        name, _, _ = LEVELS[self.level]

        tk.Label(
            self.container, text="結果発表",
            font=self.title_font, bg=bg
        ).pack(pady=(40, 15))

        total = len(self.questions)
        rate = 0 if total == 0 else round(self.score / total * 100)

        tk.Label(
            self.container,
            text=(
                f"モード：{name}\n"
                f"得点：{self.score} / {total}　（正答率 {rate}%）\n"
                f"獲得コイン：{self.coins_earned_session} 枚\n"
                f"現在の所持コイン：{self.coins} 枚"
            ),
            font=self.normal_font, bg=bg, justify="center"
        ).pack(pady=(0, 30))

        tk.Button(
            self.container, text="もう一度このモードで挑戦",
            font=self.button_font, width=28, height=2,
            command=lambda: self.start_level(self.level)
        ).pack(pady=6)

        tk.Button(
            self.container, text="🛒 ショップへ",
            font=self.button_font, width=28, height=2,
            command=self.show_shop_screen
        ).pack(pady=6)

        tk.Button(
            self.container, text="モード選択に戻る",
            font=self.button_font, width=28, height=2,
            command=self.show_start_screen
        ).pack(pady=6)


if __name__ == "__main__":
    app = ChemistryGame()
    app.mainloop()