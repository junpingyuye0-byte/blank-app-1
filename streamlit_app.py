import streamlit as st
import random
import time
from questions import QUESTIONS_BY_LEVEL, LEVEL_INFO

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚗️ ChemLab Blast",
    page_icon="⚗️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

/* ── base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0D1B2A !important;
    color: #E8F4FD;
    font-family: 'Exo 2', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: #0a1520 !important; }
.block-container { padding-top: 1rem !important; max-width: 760px; }

/* ── title ── */
.game-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00F5D4 0%, #7B2D8B 60%, #FF6B35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0;
    letter-spacing: 0.04em;
    text-shadow: none;
}
.game-sub {
    text-align: center;
    color: #6CBFD4;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    margin-top: 0;
    margin-bottom: 1.6rem;
    text-transform: uppercase;
}

/* ── level cards ── */
.level-grid { display: flex; gap: 0.8rem; flex-wrap: wrap; justify-content: center; margin-bottom: 1.5rem; }
.level-card {
    border: 1.5px solid;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    width: 155px;
    cursor: pointer;
    text-align: center;
    transition: transform 0.15s, box-shadow 0.15s;
}
.level-card:hover { transform: translateY(-3px); }

/* ── hud bar ── */
.hud {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,245,212,0.2);
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    margin-bottom: 1rem;
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    gap: 0.5rem;
}
.hud-item { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.hud-label { color: #6CBFD4; font-size: 0.6rem; letter-spacing: 0.15em; }
.hud-value { color: #00F5D4; font-size: 1.1rem; font-weight: 700; }
.hud-combo { color: #FF6B35; }
.hud-time  { color: #FFD166; }

/* ── experiment gauge ── */
.gauge-wrap { margin-bottom: 1.2rem; }
.gauge-label {
    font-size: 0.7rem;
    color: #6CBFD4;
    letter-spacing: 0.15em;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
}
.gauge-outer {
    height: 18px;
    background: rgba(255,255,255,0.06);
    border-radius: 9px;
    border: 1px solid rgba(0,245,212,0.25);
    overflow: hidden;
    position: relative;
}
.gauge-inner {
    height: 100%;
    border-radius: 9px;
    transition: width 0.4s cubic-bezier(.4,2,.6,1);
    position: relative;
}
.gauge-inner::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.35) 100%);
    border-radius: 9px;
}

/* ── question card ── */
.q-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(0,245,212,0.25);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
}
.q-type-badge {
    display: inline-block;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    padding: 2px 10px;
    border-radius: 20px;
    margin-bottom: 0.7rem;
    font-family: 'Orbitron', monospace;
}
.q-text {
    font-size: 1.15rem;
    font-weight: 600;
    color: #E8F4FD;
    line-height: 1.5;
}

/* ── answer buttons ── */
.stButton > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(0,245,212,0.35) !important;
    color: #E8F4FD !important;
    border-radius: 10px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 0.55rem 1rem !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.15s !important;
    min-height: 52px !important;
}
.stButton > button:hover {
    background: rgba(0,245,212,0.12) !important;
    border-color: #00F5D4 !important;
    transform: translateX(4px) !important;
    box-shadow: 0 0 14px rgba(0,245,212,0.2) !important;
}

