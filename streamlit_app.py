import streamlit as st
import random
import time

# ════════════════════════════════════════════════════════════
# 単語データ（難易度別）
# ════════════════════════════════════════════════════════════

# ── 簡単（小学生レベル）──
EASY_WORDS = {
    "動物": [
        ("dog", "イヌ"), ("cat", "ネコ"), ("bird", "トリ"), ("fish", "サカナ"),
        ("horse", "ウマ"), ("cow", "ウシ"), ("pig", "ブタ"), ("rabbit", "ウサギ"),
        ("bear", "クマ"), ("lion", "ライオン"), ("tiger", "トラ"), ("monkey", "サル"),
        ("duck", "アヒル"), ("frog", "カエル"), ("snake", "ヘビ"),
    ],
    "食べ物": [
        ("apple", "リンゴ"), ("bread", "パン"), ("milk", "ミルク"), ("egg", "タマゴ"),
        ("rice", "ごはん"), ("cake", "ケーキ"), ("juice", "ジュース"), ("water", "みず"),
        ("meat", "にく"), ("soup", "スープ"), ("salad", "サラダ"),
        ("pizza", "ピザ"), ("candy", "アメ"), ("cookie", "クッキー"), ("tea", "おちゃ"),
    ],
    "色・形": [
        ("red", "あか"), ("blue", "あお"), ("green", "みどり"), ("yellow", "きいろ"),
        ("white", "しろ"), ("black", "くろ"), ("pink", "ピンク"), ("circle", "まる"),
        ("star", "ほし"), ("heart", "ハート"), ("big", "おおきい"), ("small", "ちいさい"),
        ("long", "ながい"), ("short", "みじかい"), ("hot", "あつい"),
    ],
    "体・家族": [
        ("hand", "て"), ("eye", "め"), ("ear", "みみ"), ("nose", "はな"),
        ("mouth", "くち"), ("head", "あたま"), ("foot", "あし"), ("mother", "おかあさん"),
        ("father", "おとうさん"), ("sister", "いもうと"), ("brother", "おとうと"),
        ("baby", "あかちゃん"), ("friend", "ともだち"), ("teacher", "せんせい"), ("name", "なまえ"),
    ],
    "乗り物・場所": [
        ("car", "くるま"), ("bus", "バス"), ("train", "でんしゃ"), ("boat", "ふね"),
        ("plane", "ひこうき"), ("bike", "じてんしゃ"), ("school", "がっこう"),
        ("park", "こうえん"), ("home", "いえ"), ("shop", "みせ"), ("road", "みち"),
        ("door", "ドア"), ("window", "まど"), ("chair", "いす"), ("desk", "つくえ"),
    ],
}

