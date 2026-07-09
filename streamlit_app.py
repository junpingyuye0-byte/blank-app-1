# -*- coding: utf-8 -*-
"""
化学クイズゲーム（Streamlit版・解説＆途中終了対応）
--------------------------------------------
実行方法:
    pip install streamlit
    streamlit run chemistry_game_streamlit.py

・4段階の難易度モード（初級／中級／上級／超級）
・各モードたくさんの問題（合計150問）
・すべての問題に解説つき
・連続正解するほど背景がだんだん明るくなる（レベルごとに配色を変更）
・正解するとコインがたまり、ショップでアイテムが買える
    - ヒント：はずれの選択肢を2つ消す
    - 全消しヒント：はずれの選択肢を全部消して正解だけにする
    - スキップ：この問題を飛ばす
    - シールド：1回だけ不正解を無効にして連続正解を守る
    - ダブルコイン：次に正解した時のコインが2倍になる
・プレイの途中でいつでもやめられる（「やめる」ボタン→確認→結果画面へ）
・コインとアイテムはファイルに保存され、次回起動時も引き継がれる
・使用ライブラリは streamlit / random / json / os のみ（AI・外部通信なし）
"""

import streamlit as st
import random
import json
import os

# =========================================================
# 問題データ（4段階・合計150問）
# 各要素: (問題文, 選択肢リスト, 正解, 解説)
# =========================================================

LEVEL1_QUESTIONS = [
    ("水素の元素記号は？", ["H", "He", "Hg", "N"], "H", "Hは水素（Hydrogen）を表します。宇宙で最も多く存在する元素です。"),
    ("酸素の元素記号は？", ["O", "Os", "Ox", "On"], "O", "Oは酸素（Oxygen）の頭文字です。呼吸や燃焼に欠かせません。"),
    ("水の化学式は？", ["H2O", "CO2", "NaCl", "O2"], "H2O", "水素原子2個と酸素原子1個が結びついた分子です。"),
    ("二酸化炭素の化学式は？", ["CO2", "CO", "O2", "H2O"], "CO2", "炭素原子1個に酸素原子2個が結びついた気体です。"),
    ("食塩（塩化ナトリウム）の化学式は？", ["NaCl", "NaOH", "KCl", "CaCl2"], "NaCl", "ナトリウムイオンと塩化物イオンが1:1で結びついたイオン結晶です。"),
    ("ヘリウムの元素記号は？", ["He", "H", "Ne", "Li"], "He", "ヘリウムは風船などに使われる、空気より軽い貴ガスです。"),
    ("炭素の元素記号は？", ["C", "Ca", "Cl", "Co"], "C", "炭素はあらゆる有機物の骨格をつくる基本元素です。"),
    ("窒素の元素記号は？", ["N", "Na", "Ne", "Ni"], "N", "窒素は空気の体積の約78％を占める気体です。"),
    ("ナトリウムの元素記号は？", ["Na", "N", "Ni", "Ne"], "Na", "ナトリウムはラテン語Natriumに由来するアルカリ金属です。"),
    ("鉄の元素記号は？", ["Fe", "F", "Ir", "Fr"], "Fe", "鉄の元素記号Feはラテン語Ferrumに由来します。"),
    ("金の元素記号は？", ["Au", "Ag", "Al", "Ar"], "Au", "金の元素記号Auはラテン語Aurumに由来します。"),
    ("銀の元素記号は？", ["Ag", "Au", "Al", "As"], "Ag", "銀の元素記号Agはラテン語Argentumに由来します。"),
    ("銅の元素記号は？", ["Cu", "Co", "Ca", "Cr"], "Cu", "銅の元素記号Cuはラテン語Cuprumに由来します。"),
    ("カルシウムの元素記号は？", ["Ca", "Cu", "Cl", "C"], "Ca", "カルシウムは骨や歯の主成分となる金属元素です。"),
    ("塩素の元素記号は？", ["Cl", "C", "Ca", "Co"], "Cl", "塩素は殺菌・消毒などに広く利用される気体です。"),
    ("アルミニウムの元素記号は？", ["Al", "Ar", "Au", "As"], "Al", "アルミニウムは軽くてさびにくい金属の代表です。"),
    ("硫黄の元素記号は？", ["S", "Si", "Sn", "Sr"], "S", "硫黄は黄色い結晶で、火山地帯によく見られます。"),
    ("カリウムの元素記号は？", ["K", "Ca", "Kr", "Co"], "K", "カリウムの元素記号Kはラテン語Kaliumに由来します。"),
    ("亜鉛の元素記号は？", ["Zn", "Ni", "Sn", "Pb"], "Zn", "亜鉛はメッキや乾電池などに使われる金属です。"),
    ("物質を構成する最小単位を何という？", ["原子", "分子", "細胞", "元素記号"], "原子", "すべての物質は原子という非常に小さな粒子からできています。"),
    ("リチウムの元素記号は？", ["Li", "La", "Lr", "Lv"], "Li", "リチウムは充電池（リチウムイオン電池）の材料として有名です。"),
    ("マグネシウムの元素記号は？", ["Mg", "Mn", "Mo", "Md"], "Mg", "マグネシウムは軽くてよく燃える金属で、花火にも使われます。"),
    ("フッ素の元素記号は？", ["F", "Fe", "Fr", "Fm"], "F", "フッ素はハロゲンの中で最も反応性が高い元素です。"),
    ("ネオンの元素記号は？", ["Ne", "N", "Na", "Ni"], "Ne", "ネオンはネオンサインの発光に使われる貴ガスです。"),
    ("臭素の元素記号は？", ["Br", "B", "Ba", "Bi"], "Br", "臭素は常温・常圧で液体である珍しい非金属元素です。"),
    ("ヨウ素の元素記号は？", ["I", "In", "Ir", "Y"], "I", "ヨウ素はうがい薬や消毒液の成分として使われます。"),
    ("ケイ素の元素記号は？", ["Si", "S", "Se", "Sn"], "Si", "ケイ素は半導体（パソコンのチップなど）の材料です。"),
    ("リンの元素記号は？", ["P", "Pb", "Pt", "Po"], "P", "リンはマッチや肥料、DNAの構成成分として使われます。"),
    ("鉛の元素記号は？", ["Pb", "P", "Pt", "Po"], "Pb", "鉛の元素記号Pbはラテン語Plumbumに由来します。"),
    ("水銀の元素記号は？", ["Hg", "H", "He", "Ho"], "Hg", "水銀の元素記号Hgはラテン語Hydrargyrumに由来し、常温で液体の金属です。"),
    ("アルゴンの元素記号は？", ["Ar", "Al", "Au", "As"], "Ar", "アルゴンは空気中に約1％含まれる反応しにくい貴ガスです。"),
    ("バリウムの元素記号は？", ["Ba", "Br", "B", "Bi"], "Ba", "バリウムはレントゲン検査の造影剤として使われます。"),
    ("マンガンの元素記号は？", ["Mn", "Mg", "Mo", "Md"], "Mn", "マンガンは乾電池の材料や鉄の合金に使われます。"),
    ("コバルトの元素記号は？", ["Co", "Cu", "Cr", "Ca"], "Co", "コバルトは青色顔料（コバルトブルー）や合金に使われます。"),
    ("ニッケルの元素記号は？", ["Ni", "Na", "Ne", "N"], "Ni", "ニッケルは硬貨やステンレスなどの合金に使われます。"),
    ("スズの元素記号は？", ["Sn", "S", "Si", "Sr"], "Sn", "スズの元素記号Snはラテン語Stannumに由来します。"),
    ("クロムの元素記号は？", ["Cr", "Co", "Cu", "Ca"], "Cr", "クロムはステンレス鋼にさびにくさを与える元素です。"),
    ("チタンの元素記号は？", ["Ti", "Sn", "Ta", "Te"], "Ti", "チタンは軽くて丈夫なため、航空機や眼鏡フレームに使われます。"),
    ("ヒ素の元素記号は？", ["As", "Ag", "Al", "Au"], "As", "ヒ素は毒性で知られる半金属元素です。"),
    ("白金（プラチナ）の元素記号は？", ["Pt", "Pb", "Po", "P"], "Pt", "白金は装飾品のほか、自動車の排ガス浄化触媒にも使われます。"),
]

