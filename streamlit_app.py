# -*- coding: utf-8 -*-
"""
化学クイズゲーム（Streamlit版・解説つき）
--------------------------------------------
実行方法:
    pip install streamlit
    streamlit run chemistry_game_streamlit.py

・4段階の難易度モード（初級／中級／上級／超級）
・各モードたくさんの問題（合計150問）
・すべての問題に解説つき（回答後に表示）
・連続正解するほど背景がだんだん明るくなる（レベルごとに配色を変更）
・正解するとコインがたまり、ショップでアイテムが買える
    - ヒント：はずれの選択肢を2つ消す
    - 全消しヒント：はずれの選択肢を全部消して正解だけにする
    - スキップ：この問題を飛ばす
    - シールド：1回だけ不正解を無効にして連続正解を守る
    - ダブルコイン：次に正解した時のコインが2倍になる
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
    ("水素の元素記号は？", ["H", "He", "Hg", "N"], "H", "水素は原子番号1で、宇宙で最も多い元素です。"),
    ("酸素の元素記号は？", ["O", "Os", "Ox", "On"], "O", "酸素は原子番号8で、呼吸や燃焼に欠かせない気体です。"),
    ("水の化学式は？", ["H2O", "CO2", "NaCl", "O2"], "H2O", "水は水素原子2個と酸素原子1個が結びついた分子です。"),
    ("二酸化炭素の化学式は？", ["CO2", "CO", "O2", "H2O"], "CO2", "炭素原子1個に酸素原子2個が結合しており、石灰水を白く濁らせます。"),
    ("食塩（塩化ナトリウム）の化学式は？", ["NaCl", "NaOH", "KCl", "CaCl2"], "NaCl", "ナトリウムイオンと塩化物イオンが結びついたイオン結晶です。"),
    ("ヘリウムの元素記号は？", ["He", "H", "Ne", "Li"], "He", "原子番号2の貴ガスで、反応しにくく風船などに使われます。"),
    ("炭素の元素記号は？", ["C", "Ca", "Cl", "Co"], "C", "原子番号6で、有機化合物や生命の主要な構成元素です。"),
    ("窒素の元素記号は？", ["N", "Na", "Ne", "Ni"], "N", "原子番号7で、空気の体積の約78%を占めます。"),
    ("ナトリウムの元素記号は？", ["Na", "N", "Ni", "Ne"], "Na", "原子番号11のアルカリ金属で、水と激しく反応します。"),
    ("鉄の元素記号は？", ["Fe", "F", "Ir", "Fr"], "Fe", "原子番号26で、鋼などの主原料として広く使われます。"),
    ("金の元素記号は？", ["Au", "Ag", "Al", "Ar"], "Au", "原子番号79の貴金属で、化学的に非常に安定しています。"),
    ("銀の元素記号は？", ["Ag", "Au", "Al", "As"], "Ag", "原子番号47で、金属の中で電気伝導性が最も高いです。"),
    ("銅の元素記号は？", ["Cu", "Co", "Ca", "Cr"], "Cu", "原子番号29で、電線や硬貨などに使われます。"),
    ("カルシウムの元素記号は？", ["Ca", "Cu", "Cl", "C"], "Ca", "原子番号20で、骨や歯の主成分です。"),
    ("塩素の元素記号は？", ["Cl", "C", "Ca", "Co"], "Cl", "原子番号17のハロゲンで、殺菌・漂白に使われます。"),
    ("アルミニウムの元素記号は？", ["Al", "Ar", "Au", "As"], "Al", "原子番号13で、軽くてさびにくい金属です。"),
    ("硫黄の元素記号は？", ["S", "Si", "Sn", "Sr"], "S", "原子番号16で、火山地帯などで黄色い固体として見られます。"),
    ("カリウムの元素記号は？", ["K", "Ca", "Kr", "Co"], "K", "原子番号19のアルカリ金属で、肥料などに使われます。"),
    ("亜鉛の元素記号は？", ["Zn", "Ni", "Sn", "Pb"], "Zn", "原子番号30で、乾電池やめっきに使われます。"),
    ("物質を構成する最小単位を何という？", ["原子", "分子", "細胞", "元素記号"], "原子", "原子は原子核と電子からなる、物質を構成する最小単位です。"),
    ("リチウムの元素記号は？", ["Li", "La", "Lr", "Lv"], "Li", "原子番号3で、最も軽い金属でリチウム電池にも使われます。"),
    ("マグネシウムの元素記号は？", ["Mg", "Mn", "Mo", "Md"], "Mg", "原子番号12で、軽量合金や葉緑素にも含まれます。"),
    ("フッ素の元素記号は？", ["F", "Fe", "Fr", "Fm"], "F", "原子番号9で、反応性が非常に高いハロゲンです。"),
    ("ネオンの元素記号は？", ["Ne", "N", "Na", "Ni"], "Ne", "原子番号10の貴ガスで、ネオンサインに使われます。"),
    ("臭素の元素記号は？", ["Br", "B", "Ba", "Bi"], "Br", "原子番号35で、常温で液体として存在する数少ない非金属です。"),
    ("ヨウ素の元素記号は？", ["I", "In", "Ir", "Y"], "I", "原子番号53のハロゲンで、うがい薬などにも使われます。"),
    ("ケイ素の元素記号は？", ["Si", "S", "Se", "Sn"], "Si", "原子番号14で、半導体や砂（ガラス）の主成分です。"),
    ("リンの元素記号は？", ["P", "Pb", "Pt", "Po"], "P", "原子番号15で、DNAや骨にも含まれる重要な元素です。"),
    ("鉛の元素記号は？", ["Pb", "P", "Pt", "Po"], "Pb", "原子番号82の重金属で、鉛蓄電池などに使われます。"),
    ("水銀の元素記号は？", ["Hg", "H", "He", "Ho"], "Hg", "原子番号80で、常温で液体である唯一の金属です。"),
    ("アルゴンの元素記号は？", ["Ar", "Al", "Au", "As"], "Ar", "原子番号18の貴ガスで、空気中に約1%含まれます。"),
    ("バリウムの元素記号は？", ["Ba", "Br", "B", "Bi"], "Ba", "原子番号56で、レントゲン検査（バリウム検査）に使われます。"),
    ("マンガンの元素記号は？", ["Mn", "Mg", "Mo", "Md"], "Mn", "原子番号25で、乾電池や鋼の強化剤として使われます。"),
    ("コバルトの元素記号は？", ["Co", "Cu", "Cr", "Ca"], "Co", "原子番号27で、青色顔料やリチウムイオン電池に使われます。"),
    ("ニッケルの元素記号は？", ["Ni", "Na", "Ne", "N"], "Ni", "原子番号28で、ステンレスやニッケル水素電池に使われます。"),
    ("スズの元素記号は？", ["Sn", "S", "Si", "Sr"], "Sn", "原子番号50で、はんだやブリキに使われる金属です。"),
    ("クロムの元素記号は？", ["Cr", "Co", "Cu", "Ca"], "Cr", "原子番号24で、ステンレス鋼の耐食性のもとになります。"),
    ("チタンの元素記号は？", ["Ti", "Sn", "Ta", "Te"], "Ti", "原子番号22で、軽くて丈夫なため航空機や人工関節に使われます。"),
    ("ヒ素の元素記号は？", ["As", "Ag", "Al", "Au"], "As", "原子番号33の半金属元素で、毒性があることで知られます。"),
    ("白金（プラチナ）の元素記号は？", ["Pt", "Pb", "Po", "P"], "Pt", "原子番号78の貴金属で、触媒や宝飾品に使われます。"),
]

LEVEL2_QUESTIONS = [
    ("メタンの化学式は？", ["CH4", "C2H6", "CO2", "NH3"], "CH4", "メタンは天然ガスの主成分で、最も単純な炭化水素です。"),
    ("アンモニアの化学式は？", ["NH3", "NO2", "N2O", "HN3"], "NH3", "刺激臭のある気体で、肥料の原料として大量に作られます。"),
    ("硫酸の化学式は？", ["H2SO4", "HCl", "HNO3", "H2SO3"], "H2SO4", "強酸の代表で、鉛蓄電池の電解液にも使われます。"),
    ("塩酸の主成分は？", ["HCl", "H2SO4", "NaOH", "HNO3"], "HCl", "塩化水素が水に溶けたもので、胃液にも含まれます。"),
    ("水酸化ナトリウムの化学式は？", ["NaOH", "NaCl", "Na2O", "NaHCO3"], "NaOH", "強い塩基性を示し、せっけん作りなどにも使われます。"),
    ("酸とアルカリが反応することを何という？", ["中和", "酸化", "還元", "電離"], "中和", "酸と塩基が反応して、塩と水ができる反応です。"),
    ("ものが燃える（完全燃焼）と主に発生する気体は？", ["二酸化炭素", "酸素", "水素", "窒素"], "二酸化炭素", "炭素が酸素と結びついて二酸化炭素が生成します。"),
    ("pHが7のとき溶液は？", ["中性", "酸性", "アルカリ性", "不明"], "中性", "水素イオン濃度と水酸化物イオン濃度が等しい状態です。"),
    ("pHが7より小さいと溶液は？", ["酸性", "アルカリ性", "中性", "中和"], "酸性", "水素イオン濃度が高いほどpHは小さくなります。"),
    ("pHが7より大きいと溶液は？", ["アルカリ性", "酸性", "中性", "中和"], "アルカリ性", "水酸化物イオン濃度が高いほどpHは大きくなります。"),
    ("原子核を構成する粒子は陽子と何？", ["中性子", "電子", "イオン", "分子"], "中性子", "中性子は電荷を持たず、陽子とともに原子核を作ります。"),
    ("電子が持つ電荷は？", ["負（マイナス）", "正（プラス）", "電荷なし", "不定"], "負（マイナス）", "電子は原子核の周りを回る負電荷の粒子です。"),
    ("陽子が持つ電荷は？", ["正（プラス）", "負（マイナス）", "電荷なし", "不定"], "正（プラス）", "陽子は原子核を構成する正電荷の粒子です。"),
    ("原子番号は何の数を表す？", ["陽子の数", "中性子の数", "電子殻の数", "分子の数"], "陽子の数", "原子番号は原子核の中の陽子の数と一致します。"),
    ("陽子の数が同じで中性子の数が異なる原子どうしを何という？", ["同位体", "同素体", "異性体", "同族体"], "同位体", "同位体は化学的性質はほぼ同じで、質量が異なります。"),
    ("炭素の同素体でないものは？", ["食塩", "ダイヤモンド", "黒鉛", "フラーレン"], "食塩", "食塩(NaCl)は化合物で、炭素の単体である同素体ではありません。"),
    ("金属が電子を放出してできるイオンを何という？", ["陽イオン", "陰イオン", "中性子", "分子イオン"], "陽イオン", "電子を失うと正の電荷を帯びた陽イオンになります。"),
    ("塩素原子が電子を受け取ってできるイオンを何という？", ["陰イオン", "陽イオン", "中性子", "同位体"], "陰イオン", "電子を受け取ると負の電荷を帯びた陰イオンになります。"),
    ("水溶液に電流が流れる物質を何という？", ["電解質", "非電解質", "触媒", "同位体"], "電解質", "水に溶けるとイオンに分かれ、電流を通す物質です。"),
    ("砂糖水のように電流が流れない物質を何という？", ["非電解質", "電解質", "酸", "塩基"], "非電解質", "水に溶けてもイオンにならないため電流を通しません。"),
    ("過酸化水素の化学式は？", ["H2O2", "H2O", "HO2", "H3O2"], "H2O2", "消毒や漂白に使われる酸化力の強い物質です。"),
    ("二酸化硫黄の化学式は？", ["SO2", "SO3", "S2O", "H2SO3"], "SO2", "刺激臭のある気体で、酸性雨の原因の一つです。"),
    ("一酸化炭素の化学式は？", ["CO", "CO2", "C2O", "COOH"], "CO", "不完全燃焼で生じる、無色・無臭で有毒な気体です。"),
    ("塩化水素が水に溶けたものを何という？", ["塩酸", "硫酸", "硝酸", "炭酸"], "塩酸", "気体の塩化水素が水に溶けると塩酸（強酸）になります。"),
    ("酸化カルシウムの別名は？", ["生石灰", "消石灰", "石灰水", "炭酸カルシウム"], "生石灰", "酸化カルシウム(CaO)は生石灰と呼ばれ、乾燥剤にも使われます。"),
    ("水酸化カルシウムの別名は？", ["消石灰", "生石灰", "石灰石", "セッコウ"], "消石灰", "生石灰に水を加えると消石灰(Ca(OH)2)ができます。"),
    ("石灰水に二酸化炭素を通すとどうなる？", ["白く濁る", "赤くなる", "透明になる", "気体が消える"], "白く濁る", "二酸化炭素と水酸化カルシウムが反応し、炭酸カルシウムの白い沈殿ができます。"),
    ("金属が酸に溶けるとき多くの場合発生する気体は？", ["水素", "酸素", "窒素", "二酸化炭素"], "水素", "亜鉛やマグネシウムなどは酸と反応して水素を発生します。"),
    ("燃焼に必ず必要な気体は？", ["酸素", "窒素", "水素", "二酸化炭素"], "酸素", "燃焼は物質が酸素と結びつく激しい酸化反応です。"),
    ("空気中で体積の割合が最も多い気体は？", ["窒素", "酸素", "二酸化炭素", "アルゴン"], "窒素", "空気の約78%は窒素、約21%は酸素です。"),
    ("硫化水素の化学式は？", ["H2S", "SO2", "H2SO4", "S2"], "H2S", "卵が腐ったような臭いがする有毒な気体です。"),
    ("二酸化窒素の化学式は？", ["NO2", "NO", "N2O", "HNO3"], "NO2", "赤褐色の気体で、大気汚染の原因物質の一つです。"),
    ("一酸化窒素の化学式は？", ["NO", "NO2", "N2O", "N2O3"], "NO", "無色の気体で、体内では血管を広げる働きも持ちます。"),
    ("炭酸の化学式は？", ["H2CO3", "CO2", "HCO3", "CaCO3"], "H2CO3", "二酸化炭素が水に溶けてできる弱い酸です。"),
    ("リン酸の化学式は？", ["H3PO4", "HPO3", "P2O5", "H3PO3"], "H3PO4", "肥料や食品添加物としても利用される酸です。"),
    ("水酸化カリウムの化学式は？", ["KOH", "K2O", "KCl", "KHCO3"], "KOH", "NaOHと同じく強い塩基性を示す物質です。"),
    ("アンモニア水は何性？", ["アルカリ性", "酸性", "中性", "不定"], "アルカリ性", "アンモニアは水に溶けると弱塩基性を示します。"),
    ("酢酸水溶液は何性？", ["酸性", "アルカリ性", "中性", "不定"], "酸性", "酢酸はカルボン酸の一種で、酸性を示します。"),
    ("中性の水溶液のpHはいくつ？", ["7", "0", "14", "1"], "7", "pH7が中性で、それより小さいと酸性、大きいとアルカリ性です。"),
    ("うすい塩酸にマグネシウムを入れると発生する気体は？", ["水素", "酸素", "二酸化炭素", "窒素"], "水素", "マグネシウムが塩酸と反応し、水素が発生します。"),
]

LEVEL3_QUESTIONS = [
    ("水の生成反応式は？ 2H2 + O2 →", ["2H2O", "H2O2", "2H2O2", "HO2"], "2H2O", "水素分子2個と酸素分子1個が反応して、水分子2個ができます。"),
    ("物質量（molの単位）が表すものは？", ["粒子の数の集まり", "重さ", "体積", "温度"], "粒子の数の集まり", "molは原子や分子など粒子の集団の数を表す単位です。"),
    ("1molに含まれる粒子の数（アボガドロ数）は約？", ["6.02×10の23乗", "3.14×10の8乗", "9.8×10の10乗", "1.0×10の6乗"], "6.02×10の23乗", "アボガドロ定数と呼ばれ、molの基準になる数値です。"),
    ("酸素と結びつく化学変化を何という？", ["酸化", "還元", "中和", "電離"], "酸化", "物質が酸素と結びつく、または電子を失う変化です。"),
    ("酸化物から酸素を奪う化学変化を何という？", ["還元", "酸化", "中和", "電離"], "還元", "酸化物が酸素を失う、または電子を得る変化です。"),
    ("塩化ナトリウムの結晶を作る結合は？", ["イオン結合", "共有結合", "金属結合", "水素結合"], "イオン結合", "陽イオンと陰イオンが静電気力で結びついています。"),
    ("水分子（H2O）を作る結合は？", ["共有結合", "イオン結合", "金属結合", "配位結合のみ"], "共有結合", "原子同士が電子を共有してできる結合です。"),
    ("周期表で縦の列（同じ族）の元素は性質が？", ["似ている", "全く異なる", "関係ない", "反応しない"], "似ている", "同じ族の元素は最外殻電子の数が同じで性質が似ています。"),
    ("ヘリウムやネオンなど反応しにくい気体を何という？", ["貴ガス（希ガス）", "ハロゲン", "アルカリ金属", "遷移金属"], "貴ガス（希ガス）", "最外殻電子が満たされているため、非常に安定しています。"),
    ("化学反応の速さを変えるが自身は変化しない物質は？", ["触媒", "溶媒", "溶質", "指示薬"], "触媒", "反応の活性化エネルギーを下げますが、自身は変化しません。"),
    ("塩酸と水酸化ナトリウム水溶液を混ぜると生じる塩は？", ["塩化ナトリウム", "硫酸ナトリウム", "炭酸ナトリウム", "硝酸ナトリウム"], "塩化ナトリウム", "HClの塩化物イオンとNaOHのナトリウムイオンが結びつきます。"),
    ("酸化銀を加熱すると発生する気体は？", ["酸素", "水素", "二酸化炭素", "窒素"], "酸素", "酸化銀は熱分解すると銀と酸素に分かれます。"),
    ("塩酸に亜鉛を入れると発生する気体は？", ["水素", "酸素", "二酸化炭素", "塩素"], "水素", "亜鉛が塩酸中の水素イオンと反応して水素が発生します。"),
    ("炭酸水素ナトリウムを加熱すると発生する気体は？", ["二酸化炭素", "酸素", "水素", "アンモニア"], "二酸化炭素", "重曹（炭酸水素ナトリウム）の熱分解で二酸化炭素が発生します。"),
    ("BTB溶液が酸性で示す色は？", ["黄色", "青色", "緑色", "赤色"], "黄色", "BTB溶液は酸性で黄色、中性で緑色、アルカリ性で青色になります。"),
    ("二酸化炭素の分子の形は？", ["直線形", "折れ線形", "三角形", "正四面体形"], "直線形", "O=C=Oが一直線に並んだ構造をしています。"),
    ("メタン分子の形は？", ["正四面体形", "直線形", "折れ線形", "平面三角形"], "正四面体形", "中心の炭素原子に4個の水素原子が均等に結合しています。"),
    ("イオン結晶の一般的な特徴は？", ["硬くてもろい", "やわらかくて伸びる", "電気を通しやすい液体状", "気体になりやすい"], "硬くてもろい", "強い静電気力で硬いですが、ずれると反発し割れやすいです。"),
    ("金属特有の光沢や展延性のもとになる結合は？", ["金属結合", "イオン結合", "共有結合", "水素結合"], "金属結合", "自由電子が金属イオン全体をつなぎとめている結合です。"),
    ("電子親和力が大きい元素ほど？", ["陰イオンになりやすい", "陽イオンになりやすい", "反応しにくい", "金属になりやすい"], "陰イオンになりやすい", "電子を受け取りやすいため、陰イオンになりやすくなります。"),
    ("イオン化エネルギーが小さい元素ほど？", ["陽イオンになりやすい", "陰イオンになりやすい", "反応しにくい", "非金属になりやすい"], "陽イオンになりやすい", "電子を放出しやすいため、陽イオンになりやすくなります。"),
    ("ハロゲンに分類される元素は？", ["塩素", "ナトリウム", "鉄", "ヘリウム"], "塩素", "ハロゲンは周期表の17族に属する元素です。"),
    ("アルカリ金属に分類される元素は？", ["ナトリウム", "塩素", "ヘリウム", "鉄"], "ナトリウム", "アルカリ金属は周期表の1族に属する元素です。"),
    ("遷移元素に分類される元素は？", ["鉄", "ナトリウム", "塩素", "ヘリウム"], "鉄", "遷移元素は周期表の中央付近に位置する金属元素です。"),
    ("化学反応式の係数は何を表す？", ["物質の粒子（分子・イオン）の数の比", "反応にかかる時間", "物質の色", "反応の温度"], "物質の粒子（分子・イオン）の数の比", "係数は反応に関わる粒子の数の割合を示しています。"),
    ("化学反応の前後で物質の総質量は変わらないという法則は？", ["質量保存の法則", "定比例の法則", "気体反応の法則", "倍数比例の法則"], "質量保存の法則", "反応の前後で原子の種類と数は変わらないため、質量も変わりません。"),
    ("一つの化合物中の成分元素の質量比は常に一定という法則は？", ["定比例の法則", "質量保存の法則", "気体反応の法則", "ボイルの法則"], "定比例の法則", "プルーストが発見した法則で、化合物の組成は常に一定です。"),
    ("原子核に最も近い電子殻を何という？", ["K殻", "L殻", "M殻", "N殻"], "K殻", "電子殻は内側からK殻・L殻・M殻…と名付けられています。"),
    ("最外殻電子のうち化学結合に関わる電子を何という？", ["価電子", "自由電子", "内殻電子", "共有電子"], "価電子", "価電子の数が原子の化学的性質を大きく左右します。"),
    ("貴ガス（希ガス）の最外殻電子の状態は？", ["安定している（閉殻）", "反応しやすい", "不安定", "常に1個だけ"], "安定している（閉殻）", "最外殻が電子で満たされているため、非常に安定しています。"),
    ("分子結晶（例：ドライアイス）の一般的な特徴は？", ["融点が低い", "非常に硬い", "電気をよく通す", "延性に富む"], "融点が低い", "分子間力が弱いため、比較的低い温度で融けたり昇華したりします。"),
    ("共有結合の結晶（例：ダイヤモンド）の特徴は？", ["非常に硬い", "やわらかい", "電気をよく通す", "融点が低い"], "非常に硬い", "共有結合が網目状に広がっているため非常に硬くなります。"),
    ("水溶液の水素イオン濃度からpHを測定する器具の一つは？", ["pHメーター", "気圧計", "温度計", "比重計"], "pHメーター", "電極を使って水素イオン濃度を電気的に測定する器具です。"),
    ("弱酸・弱塩基が水溶液中で電離する割合は？", ["一部だけ電離する", "完全に電離する", "全く電離しない", "常に半分電離する"], "一部だけ電離する", "弱酸・弱塩基は平衡状態にあり、一部だけがイオンになります。"),
    ("強酸・強塩基が水溶液中で電離する割合は？", ["ほぼ完全に電離する", "一部だけ電離する", "全く電離しない", "常に半分電離する"], "ほぼ完全に電離する", "強酸・強塩基は水中でほとんどすべてがイオンに分かれます。"),
]

LEVEL4_QUESTIONS = [
    ("NaOH + HCl → NaCl + ？", ["H2O", "H2", "O2", "Cl2"], "H2O", "中和反応では塩と水が生成します。"),
    ("水（H2O）のモル質量は約18g/molである。0.5molの水の質量は？", ["9g", "18g", "36g", "4.5g"], "9g", "0.5mol × 18g/mol = 9g です。"),
    ("炭酸カルシウムの化学式は？", ["CaCO3", "CaO", "Ca(OH)2", "CaCl2"], "CaCO3", "石灰石や大理石、貝殻の主成分です。"),
    ("硝酸の化学式は？", ["HNO3", "H2SO4", "HCl", "H2CO3"], "HNO3", "強酸の一つで、肥料や火薬の原料になります。"),
    ("水を電気分解すると陰極（マイナス極）に発生する気体は？", ["水素", "酸素", "窒素", "二酸化炭素"], "水素", "陰極では水素、陽極では酸素が発生し、体積比は2:1です。"),
    ("pH2の溶液はpH5の溶液に比べて水素イオン濃度が？", ["1000倍高い", "1000倍低い", "3倍高い", "同じ"], "1000倍高い", "pHが1違うと水素イオン濃度は10倍変わるので、3違うと1000倍になります。"),
    ("気体の状態方程式 PV=？ の右辺は？", ["nRT", "mgh", "F/A", "ρV"], "nRT", "理想気体の状態方程式 PV = nRT はn(物質量)、R(気体定数)、T(温度)からなります。"),
    ("標準状態（0℃・1気圧）で気体1molが占める体積は？", ["22.4L", "1L", "100L", "18mL"], "22.4L", "気体の種類によらず、標準状態では1molが約22.4Lを占めます。"),
    ("1Lの水にNaClを1mol溶かした水溶液のモル濃度は？", ["1mol/L", "0.5mol/L", "2mol/L", "10mol/L"], "1mol/L", "モル濃度＝溶質の物質量÷溶液の体積(L)で計算します。"),
    ("単体（例：O2やFeなど）を構成する原子の酸化数は？", ["0", "+1", "-1", "+2"], "0", "単体を構成する原子の酸化数は基準として0とされます。"),
    ("メタン(CH4)が完全燃焼すると生成する物質は？", ["CO2とH2O", "COとH2", "CとH2O", "CO2とH2"], "CO2とH2O", "炭化水素の完全燃焼では、二酸化炭素と水が生成します。"),
    ("エタノールの化学式は？", ["C2H5OH", "CH3OH", "C2H4", "C2H6"], "C2H5OH", "お酒に含まれるアルコールで、消毒液としても使われます。"),
    ("酢酸の化学式は？", ["CH3COOH", "HCOOH", "C2H5OH", "CH3OH"], "CH3COOH", "食酢に含まれる代表的な弱酸（カルボン酸）です。"),
    ("ダニエル電池で使われる2種類の金属は？", ["亜鉛と銅", "鉄と銅", "亜鉛と鉛", "銀と銅"], "亜鉛と銅", "亜鉛板と銅板をそれぞれの硫酸塩水溶液に浸して電池を作ります。"),
    ("イオン化傾向が最も大きい金属はどれ？", ["カリウム(K)", "金(Au)", "銀(Ag)", "銅(Cu)"], "カリウム(K)", "イオン化列の先頭に近い金属ほど陽イオンになりやすいです。"),
    ("質量パーセント濃度10%の食塩水100gに含まれる食塩は？", ["10g", "1g", "100g", "90g"], "10g", "100g × 10% = 10g の食塩が含まれます。"),
    ("0.1mol/Lの塩酸100mLに含まれるHClの物質量は？", ["0.01mol", "0.1mol", "1mol", "0.001mol"], "0.01mol", "0.1mol/L × 0.1L(100mL) = 0.01mol です。"),
    ("中和滴定で使われる指示薬の一つは？", ["フェノールフタレイン", "リトマス紙のみ", "塩化コバルト紙", "でんぷん"], "フェノールフタレイン", "酸性・中性で無色、塩基性で赤色になる指示薬です。"),
    ("強酸と強塩基がちょうど中和すると生じる塩の水溶液は？", ["中性", "酸性", "アルカリ性", "不安定"], "中性", "強酸と強塩基が過不足なく反応すると中性の塩ができます。"),
    ("平衡が移動する向きに関する原理を何という？", ["ルシャトリエの原理", "アボガドロの法則", "ボイルの法則", "質量保存の法則"], "ルシャトリエの原理", "平衡は外部からの変化を打ち消す方向に移動するという原理です。"),
    ("反応が進むときに熱を放出する反応を何という？", ["発熱反応", "吸熱反応", "中和反応", "電離反応"], "発熱反応", "エネルギーが周囲に放出され、周りの温度が上がります。"),
    ("反応が進むときに熱を吸収する反応を何という？", ["吸熱反応", "発熱反応", "酸化反応", "還元反応"], "吸熱反応", "周囲から熱を奪うため、周りの温度が下がります。"),
    ("電池の負極で一般に起こる反応は？", ["酸化", "還元", "中和", "電離"], "酸化", "負極では金属が電子を放出する酸化反応が起こります。"),
    ("電池の正極で一般に起こる反応は？", ["還元", "酸化", "中和", "電離"], "還元", "正極では物質が電子を受け取る還元反応が起こります。"),
    ("炭素骨格が環状になっている有機化合物を何という？", ["環式化合物", "鎖式化合物", "無機化合物", "高分子化合物"], "環式化合物", "ベンゼンやシクロヘキサンなど、輪の形をした炭素骨格を持ちます。"),
    ("0.2mol/Lの水酸化ナトリウム水溶液250mLに含まれるNaOHの物質量は？", ["0.05mol", "0.5mol", "0.005mol", "5mol"], "0.05mol", "0.2mol/L × 0.25L = 0.05mol です。"),
    ("アボガドロの法則が示すのは？", ["同温同圧同体積の気体は同じ数の分子を含む", "気体の体積は圧力に反比例する", "気体の体積は温度に比例する", "反応熱は一定である"], "同温同圧同体積の気体は同じ数の分子を含む", "気体の種類によらず、条件が同じなら分子数も同じになります。"),
    ("ボイルの法則が示すのは？", ["一定温度で気体の体積は圧力に反比例する", "一定圧力で気体の体積は温度に比例する", "気体の質量は保存される", "気体の密度は一定"], "一定温度で気体の体積は圧力に反比例する", "圧力を2倍にすると体積は半分になる、という関係です。"),
    ("シャルルの法則が示すのは？", ["一定圧力で気体の体積は絶対温度に比例する", "一定温度で気体の体積は圧力に反比例する", "気体の質量は保存される", "気体の密度は一定"], "一定圧力で気体の体積は絶対温度に比例する", "温度を上げると気体の体積も比例して大きくなります。"),
    ("有機化合物で炭素原子間がすべて単結合のものを何という？", ["飽和化合物", "不飽和化合物", "芳香族化合物", "無機化合物"], "飽和化合物", "炭素間がすべて単結合で、水素の数が最大になっています。"),
    ("炭素原子間に二重結合や三重結合を含むものを何という？", ["不飽和化合物", "飽和化合物", "無機化合物", "単体"], "不飽和化合物", "二重結合・三重結合があるため、さらに水素原子と結合できます。"),
    ("けん化反応で油脂と反応させる物質は？", ["水酸化ナトリウム", "塩酸", "硫酸", "アンモニア"], "水酸化ナトリウム", "油脂を水酸化ナトリウムで加水分解すると、せっけんとグリセリンができます。"),
    ("タンパク質を構成する基本単位は？", ["アミノ酸", "グルコース", "脂肪酸", "ヌクレオチド"], "アミノ酸", "多数のアミノ酸がペプチド結合でつながってタンパク質ができます。"),
    ("デンプンやセルロースのような高分子を何という？", ["多糖類", "単糖類", "二糖類", "アミノ酸"], "多糖類", "多数の単糖（グルコースなど）がつながった高分子化合物です。"),
    ("化学反応の速さは温度が高くなると一般に？", ["速くなる", "遅くなる", "変わらない", "止まる"], "速くなる", "温度が高いほど分子の運動が活発になり、衝突回数が増えるためです。"),
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


# =========================================================
# 画面：スタート
# =========================================================
def render_start_screen():
    apply_background("#f5f7ff")
    st.title("🧪 化学クイズゲーム")
    st.markdown(f"### 所持コイン：🪙 {st.session_state.coins} 枚")
    st.write("モードを選んでください。連続正解すると背景が明るくなり、コインもたまります！")
    st.caption("全ての問題に解説つき。答え合わせのあとにチェックできます。")

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
    st.markdown(f"## {question}")

    if st.session_state.feedback_text:
        st.markdown(
            f"<p style='color:{st.session_state.feedback_color}; font-size:18px; font-weight:bold;'>"
            f"{st.session_state.feedback_text}</p>",
            unsafe_allow_html=True,
        )
        st.info(f"📖 解説：{st.session_state.current_explanation}")

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