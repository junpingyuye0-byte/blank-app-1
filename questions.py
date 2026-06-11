# questions.py — ChemLab Blast 問題データベース

# ─── レベル情報 ────────────────────────────────────────────────────────────────
LEVEL_INFO = {
    1: {
        "name": "見習い研究員",
        "icon": "🔬",
        "desc": "基礎の元素記号",
        "time": 20,
        "base_pts": 100,
    },
    2: {
        "name": "ジュニア化学者",
        "icon": "⚗️",
        "desc": "化合物と基礎反応",
        "time": 15,
        "base_pts": 200,
    },
    3: {
        "name": "シニア研究員",
        "icon": "🧪",
        "desc": "反応式・実験結果",
        "time": 12,
        "base_pts": 350,
    },
    4: {
        "name": "主任研究員",
        "icon": "💥",
        "desc": "難問・複合問題",
        "time": 10,
        "base_pts": 500,
    },
}

# ─── 問題データ ────────────────────────────────────────────────────────────────
QUESTIONS_BY_LEVEL = {

    # ══════════════════════════════════════════════════
    # Lv.1 — 基礎：元素記号・原子番号・身近な元素
    # ══════════════════════════════════════════════════
    1: [
        {
            "type": "element",
            "question": "水の化学式はどれ？",
            "options": ["H₂O", "CO₂", "NaCl", "O₂"],
            "answer": 0,
            "explanation": "水は水素(H)2個と酸素(O)1個。H₂O です。"
        },
        {
            "type": "element",
            "question": "鉄の元素記号はどれ？",
            "options": ["Fe", "Ir", "Au", "Cu"],
            "answer": 0,
            "explanation": "鉄はラテン語 Ferrum から Fe。"
        },
        {
            "type": "element",
            "question": "金の元素記号はどれ？",
            "options": ["Ag", "Pt", "Au", "Go"],
            "answer": 2,
            "explanation": "金はラテン語 Aurum から Au。"
        },
        {
            "type": "element",
            "question": "銀の元素記号はどれ？",
            "options": ["Si", "Ag", "Al", "Au"],
            "answer": 1,
            "explanation": "銀はラテン語 Argentum から Ag。"
        },
        {
            "type": "element",
            "question": "酸素の元素記号はどれ？",
            "options": ["Os", "O", "Or", "Ox"],
            "answer": 1,
            "explanation": "酸素は Oxygen → O（原子番号8）。"
        },
        {
            "type": "element",
            "question": "炭素の元素記号はどれ？",
            "options": ["Ca", "Co", "C", "Cr"],
            "answer": 2,
            "explanation": "炭素は Carbon → C（原子番号6）。"
        },
        {
            "type": "element",
            "question": "食塩（塩化ナトリウム）の化学式はどれ？",
            "options": ["NaOH", "NaCl", "KCl", "MgCl₂"],
            "answer": 1,
            "explanation": "食塩はナトリウム(Na)と塩素(Cl)の化合物 NaCl。"
        },
        {
            "type": "element",
            "question": "二酸化炭素の化学式はどれ？",
            "options": ["CO", "CO₂", "C₂O", "COH"],
            "answer": 1,
            "explanation": "二酸化炭素は炭素1個と酸素2個 → CO₂。"
        },
        {
            "type": "element",
            "question": "銅の元素記号はどれ？",
            "options": ["Co", "Cr", "Cu", "C"],
            "answer": 2,
            "explanation": "銅はラテン語 Cuprum から Cu（原子番号29）。"
        },
        {
            "type": "element",
            "question": "水素の元素記号はどれ？",
            "options": ["He", "H", "Hg", "Ho"],
            "answer": 1,
            "explanation": "水素は Hydrogen → H（原子番号1、最も軽い元素）。"
        },
        {
            "type": "element",
            "question": "窒素の元素記号はどれ？",
            "options": ["Ni", "N", "Na", "Nb"],
            "answer": 1,
            "explanation": "窒素は Nitrogen → N（空気の約78%を占める）。"
        },
        {
            "type": "element",
            "question": "ナトリウムの元素記号はどれ？",
            "options": ["N", "Na", "Ni", "No"],
            "answer": 1,
            "explanation": "ナトリウムはラテン語 Natrium → Na（原子番号11）。"
        },
        {
            "type": "element",
            "question": "アルミニウムの元素記号はどれ？",
            "options": ["Am", "Ar", "Al", "Ag"],
            "answer": 2,
            "explanation": "アルミニウムは Al（原子番号13）。地殻中で最も多い金属。"
        },
        {
            "type": "element",
            "question": "塩素の元素記号はどれ？",
            "options": ["Ca", "Cs", "Cl", "Ce"],
            "answer": 2,
            "explanation": "塩素は Chlorine → Cl（原子番号17）。"
        },
        {
            "type": "element",
            "question": "原子番号1番の元素はどれ？",
            "options": ["酸素", "ヘリウム", "炭素", "水素"],
            "answer": 3,
            "explanation": "原子番号は陽子の数。水素(H)は陽子1個で最小・最軽量。"
        },
    ],

    # ══════════════════════════════════════════════════
    # Lv.2 — 化合物・基礎反応・イオン
    # ══════════════════════════════════════════════════
    2: [
        {
            "type": "reaction",
            "question": "水素と酸素が反応して水ができる反応式として正しいのは？",
            "options": [
                "H₂ + O₂ → H₂O",
                "2H₂ + O₂ → 2H₂O",
                "H + O → H₂O",
                "H₂ + 2O → H₂O₂"
            ],
            "answer": 1,
            "explanation": "原子の数が左右で一致する必要がある。2H₂ + O₂ → 2H₂O が正しい。"
        },
        {
            "type": "reaction",
            "question": "炭素が完全燃焼するときの反応式は？",
            "options": [
                "C + O₂ → CO₂",
                "C + O → CO",
                "2C + O₂ → 2CO",
                "C + 2O → CO₂"
            ],
            "answer": 0,
            "explanation": "炭素の完全燃焼は C + O₂ → CO₂。不完全燃焼では CO が生じる。"
        },
        {
            "type": "element",
            "question": "塩酸の化学式はどれ？",
            "options": ["H₂SO₄", "HNO₃", "HCl", "H₃PO₄"],
            "answer": 2,
            "explanation": "塩酸は塩化水素(HCl)が水に溶けた液体。強酸の一つ。"
        },
        {
            "type": "reaction",
            "question": "酸と塩基が反応すると何が生成される？",
            "options": ["酸化物と水", "塩と水", "エステルと水", "酸化物と塩"],
            "answer": 1,
            "explanation": "中和反応：酸 + 塩基 → 塩 + 水。例：HCl + NaOH → NaCl + H₂O。"
        },
        {
            "type": "element",
            "question": "硫酸の化学式はどれ？",
            "options": ["H₂S", "SO₃", "H₂SO₄", "HSO₃"],
            "answer": 2,
            "explanation": "硫酸は H₂SO₄（強酸・二価の酸）。工業的に最も多く使われる酸。"
        },
        {
            "type": "element",
            "question": "アンモニアの化学式はどれ？",
            "options": ["NO₂", "N₂H₄", "NH₃", "N₂O"],
            "answer": 2,
            "explanation": "アンモニアは窒素1個と水素3個の化合物 NH₃。刺激臭がある塩基性気体。"
        },
        {
            "type": "experiment",
            "question": "BTB溶液を酸性の溶液に入れると何色になる？",
            "options": ["青", "緑", "黄", "赤"],
            "answer": 2,
            "explanation": "BTB溶液：酸性→黄、中性→緑、アルカリ性→青。"
        },
        {
            "type": "element",
            "question": "水酸化ナトリウムの化学式はどれ？",
            "options": ["NaO", "Na₂O", "NaOH", "Na(OH)₂"],
            "answer": 2,
            "explanation": "水酸化ナトリウムは NaOH（強塩基）。石鹸や洗剤の製造に使われる。"
        },
        {
            "type": "reaction",
            "question": "マグネシウムが燃焼する反応式として正しいのは？",
            "options": [
                "Mg + O → MgO",
                "Mg + O₂ → MgO₂",
                "2Mg + O₂ → 2MgO",
                "Mg + 2O₂ → Mg(O₂)₂"
            ],
            "answer": 2,
            "explanation": "2Mg + O₂ → 2MgO。マグネシウムは白色の強い光を出して燃える。"
        },
        {
            "type": "experiment",
            "question": "フェノールフタレイン溶液を塩基性の溶液に入れると何色になる？",
            "options": ["黄色", "青色", "無色", "赤色（桃色）"],
            "answer": 3,
            "explanation": "フェノールフタレイン：酸性・中性→無色、塩基性→赤（桃）色。"
        },
        {
            "type": "element",
            "question": "グルコース（ブドウ糖）の化学式はどれ？",
            "options": ["C₁₂H₂₂O₁₁", "C₆H₁₂O₆", "C₂H₅OH", "CH₄"],
            "answer": 1,
            "explanation": "グルコースは C₆H₁₂O₆。生命のエネルギー源となる糖。"
        },
        {
            "type": "element",
            "question": "オゾンの化学式はどれ？",
            "options": ["O₂", "O₃", "O₄", "O"],
            "answer": 1,
            "explanation": "オゾンは O₃（酸素の同素体）。紫外線を吸収し地球を守るオゾン層を形成。"
        },
        {
            "type": "experiment",
            "question": "リトマス紙（赤）を塩基性の溶液に浸すと何色になる？",
            "options": ["赤のまま", "黄", "青", "緑"],
            "answer": 2,
            "explanation": "リトマス紙：酸性→赤、塩基性→青。赤いリトマスが青くなれば塩基性。"
        },
        {
            "type": "reaction",
            "question": "塩化水素が水に溶けると何が生成される？",
            "options": ["塩酸（水素イオン H⁺ と塩化物イオン Cl⁻）", "水酸化物イオン OH⁻ と Na⁺", "Cl₂ と H₂O", "HCl のまま変化なし"],
            "answer": 0,
            "explanation": "HCl → H⁺ + Cl⁻。強酸は水中で完全に電離する。"
        },
        {
            "type": "element",
            "question": "メタンの化学式はどれ？",
            "options": ["CH₄", "C₂H₄", "C₂H₂", "C₃H₈"],
            "answer": 0,
            "explanation": "メタンは最もシンプルな有機化合物 CH₄。天然ガスの主成分。"
        },
    ],

    # ══════════════════════════════════════════════════
    # Lv.3 — 反応式の係数・実験の応用・酸化還元
    # ══════════════════════════════════════════════════
    3: [
        {
            "type": "reaction",
            "question": "アルミニウムと希硫酸の反応式として正しいのは？",
            "options": [
                "Al + H₂SO₄ → AlSO₄ + H₂",
                "2Al + 3H₂SO₄ → Al₂(SO₄)₃ + 3H₂",
                "Al + 3H₂SO₄ → Al(SO₄)₃ + H₂",
                "2Al + H₂SO₄ → Al₂SO₄ + H₂"
            ],
            "answer": 1,
            "explanation": "アルミニウムは3価なので Al₂(SO₄)₃。2Al + 3H₂SO₄ → Al₂(SO₄)₃ + 3H₂。"
        },
        {
            "type": "reaction",
            "question": "エタノールの燃焼反応式として正しいのは？",
            "options": [
                "C₂H₅OH + O₂ → CO₂ + H₂O",
                "C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O",
                "2C₂H₅OH + O₂ → 4CO + 6H₂",
                "C₂H₅OH + 2O₂ → CO₂ + 2H₂O"
            ],
            "answer": 1,
            "explanation": "C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O。左右の原子数を確認しよう。"
        },
        {
            "type": "experiment",
            "question": "硫酸銅(II)水溶液に亜鉛板を入れると何が起きる？",
            "options": [
                "亜鉛板が溶け出し溶液が無色になる",
                "亜鉛板の表面に銅が析出し、溶液の青色が薄くなる",
                "気体が発生して亜鉛板が消える",
                "沈殿が生じて溶液が白くなる"
            ],
            "answer": 1,
            "explanation": "Zn は Cu²⁺ を還元する（Zn → Zn²⁺ + 2e⁻）。亜鉛が溶け、銅が析出。これが酸化還元反応。"
        },
        {
            "type": "reaction",
            "question": "酸化還元反応において、「酸化される」とはどういう意味？",
            "options": [
                "電子を受け取ること",
                "電子を失うこと",
                "水素を受け取ること",
                "酸素を失うこと"
            ],
            "answer": 1,
            "explanation": "酸化＝電子を失う（OIL: Oxidation Is Loss）。還元＝電子を得る（RIG: Reduction Is Gain）。"
        },
        {
            "type": "experiment",
            "question": "ヨウ素デンプン反応で、デンプンにヨウ素液を加えると何色になる？",
            "options": ["赤褐色", "黄色", "青紫色", "緑色"],
            "answer": 2,
            "explanation": "デンプンはアミロースのらせん構造にヨウ素分子が取り込まれ青紫色になる。"
        },
        {
            "type": "reaction",
            "question": "アンモニアの工業的合成（ハーバー・ボッシュ法）の反応式は？",
            "options": [
                "N + 3H → NH₃",
                "N₂ + 3H₂ ⇌ 2NH₃",
                "2N + 3H₂ → 2NH₃",
                "N₂ + H₂ → NH₂"
            ],
            "answer": 1,
            "explanation": "N₂ + 3H₂ ⇌ 2NH₃。高温高圧で鉄触媒を使う可逆反応。農業用肥料の製造に不可欠。"
        },
        {
            "type": "experiment",
            "question": "二酸化炭素を石灰水に吹き込むと何が起きる？",
            "options": [
                "石灰水が黄色に変わる",
                "石灰水が白く濁る",
                "気泡が発生して溶液が沸騰する",
                "変化なし"
            ],
            "answer": 1,
            "explanation": "CO₂ + Ca(OH)₂ → CaCO₃↓ + H₂O。炭酸カルシウムが析出して白く濁る。"
        },
        {
            "type": "reaction",
            "question": "鉄が塩酸と反応したとき生成されるのは？",
            "options": [
                "Fe₂O₃ と H₂",
                "FeCl₃ と H₂O",
                "FeCl₂ と H₂",
                "FeO と HCl"
            ],
            "answer": 2,
            "explanation": "Fe + 2HCl → FeCl₂ + H₂↑。鉄は希塩酸に溶けて塩化鉄(II)と水素ガスを生成。"
        },
        {
            "type": "experiment",
            "question": "塩化アンモニウムと水酸化カルシウムを混ぜて加熱すると発生する気体は？",
            "options": ["水素", "窒素", "アンモニア", "塩化水素"],
            "answer": 2,
            "explanation": "2NH₄Cl + Ca(OH)₂ → CaCl₂ + 2H₂O + 2NH₃。アンモニアは上方置換で捕集する。"
        },
        {
            "type": "reaction",
            "question": "過酸化水素の分解反応（酸化マンガンIVが触媒）として正しいのは？",
            "options": [
                "H₂O₂ → H₂ + O",
                "2H₂O₂ → 2H₂O + O₂",
                "H₂O₂ → H₂O + O",
                "2H₂O₂ → H₄O₂ + O₂"
            ],
            "answer": 1,
            "explanation": "2H₂O₂ → 2H₂O + O₂。触媒(MnO₂)は反応速度を上げるが自身は変化しない。"
        },
        {
            "type": "experiment",
            "question": "銀鏡反応で銀が析出されるのは、どんな糖を使ったとき？",
            "options": ["スクロース（砂糖）", "グルコース（ブドウ糖）", "デンプン", "セルロース"],
            "answer": 1,
            "explanation": "グルコースは還元性を持ち、アルデヒド基(-CHO)がアンモニア性硝酸銀を還元して銀を析出する。"
        },
        {
            "type": "reaction",
            "question": "銅が希硝酸と反応するとき発生する気体は？",
            "options": ["H₂", "NO₂", "NO", "N₂"],
            "answer": 2,
            "explanation": "3Cu + 8HNO₃(希) → 3Cu(NO₃)₂ + 4H₂O + 2NO↑。希硝酸では一酸化窒素(NO)が発生。"
        },
        {
            "type": "experiment",
            "question": "炎色反応でナトリウムが示す色は？",
            "options": ["赤", "黄", "緑", "紫"],
            "answer": 1,
            "explanation": "Na→黄、Li→赤、K→紫、Cu→緑、Ca→橙、Ba→黄緑。語呂合わせで覚えよう！"
        },
        {
            "type": "reaction",
            "question": "電気分解で陰極(カソード)で起きる反応はどれ？",
            "options": ["酸化反応（電子を放出）", "還元反応（電子を受け取る）", "中和反応", "分解反応"],
            "answer": 1,
            "explanation": "陰極はマイナス極→電子を供給→還元反応。陽極はプラス極→電子を奪う→酸化反応。"
        },
        {
            "type": "experiment",
            "question": "水の電気分解で陰極(-)側に多く発生する気体は？",
            "options": ["酸素", "水素", "同量", "窒素"],
            "answer": 1,
            "explanation": "2H₂O → 2H₂ + O₂。水素(陰極):酸素(陽極) = 2:1 の体積比で発生。"
        },
    ],

    # ══════════════════════════════════════════════════
    # Lv.4 — 難問：有機化学・平衡・熱化学・量子化学
    # ══════════════════════════════════════════════════
    4: [
        {
            "type": "reaction",
            "question": "エステル化反応で酢酸とエタノールから生成される物質は？",
            "options": [
                "エチルエーテル + 水",
                "酢酸エチル + 水",
                "エタン酸 + メタノール",
                "プロパノール + CO₂"
            ],
            "answer": 1,
            "explanation": "CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O。酢酸エチルは果実のような香り。"
        },
        {
            "type": "reaction",
            "question": "ルシャトリエの原理として正しいのは？",
            "options": [
                "反応速度は温度に関係しない",
                "平衡状態の系に変化を加えると、その変化を打ち消す方向に平衡が移動する",
                "触媒は平衡の位置を右に移動させる",
                "濃度変化は平衡定数を変化させる"
            ],
            "answer": 1,
            "explanation": "ルシャトリエの原理：系への外的変化（濃度・温度・圧力）に対して、変化を緩和する方向に平衡移動。"
        },
        {
            "type": "experiment",
            "question": "フェーリング反応（フェーリング液の還元）が陽性（赤褐色沈殿）を示すのはどれ？",
            "options": [
                "アセトン",
                "ベンゼン",
                "グルコース",
                "エタノール"
            ],
            "answer": 2,
            "explanation": "グルコースはアルデヒド基を持ち還元性がある。フェーリング液（Cu²⁺）を還元し Cu₂O の赤褐色沈殿が生じる。"
        },
        {
            "type": "reaction",
            "question": "ベンゼンの臭素との反応（FeBr₃ 触媒）はどれ？",
            "options": [
                "付加反応でシクロヘキサンになる",
                "置換反応でブロモベンゼンになる",
                "酸化反応で安息香酸になる",
                "重合反応でポリベンゼンになる"
            ],
            "answer": 1,
            "explanation": "ベンゼンは安定な π 電子系を保つため、付加ではなく求電子置換反応が起こる。C₆H₅Br（ブロモベンゼン）が生成。"
        },
        {
            "type": "reaction",
            "question": "メタンの熱化学方程式（標準生成エンタルピー）として正しいのは？",
            "options": [
                "C(黒鉛) + 2H₂(g) → CH₄(g)  ΔH = +74.8 kJ",
                "C(黒鉛) + 2H₂(g) → CH₄(g)  ΔH = −74.8 kJ",
                "CH₄(g) → C(黒鉛) + 2H₂(g)  ΔH = −74.8 kJ",
                "C(g) + 4H(g) → CH₄(g)  ΔH = −74.8 kJ"
            ],
            "answer": 1,
            "explanation": "標準生成エンタルピーは安定な単体から1molを生成するときの ΔH。CH₄は発熱的に生成（ΔH < 0）。"
        },
        {
            "type": "experiment",
            "question": "ニンヒドリン反応（ニンヒドリン溶液を噴霧・加熱）で紫色になるのは？",
            "options": [
                "核酸（DNA）",
                "糖類",
                "アミノ酸・タンパク質",
                "脂質"
            ],
            "answer": 2,
            "explanation": "ニンヒドリン反応はアミノ酸の α-アミノ基と反応して青紫色（ルーエマン紫）を生じる。タンパク質も陽性。"
        },
        {
            "type": "reaction",
            "question": "ヘスの法則（総熱量保存の法則）とは？",
            "options": [
                "触媒があれば反応熱が変化する",
                "反応熱は反応経路によらず始状態と終状態だけで決まる",
                "発熱反応は必ず自発的に進む",
                "活性化エネルギーが低いほど反応熱が大きい"
            ],
            "answer": 1,
            "explanation": "ヘスの法則：反応の経路に依らず、始状態と終状態が同じなら反応熱は等しい（エンタルピーは状態関数）。"
        },
        {
            "type": "experiment",
            "question": "薄層クロマトグラフィー(TLC)で Rf 値が大きい物質の特徴は？",
            "options": [
                "固定相（シリカゲル）との相互作用が強い",
                "移動相（溶媒）への溶解性が高く、固定相との相互作用が弱い",
                "分子量が大きい",
                "極性が高い"
            ],
            "answer": 1,
            "explanation": "Rf = (スポットの移動距離) / (溶媒前線の移動距離)。移動相に乗りやすい非極性物質は Rf が大きい。"
        },
        {
            "type": "reaction",
            "question": "パウリの排他原理とは？",
            "options": [
                "同じ軌道の電子数は最大10個",
                "一つの軌道に入れる電子は最大2個で、スピンが逆向きでなければならない",
                "電子は最もエネルギーの高い軌道から埋まる",
                "同じ電子雲に同一スピンの電子は入れない制限はない"
            ],
            "answer": 1,
            "explanation": "パウリの排他原理：一つの量子状態（軌道・スピンの組合せ）には最大1個の電子しか入れない。1つの軌道に↑↓の2個まで。"
        },
        {
            "type": "experiment",
            "question": "核磁気共鳴（¹H NMR）スペクトルで、化学シフト δ の基準物質は？",
            "options": [
                "ベンゼン（C₆H₆）",
                "テトラメチルシラン（TMS）",
                "クロロホルム（CDCl₃）",
                "水（D₂O）"
            ],
            "answer": 1,
            "explanation": "TMS (Si(CH₃)₄) は化学的に不活性で12個の等価な H をもつ。δ = 0 ppm の基準に使われる。"
        },
        {
            "type": "reaction",
            "question": "有機化合物のマルコフニコフ則は何を予測する？",
            "options": [
                "ラジカル反応の生成物",
                "HX のアルケンへの付加反応で H がより多く H の付いた炭素に付く",
                "置換反応の速度",
                "エステル化の平衡定数"
            ],
            "answer": 1,
            "explanation": "マルコフニコフ則：HX がアルケンに付加するとき、H は既に H の多い C に付く（より安定なカルボカチオン中間体を経由）。"
        },
        {
            "type": "reaction",
            "question": "電池（ダニエル電池）において、亜鉛板は何極？",
            "options": [
                "正極（カソード、還元が起きる）",
                "負極（アノード、酸化が起きる）",
                "正極（アノード、酸化が起きる）",
                "負極（カソード、還元が起きる）"
            ],
            "answer": 1,
            "explanation": "Zn → Zn²⁺ + 2e⁻（酸化）が起きる亜鉛板が負極（アノード）。電子は亜鉛から銅板へ外部回路を流れる。"
        },
        {
            "type": "experiment",
            "question": "質量分析法（MS）で観測される分子イオンピーク [M]⁺ から直接わかることは？",
            "options": [
                "化合物の構造",
                "化合物の分子量",
                "化合物の融点",
                "官能基の種類"
            ],
            "answer": 1,
            "explanation": "分子イオンピーク m/z は分子量（厳密には分子の相対質量）を示す。高分解能 MS では分子式も決定可能。"
        },
        {
            "type": "reaction",
            "question": "アルドール縮合とはどのような反応か？",
            "options": [
                "アルケンへの付加反応",
                "カルボニル化合物の α-水素が塩基に引き抜かれ、エノラートが別のカルボニル化合物に付加する反応",
                "アルコールの酸化反応",
                "エステルの加水分解"
            ],
            "answer": 1,
            "explanation": "アルドール縮合は C-C 結合形成反応。エノラートイオンがアルデヒドのカルボニル炭素を攻撃してβ-ヒドロキシカルボニル化合物を生成。"
        },
        {
            "type": "experiment",
            "question": "酸素センサー（ジルコニア型）の動作原理は？",
            "options": [
                "可視光の吸収量で O₂ 濃度を測定",
                "O₂⁻ イオンが固体電解質（ZrO₂）中を移動することで起電力が生じる",
                "O₂ が触媒上で H₂ と反応する熱量を計測",
                "O₂ の常磁性を利用した磁気センサー"
            ],
            "answer": 1,
            "explanation": "ジルコニアセンサーは O₂⁻ 導電体 ZrO₂ を使い、両側の O₂ 分圧差によってネルンスト式に従う起電力が生じる。"
        },
    ],
}