LEVEL2_QUESTIONS = [
    ("メタンの化学式は？", ["CH4", "C2H6", "CO2", "NH3"], "CH4", "メタンは炭素1個に水素4個が結合した、最も単純な炭化水素です。"),
    ("アンモニアの化学式は？", ["NH3", "NO2", "N2O", "HN3"], "NH3", "アンモニアは窒素1個に水素3個が結合した刺激臭のある気体です。"),
    ("硫酸の化学式は？", ["H2SO4", "HCl", "HNO3", "H2SO3"], "H2SO4", "硫酸は工業的に最も多く生産される強酸の一つです。"),
    ("塩酸の主成分は？", ["HCl", "H2SO4", "NaOH", "HNO3"], "HCl", "塩酸は塩化水素（HCl）の水溶液で、胃液にも含まれます。"),
    ("水酸化ナトリウムの化学式は？", ["NaOH", "NaCl", "Na2O", "NaHCO3"], "NaOH", "水酸化ナトリウムは強い塩基で「か性ソーダ」とも呼ばれます。"),
    ("酸とアルカリが反応することを何という？", ["中和", "酸化", "還元", "電離"], "中和", "中和は酸と塩基が反応して水と塩（えん）を生じる反応です。"),
    ("ものが燃える（完全燃焼）と主に発生する気体は？", ["二酸化炭素", "酸素", "水素", "窒素"], "二酸化炭素", "有機物が完全燃焼すると、炭素が酸素と結びついて二酸化炭素になります。"),
    ("pHが7のとき溶液は？", ["中性", "酸性", "アルカリ性", "不明"], "中性", "pH7は水素イオンと水酸化物イオンの濃度が等しい中性の状態です。"),
    ("pHが7より小さいと溶液は？", ["酸性", "アルカリ性", "中性", "中和"], "酸性", "pHが小さいほど水素イオン濃度が高く、酸性が強くなります。"),
    ("pHが7より大きいと溶液は？", ["アルカリ性", "酸性", "中性", "中和"], "アルカリ性", "pHが大きいほど水酸化物イオン濃度が高く、アルカリ性が強くなります。"),
    ("原子核を構成する粒子は陽子と何？", ["中性子", "電子", "イオン", "分子"], "中性子", "原子核は陽子と中性子という2種類の粒子からできています。"),
    ("電子が持つ電荷は？", ["負（マイナス）", "正（プラス）", "電荷なし", "不定"], "負（マイナス）", "電子は原子核の周りを飛び回る、負の電荷を持つ粒子です。"),
    ("陽子が持つ電荷は？", ["正（プラス）", "負（マイナス）", "電荷なし", "不定"], "正（プラス）", "陽子は原子核の中にある、正の電荷を持つ粒子です。"),
    ("原子番号は何の数を表す？", ["陽子の数", "中性子の数", "電子殻の数", "分子の数"], "陽子の数", "原子番号はその原子が持つ陽子の数と等しくなります。"),
    ("陽子の数が同じで中性子の数が異なる原子どうしを何という？", ["同位体", "同素体", "異性体", "同族体"], "同位体", "同位体は陽子数が同じでも中性子数が違うため、質量がわずかに異なります。"),
    ("炭素の同素体でないものは？", ["食塩", "ダイヤモンド", "黒鉛", "フラーレン"], "食塩", "食塩（NaCl）は炭素からできていないため、炭素の同素体ではありません。"),
    ("金属が電子を放出してできるイオンを何という？", ["陽イオン", "陰イオン", "中性子", "分子イオン"], "陽イオン", "電子を失うと正の電荷が残るため、陽イオンになります。"),
    ("塩素原子が電子を受け取ってできるイオンを何という？", ["陰イオン", "陽イオン", "中性子", "同位体"], "陰イオン", "電子を受け取ると負の電荷を帯びるため、陰イオンになります。"),
    ("水溶液に電流が流れる物質を何という？", ["電解質", "非電解質", "触媒", "同位体"], "電解質", "電解質は水に溶けるとイオンに分かれ、電流を流せる物質です。"),
    ("砂糖水のように電流が流れない物質を何という？", ["非電解質", "電解質", "酸", "塩基"], "非電解質", "砂糖のようにイオンに分かれない物質は非電解質と呼ばれます。"),
    ("過酸化水素の化学式は？", ["H2O2", "H2O", "HO2", "H3O2"], "H2O2", "過酸化水素はオキシドールなどの消毒液に使われています。"),
    ("二酸化硫黄の化学式は？", ["SO2", "SO3", "S2O", "H2SO3"], "SO2", "二酸化硫黄は火山ガスにも含まれる、刺激臭のある気体です。"),
    ("一酸化炭素の化学式は？", ["CO", "CO2", "C2O", "COOH"], "CO", "一酸化炭素は不完全燃焼で発生する、無色無臭の有毒な気体です。"),
    ("塩化水素が水に溶けたものを何という？", ["塩酸", "硫酸", "硝酸", "炭酸"], "塩酸", "塩化水素（HCl）が水に溶けた水溶液を塩酸と呼びます。"),
    ("酸化カルシウムの別名は？", ["生石灰", "消石灰", "石灰水", "炭酸カルシウム"], "生石灰", "酸化カルシウム（CaO）は生石灰と呼ばれ、乾燥剤にも使われます。"),
    ("水酸化カルシウムの別名は？", ["消石灰", "生石灰", "石灰石", "セッコウ"], "消石灰", "水酸化カルシウム（Ca(OH)2）は消石灰と呼ばれ、運動場のライン引きにも使われます。"),
    ("石灰水に二酸化炭素を通すとどうなる？", ["白く濁る", "赤くなる", "透明になる", "気体が消える"], "白く濁る", "二酸化炭素と反応して炭酸カルシウムの白い沈殿ができるためです。"),
    ("金属が酸に溶けるとき多くの場合発生する気体は？", ["水素", "酸素", "窒素", "二酸化炭素"], "水素", "亜鉛やマグネシウムなどの金属が酸に溶けると水素が発生します。"),
    ("燃焼に必ず必要な気体は？", ["酸素", "窒素", "水素", "二酸化炭素"], "酸素", "燃焼は物質が酸素と結びついて熱と光を出す反応です。"),
    ("空気中で体積の割合が最も多い気体は？", ["窒素", "酸素", "二酸化炭素", "アルゴン"], "窒素", "空気の体積の約78％を窒素が占めています。"),
    ("硫化水素の化学式は？", ["H2S", "SO2", "H2SO4", "S2"], "H2S", "硫化水素は腐った卵のようなにおいがする有毒な気体です。"),
    ("二酸化窒素の化学式は？", ["NO2", "NO", "N2O", "HNO3"], "NO2", "二酸化窒素は大気汚染の原因物質の一つとして知られています。"),
    ("一酸化窒素の化学式は？", ["NO", "NO2", "N2O", "N2O3"], "NO", "一酸化窒素は体内の血管拡張にも関わる重要な分子です。"),
    ("炭酸の化学式は？", ["H2CO3", "CO2", "HCO3", "CaCO3"], "H2CO3", "炭酸は二酸化炭素が水に溶けてできる弱酸です。"),
    ("リン酸の化学式は？", ["H3PO4", "HPO3", "P2O5", "H3PO3"], "H3PO4", "リン酸は肥料や食品添加物（酸味料）などに使われます。"),
    ("水酸化カリウムの化学式は？", ["KOH", "K2O", "KCl", "KHCO3"], "KOH", "水酸化カリウムは強塩基で、石けん作りにも使われます。"),
    ("アンモニア水は何性？", ["アルカリ性", "酸性", "中性", "不定"], "アルカリ性", "アンモニアが水に溶けると水酸化物イオンを生じ、アルカリ性を示します。"),
    ("酢酸水溶液は何性？", ["酸性", "アルカリ性", "中性", "不定"], "酸性", "酢酸は弱酸ですが、水溶液は酸性を示します。"),
    ("中性の水溶液のpHはいくつ？", ["7", "0", "14", "1"], "7", "pH7が中性で、それより小さいと酸性、大きいとアルカリ性です。"),
    ("うすい塩酸にマグネシウムを入れると発生する気体は？", ["水素", "酸素", "二酸化炭素", "窒素"], "水素", "マグネシウムが塩酸と反応すると塩化マグネシウムと水素が発生します。"),
]

