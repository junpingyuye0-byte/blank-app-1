import streamlit as st
import random
import time
from words import WORD_DATABASE, IDIOM_DATABASE

# ─── ページ設定 ───────────────────────────────────────────────
st.set_page_config(
    page_title="英単語マスター",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── CSS スタイリング ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700;900&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1e1e2a;
    --accent: #7c3aed;
    --accent2: #06b6d4;
    --green: #10b981;
    --red: #ef4444;
    --yellow: #f59e0b;
    --text: #e2e8f0;
    --muted: #64748b;
}

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans JP', sans-serif;
}

/* サイドバー */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid rgba(124,58,237,0.3);
}
section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* メインコンテンツ */
.block-container {
    padding: 2rem 1.5rem !important;
    max-width: 800px !important;
}

/* タイトルカード */
.title-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.2) 0%, rgba(6,182,212,0.1) 100%);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 2rem;
}
.title-card h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.title-card p {
    color: var(--muted);
    margin-top: 0.5rem;
    font-size: 0.95rem;
}

/* ステータスバー */
.status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    gap: 1rem;
}
.stat-item {
    text-align: center;
    flex: 1;
}
.stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent2);
}
.stat-label {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* タイマーバー */
.timer-container {
    margin-bottom: 1.5rem;
}
.timer-bar-bg {
    background: var(--surface2);
    border-radius: 8px;
    height: 10px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
}

/* 問題カード */
.question-card {
    background: var(--surface);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
}
.question-num {
    font-size: 0.75rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.question-word {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    color: white;
    margin: 0.5rem 0 0.25rem;
    letter-spacing: -1px;
}
.question-hint {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.5rem;
}
.difficulty-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.diff-1 { background: rgba(16,185,129,0.2); color: #10b981; border: 1px solid #10b981; }
.diff-2 { background: rgba(6,182,212,0.2); color: #06b6d4; border: 1px solid #06b6d4; }
.diff-3 { background: rgba(245,158,11,0.2); color: #f59e0b; border: 1px solid #f59e0b; }
.diff-4 { background: rgba(239,68,68,0.2); color: #ef4444; border: 1px solid #ef4444; }

/* 選択肢ボタン */
.stButton > button {
    width: 100%;
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.5rem !important;
    font-family: 'Noto Sans JP', sans-serif !important;
    font-size: 1rem !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 0.5rem !important;
}
.stButton > button:hover {
    background: rgba(124,58,237,0.2) !important;
    border-color: var(--accent) !important;
    transform: translateX(4px) !important;
}

/* 正解・不正解フィードバック */
.feedback-correct {
    background: rgba(16,185,129,0.15);
    border: 1px solid var(--green);
    border-radius: 12px;
    padding: 1.25rem;
    margin-top: 1rem;
    animation: slideIn 0.3s ease;
}
.feedback-wrong {
    background: rgba(239,68,68,0.15);
    border: 1px solid var(--red);
    border-radius: 12px;
    padding: 1.25rem;
    margin-top: 1rem;
    animation: slideIn 0.3s ease;
}
.feedback-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.feedback-related {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.5rem;
}
.feedback-related span {
    background: rgba(124,58,237,0.2);
    border: 1px solid rgba(124,58,237,0.4);
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    margin-right: 0.3rem;
    color: #a78bfa;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
}

/* スピードランモード特有 */
.speedrun-warning {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    color: #fca5a5;
    text-align: center;
    margin-bottom: 1rem;
}

/* 結果画面 */
.result-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(6,182,212,0.1));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin: 1rem 0;
}
.result-score {
    font-family: 'Space Mono', monospace;
    font-size: 4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.result-grade {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0.5rem 0;
}
.miss-list {
    background: var(--surface);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: left;
    margin-top: 1.5rem;
}
.miss-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.9rem;
}
.miss-word { 
    font-family: 'Space Mono', monospace; 
    color: #a78bfa;
    font-weight: 700;
}
.miss-meaning { color: var(--muted); }

/* ウェーブアニメ */
@keyframes slideIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Streamlit デフォルト要素を非表示 */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

/* セレクトボックス */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border-color: rgba(255,255,255,0.1) !important;
}
.stRadio > div {
    background: transparent !important;
}
.stRadio label {
    color: var(--text) !important;
}
div[data-testid="stRadio"] > div {
    flex-direction: column;
    gap: 0.25rem;
}

/* プログレスバー */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #06b6d4) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── セッション状態初期化 ────────────────────────────────────
def init_session():
    defaults = {
        "screen": "home",          # home | game | result
        "mode": "normal",          # normal | speedrun | retry
        "word_mode": "vocab",      # vocab | idiom
        "difficulty": 1,           # 1-4
        "questions": [],
        "current_q": 0,
        "score": 0,
        "total": 10,
        "answered": False,
        "last_correct": None,
        "missed_words": [],
        "wrong_related": [],       # 間違えた単語の関連語（次回出題用）
        "start_time": None,
        "q_start_time": None,
        "speedrun_base_time": 10.0,
        "speedrun_level": 1,
        "lives": 3,                # スピードランのライフ
        "streak": 0,
        "best_streak": 0,
        "q_elapsed": 0,
        "time_expired": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_db():
    return IDIOM_DATABASE if st.session_state.word_mode == "idiom" else WORD_DATABASE


def build_question_pool(difficulty, mode, wrong_related=None):
    """問題セットを構築（間違えた関連語を優先）"""
    db = get_db()
    
    if mode == "retry" and wrong_related:
        # やり直しモード：間違えた単語の関連語を検索して出題
        pool = []
        for d in range(1, 5):
            for w in db.get(d, []):
                if w["word"] in wrong_related or any(r in wrong_related for r in w.get("related", [])):
                    pool.append(w)
        if not pool:
            # フォールバック：同難易度から
            pool = db.get(difficulty, [])
    elif mode == "speedrun":
        # スピードラン：現在の難易度から
        pool = []
        for d in range(1, min(difficulty + 1, 5)):
            pool.extend(db.get(d, []))
    else:
        pool = db.get(difficulty, [])
    
    if not pool:
        pool = db.get(1, [])
    
    # 間違えた関連語が存在すれば優先
    if wrong_related and mode != "retry":
        priority = [w for w in pool if any(r in wrong_related for r in w.get("related", []))]
        rest = [w for w in pool if w not in priority]
        pool = priority + rest
    
    random.shuffle(pool)
    return pool[:st.session_state.total]


def get_speedrun_time_limit():
    """スピードランの残り時間制限（問題が進むごとに短くなる）"""
    level = st.session_state.speedrun_level
    base = st.session_state.speedrun_base_time
    return max(3.0, base - (level - 1) * 0.5)


# ─── ホーム画面 ──────────────────────────────────────────────
def render_home():
    st.markdown("""
    <div class="title-card">
        <h1>📚 VOCAB MASTER</h1>
        <p>英単語・熟語マスターへの道</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🎯 単語モード")
        word_mode = st.radio("", ["vocab", "idiom"], 
                              format_func=lambda x: "📖 単語" if x == "vocab" else "💬 熟語",
                              key="wm_select", horizontal=False)
    with col2:
        st.markdown("#### ⚙️ 難易度")
        diff_map = {
            "🟢 Lv.1 基礎": 1,
            "🔵 Lv.2 中級": 2,
            "🟡 Lv.3 上級": 3,
            "🔴 Lv.4 難関大": 4,
        }
        diff_label = st.radio("", list(diff_map.keys()), key="diff_select", horizontal=False)
        difficulty = diff_map[diff_label]

    st.markdown("---")
    st.markdown("#### 🕹️ ゲームモード")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div style='background:rgba(16,185,129,0.1);border:1px solid #10b981;border-radius:12px;padding:1rem;text-align:center;margin-bottom:0.5rem;'>
            <div style='font-size:2rem'>📝</div>
            <div style='font-weight:700;color:#10b981'>ノーマル</div>
            <div style='font-size:0.75rem;color:#64748b;margin-top:0.3rem'>じっくり学習</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ノーマルで開始", key="start_normal", use_container_width=True):
            start_game("normal", word_mode, difficulty)

    with c2:
        st.markdown("""
        <div style='background:rgba(239,68,68,0.1);border:1px solid #ef4444;border-radius:12px;padding:1rem;text-align:center;margin-bottom:0.5rem;'>
            <div style='font-size:2rem'>⚡</div>
            <div style='font-weight:700;color:#ef4444'>スピードラン</div>
            <div style='font-size:0.75rem;color:#64748b;margin-top:0.3rem'>制限時間付き</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("スピードランで開始", key="start_speed", use_container_width=True):
            start_game("speedrun", word_mode, difficulty)

    with c3:
        has_missed = len(st.session_state.missed_words) > 0
        badge = "" if has_missed else "🔒"
        color = "#f59e0b" if has_missed else "#64748b"
        st.markdown(f"""
        <div style='background:rgba(245,158,11,0.1);border:1px solid {color};border-radius:12px;padding:1rem;text-align:center;margin-bottom:0.5rem;'>
            <div style='font-size:2rem'>{badge}🔄</div>
            <div style='font-weight:700;color:{color}'>やり直し</div>
            <div style='font-size:0.75rem;color:#64748b;margin-top:0.3rem'>間違い克服</div>
        </div>
        """, unsafe_allow_html=True)
        btn_disabled = not has_missed
        if st.button("やり直しで開始" + ("" if has_missed else " (未プレイ)"), 
                     key="start_retry", use_container_width=True, disabled=btn_disabled):
            start_game("retry", word_mode, difficulty)

    # 過去の間違い単語表示
    if st.session_state.missed_words:
        with st.expander(f"📌 間違えた単語 ({len(st.session_state.missed_words)}語)"):
            for m in st.session_state.missed_words[-10:]:
                st.markdown(f"- **{m['word']}** → {m['meaning']}")


def start_game(mode, word_mode, difficulty):
    wrong_related = [w["word"] for w in st.session_state.missed_words] + \
                    [r for w in st.session_state.missed_words for r in w.get("related", [])]
    
    st.session_state.mode = mode
    st.session_state.word_mode = word_mode
    st.session_state.difficulty = difficulty
    st.session_state.questions = build_question_pool(difficulty, mode, wrong_related if mode == "retry" else None)
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_correct = None
    st.session_state.start_time = time.time()
    st.session_state.q_start_time = time.time()
    st.session_state.speedrun_level = 1
    st.session_state.lives = 3
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.time_expired = False
    if mode != "retry":
        st.session_state.wrong_related = wrong_related
    st.session_state.screen = "game"
    st.rerun()


# ─── ゲーム画面 ──────────────────────────────────────────────
def render_game():
    qs = st.session_state.questions
    qi = st.session_state.current_q
    mode = st.session_state.mode
    
    if not qs or qi >= len(qs):
        st.session_state.screen = "result"
        st.rerun()
        return

    q = qs[qi]
    total = len(qs)
    diff_names = {1: "基礎", 2: "中級", 3: "上級", 4: "難関大"}
    diff_colors = {1: "diff-1", 2: "diff-2", 3: "diff-3", 4: "diff-4"}

    # ── ステータスバー ──
    elapsed_total = time.time() - st.session_state.start_time if st.session_state.start_time else 0
    
    col_stat = st.columns(4)
    metrics = [
        ("問題", f"{qi + 1} / {total}"),
        ("正解数", str(st.session_state.score)),
        ("連続正解", f"🔥 {st.session_state.streak}" if st.session_state.streak >= 3 else str(st.session_state.streak)),
        ("経過", f"{int(elapsed_total)}s"),
    ]
    if mode == "speedrun":
        metrics[3] = ("ライフ", "❤️" * st.session_state.lives + "🖤" * (3 - st.session_state.lives))

    for col, (label, val) in zip(col_stat, metrics):
        with col:
            st.markdown(f"""
            <div class='stat-item'>
                <div class='stat-value'>{val}</div>
                <div class='stat-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # プログレスバー
    st.progress((qi) / total)

    # ── スピードランタイマー ──
    if mode == "speedrun" and not st.session_state.answered:
        time_limit = get_speedrun_time_limit()
        elapsed_q = time.time() - (st.session_state.q_start_time or time.time())
        remaining = max(0, time_limit - elapsed_q)
        ratio = remaining / time_limit

        color = "#10b981" if ratio > 0.5 else ("#f59e0b" if ratio > 0.25 else "#ef4444")
        st.markdown(f"""
        <div class='timer-container'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>
                <span style='font-size:0.75rem;color:#64748b;font-family:Space Mono,monospace;'>⏱ 残り時間</span>
                <span style='font-family:Space Mono,monospace;color:{color};font-weight:700;font-size:1.1rem;'>{remaining:.1f}s</span>
            </div>
            <div class='timer-bar-bg'>
                <div style='height:100%;width:{ratio*100:.1f}%;background:{color};border-radius:8px;transition:width 0.1s linear;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 時間切れチェック
        if remaining <= 0 and not st.session_state.time_expired:
            st.session_state.time_expired = True
            st.session_state.answered = True
            st.session_state.last_correct = False
            st.session_state.lives -= 1
            if q not in st.session_state.missed_words:
                st.session_state.missed_words.append(q)
            st.session_state.streak = 0
            st.rerun()

    # スピードランレベル表示
    if mode == "speedrun":
        level = st.session_state.speedrun_level
        time_lim = get_speedrun_time_limit()
        st.markdown(f"""
        <div class='speedrun-warning'>
            ⚡ スピードラン Lv.{level} | 制限時間: {time_lim:.1f}秒 | 難易度は徐々に上昇します
        </div>
        """, unsafe_allow_html=True)

    # ── 問題カード ──
    diff = q.get("difficulty", st.session_state.difficulty)
    wm = "熟語" if st.session_state.word_mode == "idiom" else "単語"
    st.markdown(f"""
    <div class='question-card'>
        <div class='question-num'>{wm} No.{qi + 1} {'⏰ 時間切れ!' if st.session_state.time_expired else ''}</div>
        <div class='question-word'>{q['word']}</div>
        <div class='question-hint'>正しい意味を選んでください</div>
        <div class='difficulty-badge {diff_colors[diff]}'>{diff_names[diff]}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 選択肢 ──
    if not st.session_state.answered:
        options = q["options"].copy()
        random.shuffle(options)
        
        for i, opt in enumerate(options):
            if st.button(f"　{opt}", key=f"opt_{qi}_{i}", use_container_width=True):
                correct = (opt == q["meaning"])
                st.session_state.answered = True
                st.session_state.last_correct = correct
                st.session_state.time_expired = False
                
                if correct:
                    st.session_state.score += 1
                    st.session_state.streak += 1
                    if st.session_state.streak > st.session_state.best_streak:
                        st.session_state.best_streak = st.session_state.streak
                else:
                    if q not in st.session_state.missed_words:
                        st.session_state.missed_words.append(q)
                    # 関連語を記録
                    for r in q.get("related", []):
                        if r not in st.session_state.wrong_related:
                            st.session_state.wrong_related.append(r)
                    st.session_state.streak = 0
                    if mode == "speedrun":
                        st.session_state.lives -= 1
                
                st.rerun()
    else:
        # ── フィードバック ──
        time_expired = st.session_state.time_expired
        correct = st.session_state.last_correct
        
        if time_expired:
            st.markdown(f"""
            <div class='feedback-wrong'>
                <div class='feedback-icon'>⏰</div>
                <div><strong>時間切れ！</strong></div>
                <div style='margin-top:0.5rem;'>正解：<strong style='color:#10b981'>{q['meaning']}</strong></div>
                <div class='feedback-related'>
                    関連語: {''.join([f"<span>{r}</span>" for r in q.get('related', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif correct:
            streak_msg = f" 🔥 {st.session_state.streak}連続正解！" if st.session_state.streak >= 3 else ""
            st.markdown(f"""
            <div class='feedback-correct'>
                <div class='feedback-icon'>✅</div>
                <div><strong>正解！{streak_msg}</strong></div>
                <div style='margin-top:0.5rem;color:#94a3b8;font-size:0.9rem;'>{q['meaning']}</div>
                <div class='feedback-related'>
                    類義語: {''.join([f"<span>{r}</span>" for r in q.get('related', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='feedback-wrong'>
                <div class='feedback-icon'>❌</div>
                <div><strong>不正解</strong></div>
                <div style='margin-top:0.5rem;'>正解：<strong style='color:#10b981'>{q['meaning']}</strong></div>
                <div class='feedback-related'>
                    ⚠️ 次回は関連語から出題: {''.join([f"<span>{r}</span>" for r in q.get('related', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ライフ切れチェック
        if mode == "speedrun" and st.session_state.lives <= 0:
            st.warning("💀 ライフがなくなりました！")
            if st.button("🏁 結果を見る", use_container_width=True):
                st.session_state.screen = "result"
                st.rerun()
            return

        # 次へ / 終了
        is_last = (qi + 1 >= total)
        btn_label = "🏁 結果を見る" if is_last else "次の問題 →"
        
        if st.button(btn_label, use_container_width=True, type="primary"):
            if is_last:
                st.session_state.screen = "result"
            else:
                st.session_state.current_q += 1
                st.session_state.answered = False
                st.session_state.last_correct = None
                st.session_state.time_expired = False
                st.session_state.q_start_time = time.time()
                # スピードラン：問題が進むごとにレベルアップ
                if mode == "speedrun":
                    new_level = (st.session_state.current_q // 3) + 1
                    st.session_state.speedrun_level = min(new_level, 8)
            st.rerun()


# ─── 結果画面 ────────────────────────────────────────────────
def render_result():
    score = st.session_state.score
    total = len(st.session_state.questions)
    pct = (score / total * 100) if total > 0 else 0
    elapsed = time.time() - (st.session_state.start_time or time.time())
    mode_names = {"normal": "ノーマル", "speedrun": "スピードラン", "retry": "やり直し"}
    
    # 評価
    if pct >= 90:
        grade, grade_color, msg = "S", "#f59e0b", "完璧！マスタークラス！"
    elif pct >= 75:
        grade, grade_color, msg = "A", "#10b981", "素晴らしい！"
    elif pct >= 60:
        grade, grade_color, msg = "B", "#06b6d4", "なかなか良い！"
    elif pct >= 40:
        grade, grade_color, msg = "C", "#7c3aed", "もう少し頑張ろう"
    else:
        grade, grade_color, msg = "D", "#ef4444", "要復習！"

    st.markdown(f"""
    <div class='result-card'>
        <div style='font-size:0.8rem;color:#64748b;letter-spacing:2px;text-transform:uppercase;margin-bottom:1rem;'>
            {mode_names.get(st.session_state.mode, "")} | {int(elapsed)}秒
        </div>
        <div class='result-score'>{score} / {total}</div>
        <div class='result-grade' style='color:{grade_color};'>ランク {grade}　{msg}</div>
        <div style='margin-top:1rem;color:#94a3b8;font-size:0.9rem;'>
            正答率 {pct:.0f}%　|　最大連続正解 {st.session_state.best_streak}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 間違えた単語リスト
    session_missed = [q for q in st.session_state.questions 
                      if q not in [w for w in st.session_state.missed_words 
                                   if w not in st.session_state.questions]] 
    # 今回の間違い
    current_missed = []
    for q in st.session_state.questions:
        if q in st.session_state.missed_words:
            current_missed.append(q)

    if current_missed:
        st.markdown("<div class='miss-list'>", unsafe_allow_html=True)
        st.markdown("**📌 今回間違えた単語**")
        for m in current_missed:
            related_str = " / ".join(m.get("related", [])[:3])
            st.markdown(f"""
            <div class='miss-item'>
                <span class='miss-word'>{m['word']}</span>
                <span class='miss-meaning'>{m['meaning']}</span>
            </div>
            <div style='font-size:0.75rem;color:#475569;padding-bottom:0.5rem;padding-left:0.5rem;'>
                類義語: {related_str}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 ホームに戻る", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()
    with c2:
        has_missed = len(st.session_state.missed_words) > 0
        if st.button(f"🔄 やり直しモード {'(' + str(len(st.session_state.missed_words)) + '語)' if has_missed else ''}", 
                     use_container_width=True, disabled=not has_missed):
            start_game("retry", st.session_state.word_mode, st.session_state.difficulty)


# ─── サイドバー ──────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("### 📊 セッション統計")
        st.metric("累積ミス単語", len(st.session_state.missed_words))
        st.metric("最大連続正解", st.session_state.best_streak)
        
        st.markdown("---")
        st.markdown("### ℹ️ 難易度ガイド")
        levels = [
            ("🟢 Lv.1", "基礎", "高校基礎〜日常語"),
            ("🔵 Lv.2", "中級", "大学受験基礎"),
            ("🟡 Lv.3", "上級", "難関私大レベル"),
            ("🔴 Lv.4", "難関大", "東大・京大・旧帝大"),
        ]
        for icon, name, desc in levels:
            st.markdown(f"{icon} **{name}** — {desc}")
        
        st.markdown("---")
        st.markdown("### 🎮 ゲームモード説明")
        st.markdown("""
- **ノーマル**: 制限なし、じっくり学習
- **スピードラン**: 制限時間付き、進むほど短くなる
- **やり直し**: 間違えた単語の関連語を重点出題
        """)
        
        if st.session_state.missed_words:
            if st.button("🗑️ 間違いリストをリセット"):
                st.session_state.missed_words = []
                st.session_state.wrong_related = []
                st.rerun()


# ─── メインルーター ──────────────────────────────────────────
def main():
    init_session()
    render_sidebar()
    
    screen = st.session_state.screen
    if screen == "home":
        render_home()
    elif screen == "game":
        render_game()
    elif screen == "result":
        render_result()
    
    # スピードランは自動リフレッシュが必要
    if st.session_state.screen == "game" and st.session_state.mode == "speedrun" \
       and not st.session_state.answered:
        time.sleep(0.1)
        st.rerun()


if __name__ == "__main__":
    main()