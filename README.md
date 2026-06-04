Claudeが応答を完了しました
すとりーむりっとで歴史の問題を解く問題を作りたい。難易度は４つつくって、日本史で人物をこたえるやつと年号を答えるもの、人物がしたことがでるモードをだして。間違えたところをノートでまとめられるように詳しい解説をかいて。問題出大にAIを使わないようにして。パイソンのコードよろしく

16:56

Reading frontend design skill
Reading frontend design skill
StreamlitはPythonなので、フロントエンドスキルは参考程度にして、Streamlitアプリを作ります。


4個のコマンドを実行しました, ファイルを作成しました, ファイルを読み取りました
4個のコマンドを実行しました, ファイルを作成しました, ファイルを読み取りました
完成しました！起動方法と内容を説明します。

起動方法
bash
pip install streamlit
streamlit run nihonshi_quiz.py
機能一覧
📚 3つのモード
モード	内容
👤 人物	時代・出来事から人物名を答える
📅 年号	出来事の西暦年を答える
⚔️ できごと	業績・政策から関連人物を答える
⭐ 難易度4段階（各モード5問ずつ収録）
⭐ 易しい：教科書の基本レベル（家康・信長・黒船など）
⭐⭐ 普通：高校入試・センター試験レベル
⭐⭐⭐ 難しい：大学入試・歴史検定2〜3級レベル
⭐⭐⭐⭐ 超難問：林子平・工藤平助・持統天皇など玄人向け
📓 間違いノート機能
間違えた問題が自動保存
モード・難易度でフィルタリング可能
各問題に詳細解説（背景・文脈・関連事項を記載）
テキストエクスポートでノート印刷にも対応
個別削除・一括削除も可能
その他
累計回答数・正解率の統計表示
回答後は選択肢を色分け表示（正解緑・誤答赤）
和風デザイン（Noto Serif JPフォント・茶系カラー）

Nihonshi quiz
PY 
容量が大きくて、起動できないから、難易度は３つにして再度パイソンのコードでお願い

17:18

Check file size
Check file size
問題データを各難易度3問に絞り、難易度を3段階（易・普通・難）に減らしてコンパクトにします。


Create compact v2 quiz app
Create compact v2 quiz app

Create compact v2 quiz app
bash

cat > /home/claude/nihonshi_quiz_v2.py << 'PYEOF'
import streamlit as st
import random
from datetime import datetime