LEVEL3_QUESTIONS = [
    ("水の生成反応式は？ 2H2 + O2 →", ["2H2O", "H2O2", "2H2O2", "HO2"], "2H2O", "水素分子2個と酸素分子1個が反応すると、水分子2個が生じます。"),
    ("物質量（molの単位）が表すものは？", ["粒子の数の集まり", "重さ", "体積", "温度"], "粒子の数の集まり", "molは原子や分子などの粒子の集まりの量を表す単位です。"),
    ("1molに含まれる粒子の数（アボガドロ数）は約？", ["6.02×10の23乗", "3.14×10の8乗", "9.8×10の10乗", "1.0×10の6乗"], "6.02×10の23乗", "アボガドロ数は1molあたりの粒子数を表す定数です。"),
    ("酸素と結びつく化学変化を何という？", ["酸化", "還元", "中和", "電離"], "酸化", "物質が酸素と結びつく変化を酸化といいます。"),
    ("酸化物から酸素を奪う化学変化を何という？", ["還元", "酸化", "中和", "電離"], "還元", "酸化物から酸素が奪われる変化を還元といい、酸化と対になる反応です。"),
    ("塩化ナトリウムの結晶を作る結合は？", ["イオン結合", "共有結合", "金属結合", "水素結合"], "イオン結合", "陽イオンと陰イオンが静電気力で引き合う結合をイオン結合といいます。"),
    ("水分子（H2O）を作る結合は？", ["共有結合", "イオン結合", "金属結合", "配位結合のみ"], "共有結合", "非金属原子どうしが電子を共有してできる結合を共有結合といいます。"),
    ("周期表で縦の列（同じ族）の元素は性質が？", ["似ている", "全く異なる", "関係ない", "反応しない"], "似ている", "同じ族の元素は最外殻電子の数が同じため、化学的性質が似ています。"),
    ("ヘリウムやネオンなど反応しにくい気体を何という？", ["貴ガス（希ガス）", "ハロゲン", "アルカリ金属", "遷移金属"], "貴ガス（希ガス）", "貴ガスは最外殻電子が安定しているため、他の物質と反応しにくいです。"),
    ("化学反応の速さを変えるが自身は変化しない物質は？", ["触媒", "溶媒", "溶質", "指示薬"], "触媒", "触媒は反応の前後で自身は変化せず、反応速度だけを変える物質です。"),
    ("塩酸と水酸化ナトリウム水溶液を混ぜると生じる塩は？", ["塩化ナトリウム", "硫酸ナトリウム", "炭酸ナトリウム", "硝酸ナトリウム"], "塩化ナトリウム", "HClとNaOHが中和すると、塩化ナトリウムと水が生じます。"),
    ("酸化銀を加熱すると発生する気体は？", ["酸素", "水素", "二酸化炭素", "窒素"], "酸素", "酸化銀を加熱すると銀と酸素に分解されます。"),
    ("塩酸に亜鉛を入れると発生する気体は？", ["水素", "酸素", "二酸化炭素", "塩素"], "水素", "亜鉛が塩酸と反応すると塩化亜鉛と水素が発生します。"),
    ("炭酸水素ナトリウムを加熱すると発生する気体は？", ["二酸化炭素", "酸素", "水素", "アンモニア"], "二酸化炭素", "重曹（炭酸水素ナトリウム）を加熱すると二酸化炭素と水、炭酸ナトリウムに分解されます。"),
    ("BTB溶液が酸性で示す色は？", ["黄色", "青色", "緑色", "赤色"], "黄色", "BTB溶液は酸性で黄色、中性で緑色、アルカリ性で青色を示します。"),
    ("二酸化炭素の分子の形は？", ["直線形", "折れ線形", "三角形", "正四面体形"], "直線形", "二酸化炭素はO=C=Oのように原子が一直線に並んだ構造をしています。"),
    ("メタン分子の形は？", ["正四面体形", "直線形", "折れ線形", "平面三角形"], "正四面体形", "メタンは炭素を中心に4つの水素が正四面体状に配置されています。"),
    ("イオン結晶の一般的な特徴は？", ["硬くてもろい", "やわらかくて伸びる", "電気を通しやすい液体状", "気体になりやすい"], "硬くてもろい", "イオン結晶は硬いですが、強い力を加えると割れやすい性質があります。"),
    ("金属特有の光沢や展延性のもとになる結合は？", ["金属結合", "イオン結合", "共有結合", "水素結合"], "金属結合", "金属結合では自由電子が金属原子の間を自由に動けるため、光沢や展延性が生まれます。"),
    ("電子親和力が大きい元素ほど？", ["陰イオンになりやすい", "陽イオンになりやすい", "反応しにくい", "金属になりやすい"], "陰イオンになりやすい", "電子親和力が大きいほど電子を受け取りやすく、陰イオンになりやすいです。"),
    ("イオン化エネルギーが小さい元素ほど？", ["陽イオンになりやすい", "陰イオンになりやすい", "反応しにくい", "非金属になりやすい"], "陽イオンになりやすい", "イオン化エネルギーが小さいほど電子を放出しやすく、陽イオンになりやすいです。"),
    ("ハロゲンに分類される元素は？", ["塩素", "ナトリウム", "鉄", "ヘリウム"], "塩素", "ハロゲンはフッ素・塩素・臭素・ヨウ素などが属するグループです。"),
    ("アルカリ金属に分類される元素は？", ["ナトリウム", "塩素", "ヘリウム", "鉄"], "ナトリウム", "アルカリ金属はリチウム・ナトリウム・カリウムなど、周期表の1族の元素です。"),
    ("遷移元素に分類される元素は？", ["鉄", "ナトリウム", "塩素", "ヘリウム"], "鉄", "遷移元素は周期表の中央付近に位置する金属元素のグループです。"),
    ("化学反応式の係数は何を表す？", ["物質の粒子（分子・イオン）の数の比", "反応にかかる時間", "物質の色", "反応の温度"], "物質の粒子（分子・イオン）の数の比", "係数は反応に関わる物質の粒子数の比を示します。"),
    ("化学反応の前後で物質の総質量は変わらないという法則は？", ["質量保存の法則", "定比例の法則", "気体反応の法則", "倍数比例の法則"], "質量保存の法則", "反応の前後で原子の組み合わせは変わりますが、原子自体は増減しないため質量は保存されます。"),
    ("一つの化合物中の成分元素の質量比は常に一定という法則は？", ["定比例の法則", "質量保存の法則", "気体反応の法則", "ボイルの法則"], "定比例の法則", "同じ化合物であれば、どこで作られても成分元素の質量比は一定です。"),
    ("原子核に最も近い電子殻を何という？", ["K殻", "L殻", "M殻", "N殻"], "K殻", "電子殻は原子核に近い方からK殻、L殻、M殻…と呼ばれます。"),
    ("最外殻電子のうち化学結合に関わる電子を何という？", ["価電子", "自由電子", "内殻電子", "共有電子"], "価電子", "価電子は原子の一番外側の電子殻にあり、化学結合に関わる電子です。"),
    ("貴ガス（希ガス）の最外殻電子の状態は？", ["安定している（閉殻）", "反応しやすい", "不安定", "常に1個だけ"], "安定している（閉殻）", "貴ガスは最外殻が電子で満たされた安定な状態のため、反応しにくいです。"),
    ("分子結晶（例：ドライアイス）の一般的な特徴は？", ["融点が低い", "非常に硬い", "電気をよく通す", "延性に富む"], "融点が低い", "分子どうしを結びつける力が弱いため、分子結晶は融点が低い傾向があります。"),
    ("共有結合の結晶（例：ダイヤモンド）の特徴は？", ["非常に硬い", "やわらかい", "電気をよく通す", "融点が低い"], "非常に硬い", "共有結合が立体的に連なっているため、ダイヤモンドは非常に硬い結晶です。"),
    ("水溶液の水素イオン濃度からpHを測定する器具の一つは？", ["pHメーター", "気圧計", "温度計", "比重計"], "pHメーター", "pHメーターは水素イオン濃度を電気的に測定してpH値を表示する器具です。"),
    ("弱酸・弱塩基が水溶液中で電離する割合は？", ["一部だけ電離する", "完全に電離する", "全く電離しない", "常に半分電離する"], "一部だけ電離する", "弱酸・弱塩基は水溶液中で一部の分子だけがイオンに分かれます。"),
    ("強酸・強塩基が水溶液中で電離する割合は？", ["ほぼ完全に電離する", "一部だけ電離する", "全く電離しない", "常に半分電離する"], "ほぼ完全に電離する", "強酸・強塩基は水溶液中でほとんどの分子がイオンに分かれます。"),
]