# ── 普通（中学生レベル）──
NORMAL_WORDS = {
    "動物": [
        ("elephant", "ゾウ"), ("giraffe", "キリン"), ("dolphin", "イルカ"),
        ("penguin", "ペンギン"), ("butterfly", "チョウ"), ("crocodile", "ワニ"),
        ("kangaroo", "カンガルー"), ("octopus", "タコ"), ("squirrel", "リス"),
        ("flamingo", "フラミンゴ"), ("cheetah", "チーター"), ("gorilla", "ゴリラ"),
        ("hedgehog", "ハリネズミ"), ("leopard", "ヒョウ"), ("parrot", "オウム"),
    ],
    "食べ物": [
        ("avocado", "アボカド"), ("broccoli", "ブロッコリー"), ("strawberry", "イチゴ"),
        ("pineapple", "パイナップル"), ("mushroom", "キノコ"), ("blueberry", "ブルーベリー"),
        ("asparagus", "アスパラガス"), ("watermelon", "スイカ"), ("eggplant", "ナス"),
        ("peach", "モモ"), ("cucumber", "キュウリ"), ("spinach", "ほうれん草"),
        ("mango", "マンゴー"), ("raspberry", "ラズベリー"), ("pumpkin", "カボチャ"),
    ],
    "職業": [
        ("architect", "建築家"), ("astronaut", "宇宙飛行士"), ("carpenter", "大工"),
        ("pharmacist", "薬剤師"), ("journalist", "記者"), ("accountant", "会計士"),
        ("surgeon", "外科医"), ("photographer", "写真家"), ("librarian", "司書"),
        ("diplomat", "外交官"), ("engineer", "エンジニア"), ("scientist", "科学者"),
        ("musician", "音楽家"), ("painter", "画家"), ("athlete", "スポーツ選手"),
    ],
    "自然・地理": [
        ("volcano", "火山"), ("glacier", "氷河"), ("canyon", "峡谷"),
        ("peninsula", "半島"), ("plateau", "高原"), ("lagoon", "潟湖"),
        ("typhoon", "台風"), ("earthquake", "地震"), ("waterfall", "滝"),
        ("desert", "砂漠"), ("rainforest", "熱帯雨林"), ("continent", "大陸"),
        ("island", "島"), ("ocean", "海洋"), ("mountain", "山"),
    ],
    "スポーツ・趣味": [
        ("archery", "アーチェリー"), ("gymnastics", "体操"), ("volleyball", "バレーボール"),
        ("wrestling", "レスリング"), ("badminton", "バドミントン"), ("marathon", "マラソン"),
        ("skiing", "スキー"), ("skating", "スケート"), ("surfing", "サーフィン"),
        ("cycling", "自転車競技"), ("boxing", "ボクシング"), ("painting", "絵画"),
        ("camping", "キャンプ"), ("fishing", "釣り"), ("dancing", "ダンス"),
    ],
}

# ── 難しい（高校〜大学レベル）──
HARD_WORDS = {
    "学術・科学": [
        ("hypothesis", "仮説"), ("chromosome", "染色体"), ("thermodynamics", "熱力学"),
        ("electromagnetic", "電磁気の"), ("photosynthesis", "光合成"),
        ("metabolism", "代謝"), ("ecosystem", "生態系"), ("gravitational", "重力の"),
        ("condensation", "凝縮"), ("evaporation", "蒸発"), ("combustion", "燃焼"),
        ("precipitation", "沈殿・降水"), ("diffusion", "拡散"),
        ("osmosis", "浸透"), ("catalysis", "触媒作用"),
    ],
    "社会・政治": [
        ("sovereignty", "主権"), ("bureaucracy", "官僚制"), ("legislation", "立法"),
        ("constitution", "憲法"), ("democracy", "民主主義"), ("referendum", "国民投票"),
        ("sanctions", "制裁"), ("diplomacy", "外交"), ("propaganda", "プロパガンダ"),
        ("aristocracy", "貴族制"), ("totalitarian", "全体主義の"), ("capitalism", "資本主義"),
        ("imperialism", "帝国主義"), ("colonialism", "植民地主義"), ("utopia", "理想郷"),
    ],
    "医学・心理": [
        ("diagnosis", "診断"), ("inflammation", "炎症"), ("antibody", "抗体"),
        ("psychology", "心理学"), ("cognition", "認知"), ("perception", "知覚"),
        ("hallucination", "幻覚"), ("schizophrenia", "統合失調症"), ("dementia", "認知症"),
        ("neurology", "神経学"), ("cardiovascular", "心血管の"), ("psychiatric", "精神医学の"),
        ("immune", "免疫の"), ("syndrome", "症候群"), ("pathology", "病理学"),
    ],
    "文学・芸術": [
        ("metaphor", "比喩"), ("allegory", "寓話"), ("paradox", "逆説"),
        ("protagonist", "主人公"), ("antagonist", "敵役"), ("soliloquy", "独白"),
        ("renaissance", "ルネサンス"), ("baroque", "バロック"), ("impressionism", "印象主義"),
        ("surrealism", "シュルレアリスム"), ("satire", "風刺"), ("irony", "皮肉"),
        ("rhetoric", "修辞学"), ("aesthetics", "美学"), ("contemporary", "現代の"),
    ],
    "経済・ビジネス": [
        ("inflation", "インフレ"), ("recession", "景気後退"), ("liability", "負債"),
        ("monopoly", "独占"), ("dividend", "配当"), ("acquisition", "買収"),
        ("depreciation", "減価償却"), ("entrepreneur", "起業家"), ("fiscal", "財政の"),
        ("subsidy", "補助金"), ("tariff", "関税"), ("portfolio", "資産構成"),
        ("liquidation", "清算"), ("bankruptcy", "破産"), ("arbitrage", "裁定取引"),
    ],
}