/* ── feedback ── */
.feedback-correct {
    background: rgba(0,245,212,0.12);
    border: 1.5px solid #00F5D4;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    color: #00F5D4;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
.feedback-wrong {
    background: rgba(255,107,53,0.12);
    border: 1.5px solid #FF6B35;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    color: #FF6B35;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
.explosion-banner {
    background: linear-gradient(135deg, rgba(255,107,53,0.2), rgba(123,45,139,0.2));
    border: 2px solid #FF6B35;
    border-radius: 14px;
    padding: 0.9rem;
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    color: #FF6B35;
    animation: pulse 0.6s ease-in-out;
    margin-bottom: 0.8rem;
}
@keyframes pulse {
    0%   { transform: scale(0.95); opacity: 0.6; }
    50%  { transform: scale(1.03); opacity: 1; }
    100% { transform: scale(1);    opacity: 1; }
}

/* ── result screen ── */
.result-card {
    background: rgba(255,255,255,0.04);
    border: 2px solid rgba(0,245,212,0.4);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}
.result-rank {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 900;
    margin-bottom: 0.3rem;
}
.result-score {
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    color: #00F5D4;
    margin-bottom: 0.5rem;
}

/* ── streamlit overrides ── */
div[data-testid="column"] { gap: 0.5rem; }
.stSelectbox > div { background: #0D1B2A !important; }
hr { border-color: rgba(0,245,212,0.15) !important; }
p { color: #C8DDE8; }
</style>
""", unsafe_allow_html=True)


# ─── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = dict(
        screen="home",         # home | playing | result
        level=None,
        questions=[],
        q_index=0,
        score=0,
        combo=0,
        max_combo=0,
        multiplier=1.0,
        exp_gauge=0,           # 0-100 experiment gauge
        explosion_pending=False,
        answered=False,
        correct_this=False,
        chosen_idx=None,
        q_start_time=None,
        total_time=0.0,
        time_bonus=0,
        lives=3,
        wrong_this_q=False,
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
S = st.session_state


# ─── Helpers ──────────────────────────────────────────────────────────────────
GAUGE_COLORS = {
    1: "#00F5D4",
    2: "#4FC3F7",
    3: "#AB47BC",
    4: "#FF6B35",
}

def gauge_color(level):
    return GAUGE_COLORS.get(level, "#00F5D4")

def rank(score, total):
    pct = score / max(total, 1)
    if pct >= 0.95: return "🥇 S RANK", "#FFD700"
    if pct >= 0.80: return "🥈 A RANK", "#00F5D4"
    if pct >= 0.60: return "🥉 B RANK", "#7B2D8B"
    if pct >= 0.40: return "⚗️ C RANK", "#4FC3F7"
    return "🔬 D RANK", "#FF6B35"

def start_game(level):
    pool = QUESTIONS_BY_LEVEL[level][:]
    random.shuffle(pool)
    S.level       = level
    S.questions   = pool[:10]
    S.q_index     = 0
    S.score       = 0
    S.combo       = 0
    S.max_combo   = 0
    S.multiplier  = 1.0
    S.exp_gauge   = 0
    S.explosion_pending = False
    S.answered    = False
    S.correct_this= False
    S.chosen_idx  = None
    S.q_start_time= time.time()
    S.total_time  = 0.0
    S.time_bonus  = 0
    S.lives       = 3
    S.wrong_this_q= False
    S.screen      = "playing"

def advance():
    S.q_index     += 1
    S.answered    = False
    S.correct_this= False
    S.chosen_idx  = None
    S.explosion_pending = False
    S.q_start_time= time.time()
    S.wrong_this_q= False
    if S.q_index >= len(S.questions):
        S.screen = "result"

def answer(idx):
    if S.answered:
        return
    S.answered   = True
    S.chosen_idx = idx
    q = S.questions[S.q_index]
    elapsed = time.time() - S.q_start_time
    S.total_time += elapsed

    level_info = LEVEL_INFO[S.level]
    time_limit = level_info["time"]
    base_pts   = level_info["base_pts"]

    if idx == q["answer"]:
        S.correct_this = True
        # time bonus
        if elapsed < time_limit:
            tb = int((1 - elapsed / time_limit) * base_pts * 0.5)
        else:
            tb = 0
        S.time_bonus = tb

        # combo & multiplier
        S.combo += 1
        S.max_combo = max(S.max_combo, S.combo)
        S.multiplier = round(min(1.0 + (S.combo - 1) * 0.25, 3.0), 2)

        # exp gauge
        gauge_gain = 20 + (S.combo * 5)
        S.exp_gauge = min(S.exp_gauge + gauge_gain, 100)
        if S.exp_gauge >= 100:
            S.explosion_pending = True
            S.exp_gauge = 0

        pts = int((base_pts + tb) * S.multiplier)
        if S.explosion_pending:
            pts = int(pts * 1.5)  # explosion bonus
        S.score += pts
    else:
        S.correct_this = False
        S.combo        = 0
        S.multiplier   = 1.0
        S.exp_gauge    = max(S.exp_gauge - 15, 0)
        if not S.wrong_this_q:
            S.lives -= 1
            S.wrong_this_q = True


# ─── SCREEN: HOME ─────────────────────────────────────────────────────────────
if S.screen == "home":
    st.markdown('<h1 class="game-title">⚗️ ChemLab Blast</h1>', unsafe_allow_html=True)
    st.markdown('<p class="game-sub">元素・反応式・実験 — 化学をぶっ壊せ</p>', unsafe_allow_html=True)

    # System explanation
    with st.expander("🔥 ゲームシステムを見る"):
        st.markdown("""
**⚡ コンボ & 倍率システム**  
連続正解でコンボが積み上がり、得点倍率が最大 **×3.0** まで上昇！

**⏱ タイムボーナス**  
制限時間内に早く答えるほどボーナス得点 UP。瞬発力が試される！

**🧪 実験ゲージ**  
正解でゲージが溜まり **100%** に達すると **EXPLOSION!! 💥**  
その問題の得点が **×1.5** になる大チャンス。ゲージは間違えると減る。

**❤️ ライフ制**  
ライフは3つ。間違えるたびに1消費（問題ごとに1回まで）。

**🏆 ランク判定**  
最終スコアで S / A / B / C / D ランクを認定。S ランクを目指せ！
        """)

    st.markdown("---")
    st.markdown("#### レベルを選んでスタート")

    cols = st.columns(4)
    for lv in [1, 2, 3, 4]:
        info = LEVEL_INFO[lv]
        with cols[lv - 1]:
            color = gauge_color(lv)
            st.markdown(f"""
<div class="level-card" style="border-color:{color}22; background:rgba(255,255,255,0.03);">
  <div style="font-family:'Orbitron',monospace; color:{color}; font-size:1.3rem; font-weight:900;">Lv.{lv}</div>
  <div style="font-size:1.4rem; margin:4px 0;">{info['icon']}</div>
  <div style="font-weight:700; color:#E8F4FD; font-size:0.85rem;">{info['name']}</div>
  <div style="color:#6CBFD4; font-size:0.7rem; margin-top:4px;">{info['desc']}</div>
  <div style="color:{color}; font-size:0.7rem; margin-top:6px; font-family:'Orbitron',monospace;">⏱ {info['time']}秒</div>
</div>
""", unsafe_allow_html=True)
            if st.button(f"Lv.{lv} スタート", key=f"start_{lv}", use_container_width=True):
                start_game(lv)
                st.rerun()


# ─── SCREEN: PLAYING ──────────────────────────────────────────────────────────
elif S.screen == "playing":
    if S.lives <= 0 and not S.answered:
        S.screen = "result"
        st.rerun()

    q = S.questions[S.q_index]
    info = LEVEL_INFO[S.level]
    color = gauge_color(S.level)
    total_qs = len(S.questions)

    # HUD
    hearts = "❤️" * S.lives + "🖤" * (3 - S.lives)
    elapsed_now = time.time() - S.q_start_time if not S.answered else 0
    remaining = max(info["time"] - elapsed_now, 0)

    st.markdown(f"""
<div class="hud">
  <div class="hud-item"><span class="hud-label">SCORE</span><span class="hud-value">{S.score:,}</span></div>
  <div class="hud-item"><span class="hud-label">COMBO</span><span class="hud-value hud-combo">×{S.multiplier:.2f}</span></div>
  <div class="hud-item"><span class="hud-label">Q</span><span class="hud-value">{S.q_index+1}/{total_qs}</span></div>
  <div class="hud-item"><span class="hud-label">TIME</span><span class="hud-value hud-time">{remaining:.0f}s</span></div>
  <div class="hud-item"><span class="hud-label">LIFE</span><span class="hud-value" style="font-size:0.9rem;">{hearts}</span></div>
</div>
""", unsafe_allow_html=True)

    # Experiment Gauge
    gauge_w = S.exp_gauge
    st.markdown(f"""
<div class="gauge-wrap">
  <div class="gauge-label">
    <span>🧪 EXPERIMENT GAUGE</span>
    <span style="color:{color};">{S.exp_gauge}% {'⚡ COMBO ×' + str(S.combo) if S.combo > 1 else ''}</span>
  </div>
  <div class="gauge-outer">
    <div class="gauge-inner" style="width:{gauge_w}%; background:linear-gradient(90deg,{color}88,{color});"></div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Explosion banner
    if S.explosion_pending and S.answered:
        st.markdown('<div class="explosion-banner">💥 EXPLOSION!! 得点 ×1.5 ボーナス発動！</div>', unsafe_allow_html=True)

    # Question card
    type_colors = {
        "element": ("#00F5D4", "元素記号"),
        "reaction": ("#AB47BC", "化学反応式"),
        "experiment": ("#FF6B35", "実験結果"),
    }
    tc, tl = type_colors.get(q.get("type", "element"), ("#00F5D4", "化学"))
    st.markdown(f"""
<div class="q-card">
  <span class="q-type-badge" style="background:{tc}22; color:{tc}; border:1px solid {tc}55;">
    {tl}
  </span>
  <div class="q-text">{q["question"]}</div>
</div>
""", unsafe_allow_html=True)

    # Answer choices
    for i, opt in enumerate(q["options"]):
        label = f"{'ABCD'[i]}. {opt}"
        if st.button(label, key=f"opt_{i}", use_container_width=True):
            if not S.answered:
                answer(i)
                st.rerun()

    # Feedback
    if S.answered:
        correct_opt = q["options"][q["answer"]]
        if S.correct_this:
            pts_gained = int((info["base_pts"] + S.time_bonus) * (S.multiplier / (1 + 0.25 * max(S.combo - 1, 0)) if S.combo > 1 else 1.0))
            bonus_str = f" ⚡ タイムボーナス +{S.time_bonus}" if S.time_bonus > 0 else ""
            combo_str = f" 🔥 コンボ {S.combo}×！" if S.combo > 1 else ""
            st.markdown(f'<div class="feedback-correct">✅ 正解！{bonus_str}{combo_str}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-wrong">❌ 不正解… 正解は「{correct_opt}」でした。</div>', unsafe_allow_html=True)

        if q.get("explanation"):
            st.info(f"💡 {q['explanation']}")

        col1, col2 = st.columns([1, 2])
        with col2:
            label = "次の問題 →" if S.q_index < total_qs - 1 else "結果を見る 🏁"
            if st.button(label, type="primary", use_container_width=True):
                advance()
                st.rerun()

    # Time-up check (auto-advance after time_limit if not answered)
    if not S.answered:
        elapsed_check = time.time() - S.q_start_time
        if elapsed_check > info["time"]:
            answer(-1)  # wrong (no selection)
            st.rerun()
        else:
            time.sleep(0.5)
            st.rerun()


# ─── SCREEN: RESULT ───────────────────────────────────────────────────────────
elif S.screen == "result":
    info = LEVEL_INFO[S.level]
    max_possible = info["base_pts"] * len(S.questions) * 3  # rough max with multiplier
    rank_txt, rank_col = rank(S.score, max_possible)

    st.markdown('<h1 class="game-title">RESULT</h1>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="result-card">
  <div class="result-rank" style="color:{rank_col};">{rank_txt}</div>
  <div class="result-score">{S.score:,} pt</div>
  <div style="color:#6CBFD4; font-size:0.85rem;">Lv.{S.level} {info['name']} | 10問</div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        correct_count = sum(
            1 for i, q in enumerate(S.questions)
            if i < S.q_index
        )
        st.metric("最大コンボ", f"×{S.max_combo}")
    with col2:
        avg = S.total_time / max(S.q_index, 1)
        st.metric("平均回答時間", f"{avg:.1f}秒")
    with col3:
        st.metric("残りライフ", f"❤️ × {S.lives}")

    st.markdown("---")

    # Retry or home buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 もう一度", use_container_width=True):
            start_game(S.level)
            st.rerun()
    with c2:
        next_lv = min(S.level + 1, 4)
        if S.level < 4:
            if st.button(f"⬆️ Lv.{next_lv} に挑戦", use_container_width=True):
                start_game(next_lv)
                st.rerun()
        else:
            st.button("🏆 最高難度クリア！", disabled=True, use_container_width=True)
    with c3:
        if st.button("🏠 ホームへ", use_container_width=True):
            S.screen = "home"
            st.rerun()