LEVEL4_QUESTIONS = [
    ("NaOH + HCl → NaCl + ？", ["H2O", "H2", "O2", "Cl2"], "H2O", "水酸化ナトリウムと塩酸の中和反応では、塩化ナトリウムと水が生じます。"),
    ("水（H2O）のモル質量は約18g/molである。0.5molの水の質量は？", ["9g", "18g", "36g", "4.5g"], "9g", "質量＝モル質量×物質量なので、18g/mol×0.5mol＝9gです。"),
    ("炭酸カルシウムの化学式は？", ["CaCO3", "CaO", "Ca(OH)2", "CaCl2"], "CaCO3", "炭酸カルシウムは石灰石や貝殻の主成分です。"),
    ("硝酸の化学式は？", ["HNO3", "H2SO4", "HCl", "H2CO3"], "HNO3", "硝酸は強酸の一つで、肥料や火薬の原料にもなります。"),
    ("水を電気分解すると陰極（マイナス極）に発生する気体は？", ["水素", "酸素", "窒素", "二酸化炭素"], "水素", "水の電気分解では陰極に水素、陽極に酸素が発生し、体積比は2:1です。"),
    ("pH2の溶液はpH5の溶液に比べて水素イオン濃度が？", ["1000倍高い", "1000倍低い", "3倍高い", "同じ"], "1000倍高い", "pHが1下がるごとに水素イオン濃度は10倍になるため、差が3のときは1000倍になります。"),
    ("気体の状態方程式 PV=？ の右辺は？", ["nRT", "mgh", "F/A", "ρV"], "nRT", "気体の状態方程式はPV=nRT（圧力×体積＝物質量×気体定数×絶対温度）です。"),
    ("標準状態（0℃・1気圧）で気体1molが占める体積は？", ["22.4L", "1L", "100L", "18mL"], "22.4L", "気体の種類によらず、標準状態では1molの気体は約22.4Lの体積を占めます。"),
    ("1Lの水にNaClを1mol溶かした水溶液のモル濃度は？", ["1mol/L", "0.5mol/L", "2mol/L", "10mol/L"], "1mol/L", "モル濃度＝溶質の物質量÷溶液の体積(L)なので、1mol÷1L＝1mol/Lです。"),
    ("単体（例：O2やFeなど）を構成する原子の酸化数は？", ["0", "+1", "-1", "+2"], "0", "単体を構成する原子の酸化数は必ず0と決められています。"),
    ("メタン(CH4)が完全燃焼すると生成する物質は？", ["CO2とH2O", "COとH2", "CとH2O", "CO2とH2"], "CO2とH2O", "メタンが十分な酸素と反応すると、二酸化炭素と水が生成します。"),
    ("エタノールの化学式は？", ["C2H5OH", "CH3OH", "C2H4", "C2H6"], "C2H5OH", "エタノールはお酒に含まれるアルコールで、C2H5OHと表されます。"),
    ("酢酸の化学式は？", ["CH3COOH", "HCOOH", "C2H5OH", "CH3OH"], "CH3COOH", "酢酸は食酢の主成分で、水溶液は弱酸性を示します。"),
    ("ダニエル電池で使われる2種類の金属は？", ["亜鉛と銅", "鉄と銅", "亜鉛と鉛", "銀と銅"], "亜鉛と銅", "ダニエル電池は亜鉛板と銅板をそれぞれの硫酸塩水溶液に浸した電池です。"),
    ("イオン化傾向が最も大きい金属はどれ？", ["カリウム(K)", "金(Au)", "銀(Ag)", "銅(Cu)"], "カリウム(K)", "イオン化傾向はK>Ca>Na>…>Au の順に並び、カリウムは非常にイオンになりやすい金属です。"),
    ("質量パーセント濃度10%の食塩水100gに含まれる食塩は？", ["10g", "1g", "100g", "90g"], "10g", "質量パーセント濃度は溶質の質量÷溶液の質量×100なので、100g×10%＝10gです。"),
    ("0.1mol/Lの塩酸100mLに含まれるHClの物質量は？", ["0.01mol", "0.1mol", "1mol", "0.001mol"], "0.01mol", "物質量＝モル濃度×体積(L)なので、0.1mol/L×0.1L＝0.01molです。"),
    ("中和滴定で使われる指示薬の一つは？", ["フェノールフタレイン", "リトマス紙のみ", "塩化コバルト紙", "でんぷん"], "フェノールフタレイン", "フェノールフタレインは中性〜酸性で無色、アルカリ性で赤色になる指示薬です。"),
    ("強酸と強塩基がちょうど中和すると生じる塩の水溶液は？", ["中性", "酸性", "アルカリ性", "不安定"], "中性", "強酸と強塩基が過不足なく中和すると、生じる塩の水溶液は中性になります。"),
    ("平衡が移動する向きに関する原理を何という？", ["ルシャトリエの原理", "アボガドロの法則", "ボイルの法則", "質量保存の法則"], "ルシャトリエの原理", "ルシャトリエの原理は、外部条件の変化に対して平衡がそれを打ち消す方向に移動するという原理です。"),
    ("反応が進むときに熱を放出する反応を何という？", ["発熱反応", "吸熱反応", "中和反応", "電離反応"], "発熱反応", "発熱反応は反応が進むにつれて周囲に熱を放出する反応です。"),
    ("反応が進むときに熱を吸収する反応を何という？", ["吸熱反応", "発熱反応", "酸化反応", "還元反応"], "吸熱反応", "吸熱反応は反応が進むために周囲から熱を吸収する反応です。"),
    ("電池の負極で一般に起こる反応は？", ["酸化", "還元", "中和", "電離"], "酸化", "電池の負極ではイオン化傾向の大きい金属が電子を放出する酸化反応が起こります。"),
    ("電池の正極で一般に起こる反応は？", ["還元", "酸化", "中和", "電離"], "還元", "電池の正極では負極から流れてきた電子を受け取る還元反応が起こります。"),
    ("炭素骨格が環状になっている有機化合物を何という？", ["環式化合物", "鎖式化合物", "無機化合物", "高分子化合物"], "環式化合物", "炭素原子が輪のようにつながった構造を持つ有機化合物を環式化合物といいます。"),
    ("0.2mol/Lの水酸化ナトリウム水溶液250mLに含まれるNaOHの物質量は？", ["0.05mol", "0.5mol", "0.005mol", "5mol"], "0.05mol", "0.2mol/L×0.25L＝0.05molです。"),
    ("アボガドロの法則が示すのは？", ["同温同圧同体積の気体は同じ数の分子を含む", "気体の体積は圧力に反比例する", "気体の体積は温度に比例する", "反応熱は一定である"], "同温同圧同体積の気体は同じ数の分子を含む", "アボガドロの法則は、気体の種類によらず同温同圧同体積であれば分子の数が等しいというものです。"),
    ("ボイルの法則が示すのは？", ["一定温度で気体の体積は圧力に反比例する", "一定圧力で気体の体積は温度に比例する", "気体の質量は保存される", "気体の密度は一定"], "一定温度で気体の体積は圧力に反比例する", "ボイルの法則は温度が一定のとき、気体の体積が圧力に反比例することを示します。"),
    ("シャルルの法則が示すのは？", ["一定圧力で気体の体積は絶対温度に比例する", "一定温度で気体の体積は圧力に反比例する", "気体の質量は保存される", "気体の密度は一定"], "一定圧力で気体の体積は絶対温度に比例する", "シャルルの法則は圧力が一定のとき、気体の体積が絶対温度に比例することを示します。"),
    ("有機化合物で炭素原子間がすべて単結合のものを何という？", ["飽和化合物", "不飽和化合物", "芳香族化合物", "無機化合物"], "飽和化合物", "炭素原子間の結合がすべて単結合の化合物を飽和化合物といいます。"),
    ("炭素原子間に二重結合や三重結合を含むものを何という？", ["不飽和化合物", "飽和化合物", "無機化合物", "単体"], "不飽和化合物", "二重結合や三重結合を含む化合物を不飽和化合物といいます。"),
    ("けん化反応で油脂と反応させる物質は？", ["水酸化ナトリウム", "塩酸", "硫酸", "アンモニア"], "水酸化ナトリウム", "油脂を水酸化ナトリウムと反応させると、せっけん（脂肪酸ナトリウム）とグリセリンが生じます。"),
    ("タンパク質を構成する基本単位は？", ["アミノ酸", "グルコース", "脂肪酸", "ヌクレオチド"], "アミノ酸", "タンパク質は多数のアミノ酸がつながってできた高分子です。"),
    ("デンプンやセルロースのような高分子を何という？", ["多糖類", "単糖類", "二糖類", "アミノ酸"], "多糖類", "多くの糖（単糖）が結合してできた高分子を多糖類といいます。"),
    ("化学反応の速さは温度が高くなると一般に？", ["速くなる", "遅くなる", "変わらない", "止まる"], "速くなる", "温度が高くなると分子の運動が活発になり、反応速度は一般に速くなります。"),
]