# ── 問題データ（難易度3段階・AIなし）──────────────────────
QUESTIONS = {
    "人物": [
        # 易しい
        {"diff": 1, "q": "江戸幕府を開いた人物は誰ですか？",
         "a": "徳川家康", "c": ["徳川家康","豊臣秀吉","織田信長","源頼朝"],
         "exp": "徳川家康（1543〜1616）は1603年に征夷大将軍となり江戸幕府を開いた。関ヶ原の戦い（1600年）で石田三成ら西軍を破り覇権を握った後、260年以上続く幕府の基礎を築いた。参勤交代・鎖国などの制度も整備された。",
         "era": "江戸時代初期"},
        {"diff": 1, "q": "鎌倉幕府を開いた人物は誰ですか？",
         "a": "源頼朝", "c": ["源頼朝","源義経","北条時政","平清盛"],
         "exp": "源頼朝（1147〜1199）は1185年に守護・地頭の設置権を得て、1192年に征夷大将軍となり鎌倉幕府を開いた。御家人制度と封建的主従関係を確立し、武家政治の礎を作った。",
         "era": "鎌倉時代"},
        {"diff": 1, "q": "奈良時代に東大寺の大仏造立を命じた天皇は誰ですか？",
         "a": "聖武天皇", "c": ["聖武天皇","天武天皇","元明天皇","桓武天皇"],
         "exp": "聖武天皇（701〜756）は天然痘の流行や社会不安を仏教の力で鎮めようと743年に大仏造立の詔を発した。752年に東大寺の大仏（盧舎那仏）が完成。遺品は正倉院に納められシルクロード文化を今に伝える。",
         "era": "奈良時代"},
        # 普通
        {"diff": 2, "q": "江戸幕府8代将軍として享保の改革を行ったのは誰ですか？",
         "a": "徳川吉宗", "c": ["徳川吉宗","松平定信","水野忠邦","田沼意次"],
         "exp": "徳川吉宗（1684〜1751）は紀州藩主から8代将軍となり1716年から享保の改革を行った。目安箱の設置・小石川養生所の開設・公事方御定書の制定など幕政を立て直した。「米将軍」とも呼ばれる。",
         "era": "江戸時代中期"},
        {"diff": 2, "q": "平安時代に摂関政治の全盛期を築いた人物は誰ですか？",
         "a": "藤原道長", "c": ["藤原道長","藤原頼通","藤原冬嗣","藤原基経"],
         "exp": "藤原道長（966〜1027）は4人の娘を天皇の后とし、外祖父として摂政・太政大臣を歴任した。「この世をば わが世とぞ思ふ 望月の…」の和歌が有名。日記『御堂関白記』はユネスコ記憶遺産に登録されている。",
         "era": "平安時代"},
        {"diff": 2, "q": "西南戦争を起こし「最後の武士」とも呼ばれた人物は誰ですか？",
         "a": "西郷隆盛", "c": ["西郷隆盛","大久保利通","木戸孝允","板垣退助"],
         "exp": "西郷隆盛（1828〜1877）は薩摩藩出身の維新志士。征韓論で下野後、1877年に士族の不満を背景に西南戦争を起こしたが熊本城攻略に失敗、鹿児島城山で自刃した。西郷の死が士族時代の終焉を象徴した。",
         "era": "明治時代初期"},
        # 難しい
        {"diff": 3, "q": "室町幕府3代将軍として南北朝合一を実現し、北山文化を花開かせた人物は誰ですか？",
         "a": "足利義満", "c": ["足利義満","足利尊氏","足利義政","足利義昭"],
         "exp": "足利義満（1358〜1408）は1392年に南北朝合一を成し遂げ幕府権力を確立。北山に金閣を建て北山文化を隆盛させた。日明貿易（勘合貿易）を開始し明の皇帝から「日本国王」に冊封された。能を保護し世阿弥も援助した。",
         "era": "室町時代"},
        {"diff": 3, "q": "1600年の関ヶ原の戦いで西軍の実質的指導者となった豊臣政権の奉行は誰ですか？",
         "a": "石田三成", "c": ["石田三成","小西行長","宇喜多秀家","毛利輝元"],
         "exp": "石田三成（1560〜1600）は豊臣秀吉の側近で五奉行の一人。秀吉没後、徳川家康打倒のため毛利輝元を総大将に西軍を組織したが関ヶ原で敗北、六条河原で処刑された。小早川秀秋の裏切りが決定打となった。",
         "era": "安土桃山〜江戸初期"},
        {"diff": 3, "q": "明治政府の岩倉使節団に参加せず、国内で民撰議院設立建白書を提出した人物は誰ですか？",
         "a": "板垣退助", "c": ["板垣退助","大隈重信","後藤象二郎","江藤新平"],
         "exp": "板垣退助（1837〜1919）は土佐藩出身の維新志士。征韓論で下野後の1874年、後藤象二郎らと民撰議院設立建白書を提出し自由民権運動の口火を切った。1881年に自由党を結成。「板垣死すとも自由は死せず」で知られる。",
         "era": "明治時代"},
    ],
    "年号": [
        # 易しい
        {"diff": 1, "q": "江戸幕府が開かれたのは何年ですか？",
         "a": "1603年", "c": ["1603年","1600年","1615年","1590年"],
         "exp": "1603年、徳川家康が征夷大将軍に任命されて江戸幕府を開いた。1600年の関ヶ原の戦い勝利後、政権を確立した。1605年には息子・秀忠に将軍職を譲り、徳川家の世襲を示した。",
         "era": "江戸時代"},
        {"diff": 1, "q": "明治維新が起きた年（明治元年）はいつですか？",
         "a": "1868年", "c": ["1868年","1853年","1871年","1858年"],
         "exp": "1868年（明治元年）、鳥羽・伏見の戦いで旧幕府軍を破った新政府が王政復古の大号令を発し、明治天皇を中心とした新政府が発足した。同年に五箇条の御誓文も発布された。",
         "era": "明治時代"},
        {"diff": 1, "q": "日本が第二次世界大戦で降伏したのは何年ですか？",
         "a": "1945年", "c": ["1945年","1943年","1941年","1947年"],
         "exp": "1945年8月15日、昭和天皇の玉音放送で終戦が告げられポツダム宣言を受諾。9月2日に戦艦ミズーリ号上で降伏文書に調印し第二次世界大戦が正式に終結した。",
         "era": "昭和時代"},
        # 普通
        {"diff": 2, "q": "鎌倉幕府が滅亡したのは何年ですか？",
         "a": "1333年", "c": ["1333年","1336年","1185年","1221年"],
         "exp": "1333年、後醍醐天皇の倒幕運動に呼応した足利尊氏が六波羅探題を攻略、新田義貞が鎌倉を攻め、北条高時ら北条一族は東勝寺で自刃して鎌倉幕府は滅亡した。",
         "era": "鎌倉末期"},
        {"diff": 2, "q": "大日本帝国憲法が発布されたのは何年ですか？",
         "a": "1889年", "c": ["1889年","1885年","1890年","1881年"],
         "exp": "1889年2月11日（紀元節）、大日本帝国憲法が発布された。伊藤博文がプロイセン憲法を参考に起草し、主権は天皇にある欽定憲法だった。翌1890年に第1回帝国議会が開会した。",
         "era": "明治時代"},
        {"diff": 2, "q": "応仁の乱が始まったのは何年ですか？",
         "a": "1467年", "c": ["1467年","1477年","1392年","1441年"],
         "exp": "1467年（応仁元年）、足利将軍家の継嗣問題・管領家の相続問題を契機に細川勝元（東軍）と山名宗全（西軍）が対立し応仁の乱が勃発。京都は11年にわたり焦土と化し、戦国時代の幕開けとなった。",
         "era": "室町時代"},
        # 難しい
        {"diff": 3, "q": "承久の乱が起きた年はいつですか？",
         "a": "1221年", "c": ["1221年","1185年","1232年","1274年"],
         "exp": "1221年（承久3年）、後鳥羽上皇が幕府打倒を呼びかけ挙兵したが北条義時率いる幕府軍に大敗した（承久の乱）。上皇は隠岐に流され朝廷の勢力は大きく後退、幕府は六波羅探題を設置して朝廷を監視した。",
         "era": "鎌倉時代"},
        {"diff": 3, "q": "日本が国際連盟を脱退したのは何年ですか？",
         "a": "1933年", "c": ["1933年","1931年","1937年","1941年"],
         "exp": "1933年3月、満洲事変（1931年）後にリットン調査団が満洲国建国の不当性を報告し、国際連盟総会で日本軍の撤退勧告が採択されたことを受け日本は脱退した。以後、国際的孤立が深まっていった。",
         "era": "昭和時代（戦前）"},
        {"diff": 3, "q": "五・一五事件が起きたのは何年ですか？",
         "a": "1932年", "c": ["1932年","1931年","1936年","1929年"],
         "exp": "1932年5月15日、海軍青年将校らが犬養毅首相を暗殺した（五・一五事件）。「話せばわかる」と語りかける犬養に「問答無用」と発砲したとされる。この事件で政党内閣の時代が終わり軍部の政治介入が強まった。",
         "era": "昭和時代（戦前）"},
    ],
    "できごと": [
        # 易しい
        {"diff": 1, "q": "黒船で来航し日本に開国を迫ったアメリカの提督は誰ですか？",
         "a": "ペリー", "c": ["ペリー","ハリス","リンカーン","マッカーサー"],
         "exp": "マシュー・ペリー（1794〜1858）は1853年に4隻の黒船を率いて浦賀に来航し大統領の国書を提出した。翌1854年に再来航して日米和親条約を締結。「泰平の眠りを覚ます上喜撰 たった四杯で夜も眠れず」と狂歌に詠まれた。",
         "era": "江戸末期"},
        {"diff": 1, "q": "江戸幕府最後の将軍として大政奉還を行ったのは誰ですか？",
         "a": "徳川慶喜", "c": ["徳川慶喜","徳川家茂","徳川斉昭","徳川慶福"],
         "exp": "徳川慶喜（1837〜1913）は15代将軍。1867年10月に政権を朝廷に返上する大政奉還を行い薩長の倒幕口実を封じようとしたが、王政復古の大号令で旧幕府勢力が排除。鳥羽・伏見の戦いに敗れ江戸城を無血開城した。",
         "era": "江戸末期"},
        {"diff": 1, "q": "飛鳥時代に遣隋使として隋に派遣された人物は誰ですか？",
         "a": "小野妹子", "c": ["小野妹子","阿倍仲麻呂","藤原鎌足","犬上御田鍬"],
         "exp": "小野妹子は607年に聖徳太子の命で遣隋使として隋の煬帝のもとへ派遣された。「日出ずる処の天子…」で始まる対等な国書に煬帝は不快を示したとされる。帰国の際に裴世清を伴い帰朝した。",
         "era": "飛鳥時代"},
        # 普通
        {"diff": 2, "q": "「学問のすゝめ」を著し慶應義塾を創設した人物は誰ですか？",
         "a": "福澤諭吉", "c": ["福澤諭吉","森有礼","新島襄","大隈重信"],
         "exp": "福澤諭吉（1835〜1901）は豊前中津藩出身。「天は人の上に人を造らず」で始まる『学問のすゝめ』（1872〜76）で平等思想と実学の重要性を説いた。慶應義塾（現・慶應義塾大学）を創設し明治の啓蒙思想家として活躍した。",
         "era": "明治時代"},
        {"diff": 2, "q": "豊臣秀吉が農民から武器を取り上げた政策を何といいますか？（この政策を行ったのは誰ですか）",
         "a": "豊臣秀吉", "c": ["豊臣秀吉","織田信長","徳川家康","足利義満"],
         "exp": "豊臣秀吉は1588年に刀狩令を発令し農民の武装解除を行った。表向きは「大仏造立のための材料収集」だったが、真の目的は一揆の防止・兵農分離の徹底にあった。1591年の身分統制令とあわせて近世封建社会の基礎が作られた。",
         "era": "安土桃山時代"},
        {"diff": 2, "q": "元禄文化を代表する俳人で「奥の細道」を著したのは誰ですか？",
         "a": "松尾芭蕉", "c": ["松尾芭蕉","与謝蕪村","小林一茶","井原西鶴"],
         "exp": "松尾芭蕉（1644〜1694）は伊賀国出身の俳人で俳諧を芸術の域に高めた。1689年に弟子・河合曾良と江戸を出発してみちのく・北陸を旅した紀行文『奥の細道』が代表作。「古池や 蛙飛び込む 水の音」など名句を多数残した。",
         "era": "江戸時代（元禄）"},
        # 難しい
        {"diff": 3, "q": "国学を大成し「古事記伝」を著したのは誰ですか？",
         "a": "本居宣長", "c": ["本居宣長","賀茂真淵","荷田春満","平田篤胤"],
         "exp": "本居宣長（1730〜1801）は伊勢松阪の医師で賀茂真淵に師事した国学者。約35年をかけた『古事記伝』（全44巻）は国学の最高峰とされる。「もののあわれ」を日本文学の本質と説き、儒教・仏教以前の「やまとごころ」を強調した。",
         "era": "江戸時代後期"},
        {"diff": 3, "q": "室町幕府が明との間で始めた勘合貿易を本格化させた将軍は誰ですか？",
         "a": "足利義満", "c": ["足利義満","足利義持","足利義政","足利義教"],
         "exp": "足利義満は1404年に明との勘合貿易（日明貿易）を開始した。勘合符（合い札）で正式船と倭寇を区別し、明から銅銭・生糸・陶磁器を輸入、日本からは銅・刀剣・硫黄を輸出した。義満が「日本国王」として冊封を受けた点は後世からも議論を呼んだ。",
         "era": "室町時代"},
        {"diff": 3, "q": "江戸時代初期にキリシタン弾圧の中で起きた島原の乱で一揆軍の総大将となった少年は誰ですか？",
         "a": "天草四郎（益田時貞）", "c": ["天草四郎（益田時貞）","小西行長","有馬晴信","鍋島直茂"],
         "exp": "天草四郎（本名・益田時貞、1621頃〜1638）は島原藩・唐津藩の重税とキリシタン弾圧に苦しむ農民に推戴され16歳前後で一揆の総大将となった。原城に籠城した約3万7千人は幕府軍12万に攻め落とされほぼ全員が討ち死にした。",
         "era": "江戸時代初期"},
    ],
}