# ── 鬼（超難関：難解語彙・専門用語）──
ONI_WORDS = {
    "哲学・論理": [
        ("epistemology", "認識論"), ("ontology", "存在論"), ("solipsism", "独我論"),
        ("phenomenology", "現象学"), ("dialectic", "弁証法"), ("nihilism", "虚無主義"),
        ("existentialism", "実存主義"), ("determinism", "決定論"), ("empiricism", "経験論"),
        ("pragmatism", "実用主義"), ("hedonism", "快楽主義"), ("stoicism", "禁欲主義"),
        ("syllogism", "三段論法"), ("tautology", "同語反復"), ("axiom", "公理"),
    ],
    "高度医学・生物": [
        ("mitochondria", "ミトコンドリア"), ("ribosomes", "リボソーム"),
        ("telomere", "テロメア"), ("epigenetics", "エピジェネティクス"),
        ("homeostasis", "恒常性"), ("apoptosis", "アポトーシス"),
        ("phagocytosis", "食作用"), ("meiosis", "減数分裂"), ("anaphylaxis", "アナフィラキシー"),
        ("pharmacokinetics", "薬物動態学"), ("immunosuppression", "免疫抑制"),
        ("neurotransmitter", "神経伝達物質"), ("carcinogenesis", "発癌過程"),
        ("endocrinology", "内分泌学"), ("cytokine", "サイトカイン"),
    ],
    "高度物理・数学": [
        ("eigenvalue", "固有値"), ("stochastic", "確率論的"), ("topology", "位相幾何学"),
        ("isomorphism", "同型"), ("quaternion", "四元数"), ("asymptote", "漸近線"),
        ("hyperbola", "双曲線"), ("permutation", "順列"), ("combinatorics", "組合せ論"),
        ("differential", "微分"), ("manifold", "多様体"), ("entropy", "エントロピー"),
        ("quasar", "クエーサー"), ("singularity", "特異点"), ("parallax", "視差"),
    ],
    "法律・行政": [
        ("jurisprudence", "法学・法哲学"), ("promulgation", "公布"),
        ("adjudication", "裁決"), ("expropriation", "収用"), ("indemnification", "補償"),
        ("subpoena", "召喚状"), ("jurisdiction", "管轄権"), ("extradition", "犯罪人引渡し"),
        ("injunction", "差止命令"),
        ("tort", "不法行為"), ("statute", "成文法"), ("plaintiff", "原告"),
        ("defendant", "被告"), ("perjury", "偽証罪"), ("affidavit", "宣誓供述書"),
    ],
    "高度語彙": [
        ("sesquipedalian", "長い言葉を使いたがる"), ("loquacious", "おしゃべりな"),
        ("surreptitious", "こっそりとした"), ("ephemeral", "はかない"),
        ("obfuscate", "難解にする"), ("perspicacious", "洞察力のある"),
        ("equanimity", "冷静さ"), ("magnanimous", "寛大な"),
        ("recalcitrant", "反抗的な"), ("mendacious", "虚偽の"),
        ("propitious", "吉兆の"), ("pusillanimous", "臆病な"),
        ("verisimilitude", "真実らしさ"), ("lassitude", "倦怠感"),
        ("schadenfreude", "他者の不幸を喜ぶ気持ち"),
    ],
}