LEVELS = {
    1: ("初級", LEVEL1_QUESTIONS, "#ffe1ef"),   # 桜色
    2: ("中級", LEVEL2_QUESTIONS, "#dff7e6"),   # ミントグリーン
    3: ("上級", LEVEL3_QUESTIONS, "#fff4d6"),   # レモンイエロー
    4: ("超級", LEVEL4_QUESTIONS, "#e3e0ff"),   # ラベンダー
}

MAX_STREAK_FOR_BRIGHTNESS = 8  # このくらい連続正解すると最大の明るさになる

# =========================================================
# アイテム定義（5種類）
# =========================================================
ITEMS = {
    "hint":   {"name": "💡 ヒント",         "cost": 8,  "desc": "はずれの選択肢を2つ消します"},
    "reveal": {"name": "✨ 全消しヒント",     "cost": 22, "desc": "はずれの選択肢を全部消して正解だけにします"},
    "skip":   {"name": "⏭ スキップ",        "cost": 12, "desc": "この問題を飛ばします（コインは増えません）"},
    "shield": {"name": "🛡 シールド",        "cost": 15, "desc": "1回だけ不正解を無効にして連続正解を守ります"},
    "double": {"name": "🪙 ダブルコイン",     "cost": 10, "desc": "次に正解した時のコインが2倍になります"},
}

SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chemistry_save.json")


# =========================================================
# セーブデータ読み書き
# =========================================================
def load_save():
    default = {"coins": 0, "inventory": {k: 0 for k in ITEMS}}
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


def disable_browser_translation():
    """
    ブラウザの自動翻訳（Google翻訳など）が化学式（H2Oなど）を
    勝手に翻訳・書き換えてしまい、選択肢が読み取れなくなる問題への対策。
    ページ全体と、ボタン要素に「翻訳しない」指示を付与する。
    """
    st.markdown(
        """
        <meta name="google" content="notranslate">
        <script>
        (function() {
            try {
                document.documentElement.setAttribute('translate', 'no');
                document.documentElement.classList.add('notranslate');

                if (!document.querySelector('meta[name="google"]')) {
                    var meta = document.createElement('meta');
                    meta.name = 'google';
                    meta.content = 'notranslate';
                    document.head.appendChild(meta);
                }

                function markNoTranslate() {
                    document.querySelectorAll('button, .stMarkdown, p, h1, h2, h3').forEach(function (el) {
                        el.setAttribute('translate', 'no');
                        el.classList.add('notranslate');
                    });
                }
                markNoTranslate();
                setTimeout(markNoTranslate, 300);
                setTimeout(markNoTranslate, 1000);
            } catch (e) {
                // 何もしない（対応できないブラウザでも壊れないように）
            }
        })();
        </script>
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
    st.session_state.quit_early = False

    st.session_state.shield_active = False
    st.session_state.double_active = False
    st.session_state.choices_locked_this_q = False  # ヒント/全消しを使用済みか
    st.session_state.disabled_choices = []
    st.session_state.current_choices = []
    st.session_state.current_answer = None
    st.session_state.current_explanation = ""
    st.session_state.answered = False
    st.session_state.feedback_text = ""
    st.session_state.feedback_color = "black"
    st.session_state.prepared_q_index = -1
    st.session_state.confirm_quit = False

    st.session_state.initialized = True


def prepare_question():
    """現在の q_index の問題の選択肢をシャッフルして保持する"""
    if st.session_state.prepared_q_index == st.session_state.q_index:
        return
    if st.session_state.q_index >= len(st.session_state.questions):
        return
    _, choices, answer, explanation = st.session_state.questions[st.session_state.q_index]
    shuffled = choices[:]
    random.shuffle(shuffled)
    st.session_state.current_choices = shuffled
    st.session_state.current_answer = answer
    st.session_state.current_explanation = explanation
    st.session_state.disabled_choices = []
    st.session_state.choices_locked_this_q = False
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
    st.session_state.double_active = False
    st.session_state.prepared_q_index = -1
    st.session_state.quit_early = False
    st.session_state.confirm_quit = False
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
        if st.session_state.double_active:
            earned *= 2
            st.session_state.double_active = False
            bonus_msg = "（ダブルコイン発動！）"
        else:
            bonus_msg = ""
        st.session_state.coins += earned
        st.session_state.coins_earned_session += earned
        st.session_state.feedback_text = f"○ 正解！　+{earned} コイン {bonus_msg}"
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
    if st.session_state.choices_locked_this_q or st.session_state.inventory.get("hint", 0) <= 0:
        return
    wrong = [c for c in st.session_state.current_choices if c != st.session_state.current_answer]
    random.shuffle(wrong)
    st.session_state.disabled_choices = wrong[:2]
    st.session_state.inventory["hint"] -= 1
    st.session_state.choices_locked_this_q = True
    write_save()


def use_reveal():
    if st.session_state.choices_locked_this_q or st.session_state.inventory.get("reveal", 0) <= 0:
        return
    wrong = [c for c in st.session_state.current_choices if c != st.session_state.current_answer]
    st.session_state.disabled_choices = wrong
    st.session_state.inventory["reveal"] -= 1
    st.session_state.choices_locked_this_q = True
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


def use_double():
    if st.session_state.double_active or st.session_state.inventory.get("double", 0) <= 0:
        return
    st.session_state.inventory["double"] -= 1
    st.session_state.double_active = True
    write_save()


def buy_item(item_id):
    cost = ITEMS[item_id]["cost"]
    if st.session_state.coins >= cost:
        st.session_state.coins -= cost
        st.session_state.inventory[item_id] = st.session_state.inventory.get(item_id, 0) + 1
        write_save()


def discard_item(item_id):
    if st.session_state.inventory.get(item_id, 0) > 0:
        st.session_state.inventory[item_id] -= 1
        write_save()


# =========================================================
# 画面：スタート
# =========================================================
def render_start_screen():
    apply_background("#f5f7ff")
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
    apply_background("#f5f7ff")
    st.title("🛒 ショップ")
    st.markdown(f"### 所持コイン：🪙 {st.session_state.coins} 枚")

    for item_id, info in ITEMS.items():
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{info['name']}**　（{info['cost']}コイン）")
                st.caption(info["desc"])
                st.write(f"所持数：{st.session_state.inventory.get(item_id, 0)} 個")
            with col2:
                disabled = st.session_state.coins < info["cost"]
                if st.button("購入する", key=f"buy_{item_id}", disabled=disabled, use_container_width=True):
                    buy_item(item_id)
                    st.rerun()
            with col3:
                owned = st.session_state.inventory.get(item_id, 0) <= 0
                if st.button("捨てる", key=f"discard_{item_id}", disabled=owned, use_container_width=True):
                    discard_item(item_id)
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

    # ----- 途中でやめる確認ダイアログ -----
    if st.session_state.confirm_quit:
        st.warning("本当にここでやめますか？ここまでの結果が記録されます。")
        c_yes, c_no = st.columns(2)
        with c_yes:
            if st.button("はい、やめる", use_container_width=True):
                st.session_state.quit_early = True
                st.session_state.confirm_quit = False
                st.session_state.screen = "result"
                st.rerun()
        with c_no:
            if st.button("いいえ、続ける", use_container_width=True):
                st.session_state.confirm_quit = False
                st.rerun()
        return

    status_line = (
        f"**【{name}】** 第{st.session_state.q_index + 1}問 / 全{total}問　　"
        f"得点: {st.session_state.score}　　連続正解: {st.session_state.streak}　　"
        f"🪙 コイン: {st.session_state.coins}"
    )
    if st.session_state.shield_active:
        status_line += "　　🛡 シールド発動中"
    if st.session_state.double_active:
        status_line += "　　🪙 ダブルコイン待機中"

    st.markdown(status_line)
    st.progress(st.session_state.q_index / total)

    question, _, _, _ = st.session_state.questions[st.session_state.q_index]
    st.markdown(
        f"<h2 translate='no' class='notranslate'>{question}</h2>",
        unsafe_allow_html=True,
    )

    if st.session_state.feedback_text:
        st.markdown(
            f"<p style='color:{st.session_state.feedback_color}; font-size:18px; font-weight:bold;'>"
            f"{st.session_state.feedback_text}</p>",
            unsafe_allow_html=True,
        )
        st.info(f"📘 解説：{st.session_state.current_explanation}")

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
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        n = st.session_state.inventory.get("hint", 0)
        if st.button(f"💡\n{n}", disabled=(n <= 0 or st.session_state.choices_locked_this_q or st.session_state.answered),
                     use_container_width=True, help=ITEMS["hint"]["desc"]):
            use_hint()
            st.rerun()

    with c2:
        n = st.session_state.inventory.get("reveal", 0)
        if st.button(f"✨\n{n}", disabled=(n <= 0 or st.session_state.choices_locked_this_q or st.session_state.answered),
                     use_container_width=True, help=ITEMS["reveal"]["desc"]):
            use_reveal()
            st.rerun()

    with c3:
        n = st.session_state.inventory.get("skip", 0)
        if st.button(f"⏭\n{n}", disabled=(n <= 0 or st.session_state.answered),
                     use_container_width=True, help=ITEMS["skip"]["desc"]):
            use_skip()
            st.rerun()

    with c4:
        n = st.session_state.inventory.get("shield", 0)
        if st.button(f"🛡\n{n}", disabled=(st.session_state.shield_active or n <= 0),
                     use_container_width=True, help=ITEMS["shield"]["desc"]):
            use_shield()
            st.rerun()

    with c5:
        n = st.session_state.inventory.get("double", 0)
        if st.button(f"🪙x2\n{n}", disabled=(st.session_state.double_active or n <= 0),
                     use_container_width=True, help=ITEMS["double"]["desc"]):
            use_double()
            st.rerun()

    st.write("")
    if st.button("🚪 途中でやめる", use_container_width=True):
        st.session_state.confirm_quit = True
        st.rerun()


# =========================================================
# 画面：結果
# =========================================================
def render_result_screen():
    apply_background(st.session_state.base_color)
    name, _, _ = LEVELS[st.session_state.level]
    total = len(st.session_state.questions)
    answered_count = st.session_state.q_index if st.session_state.quit_early else total
    rate = 0 if answered_count == 0 else round(st.session_state.score / answered_count * 100)

    if st.session_state.quit_early:
        st.title("🚪 途中結果")
        st.write(f"第{answered_count}問目でやめました。")
    else:
        st.title("🎉 結果発表")

    st.markdown(f"### モード：{name}")
    st.markdown(f"### 得点：{st.session_state.score} / {answered_count}　（正答率 {rate}%）")
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
    disable_browser_translation()
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