DIFF_LABEL = {1: "⭐ 易しい", 2: "⭐⭐ 普通", 3: "⭐⭐⭐ 難しい"}
DIFF_COLOR = {1: ("#d4edda","#155724"), 2: ("#fff3cd","#856404"), 3: ("#f8d7da","#721c24")}
MODE_EMOJI = {"人物": "👤", "年号": "📅", "できごと": "⚔️"}

# ── ページ設定 ──────────────────────────────────
st.set_page_config(page_title="日本史クイズ", page_icon="⛩️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&family=Noto+Sans+JP&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }
h1, h2 { font-family: 'Noto Serif JP', serif; }
.q-card {
    background: #fdf6e3; border: 2px solid #d4a96a; border-radius: 12px;
    padding: 1.4em; margin-bottom: 1em;
    box-shadow: 3px 3px 8px rgba(139,69,19,0.12);
}
.exp-box {
    background: #e8f4fd; border-left: 4px solid #2980b9;
    border-radius: 0 8px 8px 0; padding: 1em 1.2em;
    color: #1a4a6b; line-height: 1.8; font-size: 0.96rem; margin-top: 0.6em;
}
.note-card {
    background: #fffdf5; border: 1px solid #e8c97a; border-radius: 8px;
    padding: 1em; margin-bottom: 0.8em; border-left: 4px solid #e8962a;
}
.tag {
    display: inline-block; background: #f0e6d3; color: #6b3a1f;
    padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;
    border: 1px solid #d4a96a; margin-right: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── セッション初期化 ────────────────────────────
for k, v in {
    "page": "home", "mode": None, "diff": None,
    "questions": [], "idx": 0, "score": 0,
    "answered": False, "selected": None,
    "results": [], "wrong_notes": [],
    "total_ans": 0, "total_cor": 0,
    "sel_mode": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page): st.session_state.page = page

def start_quiz(mode, diff):
    pool = [q for q in QUESTIONS[mode] if q["diff"] == diff]
    random.shuffle(pool)
    st.session_state.update({
        "mode": mode, "diff": diff, "questions": pool,
        "idx": 0, "score": 0, "answered": False,
        "selected": None, "results": [], "page": "quiz",
    })

# ── ホーム ──────────────────────────────────────
def page_home():
    st.markdown('<h1 style="text-align:center;color:#2c1810;">⛩️ 日本史クイズ</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#8b4513;">人物・年号・できごと ／ 難易度3段階</p>', unsafe_allow_html=True)

    if st.session_state.total_ans > 0:
        rate = int(st.session_state.total_cor / st.session_state.total_ans * 100)
        c1, c2, c3 = st.columns(3)
        c1.metric("累計回答", st.session_state.total_ans)
        c2.metric("累計正解", st.session_state.total_cor)
        c3.metric("正解率", f"{rate}%")

    st.divider()
    st.subheader("📚 モードを選んでください")
    descs = {"人物": "人物名を答える", "年号": "西暦年を答える", "できごと": "業績から人物を答える"}
    cols = st.columns(3)
    for i, (m, d) in enumerate(descs.items()):
        with cols[i]:
            if st.button(f"{MODE_EMOJI[m]} {m}", key=f"m_{m}", use_container_width=True):
                st.session_state.sel_mode = m
                st.rerun()
            st.caption(d)

    if st.session_state.sel_mode:
        st.divider()
        m = st.session_state.sel_mode
        st.subheader(f"{MODE_EMOJI[m]} {m} ─ 難易度を選んでください")
        c1, c2, c3 = st.columns(3)
        for col, (d, label) in zip([c1, c2, c3], DIFF_LABEL.items()):
            n = len([q for q in QUESTIONS[m] if q["diff"] == d])
            with col:
                if st.button(f"{label}\n（{n}問）", key=f"d_{d}", use_container_width=True):
                    start_quiz(m, d)
                    st.rerun()

    st.divider()
    nc = len(st.session_state.wrong_notes)
    if nc > 0:
        st.info(f"📓 間違いが {nc} 件あります")
        if st.button("📓 間違いノートを見る", use_container_width=True):
            go("notes"); st.rerun()
    else:
        st.caption("📓 間違えた問題は「間違いノート」に自動保存されます")

# ── クイズ ──────────────────────────────────────
def page_quiz():
    qs = st.session_state.questions
    idx = st.session_state.idx
    if not qs or idx >= len(qs):
        go("result"); st.rerun(); return

    q = qs[idx]
    total = len(qs)

    # ヘッダー
    ch, _, cs = st.columns([1, 2, 1])
    with ch:
        if st.button("🏠 ホーム"):
            go("home"); st.session_state.sel_mode = None; st.rerun()
    with cs:
        bg, fg = DIFF_COLOR[q["diff"]]
        st.markdown(f'<span style="background:{bg};color:{fg};padding:3px 10px;border-radius:12px;font-size:0.85rem;font-weight:bold;">{DIFF_LABEL[q["diff"]]}</span>', unsafe_allow_html=True)

    prog = idx / total
    st.progress(prog)
    st.caption(f"問題 {idx+1} / {total}　｜　正解: {st.session_state.score}")

    # 問題
    st.markdown(f"""
    <div class="q-card">
        <span class="tag">{q['era']}</span><br><br>
        <span style="font-family:'Noto Serif JP',serif;font-size:1.2rem;color:#2c1810;">
            {MODE_EMOJI[st.session_state.mode]} <b>問題 {idx+1}</b><br><br>{q['q']}
        </span>
    </div>""", unsafe_allow_html=True)

    answered = st.session_state.answered
    selected = st.session_state.selected

    if not answered:
        for ch in q["c"]:
            if st.button(ch, key=f"ch_{ch}", use_container_width=True):
                st.session_state.selected = ch
                st.session_state.answered = True
                st.session_state.total_ans += 1
                correct = ch == q["a"]
                if correct:
                    st.session_state.score += 1
                    st.session_state.total_cor += 1
                    st.session_state.results.append({"q": q, "ok": True, "sel": ch})
                else:
                    st.session_state.results.append({"q": q, "ok": False, "sel": ch})
                    existing = [n["q"] for n in st.session_state.wrong_notes]
                    if q["q"] not in existing:
                        st.session_state.wrong_notes.append({
                            **q, "wrong": ch,
                            "ts": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                st.rerun()
    else:
        ok = selected == q["a"]
        if ok:
            st.success(f"✅ 正解！　**{q['a']}**")
        else:
            st.error(f"❌ 不正解　あなた: {selected}　　正解: **{q['a']}**")

        for ch in q["c"]:
            if ch == q["a"]: st.success(f"✅ {ch}（正解）")
            elif ch == selected and not ok: st.error(f"❌ {ch}（あなたの回答）")
            else: st.write(f"　　{ch}")

        st.markdown(f'<div class="exp-box"><b>📖 解説</b><br><br>{q["exp"]}</div>', unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            label = "次の問題 ▶" if idx + 1 < total else "結果を見る 🏆"
            if st.button(label, use_container_width=True, type="primary"):
                st.session_state.idx += 1
                st.session_state.answered = False
                st.session_state.selected = None
                if idx + 1 >= total: go("result")
                st.rerun()
        with b2:
            if st.button("📓 ノートを見る", use_container_width=True):
                go("notes"); st.rerun()

# ── 結果 ────────────────────────────────────────
def page_result():
    st.markdown('<h2 style="text-align:center;font-family:Noto Serif JP,serif;color:#2c1810;">🏆 クイズ終了！</h2>', unsafe_allow_html=True)
    results = st.session_state.results
    score = st.session_state.score
    total = len(results) or len(st.session_state.questions)
    rate = int(score / total * 100) if total else 0

    emoji = "🥇" if rate >= 80 else "🥈" if rate >= 60 else "🥉" if rate >= 40 else "📚"
    msg = "素晴らしい！" if rate >= 80 else "よくできました！" if rate >= 60 else "もう少し頑張ろう！" if rate >= 40 else "復習が必要です！"
    color = "#28a745" if rate >= 80 else "#17a2b8" if rate >= 60 else "#ffc107" if rate >= 40 else "#dc3545"

    st.markdown(f"""
    <div style="text-align:center;padding:2em;background:#fdf6e3;border:2px solid #d4a96a;border-radius:16px;margin-bottom:1.5em;">
        <div style="font-size:3.5rem;">{emoji}</div>
        <div style="font-size:2rem;font-weight:bold;color:{color};">{score} / {total}</div>
        <div style="font-size:1.4rem;color:{color};">{rate}% 正解　{msg}</div>
        <div style="font-size:0.9rem;color:#888;margin-top:0.4em;">
            {MODE_EMOJI[st.session_state.mode]} {st.session_state.mode}　{DIFF_LABEL[st.session_state.diff]}
        </div>
    </div>""", unsafe_allow_html=True)

    if results:
        st.subheader("📋 問題別結果")
        for i, r in enumerate(results):
            icon = "✅" if r["ok"] else "❌"
            with st.expander(f"{icon} Q{i+1}: {r['q']['q'][:45]}..."):
                bg = "#d4edda" if r["ok"] else "#f8d7da"
                st.markdown(f'<div style="background:{bg};padding:0.8em;border-radius:8px;"><b>あなた:</b> {r["sel"]}<br><b>正解:</b> {r["q"]["a"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="exp-box">{r["q"]["exp"]}</div>', unsafe_allow_html=True)

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 もう一度", use_container_width=True, type="primary"):
            start_quiz(st.session_state.mode, st.session_state.diff); st.rerun()
    with c2:
        if st.button("📓 間違いノート", use_container_width=True):
            go("notes"); st.rerun()
    with c3:
        if st.button("🏠 ホームへ", use_container_width=True):
            go("home"); st.session_state.sel_mode = None; st.rerun()