# 難易度設定マスター
DIFFICULTY_CONFIG = {
    "😊 簡単": {
        "words": EASY_WORDS,
        "time_limit": 25,
        "choices": 4,
        "hint": True,
        "typo_mode": False,
        "score_base": 50,
        "color": "#2ed573",
        "desc": "小学生レベル　やさしい単語ばかり！",
        "emoji": "😊",
    },
    "📘 普通": {
        "words": NORMAL_WORDS,
        "time_limit": 20,
        "choices": 4,
        "hint": False,
        "typo_mode": False,
        "score_base": 100,
        "color": "#1e90ff",
        "desc": "中学生レベル　基本的な英単語",
        "emoji": "📘",
    },
    "🔥 難しい": {
        "words": HARD_WORDS,
        "time_limit": 15,
        "choices": 6,
        "hint": False,
        "typo_mode": False,
        "score_base": 200,
        "color": "#ffa502",
        "desc": "高校〜大学レベル　専門用語・難単語",
        "emoji": "🔥",
    },
    "💀 鬼": {
        "words": ONI_WORDS,
        "time_limit": 10,
        "choices": 6,
        "hint": False,
        "typo_mode": True,
        "score_base": 500,
        "color": "#ff4757",
        "desc": "超難関！専門家レベル　スペル入力あり",
        "emoji": "💀",
    },
}

# ════════════════════════════════════════════════════════════
# 状態管理
# ════════════════════════════════════════════════════════════

