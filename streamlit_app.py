import streamlit as st
import random
import time

# ────────────────────────────────────────────────
# 単語データ（カテゴリ別）
# ────────────────────────────────────────────────
WORD_DATA = {
    "動物": [
        ("elephant", "ゾウ"), ("giraffe", "キリン"), ("dolphin", "イルカ"),
        ("penguin", "ペンギン"), ("butterfly", "チョウ"), ("crocodile", "ワニ"),
        ("kangaroo", "カンガルー"), ("octopus", "タコ"), ("squirrel", "リス"),
        ("flamingo", "フラミンゴ"), ("cheetah", "チーター"), ("gorilla", "ゴリラ"),
        ("hedgehog", "ハリネズミ"), ("platypus", "カモノハシ"), ("leopard", "ヒョウ"),
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
        ("surgeon", "外科医"), ("psychologist", "心理士"), ("economist", "経済学者"),
        ("electrician", "電気技師"), ("veterinarian", "獣医"), ("photographer", "写真家"),
        ("librarian", "司書"), ("geologist", "地質学者"), ("diplomat", "外交官"),
    ],
    "自然・地理": [
        ("volcano", "火山"), ("glacier", "氷河"), ("canyon", "峡谷"),
        ("peninsula", "半島"), ("archipelago", "群島"), ("plateau", "高原"),
        ("lagoon", "潟湖"), ("tundra", "ツンドラ"), ("savanna", "サバンナ"),
        ("typhoon", "台風"), ("earthquake", "地震"), ("waterfall", "滝"),
        ("desert", "砂漠"), ("rainforest", "熱帯雨林"), ("fjord", "フィヨルド"),
    ],
    "スポーツ": [
        ("archery", "アーチェリー"), ("gymnastics", "体操"), ("volleyball", "バレーボール"),
        ("wrestling", "レスリング"), ("fencing", "フェンシング"), ("rowing", "ボート競技"),
        ("badminton", "バドミントン"), ("marathon", "マラソン"), ("triathlon", "トライアスロン"),
        ("skiing", "スキー"), ("skating", "スケート"), ("surfing", "サーフィン"),
        ("cycling", "自転車競技"), ("boxing", "ボクシング"), ("judo", "柔道"),
    ],
}

# ────────────────────────────────────────────────
# 初期化
# ────────────────────────────────────────────────
def init_state():
    defaults = {
        "phase": "start",        # start / playing / result
        "score": 0,
        "question_no": 0,
        "total_questions": 10,
        "time_limit": 20,
        "start_time": None,
        "current_word": None,
        "current_answer": None,
        "choices": [],
        "selected": None,
        "correct": None,
        "used_words": [],
        "history": [],
        "category": "全カテゴリ",
        "mode": "日本語→英語",
        "streak": 0,
        "max_streak": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_word_pool(category):
    if category == "全カテゴリ":
        pool = []
        for words in WORD_DATA.values():
            pool.extend(words)
    else:
        pool = WORD_DATA.get(category, [])
    return pool

def new_question():
    pool = get_word_pool(st.session_state.category)
    available = [w for w in pool if w not in st.session_state.used_words]
    if not available:
        st.session_state.used_words = []
        available = pool

    word_pair = random.choice(available)
    st.session_state.used_words.append(word_pair)
    st.session_state.current_word = word_pair[0]
    st.session_state.current_answer = word_pair[1]

    # 選択肢（4択）
    mode = st.session_state.mode
    wrong_pool = [w for w in pool if w != word_pair]
    wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))

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
    st.session_state.start_time = time.time()

