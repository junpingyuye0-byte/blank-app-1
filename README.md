import streamlit as st
import random

# ページ設定
st.set_page_config(page_title="じゃんけんゲーム", page_icon="✊", layout="centered")

# 定数
HANDS = {"グー": "✊", "チョキ": "✌️", "パー": "✋"}
WIN_MAP = {"グー": "チョキ", "チョキ": "パー", "パー": "グー"}  # key が key.value に勝つ

# スタイル
st.markdown("""
<style>
    .result-win  { font-size: 2rem; color: #2ecc71; font-weight: bold; text-align: center; }
    .result-lose { font-size: 2rem; color: #e74c3c; font-weight: bold; text-align: center; }
    .result-draw { font-size: 2rem; color: #f39c12; font-weight: bold; text-align: center; }
    .hand-display { font-size: 4rem; text-align: center; }
    .score-box { background: #f0f2f6; border-radius: 10px; padding: 10px 20px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "history" not in st.session_state:
    st.session_state.history = []

# タイトル
st.title("✊✌️✋ じゃんけんゲーム")
st.divider()

# スコアボード
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="score-box">', unsafe_allow_html=True)
    st.metric("🏆 勝ち", st.session_state.wins)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="score-box">', unsafe_allow_html=True)
    st.metric("🤝 引き分け", st.session_state.draws)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="score-box">', unsafe_allow_html=True)
    st.metric("💔 負け", st.session_state.losses)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 手を選ぶボタン
st.subheader("手を選んでください")
btn_cols = st.columns(3)
player_choice = None

for i, (hand, emoji) in enumerate(HANDS.items()):
    if btn_cols[i].button(f"{emoji} {hand}", use_container_width=True, key=hand):
        player_choice = hand

# 結果表示
if player_choice:
    cpu_choice = random.choice(list(HANDS.keys()))

    # 勝敗判定
    if WIN_MAP[player_choice] == cpu_choice:
        result = "win"
        result_text = "🎉 あなたの勝ち！"
        result_class = "result-win"
        st.session_state.wins += 1
    elif WIN_MAP[cpu_choice] == player_choice:
        result = "lose"
        result_text = "😢 あなたの負け…"
        result_class = "result-lose"
        st.session_state.losses += 1
    else:
        result = "draw"
        result_text = "🤝 引き分け！"
        result_class = "result-draw"
        st.session_state.draws += 1

    # 手を表示
    st.divider()
    display_cols = st.columns(2)
    with display_cols[0]:
        st.markdown(f"**あなた**")
        st.markdown(f'<div class="hand-display">{HANDS[player_choice]}</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center'>{player_choice}</div>", unsafe_allow_html=True)
    with display_cols[1]:
        st.markdown(f"**CPU**")
        st.markdown(f'<div class="hand-display">{HANDS[cpu_choice]}</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center'>{cpu_choice}</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="{result_class}">{result_text}</div>', unsafe_allow_html=True)

    # 履歴に追加
    st.session_state.history.append({
        "あなた": f"{HANDS[player_choice]} {player_choice}",
        "CPU": f"{HANDS[cpu_choice]} {cpu_choice}",
        "結果": result_text,
    })

# 対戦履歴
if st.session_state.history:
    st.divider()
    with st.expander("📜 対戦履歴を見る"):
        for i, record in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.write(f"**{i}.** あなた: {record['あなた']} ／ CPU: {record['CPU']} → {record['結果']}")

    if st.button("🔄 スコアをリセット"):
        st.session_state.wins = 0
        st.session_state.losses = 0
        st.session_state.draws = 0
        st.session_state.history = []
        st.rerun()