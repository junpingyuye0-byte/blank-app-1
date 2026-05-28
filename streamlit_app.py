import streamlit as st
import anthropic
import json
import os
import re
from datetime import datetime

# ─── ページ設定 ───────────────────────────────────────────────
st.set_page_config(
    page_title="世界史クイズ📜",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── カスタムCSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&family=Noto+Sans+JP:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
}
h1, h2, h3 { font-family: 'Noto Serif JP', serif; }

.main-title {
    text-align: center;
    font-family: 'Noto Serif JP', serif;
    font-size: 2.8rem;
    color: #2c1810;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 0.2rem;
}
.sub-title {
    text-align: center;
    color: #8B6914;
    font-size: 1rem;
    margin-bottom: 2rem;
    letter-spacing: 0.2em;
}
.question-box {
    background: linear-gradient(135deg, #1a0f0a, #2c1810);
    border: 2px solid #c8a96e;
    border-radius: 16px;
    padding: 2rem;
    color: #fdf6e3;
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.question-number {
    font-size: 0.75rem;
    color: #c8a96e;
    letter-spacing: 0.15em;
    margin-bottom: 0.5rem;
}
.correct-banner {
    background: linear-gradient(135deg, #1a4a1a, #2d7a2d);
    border: 2px solid #4CAF50;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #a8f0a8;
    font-size: 1.1rem;
    font-weight: bold;
    margin: 1rem 0;
    text-align: center;
}
.wrong-banner {
    background: linear-gradient(135deg, #4a1a1a, #7a2d2d);
    border: 2px solid #f44336;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #faa;
    font-size: 1.1rem;
    font-weight: bold;
    margin: 1rem 0;
    text-align: center;
}
.explanation-box {
    background: #2c1810;
    border-left: 4px solid #c8a96e;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.5rem;
    color: #fdf6e3;
    margin: 1rem 0;
    font-size: 0.95rem;
    line-height: 1.7;
}
.note-card {
    background: linear-gradient(135deg, #fffbf0, #fdf1d3);
    border: 1px solid #e8c87a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid #c8a96e;
}
.note-tag {
    background: #c8a96e;
    color: white;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin-right: 0.5rem;
}
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #c8a96e, #f0c96e);
    color: #1a0f0a;
    font-weight: bold;
    font-size: 1.5rem;
    padding: 0.5rem 1.5rem;
    border-radius: 30px;
    box-shadow: 0 2px 10px rgba(200, 169, 110, 0.5);
}
.sidebar-stat {
    background: rgba(200, 169, 110, 0.1);
    border-radius: 8px;
    padding: 0.6rem 0.8rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #fdf6e3;
}
div[data-testid="stTabs"] button {
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 0.9rem;
}
.stButton > button {
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─── データ保存パス ───────────────────────────────────────────
DATA_DIR = os.path.expanduser("~/.history_quiz_data")
os.makedirs(DATA_DIR, exist_ok=True)
NOTES_FILE    = os.path.join(DATA_DIR, "notes.json")
HISTORY_FILE  = os.path.join(DATA_DIR, "history.json")
MISTAKES_FILE = os.path.join(DATA_DIR, "mistakes.json")


def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─── セッション初期化 ─────────────────────────────────────────
def init_session():
    defaults = {
        "mode": None,
        "question": None,
        "answer": None,
        "explanation": None,
        "choices": None,
        "user_answer": None,
        "answered": False,
        "is_correct": None,
        "score": 0,
        "total": 0,
        "mistake_added": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─── Anthropic クライアント ───────────────────────────────────
client = anthropic.Anthropic()

MODES = {
    "📅 年号クイズ":      "year",
    "👤 人物名クイズ":    "person",
    "⚡ 出来事クイズ":    "event",
    "🏆 人物の業績クイズ": "achievement",
}

MODE_PROMPTS = {
    "year":        "世界史の重要な出来事の年号を問う4択クイズを1問作ってください。",
    "person":      "世界史上の重要な人物名を問う4択クイズを1問作ってください。",
    "event":       "世界史上の重要な出来事・事件を問う4択クイズを1問作ってください。",
    "achievement": "世界史上の人物が行ったことや業績・功績を問う4択クイズを1問作ってください。",
}


def generate_question(mode: str):
    prompt = MODE_PROMPTS[mode] + """

以下のJSON形式のみで答えてください。マークダウンコードブロックは不要です：
{
  "question": "問題文",
  "choices": ["A. 選択肢1", "B. 選択肢2", "C. 選択肢3", "D. 選択肢4"],
  "answer": "A",
  "explanation": "解説（100字程度）"
}"""

    full_text = ""
    placeholder = st.empty()
    placeholder.info("⏳ 問題を生成中...")

    try:
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                full_text += text

        placeholder.empty()
        json_match = re.search(r"\{.*\}", full_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        placeholder.error(f"エラーが発生しました: {e}")
    return None


def add_mistake(question_data: dict, mode: str, user_answer: str):
    mistakes = load_json(MISTAKES_FILE, [])
    mistakes.append({
        "id":          datetime.now().isoformat(),
        "date":        datetime.now().strftime("%Y/%m/%d %H:%M"),
        "mode":        mode,
        "question":    question_data.get("question", ""),
        "choices":     question_data.get("choices", []),
        "answer":      question_data.get("answer", ""),
        "explanation": question_data.get("explanation", ""),
        "user_answer": user_answer,
    })
    save_json(MISTAKES_FILE, mistakes)


def add_to_history(question: str, correct: bool, mode: str):
    history = load_json(HISTORY_FILE, [])
    history.append({
        "date":     datetime.now().strftime("%Y/%m/%d %H:%M"),
        "mode":     mode,
        "question": question[:60] + "…" if len(question) > 60 else question,
        "correct":  correct,
    })
    if len(history) > 200:
        history = history[-200:]
    save_json(HISTORY_FILE, history)


# ─── ヘッダー ─────────────────────────────────────────────────
st.markdown('<h1 class="main-title">📜 世界史クイズ</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">WORLD HISTORY QUIZ — AI POWERED</p>', unsafe_allow_html=True)

# ─── サイドバー ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗺️ ナビゲーション")

    history_data = load_json(HISTORY_FILE, [])
    mistakes_data = load_json(MISTAKES_FILE, [])
    total_q   = len(history_data)
    correct_q = sum(1 for h in history_data if h.get("correct"))
    accuracy  = f"{correct_q/total_q*100:.0f}%" if total_q > 0 else "—"

    st.markdown(f"""
    <div class="sidebar-stat">📊 総問題数：<b>{total_q}</b> 問</div>
    <div class="sidebar-stat">✅ 正解数：<b>{correct_q}</b> 問</div>
    <div class="sidebar-stat">🎯 正答率：<b>{accuracy}</b></div>
    <div class="sidebar-stat">❌ 要復習：<b>{len(mistakes_data)}</b> 問</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎮 モード選択")
    for label, key in MODES.items():
        if st.button(label, key=f"mode_{key}", use_container_width=True):
            st.session_state.mode      = key
            st.session_state.question  = None
            st.session_state.answered  = False
            st.session_state.user_answer = None
            st.session_state.is_correct  = None
            st.session_state.mistake_added = False
            st.rerun()

# ─── タブ ─────────────────────────────────────────────────────
tab_quiz, tab_notes, tab_history, tab_mistakes = st.tabs(
    ["🎮 クイズ", "📒 ノート", "📈 履歴", "❌ 間違いリスト"]
)

# ══════════════════════════════════════════════
# TAB 1: クイズ
# ══════════════════════════════════════════════
with tab_quiz:
    if st.session_state.mode is None:
        st.markdown("### 👈 左のサイドバーからモードを選んでください")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**📅 年号クイズ** — 重要な出来事の年を問う  
**👤 人物名クイズ** — 歴史的人物の名前を当てる
""")
        with col2:
            st.markdown("""
**⚡ 出来事クイズ** — 何が起きたかを問う  
**🏆 業績クイズ** — 誰が何をしたかを問う
""")
    else:
        mode = st.session_state.mode
        mode_labels = {v: k for k, v in MODES.items()}
        st.markdown(f"#### {mode_labels.get(mode, mode)}")

        # 問題生成
        if st.session_state.question is None:
            if st.button("🎲 問題を出す", type="primary", use_container_width=True):
                data = generate_question(mode)
                if data:
                    st.session_state.question    = data.get("question")
                    st.session_state.choices     = data.get("choices", [])
                    st.session_state.answer      = data.get("answer")
                    st.session_state.explanation = data.get("explanation")
                    st.session_state.answered    = False
                    st.session_state.user_answer = None
                    st.session_state.is_correct  = None
                    st.session_state.mistake_added = False
                    st.rerun()
        else:
            # 問題表示
            st.markdown(f"""
<div class="question-box">
    <div class="question-number">QUESTION</div>
    <div style="font-size:1.15rem; font-weight:500;">{st.session_state.question}</div>
</div>
""", unsafe_allow_html=True)

            if not st.session_state.answered:
                choices = st.session_state.choices or []
                cols = st.columns(2)
                for i, choice in enumerate(choices):
                    with cols[i % 2]:
                        if st.button(choice, key=f"choice_{i}", use_container_width=True):
                            letter = choice[0]
                            st.session_state.user_answer = letter
                            st.session_state.answered    = True
                            correct = (letter == st.session_state.answer)
                            st.session_state.is_correct  = correct
                            add_to_history(st.session_state.question, correct, mode)
                            if correct:
                                st.session_state.score += 1
                            elif not st.session_state.mistake_added:
                                add_mistake({
                                    "question":    st.session_state.question,
                                    "choices":     st.session_state.choices,
                                    "answer":      st.session_state.answer,
                                    "explanation": st.session_state.explanation,
                                }, mode, letter)
                                st.session_state.mistake_added = True
                            st.session_state.total += 1
                            st.rerun()
            else:
                if st.session_state.is_correct:
                    st.markdown('<div class="correct-banner">🎉 正解！素晴らしい！</div>', unsafe_allow_html=True)
                else:
                    correct_choice = next(
                        (c for c in (st.session_state.choices or []) if c.startswith(st.session_state.answer)), ""
                    )
                    st.markdown(
                        f'<div class="wrong-banner">❌ 不正解… 正解は「{correct_choice}」です</div>',
                        unsafe_allow_html=True,
                    )

                if st.session_state.explanation:
                    st.markdown(f"""
<div class="explanation-box">
📚 <b>解説</b><br>{st.session_state.explanation}
</div>
""", unsafe_allow_html=True)

                s, t = st.session_state.score, st.session_state.total
                acc = f"{s/t*100:.0f}%" if t > 0 else "—"
                st.markdown(f"""
<div style="text-align:center; margin:1rem 0;">
    <span class="score-badge">✅ {s} / {t}　（{acc}）</span>
</div>
""", unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("➡️ 次の問題", type="primary", use_container_width=True):
                        st.session_state.question    = None
                        st.session_state.answered    = False
                        st.session_state.user_answer = None
                        st.session_state.is_correct  = None
                        st.session_state.mistake_added = False
                        st.rerun()
                with col_b:
                    if not st.session_state.is_correct:
                        if st.button("📒 ノートに追加", use_container_width=True):
                            notes = load_json(NOTES_FILE, [])
                            notes.append({
                                "id":      datetime.now().isoformat(),
                                "date":    datetime.now().strftime("%Y/%m/%d %H:%M"),
                                "title":   st.session_state.question[:40] + "…",
                                "content": f"【問題】{st.session_state.question}\n【正解】{st.session_state.answer}\n【解説】{st.session_state.explanation}",
                                "tags":    [mode],
                            })
                            save_json(NOTES_FILE, notes)
                            st.success("ノートに追加しました！")

# ══════════════════════════════════════════════
# TAB 2: ノート
# ══════════════════════════════════════════════
with tab_notes:
    st.markdown("### 📒 マイノート")
    notes = load_json(NOTES_FILE, [])

    with st.expander("➕ 新しいノートを追加", expanded=False):
        note_title      = st.text_input("タイトル", placeholder="例：フランス革命のポイント")
        note_content    = st.text_area("内容", placeholder="人物・年号・出来事をまとめよう…", height=150)
        note_tags_input = st.text_input("タグ（カンマ区切り）", placeholder="例：フランス,革命,近代")
        if st.button("💾 保存する", type="primary"):
            if note_title and note_content:
                tags = [t.strip() for t in note_tags_input.split(",") if t.strip()]
                notes.append({
                    "id":      datetime.now().isoformat(),
                    "date":    datetime.now().strftime("%Y/%m/%d %H:%M"),
                    "title":   note_title,
                    "content": note_content,
                    "tags":    tags,
                })
                save_json(NOTES_FILE, notes)
                st.success("✅ 保存しました！")
                st.rerun()
            else:
                st.warning("タイトルと内容を入力してください")

    st.markdown("---")
    if not notes:
        st.info("まだノートがありません。クイズで間違えた問題を自動追加したり、自分でまとめを書いてみましょう！")
    else:
        search = st.text_input("🔍 ノートを検索", placeholder="キーワードで絞り込み")
        filtered = [n for n in notes if not search or search in n.get("title","") or search in n.get("content","")]

        for i, note in enumerate(reversed(filtered)):
            tags_html = "".join(f'<span class="note-tag">{t}</span>' for t in note.get("tags", []))
            st.markdown(f"""
<div class="note-card">
    <div style="margin-bottom:0.3rem;">{tags_html}<small style="color:#999;">{note.get('date','')}</small></div>
    <div style="font-weight:bold; color:#2c1810; margin-bottom:0.4rem;">{note.get('title','')}</div>
    <div style="color:#5a3a1a; font-size:0.9rem; white-space:pre-wrap;">{note.get('content','')}</div>
</div>
""", unsafe_allow_html=True)
            _, col_del = st.columns([5, 1])
            with col_del:
                if st.button("🗑️", key=f"del_note_{i}"):
                    note_id = note.get("id")
                    notes = [n for n in notes if n.get("id") != note_id]
                    save_json(NOTES_FILE, notes)
                    st.rerun()

# ══════════════════════════════════════════════
# TAB 3: 履歴
# ══════════════════════════════════════════════
with tab_history:
    st.markdown("### 📈 解答履歴")
    history = load_json(HISTORY_FILE, [])
    if not history:
        st.info("まだ解答履歴がありません。クイズに挑戦しましょう！")
    else:
        if st.button("🗑️ 履歴をクリア", type="secondary"):
            save_json(HISTORY_FILE, [])
            st.rerun()

        total   = len(history)
        correct = sum(1 for h in history if h.get("correct"))
        st.markdown(f"""
<div style="display:flex; gap:1rem; margin-bottom:1rem; flex-wrap:wrap;">
    <span class="score-badge" style="font-size:1rem;">総数 {total}</span>
    <span class="score-badge" style="font-size:1rem; background:linear-gradient(135deg,#2d7a2d,#4caf50); color:#fff;">正解 {correct}</span>
    <span class="score-badge" style="font-size:1rem; background:linear-gradient(135deg,#7a2d2d,#f44336); color:#fff;">不正解 {total-correct}</span>
</div>
""", unsafe_allow_html=True)

        mode_labels = {v: k for k, v in MODES.items()}
        for h in reversed(history[-50:]):
            icon       = "✅" if h.get("correct") else "❌"
            mode_label = mode_labels.get(h.get("mode",""), h.get("mode",""))
            border_col = "#4CAF50" if h.get("correct") else "#f44336"
            st.markdown(f"""
<div style="border-left:3px solid {border_col}; padding:0.4rem 0.8rem; margin-bottom:0.4rem;
            background:rgba(255,255,255,0.03); border-radius:0 6px 6px 0; font-size:0.85rem; color:#ccc;">
    {icon} <b style="color:#c8a96e;">{h.get('date','')}</b>　{mode_label}　— {h.get('question','')}
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4: 間違いリスト
# ══════════════════════════════════════════════
with tab_mistakes:
    st.markdown("### ❌ 間違いリスト（要復習）")
    mistakes = load_json(MISTAKES_FILE, [])
    if not mistakes:
        st.info("間違いリストは空です！全問正解しています 🎉")
    else:
        col_count, col_clear = st.columns([4, 1])
        with col_count:
            st.markdown(f"**{len(mistakes)} 問** が要復習です")
        with col_clear:
            if st.button("🗑️ クリア"):
                save_json(MISTAKES_FILE, [])
                st.rerun()

        mode_labels = {v: k for k, v in MODES.items()}
        for i, m in enumerate(reversed(mistakes)):
            mode_label = mode_labels.get(m.get("mode",""), m.get("mode",""))
            with st.expander(f"❌ {m.get('date','')} [{mode_label}] {m.get('question','')[:50]}…"):
                st.markdown(f"**問題：** {m.get('question','')}")
                for c in m.get("choices", []):
                    is_correct = c.startswith(m.get("answer",""))
                    was_user   = c.startswith(m.get("user_answer",""))
                    prefix = "✅ " if is_correct else ("❌ " if was_user else "　 ")
                    color  = "#4CAF50" if is_correct else ("#f44336" if was_user else "#aaa")
                    st.markdown(f'<span style="color:{color};">{prefix}{c}</span>', unsafe_allow_html=True)
                st.markdown(f"**解説：** {m.get('explanation','')}")
                if st.button("📒 ノートに追加", key=f"note_mis_{i}"):
                    notes = load_json(NOTES_FILE, [])
                    notes.append({
                        "id":      datetime.now().isoformat(),
                        "date":    datetime.now().strftime("%Y/%m/%d %H:%M"),
                        "title":   m.get("question","")[:40] + "…",
                        "content": f"【問題】{m.get('question','')}\n【正解】{m.get('answer','')}\n【解説】{m.get('explanation','')}",
                        "tags":    [m.get("mode","")],
                    })
                    save_json(NOTES_FILE, notes)
                    st.success("ノートに追加しました！")