def answer(choice):
    mode = st.session_state.mode
    if mode == "日本語→英語":
        correct = st.session_state.current_word
    else:
        correct = st.session_state.current_answer

    elapsed = time.time() - st.session_state.start_time
    is_correct = (choice == correct)
    st.session_state.selected = choice
    st.session_state.correct = correct

    # スコア計算（速いほど高得点）
    if is_correct:
        time_bonus = max(0, int((st.session_state.time_limit - elapsed) * 5))
        st.session_state.score += 100 + time_bonus
        st.session_state.streak += 1
        st.session_state.max_streak = max(st.session_state.streak, st.session_state.max_streak)
    else:
        st.session_state.streak = 0

    st.session_state.history.append({
        "en": st.session_state.current_word,
        "ja": st.session_state.current_answer,
        "correct": is_correct,
        "elapsed": round(elapsed, 1),
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

# ────────────────────────────────────────────────
# CSS
# ────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
    }

    /* タイトル */
    .game-title {
        font-family: 'Fredoka One', cursive;
        font-size: 3.2em;
        text-align: center;
        background: linear-gradient(90deg, #f7971e, #ffd200, #f7971e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2em;
        text-shadow: none;
        animation: shimmer 3s infinite;
        background-size: 200%;
    }

    @keyframes shimmer {
        0% { background-position: 0% }
        50% { background-position: 100% }
        100% { background-position: 0% }
    }

    /* 問題カード */
    .question-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 24px;
        padding: 2em 2.5em;
        text-align: center;
        margin-bottom: 1.5em;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .question-label {
        color: #ffd200;
        font-size: 0.9em;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5em;
    }

    .question-word {
        font-family: 'Fredoka One', cursive;
        font-size: 3em;
        color: #ffffff;
        margin: 0.2em 0;
    }

    /* スコア・ステータス */
    .stat-box {
        background: rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 0.8em 1.2em;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stat-label {
        color: rgba(255,255,255,0.6);
        font-size: 0.75em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .stat-value {
        color: #ffd200;
        font-family: 'Fredoka One', cursive;
        font-size: 1.8em;
        line-height: 1.2;
    }

    /* 選択肢ボタン */
    .stButton > button {
        width: 100%;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 1.1em;
        padding: 0.8em 1em;
        border-radius: 16px;
        border: 2px solid rgba(255,255,255,0.2);
        background: rgba(255,255,255,0.08);
        color: white;
        cursor: pointer;
        transition: all 0.2s ease;
        backdrop-filter: blur(10px);
    }

    .stButton > button:hover {
        background: rgba(255, 210, 0, 0.2);
        border-color: #ffd200;
        color: #ffd200;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 210, 0, 0.25);
    }

    /* 正解・不正解フィードバック */
    .feedback-correct {
        background: linear-gradient(135deg, rgba(46, 213, 115, 0.2), rgba(46, 213, 115, 0.05));
        border: 2px solid #2ed573;
        border-radius: 16px;
        padding: 1em 1.5em;
        text-align: center;
        color: #2ed573;
        font-weight: 800;
        font-size: 1.2em;
        animation: pop 0.3s ease;
    }

    .feedback-wrong {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.2), rgba(255, 71, 87, 0.05));
        border: 2px solid #ff4757;
        border-radius: 16px;
        padding: 1em 1.5em;
        text-align: center;
        color: #ff4757;
        font-weight: 800;
        font-size: 1.2em;
        animation: shake 0.3s ease;
    }

    @keyframes pop {
        0% { transform: scale(0.9); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    @keyframes shake {
        0%,100% { transform: translateX(0); }
        25% { transform: translateX(-8px); }
        75% { transform: translateX(8px); }
    }

    /* 進捗バー */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 99px;
        height: 8px;
        margin: 0.5em 0 1.5em;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 99px;
        background: linear-gradient(90deg, #f7971e, #ffd200);
        transition: width 0.4s ease;
    }

    /* リザルト */
    .result-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 24px;
        padding: 2.5em;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .result-score {
        font-family: 'Fredoka One', cursive;
        font-size: 5em;
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }

    /* ヒストリーテーブル */
    .history-row-correct {
        color: #2ed573;
        padding: 0.3em 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .history-row-wrong {
        color: #ff6b81;
        padding: 0.3em 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .stSelectbox label, .stRadio label, .stSlider label {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 600;
    }

    .stSelectbox > div > div, .stRadio > div {
        color: white;
    }

    h1, h2, h3, p {
        color: white;
    }

    .streak-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f7971e, #ffd200);
        color: #1a1a2e;
        font-family: 'Fredoka One', cursive;
        font-size: 1em;
        padding: 0.2em 0.8em;
        border-radius: 99px;
    }
    </style>
    """, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# ページ: スタート
# ────────────────────────────────────────────────
def page_start():
    st.markdown('<div class="game-title">🔤 Word Rush!</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.6);margin-bottom:2em;">英単語4択クイズ — 速く答えるほど高得点！</p>', unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.category = st.selectbox(
                "📂 カテゴリ",
                ["全カテゴリ"] + list(WORD_DATA.keys())
            )
            st.session_state.total_questions = st.slider(
                "❓ 問題数", 5, 20, 10, step=5
            )
        with col2:
            st.session_state.mode = st.radio(
                "🔄 出題モード",
                ["日本語→英語", "英語→日本語"]
            )
            st.session_state.time_limit = st.slider(
                "⏱ 制限時間（秒）", 10, 30, 20, step=5
            )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 ゲームスタート！", use_container_width=True):
        start_game()
        st.rerun()

# ────────────────────────────────────────────────
# ページ: プレイ中
# ────────────────────────────────────────────────
def page_playing():
    q_no = st.session_state.question_no
    total = st.session_state.total_questions

    # ゲーム終了チェック
    if q_no >= total and st.session_state.selected is not None:
        # 最後の問題への回答後、少し待ってからresultへ
        st.session_state.phase = "result"
        st.rerun()
        return

    # ── ヘッダー ──
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">問題</div>
            <div class="stat-value">{q_no + 1} / {total}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">スコア</div>
            <div class="stat-value">{st.session_state.score:,}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        streak = st.session_state.streak
        badge = f'<span class="streak-badge">🔥×{streak}</span>' if streak >= 3 else f'<b style="color:#ffd200">{streak}</b>'
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">連続正解</div>
            <div class="stat-value">{badge}</div>
        </div>""", unsafe_allow_html=True)

    # 進捗バー
    pct = int(q_no / total * 100)
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width:{pct}%"></div>
    </div>""", unsafe_allow_html=True)

    # タイマー
    if st.session_state.selected is None:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, st.session_state.time_limit - elapsed)
        pct_time = int(remaining / st.session_state.time_limit * 100)
        color = "#2ed573" if pct_time > 50 else "#ffd200" if pct_time > 25 else "#ff4757"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8em;">
            <span style="color:rgba(255,255,255,0.5);font-size:0.85em;font-weight:700;">⏱ {remaining:.0f}秒</span>
            <div style="flex:1;background:rgba(255,255,255,0.1);border-radius:99px;height:6px;">
                <div style="width:{pct_time}%;height:100%;border-radius:99px;background:{color};transition:width 1s linear;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # 時間切れチェック
        if remaining == 0:
            answer("__timeout__")
            new_question()
            st.rerun()

    # ── 問題カード ──
    mode = st.session_state.mode
    if mode == "日本語→英語":
        display_word = st.session_state.current_answer  # 日本語を表示
        hint = "英語に訳すと？"
    else:
        display_word = st.session_state.current_word    # 英語を表示
        hint = "日本語の意味は？"

    st.markdown(f"""
    <div class="question-card">
        <div class="question-label">{hint}</div>
        <div class="question-word">{display_word}</div>
    </div>""", unsafe_allow_html=True)

    # ── 回答済みフィードバック ──
    if st.session_state.selected is not None:
        if st.session_state.selected == st.session_state.correct:
            elapsed = st.session_state.history[-1]["elapsed"]
            st.markdown(f'<div class="feedback-correct">✅ 正解！ {elapsed}秒で回答</div>', unsafe_allow_html=True)
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

    # ── 選択肢 ──
    choices = st.session_state.choices
    col_a, col_b = st.columns(2)
    for i, choice in enumerate(choices):
        col = col_a if i % 2 == 0 else col_b
        with col:
            if st.button(choice, key=f"choice_{i}"):
                answer(choice)
                if st.session_state.question_no < total:
                    pass  # フィードバック表示のため rerun しない（次ターンで表示）
                st.rerun()

# ────────────────────────────────────────────────
# ページ: 結果
# ────────────────────────────────────────────────
def page_result():
    history = st.session_state.history
    correct_count = sum(1 for h in history if h["correct"])
    total = len(history)
    accuracy = int(correct_count / total * 100) if total else 0
    avg_time = round(sum(h["elapsed"] for h in history) / total, 1) if total else 0

    # ランク判定
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

    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:3em;margin-bottom:0.2em;">{emoji}</div>
        <div style="color:rgba(255,255,255,0.6);font-weight:700;letter-spacing:2px;text-transform:uppercase;font-size:0.9em;">{rank}</div>
        <div class="result-score">{st.session_state.score:,}</div>
        <div style="color:rgba(255,255,255,0.5);font-size:0.85em;margin-top:0.3em;">ポイント</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("正解数", f"{correct_count}/{total}"),
        ("正答率", f"{accuracy}%"),
        ("平均回答時間", f"{avg_time}秒"),
        ("最大連続正解", f"{st.session_state.max_streak}回"),
    ]
    for col, (label, val) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">{label}</div>
                <div class="stat-value" style="font-size:1.4em">{val}</div>
            </div>""", unsafe_allow_html=True)

    # 問題履歴
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 問題の振り返り")
    for i, h in enumerate(history):
        icon = "✅" if h["correct"] else "❌"
        cls = "history-row-correct" if h["correct"] else "history-row-wrong"
        st.markdown(f"""
        <div class="{cls}" style="display:flex;justify-content:space-between;align-items:center;padding:0.5em 0.3em;">
            <span>{icon} Q{i+1}. <b>{h['en']}</b> — {h['ja']}</span>
            <span style="opacity:0.7;font-size:0.85em">{h['elapsed']}秒</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 もう一度プレイ", use_container_width=True):
            start_game()
            st.rerun()
    with col2:
        if st.button("⚙️ 設定に戻る", use_container_width=True):
            st.session_state.phase = "start"
            st.rerun()

# ────────────────────────────────────────────────
# メイン
# ────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Word Rush! 英単語クイズ",
        page_icon="🔤",
        layout="centered",
    )
    init_state()
    inject_css()

    phase = st.session_state.phase
    if phase == "start":
        page_start()
    elif phase == "playing":
        page_playing()
    elif phase == "result":
        page_result()

if __name__ == "__main__":
    main()