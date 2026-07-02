# -*- coding: utf-8 -*-
"""
化学クイズゲーム（Streamlit版）
--------------------------------------------
実行方法:
    pip install streamlit
    streamlit run chemistry_game_streamlit.py

・4段階の難易度モード（初級／中級／上級／超級）
・各モードたくさんの問題（合計110問）
・連続正解するほど背景がだんだん明るくなる
・正解するとコインがたまり、ショップでアイテムが買える
    - ヒント：はずれの選択肢を2つ消す
    - スキップ：この問題を飛ばす
    - シールド：1回だけ不正解を無効にして連続正解を守る
・コインとアイテムはファイルに保存され、次回起動時も引き継がれる
・使用ライブラリは streamlit / random / json / os のみ（AI・外部通信なし）
"""

import streamlit as st
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


# =========================================================
# セーブデータ読み書き
# =========================================================
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


def write_save():
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(
                {"coins": st.session_state.coins, "inventory": st.session_state.inventory},
                f, ensure_ascii=False
            )
    except Exception:
        pass


# =========================================================
# 色計算
# =========================================================
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


def apply_background(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
            transition: background-color 0.4s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# セッション状態の初期化
# =========================================================
def init_state():
    if "initialized" in st.session_state:
        return
    save = load_save()
    st.session_state.coins = save["coins"]
    st.session_state.inventory = save["inventory"]

    st.session_state.screen = "start"     # start / shop / quiz / result
    st.session_state.level = None
    st.session_state.base_color = "#ffffff"
    st.session_state.questions = []
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.coins_earned_session = 0

    st.session_state.shield_active = False
    st.session_state.hint_used_this_q = False
    st.session_state.disabled_choices = []
    st.session_state.current_choices = []
    st.session_state.current_answer = None
    st.session_state.answered = False
    st.session_state.feedback_text = ""
    st.session_state.feedback_color = "black"
    st.session_state.prepared_q_index = -1

    st.session_state.initialized = True


def prepare_question():
    """現在の q_index の問題の選択肢をシャッフルして保持する"""
    if st.session_state.prepared_q_index == st.session_state.q_index:
        return
    if st.session_state.q_index >= len(st.session_state.questions):
        return
    _, choices, answer = st.session_state.questions[st.session_state.q_index]
    shuffled = choices[:]
    random.shuffle(shuffled)
    st.session_state.current_choices = shuffled
    st.session_state.current_answer = answer
    st.session_state.disabled_choices = []
    st.session_state.hint_used_this_q = False
    st.session_state.answered = False
    st.session_state.feedback_text = ""
    st.session_state.prepared_q_index = st.session_state.q_index


def start_level(level_num):
    name, questions, color = LEVELS[level_num]
    st.session_state.level = level_num
    st.session_state.base_color = color
    qs = questions[:]
    random.shuffle(qs)
    st.session_state.questions = qs
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.coins_earned_session = 0
    st.session_state.shield_active = False
    st.session_state.prepared_q_index = -1
    st.session_state.screen = "quiz"


def go_to_next_question():
    st.session_state.q_index += 1
    if st.session_state.q_index >= len(st.session_state.questions):
        st.session_state.screen = "result"


def check_answer(chosen):
    answer = st.session_state.current_answer
    if chosen == answer:
        st.session_state.score += 1
        st.session_state.streak += 1
        earned = coins_for_streak(st.session_state.streak)
        st.session_state.coins += earned
        st.session_state.coins_earned_session += earned
        st.session_state.feedback_text = f"○ 正解！　+{earned} コイン"
        st.session_state.feedback_color = "#0a8a2f"
    else:
        if st.session_state.shield_active:
            st.session_state.shield_active = False
            st.session_state.feedback_text = (
                f"× 不正解…でもシールド発動！連続正解記録は守られた（正解：{answer}）"
            )
            st.session_state.feedback_color = "#8a5a0a"
        else:
            st.session_state.streak = 0
            st.session_state.feedback_text = f"× 不正解…　正解は「{answer}」"
            st.session_state.feedback_color = "#c0392b"

    st.session_state.answered = True
    write_save()


def use_hint():
    if st.session_state.hint_used_this_q or st.session_state.inventory.get("hint", 0) <= 0:
        return
    wrong = [c for c in st.session_state.current_choices if c != st.session_state.current_answer]
    random.shuffle(wrong)
    st.session_state.disabled_choices = wrong[:2]
    st.session_state.inventory["hint"] -= 1
    st.session_state.hint_used_this_q = True
    write_save()


def use_skip():
    if st.session_state.inventory.get("skip", 0) <= 0 or st.session_state.answered:
        return
    st.session_state.inventory["skip"] -= 1
    write_save()
    go_to_next_question()


def use_shield():
    if st.session_state.shield_active or st.session_state.inventory.get("shield", 0) <= 0:
        return
    st.session_state.inventory["shield"] -= 1
    st.session_state.shield_active = True
    write_save()


def buy_item(item_id):
    cost = ITEMS[item_id]["cost"]
    if st.session_state.coins >= cost:
        st.session_state.coins -= cost
        st.session_state.inventory[item_id] = st.session_state.inventory.get(item_id, 0) + 1
        write_save()


# =========================================================
# 画面：スタート
# =========================================================
def render_start_screen():
    apply_background("#ffffff")
    st.title("🧪 化学クイズゲーム")
    st.markdown(f"### 所持コイン：🪙 {st.session_state.coins} 枚")
    st.write("モードを選んでください。連続正解すると背景が明るくなり、コインもたまります！")

    for level_num, (name, questions, color) in LEVELS.items():
        if st.button(f"{level_num}. {name}　（全{len(questions)}問）", key=f"level_{level_num}", use_container_width=True):
            start_level(level_num)
            st.rerun()

    st.write("")
    if st.button("🛒 ショップへ", use_container_width=True):
        st.session_state.screen = "shop"
        st.rerun()


# =========================================================
# 画面：ショップ
# =========================================================
def render_shop_screen():
    apply_background("#ffffff")
    st.title("🛒 ショップ")
    st.markdown(f"### 所持コイン：🪙 {st.session_state.coins} 枚")

    for item_id, info in ITEMS.items():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{info['name']}**　（{info['cost']}コイン）")
                st.caption(info["desc"])
                st.write(f"所持数：{st.session_state.inventory.get(item_id, 0)} 個")
            with col2:
                disabled = st.session_state.coins < info["cost"]
                if st.button("購入する", key=f"buy_{item_id}", disabled=disabled, use_container_width=True):
                    buy_item(item_id)
                    st.rerun()

    st.write("")
    if st.button("← 戻る", use_container_width=True):
        st.session_state.screen = "start"
        st.rerun()


# =========================================================
# 画面：クイズ
# =========================================================
def render_quiz_screen():
    prepare_question()

    if st.session_state.q_index >= len(st.session_state.questions):
        st.session_state.screen = "result"
        st.rerun()
        return

    color = brighten_color(st.session_state.base_color, st.session_state.streak)
    apply_background(color)

    name, _, _ = LEVELS[st.session_state.level]
    total = len(st.session_state.questions)

    st.markdown(
        f"**【{name}】** 第{st.session_state.q_index + 1}問 / 全{total}問　　"
        f"得点: {st.session_state.score}　　連続正解: {st.session_state.streak}　　"
        f"🪙 コイン: {st.session_state.coins}"
    )
    st.progress((st.session_state.q_index) / total)

    question, _, _ = st.session_state.questions[st.session_state.q_index]
    st.markdown(f"## {question}")

    if st.session_state.feedback_text:
        st.markdown(
            f"<p style='color:{st.session_state.feedback_color}; font-size:18px; font-weight:bold;'>"
            f"{st.session_state.feedback_text}</p>",
            unsafe_allow_html=True,
        )

    # ----- 選択肢ボタン -----
    for choice in st.session_state.current_choices:
        is_disabled = st.session_state.answered or choice in st.session_state.disabled_choices
        if st.button(choice, key=f"choice_{st.session_state.q_index}_{choice}",
                     disabled=is_disabled, use_container_width=True):
            check_answer(choice)
            st.rerun()

    # ----- 次へボタン（解答後のみ表示） -----
    if st.session_state.answered:
        if st.button("次の問題へ ▶", use_container_width=True, type="primary"):
            go_to_next_question()
            st.rerun()

    st.write("---")
    st.caption("アイテムを使う")
    c1, c2, c3 = st.columns(3)

    with c1:
        hint_count = st.session_state.inventory.get("hint", 0)
        if st.button(f"💡 ヒント（{hint_count}）", disabled=(hint_count <= 0 or st.session_state.hint_used_this_q or st.session_state.answered), use_container_width=True):
            use_hint()
            st.rerun()

    with c2:
        skip_count = st.session_state.inventory.get("skip", 0)
        if st.button(f"⏭ スキップ（{skip_count}）", disabled=(skip_count <= 0 or st.session_state.answered), use_container_width=True):
            use_skip()
            st.rerun()

    with c3:
        shield_count = st.session_state.inventory.get("shield", 0)
        shield_label = "🛡 使用中" if st.session_state.shield_active else f"🛡 シールド（{shield_count}）"
        if st.button(shield_label, disabled=(st.session_state.shield_active or shield_count <= 0), use_container_width=True):
            use_shield()
            st.rerun()


# =========================================================
# 画面：結果
# =========================================================
def render_result_screen():
    apply_background(st.session_state.base_color)
    name, _, _ = LEVELS[st.session_state.level]
    total = len(st.session_state.questions)
    rate = 0 if total == 0 else round(st.session_state.score / total * 100)

    st.title("🎉 結果発表")
    st.markdown(f"### モード：{name}")
    st.markdown(f"### 得点：{st.session_state.score} / {total}　（正答率 {rate}%）")
    st.markdown(f"### 獲得コイン：🪙 {st.session_state.coins_earned_session} 枚")
    st.markdown(f"### 現在の所持コイン：🪙 {st.session_state.coins} 枚")

    write_save()

    st.write("")
    if st.button("🔁 もう一度このモードで挑戦", use_container_width=True):
        start_level(st.session_state.level)
        st.rerun()
    if st.button("🛒 ショップへ", use_container_width=True):
        st.session_state.screen = "shop"
        st.rerun()
    if st.button("🏠 モード選択に戻る", use_container_width=True):
        st.session_state.screen = "start"
        st.rerun()


# =========================================================
# メイン
# =========================================================
def main():
    st.set_page_config(page_title="化学クイズゲーム", page_icon="🧪", layout="centered")
    init_state()

    screen = st.session_state.screen
    if screen == "start":
        render_start_screen()
    elif screen == "shop":
        render_shop_screen()
    elif screen == "quiz":
        render_quiz_screen()
    elif screen == "result":
        render_result_screen()


if __name__ == "__main__":
    main()