def init_state():
    defaults = {
        "phase": "start",
        "score": 0,
        "question_no": 0,
        "total_questions": 10,
        "start_time": None,
        "current_word": None,
        "current_answer": None,
        "choices": [],
        "selected": None,
        "correct": None,
        "used_words": [],
        "history": [],
        "difficulty": "📘 普通",
        "category": "全カテゴリ",
        "mode": "日本語→英語",
        "streak": 0,
        "max_streak": 0,
        "answered": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_config():
    return DIFFICULTY_CONFIG[st.session_state.difficulty]

def get_word_pool():
    cfg = get_config()
    cat = st.session_state.category
    words = cfg["words"]
    if cat == "全カテゴリ":
        pool = []
        for w in words.values():
            pool.extend(w)
    else:
        pool = words.get(cat, [])
    return pool

def new_question():
    pool = get_word_pool()
    available = [w for w in pool if w not in st.session_state.used_words]
    if not available:
        st.session_state.used_words = []
        available = pool

    word_pair = random.choice(available)
    st.session_state.used_words.append(word_pair)
    st.session_state.current_word = word_pair[0]
    st.session_state.current_answer = word_pair[1]

    cfg = get_config()
    n_choices = cfg["choices"]
    mode = st.session_state.mode

    wrong_pool = [w for w in pool if w != word_pair]
    n_wrong = min(n_choices - 1, len(wrong_pool))
    wrongs = random.sample(wrong_pool, n_wrong)

    if mode == "日本語→英語":
        correct_choice = word_pair[0]
        wrong_choices = [w[0] for w in wrongs]
    else:
        correct_choice = word_pair[1]
        wrong_choices = [w[1] for w in wrongs]

    choices = wrong_choices + [correct_choice]
    random.shuffle(choices)
    st.session_state.choices = choices
    st.session_state.selected = None
    st.session_state.correct = None
    st.session_state.answered = False
    st.session_state.start_time = time.time()

def do_answer(choice):
    cfg = get_config()
    mode = st.session_state.mode
    correct = st.session_state.current_word if mode == "日本語→英語" else st.session_state.current_answer

    elapsed = time.time() - st.session_state.start_time
    if cfg["typo_mode"]:
        is_correct = choice.strip().lower() == correct.strip().lower()
    else:
        is_correct = (choice == correct)

    st.session_state.selected = choice
    st.session_state.correct = correct
    st.session_state.answered = True

    if is_correct:
        time_bonus = max(0, int((cfg["time_limit"] - elapsed) * cfg["score_base"] / 10))
        st.session_state.score += cfg["score_base"] + time_bonus
        st.session_state.streak += 1
        st.session_state.max_streak = max(st.session_state.streak, st.session_state.max_streak)
    else:
        st.session_state.streak = 0

    st.session_state.history.append({
        "en": st.session_state.current_word,
        "ja": st.session_state.current_answer,
        "correct": is_correct,
        "elapsed": round(elapsed, 1),
        "input": choice,
    })
    st.session_state.question_no += 1

def start_game():
    st.session_state.phase = "playing"
    st.session_state.score = 0
    st.session_state.question_no = 0
    st.session_state.used_words = []
    st.session_state.history = []
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    new_question()

# ════════════════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════════════════

def inject_css(diff_color="#1e90ff"):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {{ font-family: 'Nunito', sans-serif; }}

    .stApp {{
        background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 50%, #0f1f3d 100%);
        min-height: 100vh;
    }}

    .game-title {{
        font-family: 'Fredoka One', cursive;
        font-size: 3em;
        text-align: center;
        background: linear-gradient(90deg, #f7971e, #ffd200, #f7971e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s infinite;
        background-size: 200%;
        margin-bottom: 0.1em;
    }}
    @keyframes shimmer {{ 0% {{ background-position: 0% }} 50% {{ background-position: 100% }} 100% {{ background-position: 0% }} }}

    .question-card {{
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 2px solid {diff_color}44;
        border-radius: 24px;
        padding: 1.8em 2.5em;
        text-align: center;
        margin-bottom: 1.2em;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 20px {diff_color}22;
    }}

    .question-label {{
        color: {diff_color};
        font-size: 0.85em;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5em;
    }}

    .question-word {{
        font-family: 'Fredoka One', cursive;
        font-size: 2.8em;
        color: #ffffff;
        margin: 0.2em 0;
        line-height: 1.1;
    }}

    .hint-text {{
        color: {diff_color}cc;
        font-size: 0.9em;
        font-weight: 700;
        margin-top: 0.4em;
    }}

    .stat-box {{
        background: rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 0.7em 1em;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }}
    .stat-label {{ color: rgba(255,255,255,0.5); font-size: 0.72em; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }}
    .stat-value {{ color: #ffd200; font-family: 'Fredoka One', cursive; font-size: 1.7em; line-height: 1.2; }}

    .stButton > button {{
        width: 100%;
        font-family: 'Nunito', sans-serif;
        font-weight: 800;
        font-size: 1.05em;
        padding: 0.75em 1em;
        border-radius: 14px;
        border: 2px solid rgba(255,255,255,0.15);
        background: rgba(255,255,255,0.07);
        color: white;
        transition: all 0.18s ease;
    }}
    .stButton > button:hover {{
        background: {diff_color}33;
        border-color: {diff_color};
        color: {diff_color};
        transform: translateY(-2px);
        box-shadow: 0 6px 20px {diff_color}44;
    }}

    .feedback-correct {{
        background: linear-gradient(135deg, rgba(46,213,115,0.18), rgba(46,213,115,0.04));
        border: 2px solid #2ed573;
        border-radius: 16px;
        padding: 0.9em 1.4em;
        text-align: center;
        color: #2ed573;
        font-weight: 900;
        font-size: 1.15em;
        animation: pop 0.3s ease;
    }}
    .feedback-wrong {{
        background: linear-gradient(135deg, rgba(255,71,87,0.18), rgba(255,71,87,0.04));
        border: 2px solid #ff4757;
        border-radius: 16px;
        padding: 0.9em 1.4em;
        text-align: center;
        color: #ff4757;
        font-weight: 900;
        font-size: 1.15em;
        animation: shake 0.3s ease;
    }}
    @keyframes pop {{ 0% {{ transform: scale(0.88); opacity: 0; }} 100% {{ transform: scale(1); opacity: 1; }} }}
    @keyframes shake {{ 0%,100% {{ transform: translateX(0); }} 25% {{ transform: translateX(-8px); }} 75% {{ transform: translateX(8px); }} }}

    .progress-container {{ background: rgba(255,255,255,0.08); border-radius: 99px; height: 7px; margin: 0.4em 0 1.2em; overflow: hidden; }}
    .progress-fill {{ height: 100%; border-radius: 99px; background: linear-gradient(90deg, {diff_color}, #ffd200); transition: width 0.4s ease; }}

    .diff-badge {{
        display: inline-block;
        background: {diff_color}33;
        border: 1.5px solid {diff_color};
        color: {diff_color};
        font-weight: 800;
        font-size: 0.82em;
        padding: 0.2em 0.8em;
        border-radius: 99px;
        letter-spacing: 0.5px;
    }}

    .streak-badge {{
        display: inline-block;
        background: linear-gradient(135deg, #f7971e, #ffd200);
        color: #1a1a2e;
        font-family: 'Fredoka One', cursive;
        padding: 0.15em 0.8em;
        border-radius: 99px;
    }}

    .result-card {{
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(20px);
        border: 2px solid {diff_color}44;
        border-radius: 24px;
        padding: 2.5em;
        text-align: center;
        box-shadow: 0 0 40px {diff_color}22;
    }}
    .result-score {{
        font-family: 'Fredoka One', cursive;
        font-size: 5em;
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }}

    .stTextInput > div > div > input {{
        background: rgba(255,255,255,0.06) !important;
        border: 2px solid #ff475755 !important;
        border-radius: 14px !important;
        color: white !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 1.2em !important;
        font-weight: 700 !important;
        text-align: center !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #ff4757 !important;
        box-shadow: 0 0 15px #ff475744 !important;
    }}

    h1,h2,h3,p {{ color: white; }}
    .stSelectbox label, .stRadio label, .stSlider label {{ color: rgba(255,255,255,0.8) !important; font-weight: 700; }}
    </style>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# スタート画面
# ════════════════════════════════════════════════════════════

def page_start():
    st.markdown('<div class="game-title">🔤 Word Rush!</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.5);margin-bottom:1.5em;font-weight:600;">英単語クイズ — 難易度を選んでスタート！</p>', unsafe_allow_html=True)

    st.markdown("### 🎮 難易度を選択")
    diff_cols = st.columns(4)
    diff_keys = list(DIFFICULTY_CONFIG.keys())

    for col, key in zip(diff_cols, diff_keys):
        cfg = DIFFICULTY_CONFIG[key]
        selected = st.session_state.difficulty == key
        border = f"2px solid {cfg['color']}" if selected else "2px solid rgba(255,255,255,0.1)"
        bg = f"{cfg['color']}22" if selected else "rgba(255,255,255,0.03)"
        with col:
            st.markdown(f"""
            <div style="background:{bg};border:{border};border-radius:18px;padding:1em 0.5em;text-align:center;margin-bottom:0.5em;">
                <div style="font-size:1.8em">{cfg['emoji']}</div>
                <div style="color:{cfg['color']};font-weight:900;font-size:0.95em;">{key}</div>
                <div style="color:rgba(255,255,255,0.55);font-size:0.7em;margin-top:0.3em;line-height:1.4">{cfg['desc']}</div>
                <div style="margin-top:0.6em;color:rgba(255,255,255,0.4);font-size:0.72em">⏱{cfg['time_limit']}秒 / {cfg['choices']}択{'＋入力' if cfg['typo_mode'] else ''}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("選ぶ", key=f"diff_{key}", use_container_width=True):
                st.session_state.difficulty = key
                st.rerun()

    cfg = get_config()
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        cats = ["全カテゴリ"] + list(cfg["words"].keys())
        st.session_state.category = st.selectbox("📂 カテゴリ", cats)
    with col2:
        st.session_state.mode = st.radio("🔄 出題モード", ["日本語→英語", "英語→日本語"])
    with col3:
        st.session_state.total_questions = st.slider("❓ 問題数", 5, 20, 10, step=5)

    st.markdown("<br>", unsafe_allow_html=True)
    diff_label = st.session_state.difficulty
    if st.button(f"🚀 {diff_label} でスタート！", use_container_width=True):
        start_game()
        st.rerun()

# ════════════════════════════════════════════════════════════
# プレイ中画面
# ════════════════════════════════════════════════════════════

def page_playing():
    cfg = get_config()
    q_no = st.session_state.question_no
    total = st.session_state.total_questions

    if q_no >= total and st.session_state.answered:
        st.session_state.phase = "result"
        st.rerun()
        return

    # ヘッダー
    c1, c2, c3, c4 = st.columns(4)
    streak = st.session_state.streak
    badge = f'<span class="streak-badge">🔥×{streak}</span>' if streak >= 3 else f'<b style="color:#ffd200">{streak}</b>'
    diff_name = st.session_state.difficulty
    for col, (lbl, val) in zip([c1, c2, c3, c4], [
        ("問題", f"{q_no + 1}/{total}"),
        ("スコア", f"{st.session_state.score:,}"),
        ("連続正解", badge),
        ("難易度", f'<span class="diff-badge">{diff_name}</span>'),
    ]):
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-label">{lbl}</div><div class="stat-value" style="font-size:1.3em">{val}</div></div>', unsafe_allow_html=True)

    pct = int(q_no / total * 100)
    st.markdown(f'<div class="progress-container"><div class="progress-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

    # タイマー
    if not st.session_state.answered:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, cfg["time_limit"] - elapsed)
        pct_t = int(remaining / cfg["time_limit"] * 100)
        tcol = "#2ed573" if pct_t > 60 else "#ffd200" if pct_t > 30 else "#ff4757"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8em;">
            <span style="color:{tcol};font-size:0.9em;font-weight:900;min-width:42px">⏱{remaining:.0f}s</span>
            <div style="flex:1;background:rgba(255,255,255,0.08);border-radius:99px;height:7px;">
                <div style="width:{pct_t}%;height:100%;border-radius:99px;background:{tcol};transition:width 1s linear"></div>
            </div>
        </div>""", unsafe_allow_html=True)

        if remaining == 0:
            do_answer("__timeout__")
            if st.session_state.question_no < total:
                new_question()
            st.rerun()

    # 問題カード
    mode = st.session_state.mode
    display_word = st.session_state.current_answer if mode == "日本語→英語" else st.session_state.current_word
    hint_label = "英語に訳すと？" if mode == "日本語→英語" else "日本語の意味は？"

    hint_html = ""
    if cfg["hint"] and mode == "日本語→英語" and not st.session_state.answered:
        first = st.session_state.current_word[0].upper()
        hint_html = f'<div class="hint-text">💡 ヒント：「{first}」から始まる英語</div>'

    st.markdown(f"""
    <div class="question-card">
        <div class="question-label">{hint_label}</div>
        <div class="question-word">{display_word}</div>
        {hint_html}
    </div>""", unsafe_allow_html=True)

    # フィードバック（回答後）
    if st.session_state.answered:
        if st.session_state.history and st.session_state.history[-1]["correct"]:
            elapsed = st.session_state.history[-1]["elapsed"]
            bonus = max(0, int((cfg["time_limit"] - elapsed) * cfg["score_base"] / 10))
            st.markdown(f'<div class="feedback-correct">✅ 正解！ {elapsed}秒 ＋{bonus}ボーナス</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-wrong">❌ 不正解… 正解は「{st.session_state.correct}」</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if q_no >= total:
            if st.button("📊 結果を見る", use_container_width=True):
                st.session_state.phase = "result"
                st.rerun()
        else:
            if st.button("➡️ 次の問題へ", use_container_width=True):
                new_question()
                st.rerun()
        return

    # 鬼モード：スペル入力
    if cfg["typo_mode"]:
        st.markdown('<p style="text-align:center;color:rgba(255,71,87,0.9);font-weight:800;margin-bottom:0.4em;">💀 スペルを正確に入力せよ！</p>', unsafe_allow_html=True)
        user_input = st.text_input("英単語を入力", key=f"oni_input_{q_no}", placeholder="ここに入力...", label_visibility="collapsed")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ 回答する", use_container_width=True):
                if user_input.strip():
                    do_answer(user_input.strip())
                    st.rerun()
        with col_b:
            if st.button("⏭ スキップ（0点）", use_container_width=True):
                do_answer("")
                if st.session_state.question_no < total:
                    new_question()
                st.rerun()
        return

    # 通常モード：選択肢ボタン
    choices = st.session_state.choices
    n = len(choices)
    half = (n + 1) // 2
    col_a, col_b = st.columns(2)
    for i, choice in enumerate(choices):
        col = col_a if i < half else col_b
        with col:
            if st.button(choice, key=f"choice_{i}_{q_no}"):
                do_answer(choice)
                st.rerun()

# ════════════════════════════════════════════════════════════
# 結果画面
# ════════════════════════════════════════════════════════════

def page_result():
    cfg = get_config()
    history = st.session_state.history
    correct_count = sum(1 for h in history if h["correct"])
    total = len(history)
    accuracy = int(correct_count / total * 100) if total else 0
    avg_time = round(sum(h["elapsed"] for h in history) / total, 1) if total else 0

    if accuracy == 100:
        rank, emoji = "PERFECT！", "🏆"
    elif accuracy >= 80:
        rank, emoji = "Excellent!", "🥇"
    elif accuracy >= 60:
        rank, emoji = "Good Job!", "🥈"
    elif accuracy >= 40:
        rank, emoji = "Keep Going!", "🥉"
    else:
        rank, emoji = "Try Again!", "📚"

    diff_name = st.session_state.difficulty

    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:2.8em;margin-bottom:0.2em">{emoji}</div>
        <div style="color:rgba(255,255,255,0.55);font-weight:800;letter-spacing:2px;text-transform:uppercase;font-size:0.85em">{rank}</div>
        <div class="result-score">{st.session_state.score:,}</div>
        <div style="color:rgba(255,255,255,0.4);font-size:0.82em;margin-top:0.2em">ポイント</div>
        <div style="margin-top:0.8em"><span class="diff-badge">{diff_name}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, (lbl, val) in zip([c1, c2, c3, c4], [
        ("正解数", f"{correct_count}/{total}"),
        ("正答率", f"{accuracy}%"),
        ("平均時間", f"{avg_time}秒"),
        ("最大連続", f"{st.session_state.max_streak}回"),
    ]):
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-label">{lbl}</div><div class="stat-value" style="font-size:1.3em">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 振り返り")
    for i, h in enumerate(history):
        icon = "✅" if h["correct"] else "❌"
        color = "#2ed573" if h["correct"] else "#ff6b81"
        wrong_note = ""
        if not h["correct"] and cfg["typo_mode"] and h.get("input") and h["input"] not in ("__timeout__", ""):
            wrong_note = f' <span style="opacity:0.6">（あなた：{h["input"]}）</span>'
        st.markdown(f"""
        <div style="color:{color};display:flex;justify-content:space-between;padding:0.45em 0.3em;border-bottom:1px solid rgba(255,255,255,0.05);">
            <span>{icon} Q{i+1}. <b>{h['en']}</b> — {h['ja']}{wrong_note}</span>
            <span style="opacity:0.6;font-size:0.83em">{h['elapsed']}秒</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 もう一度", use_container_width=True):
            start_game()
            st.rerun()
    with col2:
        if st.button("⚙️ 設定に戻る", use_container_width=True):
            st.session_state.phase = "start"
            st.rerun()

# ════════════════════════════════════════════════════════════
# メイン
# ════════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="Word Rush! 英単語クイズ",
        page_icon="🔤",
        layout="centered",
    )
    init_state()
    cfg = get_config()
    inject_css(cfg["color"])

    phase = st.session_state.phase
    if phase == "start":
        page_start()
    elif phase == "playing":
        page_playing()
    elif phase == "result":
        page_result()

if __name__ == "__main__":
    main()