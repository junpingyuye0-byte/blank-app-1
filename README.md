import streamlit as st
import random
import json
from datetime import datetime

# ─────────────────────────────────────────────
# 問題データベース（AIなし・ハードコード）
# ─────────────────────────────────────────────

QUESTIONS = {
    "人物": [
        # 難易度1（易しい）
        {
            "difficulty": 1,
            "question": "江戸幕府を開いた人物は誰ですか？",
            "answer": "徳川家康",
            "choices": ["徳川家康", "豊臣秀吉", "織田信長", "源頼朝"],
            "explanation": "徳川家康（1543〜1616）は1603年に征夷大将軍となり江戸幕府を開いた。桶狭間の戦いで今川義元が倒れた後、独立して勢力を伸ばし、1600年の関ヶ原の戦いで石田三成ら西軍を破って覇権を握った。江戸幕府はその後260年以上続き、鎖国政策・参勤交代などの制度を整備した。",
            "era": "江戸時代初期",
            "tags": ["幕府", "戦国〜江戸"]
        },
        {
            "difficulty": 1,
            "question": "大化の改新を推進した中大兄皇子の協力者は誰ですか？",
            "answer": "中臣鎌足",
            "choices": ["中臣鎌足", "蘇我入鹿", "聖徳太子", "天武天皇"],
            "explanation": "中臣鎌足（614〜669）は中大兄皇子（後の天智天皇）とともに645年の大化の改新を起こし、蘇我氏の専横を打破した。死の直前に「藤原」の姓を賜り、藤原氏の始祖となった。大化の改新では公地公民制や国郡里制など中央集権体制の基礎が作られた。",
            "era": "飛鳥時代",
            "tags": ["改革", "飛鳥"]
        },
        {
            "difficulty": 1,
            "question": "鎌倉幕府を開いた人物は誰ですか？",
            "answer": "源頼朝",
            "choices": ["源頼朝", "源義経", "北条時政", "平清盛"],
            "explanation": "源頼朝（1147〜1199）は1185年に守護・地頭の設置を認められ、1192年に征夷大将軍となって鎌倉幕府を開いた。弟の義経を追討するなど権力を固め、武家政治の基礎を築いた。幕府では御家人制度・封建的主従関係が確立された。",
            "era": "鎌倉時代",
            "tags": ["幕府", "武家"]
        },
        {
            "difficulty": 1,
            "question": "天下統一を目前に本能寺の変で倒れた武将は誰ですか？",
            "answer": "織田信長",
            "choices": ["織田信長", "豊臣秀吉", "明智光秀", "徳川家康"],
            "explanation": "織田信長（1534〜1582）は尾張（愛知県）出身。桶狭間の戦いで今川義元を倒し、足利義昭を奉じて上洛後に室町幕府を滅ぼした。楽市楽座や鉄砲の活用など革新的な政策を行ったが、1582年に家臣の明智光秀に本能寺で討たれた（本能寺の変）。",
            "era": "戦国時代",
            "tags": ["戦国", "統一事業"]
        },
        {
            "difficulty": 1,
            "question": "奈良時代に東大寺の大仏造立を命じた天皇は誰ですか？",
            "answer": "聖武天皇",
            "choices": ["聖武天皇", "天武天皇", "元明天皇", "桓武天皇"],
            "explanation": "聖武天皇（701〜756）は天然痘の流行や政争が続く社会不安を仏教の力で鎮めようと、743年に大仏造立の詔を出した。752年に東大寺の大仏（盧舎那仏）が完成した。聖武天皇の遺品は東大寺正倉院に収められ、シルクロード文化を伝える貴重な宝物となっている。",
            "era": "奈良時代",
            "tags": ["仏教", "文化"]
        },
        # 難易度2（普通）
        {
            "difficulty": 2,
            "question": "江戸幕府8代将軍として享保の改革を行ったのは誰ですか？",
            "answer": "徳川吉宗",
            "choices": ["徳川吉宗", "松平定信", "水野忠邦", "田沼意次"],
            "explanation": "徳川吉宗（1684〜1751）は紀州藩主から8代将軍となり、1716年から享保の改革を断行した。目安箱の設置・小石川養生所の開設・公事方御定書の制定・上げ米の制など幕政の立て直しに成功した。「米将軍」とも呼ばれ、米価安定にも尽力した。",
            "era": "江戸時代中期",
            "tags": ["改革", "幕政"]
        },
        {
            "difficulty": 2,
            "question": "「学問のすゝめ」を著し、慶應義塾を創設した人物は誰ですか？",
            "answer": "福澤諭吉",
            "choices": ["福澤諭吉", "森有礼", "新島襄", "大隈重信"],
            "explanation": "福澤諭吉（1835〜1901）は豊前中津藩（大分県）出身。「天は人の上に人を造らず」の書き出しで有名な『学問のすゝめ』（1872〜76）で平等思想・実学の重要性を説いた。慶應義塾（現・慶應義塾大学）を創設し、明治の啓蒙思想家として活躍した。現在の壱万円札の肖像でもある。",
            "era": "明治時代",
            "tags": ["啓蒙", "教育", "文明開化"]
        },
        {
            "difficulty": 2,
            "question": "平安時代に摂関政治の全盛期を築いた人物は誰ですか？",
            "answer": "藤原道長",
            "choices": ["藤原道長", "藤原頼通", "藤原冬嗣", "藤原基経"],
            "explanation": "藤原道長（966〜1027）は4人の娘を天皇の后とし、外祖父として摂政・太政大臣を歴任、摂関政治の絶頂期を実現した。「この世をば わが世とぞ思ふ 望月の 欠けたることも なしと思へば」の和歌が有名。日記『御堂関白記』はユネスコ記憶遺産に登録されている。",
            "era": "平安時代",
            "tags": ["貴族", "摂関政治"]
        },
        {
            "difficulty": 2,
            "question": "西南戦争を起こし、「最後の武士」とも呼ばれた人物は誰ですか？",
            "answer": "西郷隆盛",
            "choices": ["西郷隆盛", "大久保利通", "木戸孝允", "板垣退助"],
            "explanation": "西郷隆盛（1828〜1877）は薩摩藩出身の維新志士。倒幕・明治維新に大きく貢献したが、征韓論で敗れて下野。1877年に士族の不満を背景に西南戦争を起こしたが、熊本城攻略に失敗し、鹿児島の城山で自刃した。西郷の死をもって士族の時代が終わったとされる。",
            "era": "明治時代初期",
            "tags": ["維新", "士族"]
        },
        {
            "difficulty": 2,
            "question": "元禄文化を代表する俳人で「奥の細道」を著したのは誰ですか？",
            "answer": "松尾芭蕉",
            "choices": ["松尾芭蕉", "与謝蕪村", "小林一茶", "井原西鶴"],
            "explanation": "松尾芭蕉（1644〜1694）は伊賀国（三重県）出身の俳人で、俳諧を芸術の域に高めた。1689年に弟子・河合曾良とともに江戸を出発し、みちのく・北陸を旅した紀行文『奥の細道』が代表作。「古池や 蛙飛び込む 水の音」など数多くの名句を残した。",
            "era": "江戸時代（元禄）",
            "tags": ["文化", "文学"]
        },
        # 難易度3（難しい）
        {
            "difficulty": 3,
            "question": "江戸幕府の老中として寛政の改革を行い、「白河の清き流れに魚も住みかねて もとの濁りの田沼恋しき」と風刺された人物は誰ですか？",
            "answer": "松平定信",
            "choices": ["松平定信", "水野忠邦", "田沼意次", "老中阿部正弘"],
            "explanation": "松平定信（1758〜1829）は白河藩主で老中首座となり1787〜93年に寛政の改革を断行。旗本・御家人の救済（棄捐令）、農村復興（帰農令）、出版統制（寛政異学の禁）などを推進。前任の田沼意次の賄賂政治への反動として厳格な政治を行ったが、庶民からは「清すぎて魚も住めない」と皮肉られた。",
            "era": "江戸時代後期",
            "tags": ["改革", "幕政"]
        },
        {
            "difficulty": 3,
            "question": "室町幕府3代将軍として南北朝合一を実現し、北山文化を花開かせた人物は誰ですか？",
            "answer": "足利義満",
            "choices": ["足利義満", "足利尊氏", "足利義政", "足利義昭"],
            "explanation": "足利義満（1358〜1408）は1392年に南北朝合一を成し遂げ、幕府権力を確立。京都北山に金閣（鹿苑寺金閣）を建て北山文化を隆盛させた。また日明貿易（勘合貿易）を開始し、明の皇帝から「日本国王」に冊封された。能を保護し世阿弥を援助したことでも知られる。",
            "era": "室町時代",
            "tags": ["幕府", "文化", "外交"]
        },
        {
            "difficulty": 3,
            "question": "1600年の関ヶ原の戦いで西軍の実質的な指導者となった豊臣政権の奉行は誰ですか？",
            "answer": "石田三成",
            "choices": ["石田三成", "小西行長", "宇喜多秀家", "毛利輝元"],
            "explanation": "石田三成（1560〜1600）は豊臣秀吉の側近で五奉行の一人。朝鮮出兵での軍功を武将たちに公平に分配しようとしたことで福島正則らと対立した。秀吉没後、徳川家康打倒のため毛利輝元を総大将に関ヶ原の戦いを起こしたが敗れ、六条河原で処刑された。",
            "era": "戦国〜江戸初期",
            "tags": ["戦国", "関ヶ原"]
        },
        {
            "difficulty": 3,
            "question": "明治政府の岩倉使節団に同行せず、国内に残って民撰議院設立建白書を提出した人物は誰ですか？",
            "answer": "板垣退助",
            "choices": ["板垣退助", "大隈重信", "後藤象二郎", "江藤新平"],
            "explanation": "板垣退助（1837〜1919）は土佐藩出身の維新志士。征韓論で敗れて下野後の1874年、後藤象二郎らとともに民撰議院設立建白書を左院に提出し、自由民権運動の口火を切った。1881年に自由党を結成。「板垣死すとも自由は死せず」の言葉（岐阜事件）でも有名。",
            "era": "明治時代",
            "tags": ["自由民権", "政党"]
        },
        {
            "difficulty": 3,
            "question": "日本最初の武家政権の実権を握り、太政大臣にまで昇りつめた平氏の棟梁は誰ですか？",
            "answer": "平清盛",
            "choices": ["平清盛", "平将門", "平時忠", "源義朝"],
            "explanation": "平清盛（1118〜1181）は保元の乱・平治の乱を経て武家として初めて太政大臣に就任（1167年）。娘・徳子を高倉天皇の后とし、外孫の安徳天皇を擁立して権力の絶頂を極めた。日宋貿易を積極的に推進し、福原（神戸）を貿易拠点として整備した。しかし驕慢な権力行使が源氏の台頭を招いた。",
            "era": "平安末期",
            "tags": ["武家", "貿易"]
        },
        # 難易度4（超難問）
        {
            "difficulty": 4,
            "question": "江戸時代後期に『海国兵談』を著し、海防の必要性を説いて幕府に弾圧された地理学者は誰ですか？",
            "answer": "林子平",
            "choices": ["林子平", "高野長英", "渡辺崋山", "本多利明"],
            "explanation": "林子平（1738〜1793）は仙台藩士で、ロシアの南下を警戒し1791年に『海国兵談』を著して日本の海防強化を訴えた。当時の老中・松平定信は「天下の形勢を乱すもの」として出版を禁じ、版木を没収・蟄居処分とした。子平は「親もなく 妻も子もなし 版木もなし 金もなければ 死にたくもなし」という狂歌を詠んだことでも知られる。",
            "era": "江戸時代後期",
            "tags": ["思想", "海防", "蘭学"]
        },
        {
            "difficulty": 4,
            "question": "応仁の乱の東軍を率いた管領家の人物は誰ですか？",
            "answer": "細川勝元",
            "choices": ["細川勝元", "山名宗全", "畠山政長", "斯波義廉"],
            "explanation": "細川勝元（1430〜1473）は管領家の細川氏の当主で、応仁の乱（1467〜77）では東軍の総大将として山名宗全率いる西軍と対立した。将軍家の後継問題（足利義視vs義尚）・管領家・守護大名の利害対立が絡み合い、京都を11年にわたり焦土と化した。細川・山名ともに乱中に病死し、以後戦国時代へ突入した。",
            "era": "室町時代",
            "tags": ["応仁の乱", "守護大名"]
        },
        {
            "difficulty": 4,
            "question": "律令制度下で地方行政を担った国司の監察のために設置された令外官は何ですか？その初代に任じられた人物は誰ですか？（人物名で答えよ）",
            "answer": "菅原道真",
            "choices": ["菅原道真", "紀長谷雄", "藤原時平", "源能有"],
            "explanation": "菅原道真（845〜903）は文章博士・右大臣まで昇進した学者政治家。宇多天皇・醍醐天皇に重用されたが、左大臣・藤原時平の讒言により901年に大宰府に左遷され、その地で没した。死後、京都に疫病・洪水が相次いだため怨霊として恐れられ、北野天満宮に「天神」として祀られた。「東風吹かば にほひをこせよ 梅の花 主なしとて 春を忘るな」の歌が有名。",
            "era": "平安時代",
            "tags": ["律令", "学問", "怨霊信仰"]
        },
        {
            "difficulty": 4,
            "question": "江戸時代に「赤蝦夷風説考」を著し、蝦夷地開発・ロシアとの交易を幕府に建言した仙台藩の医師は誰ですか？",
            "answer": "工藤平助",
            "choices": ["工藤平助", "最上徳内", "近藤重蔵", "間宮林蔵"],
            "explanation": "工藤平助（1734〜1800）は仙台藩の医師・経世家。1783年に『赤蝦夷風説考』を著し、ロシアの北方進出の実情を紹介しながら蝦夷地（北海道）の開発・対ロシア交易の必要性を幕府に訴えた。田沼意次はこれを評価し、最上徳内らの蝦夷地調査を命じた。工藤の先見性は後の松前藩政改革や北方探検につながった。",
            "era": "江戸時代後期",
            "tags": ["蝦夷地", "北方探検", "経世思想"]
        },
        {
            "difficulty": 4,
            "question": "壬申の乱で大友皇子を破り天武天皇となった人物の皇后で、後に即位して持統天皇となった人物は誰ですか？",
            "answer": "鸕野讃良皇女（持統天皇）",
            "choices": ["鸕野讃良皇女（持統天皇）", "額田王", "元明天皇", "推古天皇"],
            "explanation": "持統天皇（645〜703）は天智天皇の娘で、天武天皇の皇后。天武天皇崩御後に称制、689年に飛鳥浄御原令を施行、694年に藤原京に遷都した。701年の大宝律令制定（文武天皇代）の基盤を整え、律令国家完成に大きく貢献した。『万葉集』に「春すぎて 夏来にけらし 白妙の 衣ほすてふ 天の香具山」の歌を残す。",
            "era": "飛鳥時代",
            "tags": ["律令", "女帝", "飛鳥"]
        },
    ],

    "年号": [
        # 難易度1
        {
            "difficulty": 1,
            "question": "江戸幕府が開かれたのは何年ですか？",
            "answer": "1603年",
            "choices": ["1603年", "1600年", "1615年", "1590年"],
            "explanation": "1603年、徳川家康が征夷大将軍に任命されて江戸幕府を開いた。1600年の関ヶ原の戦いで勝利した後、将軍職を得て政権を確立。1605年には息子・秀忠に将軍職を譲り、徳川家の世襲を天下に示した。",
            "era": "江戸時代",
            "tags": ["幕府", "江戸"]
        },
        {
            "difficulty": 1,
            "question": "明治維新が起きた年（明治元年）はいつですか？",
            "answer": "1868年",
            "choices": ["1868年", "1853年", "1871年", "1858年"],
            "explanation": "1868年（明治元年）、鳥羽・伏見の戦いで旧幕府軍を破った新政府が王政復古の大号令を発し、明治天皇を中心とする新政府が発足した。同年3月に五箇条の御誓文が発布され、明治という元号が定められた。",
            "era": "明治時代",
            "tags": ["維新", "近代化"]
        },
        {
            "difficulty": 1,
            "question": "大化の改新が始まった年はいつですか？",
            "answer": "645年",
            "choices": ["645年", "604年", "672年", "701年"],
            "explanation": "645年、中大兄皇子と中臣鎌足が蘇我入鹿を宮中で暗殺（乙巳の変）し、蘇我氏の専横を打破して大化の改新が始まった。翌646年に「改新の詔」が出され、公地公民・国郡里制などの改革が進められ、律令国家の基礎が作られた。",
            "era": "飛鳥時代",
            "tags": ["改革", "律令"]
        },
        {
            "difficulty": 1,
            "question": "日本が第二次世界大戦で降伏したのは何年ですか？",
            "answer": "1945年",
            "choices": ["1945年", "1943年", "1941年", "1947年"],
            "explanation": "1945年8月15日、昭和天皇がラジオ放送（玉音放送）で終戦を告げ、日本はポツダム宣言を受諾して降伏した。同年9月2日に東京湾上の戦艦ミズーリ号上で降伏文書に調印し、第二次世界大戦が正式に終結した。",
            "era": "昭和時代",
            "tags": ["戦争", "現代"]
        },
        {
            "difficulty": 1,
            "question": "関ヶ原の戦いが起きたのは何年ですか？",
            "answer": "1600年",
            "choices": ["1600年", "1603年", "1598年", "1615年"],
            "explanation": "1600年9月15日（慶長5年）、美濃国（岐阜県）関ヶ原で東軍（徳川家康）と西軍（石田三成・毛利輝元）が激突した。小早川秀秋の裏切りなどで西軍が壊滅し、わずか半日で決着がついた。この戦いが江戸幕府成立の決定的な契機となった。",
            "era": "戦国〜江戸",
            "tags": ["戦争", "戦国"]
        },
        # 難易度2
        {
            "difficulty": 2,
            "question": "鎌倉幕府が滅亡したのは何年ですか？",
            "answer": "1333年",
            "choices": ["1333年", "1336年", "1185年", "1221年"],
            "explanation": "1333年、後醍醐天皇の倒幕運動に呼応した足利尊氏が六波羅探題を攻略、新田義貞が鎌倉を攻め、北条高時ら北条一族は東勝寺で自刃して鎌倉幕府は滅亡した（元弘の変）。その後、後醍醐天皇による建武の新政（1333〜36）が始まったが短命に終わった。",
            "era": "鎌倉末期",
            "tags": ["幕府", "鎌倉"]
        },
        {
            "difficulty": 2,
            "question": "日清戦争の講和条約（下関条約）が結ばれたのは何年ですか？",
            "answer": "1895年",
            "choices": ["1895年", "1894年", "1905年", "1902年"],
            "explanation": "1895年4月、日清戦争の講和として下関条約（日清講和条約）が調印された。清は遼東半島・台湾・澎湖諸島の割譲と多額の賠償金を日本に支払うことになった。しかし同年、ロシア・フランス・ドイツによる三国干渉で遼東半島を返還させられた（臥薪嘗胆）。",
            "era": "明治時代",
            "tags": ["外交", "戦争"]
        },
        {
            "difficulty": 2,
            "question": "大日本帝国憲法が発布されたのは何年ですか？",
            "answer": "1889年",
            "choices": ["1889年", "1885年", "1890年", "1881年"],
            "explanation": "1889年2月11日（紀元節）、大日本帝国憲法（明治憲法）が発布された。伊藤博文を中心にプロイセン憲法を参考に起草され、主権は天皇にあるとする欽定憲法だった。翌1890年に第1回帝国議会が開会し、立憲政治が始まった。",
            "era": "明治時代",
            "tags": ["憲法", "政治"]
        },
        {
            "difficulty": 2,
            "question": "応仁の乱が始まったのは何年ですか？",
            "answer": "1467年",
            "choices": ["1467年", "1477年", "1392年", "1441年"],
            "explanation": "1467年（応仁元年）、足利将軍家の継嗣問題・管領家の相続問題を契機に、細川勝元（東軍）と山名宗全（西軍）が対立して応仁の乱が勃発した。主戦場となった京都は11年にわたって焦土化し、1477年に終結した。この乱を境に戦国時代が始まったとされる。",
            "era": "室町時代",
            "tags": ["戦乱", "室町"]
        },
        {
            "difficulty": 2,
            "question": "日露戦争の講和条約（ポーツマス条約）が結ばれたのは何年ですか？",
            "answer": "1905年",
            "choices": ["1905年", "1904年", "1902年", "1907年"],
            "explanation": "1905年9月、アメリカのポーツマスでポーツマス条約が調印され、日露戦争が終結した。日本は韓国の指導権・遼東半島租借権・南満州鉄道利権・樺太南半分を獲得した。しかし賠償金が得られなかったため、国内では日比谷焼き打ち事件など暴動が起きた。",
            "era": "明治時代",
            "tags": ["外交", "戦争"]
        },
        # 難易度3
        {
            "difficulty": 3,
            "question": "承久の乱が起きた年はいつですか？",
            "answer": "1221年",
            "choices": ["1221年", "1185年", "1232年", "1274年"],
            "explanation": "1221年（承久3年）、後鳥羽上皇が鎌倉幕府打倒を呼びかけて挙兵したが（承久の乱）、北条義時率いる幕府軍に大敗した。上皇は隠岐に流され、朝廷の勢力は大きく後退した。幕府はこの後、京都に六波羅探題を設置して朝廷を監視した。",
            "era": "鎌倉時代",
            "tags": ["幕府", "朝廷"]
        },
        {
            "difficulty": 3,
            "question": "大塩平八郎の乱が起きたのは何年ですか？",
            "answer": "1837年",
            "choices": ["1837年", "1825年", "1842年", "1853年"],
            "explanation": "1837年（天保8年）、大坂東町奉行所の元与力・大塩平八郎が天保の飢饉で苦しむ民衆を救うため挙兵した（大塩平八郎の乱）。乱は半日で鎮圧されたが、幕臣出身者が反乱を起こしたことは幕府に大きな衝撃を与えた。この乱は幕藩体制の動揺を示すできごととして重要。",
            "era": "江戸時代後期",
            "tags": ["反乱", "天保"]
        },
        {
            "difficulty": 3,
            "question": "日本が国際連盟を脱退したのは何年ですか？",
            "answer": "1933年",
            "choices": ["1933年", "1931年", "1937年", "1941年"],
            "explanation": "1933年（昭和8年）3月、日本は国際連盟を脱退した。前年の1931年の満洲事変後、国際連盟のリットン調査団が満洲国建国の不当性を報告し、総会で日本軍の撤退勧告が採択されたことを受けての決定だった。これ以後、日本の国際的孤立が深まっていった。",
            "era": "昭和時代（戦前）",
            "tags": ["外交", "戦前"]
        },
        {
            "difficulty": 3,
            "question": "武家諸法度が初めて制定されたのは何年ですか？",
            "answer": "1615年",
            "choices": ["1615年", "1603年", "1635年", "1600年"],
            "explanation": "1615年（元和元年）、大坂夏の陣で豊臣氏を滅ぼした直後、徳川家康・秀忠が武家諸法度（元和令）を制定した。文武弓馬の道の奨励・城郭修繕の届出・大名同士の無断婚姻禁止などを定めた。1635年の寛永令では参勤交代が義務化され、大名統制がさらに強化された。",
            "era": "江戸時代初期",
            "tags": ["幕府", "法令"]
        },
        {
            "difficulty": 3,
            "question": "五・一五事件が起きたのは何年ですか？",
            "answer": "1932年",
            "choices": ["1932年", "1931年", "1936年", "1929年"],
            "explanation": "1932年（昭和7年）5月15日、海軍青年将校らが犬養毅首相を暗殺した（五・一五事件）。犬養は「話せばわかる」と語りかけたが、将校らは「問答無用」と射殺したとされる。この事件で政党内閣の時代が終わり、軍部の政治介入が強まった。",
            "era": "昭和時代（戦前）",
            "tags": ["テロ", "軍部"]
        },
        # 難易度4
        {
            "difficulty": 4,
            "question": "江戸幕府が生類憐みの令を初めて発令したのは何年ですか？",
            "answer": "1685年",
            "choices": ["1685年", "1687年", "1690年", "1709年"],
            "explanation": "1685年（貞享2年）、5代将軍・徳川綱吉が生類憐みの令を最初に発令した。以後20年以上にわたり度重なる追加令が出され、犬・猫・鳥だけでなく魚・虫に至るまで殺生が禁じられた。江戸に巨大な犬小屋が設けられ、違反者は厳罰に処された。綱吉は仏教の影響を受けたとされ、また自身が戌年生まれだったという説もある。",
            "era": "江戸時代（元禄）",
            "tags": ["幕政", "法令"]
        },
        {
            "difficulty": 4,
            "question": "日本で最初の銀行（第一国立銀行）が設立されたのは何年ですか？",
            "answer": "1873年",
            "choices": ["1873年", "1868年", "1882年", "1876年"],
            "explanation": "1873年（明治6年）、渋沢栄一らが中心となり第一国立銀行（現・みずほ銀行の前身）が設立された。国立銀行条例（1872年）に基づき、民間が設立・運営する銀行として認可された。渋沢は後に日本勧業銀行など多くの企業・銀行設立に関わり「日本資本主義の父」と呼ばれる。",
            "era": "明治時代",
            "tags": ["経済", "近代化"]
        },
        {
            "difficulty": 4,
            "question": "奥州藤原氏の初代・藤原清衡が中尊寺金色堂を建立したのは何年ですか？",
            "answer": "1124年",
            "choices": ["1124年", "1105年", "1189年", "1087年"],
            "explanation": "1124年（天治元年）、奥州藤原氏の初代・藤原清衡が中尊寺金色堂を建立した。内外を金箔で覆い螺鈿細工を施した豪華な阿弥陀堂で、清衡・基衡・秀衡の三代のミイラが安置されている。奥州藤原氏は金・馬・絹の交易で栄え、平泉に「浄土」を体現した都市を築いた。2011年にユネスコ世界文化遺産に登録。",
            "era": "平安時代末期",
            "tags": ["文化", "建築"]
        },
        {
            "difficulty": 4,
            "question": "日米和親条約が締結されたのは何年ですか？",
            "answer": "1854年",
            "choices": ["1854年", "1853年", "1858年", "1856年"],
            "explanation": "1854年（安政元年）3月、ペリーが再来航して日米和親条約（神奈川条約）が締結された。下田・函館の2港の開港・薪水食料の補給・漂流民保護などを定めたが、通商は含まれなかった。前年1853年の最初の来航では幕府は返答を先送りにしていた。この条約が日本の開国の第一歩となった。",
            "era": "江戸時代末期（幕末）",
            "tags": ["外交", "開国"]
        },
        {
            "difficulty": 4,
            "question": "聖徳太子が十七条の憲法を制定したのは何年ですか？",
            "answer": "604年",
            "choices": ["604年", "593年", "645年", "607年"],
            "explanation": "604年（推古12年）、聖徳太子（厩戸皇子）が十七条の憲法を制定した。「和をもって貴しとなす」（第1条）・「篤く三宝を敬え」（第2条）・「詔を承りては必ず謹め」（第3条）など、仏教・儒教の思想に基づく役人・豪族の心得を示した。日本最古の成文法とされるが、近年は後世の創作説もある。",
            "era": "飛鳥時代",
            "tags": ["律令", "仏教"]
        },
    ],

    "できごと": [
        # 難易度1
        {
            "difficulty": 1,
            "question": "「天下布武」を掲げ、楽市楽座などの革新政策を行った戦国武将は誰ですか？",
            "answer": "織田信長",
            "choices": ["織田信長", "豊臣秀吉", "徳川家康", "武田信玄"],
            "explanation": "織田信長は「天下布武」（武力で天下を統一する）を印章に刻み、既存の権威に挑んだ。楽市楽座（市場の独占・課税の廃止）で商業を活性化させ、比叡山延暦寺焼き討ちで仏教勢力を弾圧、長篠の戦いで鉄砲の三段撃ちを活用した。安土城は天守閣を持つ近世城郭の先駆けとなった。",
            "era": "戦国時代",
            "tags": ["戦国", "統一"]
        },
        {
            "difficulty": 1,
            "question": "黒船で来航し、日本に開国を迫ったアメリカの提督は誰ですか？",
            "answer": "ペリー",
            "choices": ["ペリー", "ハリス", "リンカーン", "マッカーサー"],
            "explanation": "マシュー・ペリー（1794〜1858）は1853年に4隻の黒船（蒸気船）を率いて浦賀に来航し、大統領の国書を幕府に提出して開国を要求した。翌1854年に再来航し、日米和親条約を締結させた。黒船の大砲と蒸気機関の圧倒的な力は日本人に大きな衝撃を与え、「泰平の眠りを覚ます上喜撰（蒸気船）たった四杯で夜も眠れず」と狂歌に詠まれた。",
            "era": "江戸末期",
            "tags": ["外交", "開国"]
        },
        {
            "difficulty": 1,
            "question": "江戸時代の三大改革のうち、天保の改革を行った老中は誰ですか？",
            "answer": "水野忠邦",
            "choices": ["水野忠邦", "松平定信", "徳川吉宗", "田沼意次"],
            "explanation": "水野忠邦（1794〜1851）は老中首座として1841〜43年に天保の改革を断行。倹約令・株仲間の解散・人返し令・上知令などを実施したが、上知令（江戸・大坂周辺の大名・旗本領を幕府直轄地にしようとした政策）が大名・旗本の猛反発を受け、失脚した。",
            "era": "江戸時代後期",
            "tags": ["改革", "幕政"]
        },
        {
            "difficulty": 1,
            "question": "飛鳥時代に遣隋使として隋に派遣された人物は誰ですか？",
            "answer": "小野妹子",
            "choices": ["小野妹子", "阿倍仲麻呂", "藤原鎌足", "犬上御田鍬"],
            "explanation": "小野妹子は607年（推古15年）に聖徳太子の命で遣隋使として隋の煬帝のもとへ派遣された。「日出ずる処の天子、書を日没する処の天子に致す」で始まる国書を持参したが、煬帝はこの対等な表現に不快感を示したとされる。帰国の際に裴世清を伴い帰朝した。",
            "era": "飛鳥時代",
            "tags": ["外交", "遣隋使"]
        },
        {
            "difficulty": 1,
            "question": "江戸幕府最後の将軍として大政奉還を行ったのは誰ですか？",
            "answer": "徳川慶喜",
            "choices": ["徳川慶喜", "徳川家茂", "徳川斉昭", "徳川慶福"],
            "explanation": "徳川慶喜（1837〜1913）は一橋家から15代将軍となった。1867年10月に政権を朝廷に返上する大政奉還を行い、薩長による倒幕の口実を封じようとしたが、12月の王政復古の大号令で旧幕府勢力の排除が決まり、鳥羽・伏見の戦いに敗れた後、江戸城を無血開城した。",
            "era": "江戸末期・明治初期",
            "tags": ["幕末", "維新"]
        },
        # 難易度2
        {
            "difficulty": 2,
            "question": "「東海道中膝栗毛」を著し、庶民文化を代表する作品を残した江戸時代の作家は誰ですか？",
            "answer": "十返舎一九",
            "choices": ["十返舎一九", "滝沢馬琴", "式亭三馬", "葛飾北斎"],
            "explanation": "十返舎一九（1765〜1831）は1802年から刊行した『東海道中膝栗毛』で大ヒットを飛ばした。弥次郎兵衛・喜多八の珍道中を描いたこの作品は庶民の旅への憧れを反映し、続編が次々と書かれた。化政文化（文化・文政年間）を代表する滑稽本で、当時の東海道の風俗・名所が生き生きと描かれている。",
            "era": "江戸時代後期（化政文化）",
            "tags": ["文化", "文学"]
        },
        {
            "difficulty": 2,
            "question": "1945年8月6日に広島に原爆を投下したアメリカ軍の爆撃機の名前は何ですか？（人物名で答えよ：その機長は？）",
            "answer": "ポール・ティベッツ",
            "choices": ["ポール・ティベッツ", "ダグラス・マッカーサー", "チェスター・ニミッツ", "カーチス・ルメイ"],
            "explanation": "ポール・ティベッツ大佐（1915〜2007）が指揮する爆撃機B-29「エノラ・ゲイ」が1945年8月6日午前8時15分、広島市に人類史上初の原子爆弾（ウラン型「リトルボーイ」）を投下した。爆発により約7万人が即死し、年末までに14万人前後が死亡したとされる。3日後の8月9日には長崎にも原爆が投下された。",
            "era": "昭和時代（戦争末期）",
            "tags": ["戦争", "原爆"]
        },
        {
            "difficulty": 2,
            "question": "豊臣秀吉が行った刀狩りの主な目的は何ですか？（この政策を断行したのは誰ですか）",
            "answer": "豊臣秀吉",
            "choices": ["豊臣秀吉", "織田信長", "徳川家康", "足利義満"],
            "explanation": "豊臣秀吉は1588年（天正16年）に刀狩令を発令し、農民から武器を取り上げた。表向きの理由は「大仏建立のための材料収集」だったが、真の目的は農民の武装解除・一揆の防止・兵農分離の徹底にあった。1591年の身分統制令とあわせて武士・農民・町人の身分が固定されていき、近世封建社会の基礎が作られた。",
            "era": "安土桃山時代",
            "tags": ["政策", "兵農分離"]
        },
        {
            "difficulty": 2,
            "question": "明治時代の地租改正で、課税基準が「収穫高」から何に変わりましたか？（この改革を主導した大蔵卿は誰ですか）",
            "answer": "大久保利通",
            "choices": ["大久保利通", "伊藤博文", "岩倉具視", "木戸孝允"],
            "explanation": "大久保利通（1830〜1878）が主導した地租改正（1873年）では、課税基準が「収穫高の何割」から「地価の3%（後に2.5%）」へ変更された。これにより政府は安定した税収を確保できるようになった。しかし農民の税負担が重く、1876〜77年に地租改正反対一揆が各地で起こり、税率を2.5%に引き下げた。",
            "era": "明治時代",
            "tags": ["改革", "経済"]
        },
        {
            "difficulty": 2,
            "question": "日本で初めて選挙権が女性にも認められた（女性参政権）のはいつですか？その選挙を主導した内閣総理大臣は誰ですか？",
            "answer": "幣原喜重郎",
            "choices": ["幣原喜重郎", "吉田茂", "鳩山一郎", "芦田均"],
            "explanation": "幣原喜重郎内閣（1945〜46年）の下、1945年12月の選挙法改正で女性参政権が実現した。翌1946年4月10日の第22回衆議院議員総選挙が女性が投票・立候補できた初の選挙となり、39人の女性議員が誕生した。この改正はGHQの指示もあったが、幣原内閣が主体的に進めた。",
            "era": "昭和時代（戦後）",
            "tags": ["民主主義", "戦後改革"]
        },
        # 難易度3
        {
            "difficulty": 3,
            "question": "室町幕府が明（中国）との間で始めた貿易で、正式な船と倭寇を区別するために用いられた証明書を何といいますか？（この貿易を本格化させた将軍は誰ですか）",
            "answer": "足利義満",
            "choices": ["足利義満", "足利義持", "足利義政", "足利義教"],
            "explanation": "足利義満は1404年に明との間で勘合貿易（日明貿易）を開始した。勘合符（合い札）を用いて正式な朝貢貿易船と倭寇を区別し、明から銅銭・生糸・陶磁器などを輸入、日本からは銅・刀剣・硫黄などを輸出した。義満が「日本国王」として明の冊封を受けたことは後世から批判もされた。",
            "era": "室町時代",
            "tags": ["外交", "貿易"]
        },
        {
            "difficulty": 3,
            "question": "明治政府が廃藩置県（1871年）を断行した際の太政大臣は誰ですか？",
            "answer": "三条実美",
            "choices": ["三条実美", "岩倉具視", "大久保利通", "西郷隆盛"],
            "explanation": "三条実美（1837〜1891）は廃藩置県当時の太政大臣で、形式上の最高責任者だった。実質的には大久保利通・木戸孝允・西郷隆盛ら薩長の指導者が推進した。廃藩置県により約300の藩が廃止されて府県に統一され、中央集権国家の骨格が整った。元藩主（知藩事）には家禄が支給され、東京居住を命じられた。",
            "era": "明治時代",
            "tags": ["政治", "中央集権"]
        },
        {
            "difficulty": 3,
            "question": "戦時中の1940年に近衛文麿内閣が推進した政党解散・一国一党化の運動を何といいますか？（その中心組織を作ったのは誰ですか）",
            "answer": "近衛文麿",
            "choices": ["近衛文麿", "東条英機", "平沼騏一郎", "広田弘毅"],
            "explanation": "近衛文麿（1891〜1945）は1940年に大政翼賛会を組織し、既存の政党を解散させて一国一党体制を作り上げた（大政翼賛運動）。これにより自由民主主義的な政治活動が事実上禁止され、軍部主導の戦時体制が強化された。近衛は戦後、A級戦犯として逮捕される前夜に服毒自殺した。",
            "era": "昭和時代（戦時中）",
            "tags": ["戦争", "政治"]
        },
        {
            "difficulty": 3,
            "question": "江戸時代に国学を大成し「古事記伝」を著したのは誰ですか？",
            "answer": "本居宣長",
            "choices": ["本居宣長", "賀茂真淵", "荷田春満", "平田篤胤"],
            "explanation": "本居宣長（1730〜1801）は伊勢松阪の医師で、賀茂真淵に師事して国学を学んだ。約35年をかけて古事記を研究・注釈した『古事記伝』（全44巻）は国学の最高峰とされる。「もののあわれ」を日本文学の本質と説き、儒教・仏教以前の日本固有の精神「やまとごころ」を強調した。その思想は後の尊王攘夷運動にも影響を与えた。",
            "era": "江戸時代後期",
            "tags": ["国学", "文化"]
        },
        {
            "difficulty": 3,
            "question": "二・二六事件（1936年）を起こした青年将校たちが掲げたスローガン（目標）を何といいますか？（反乱部隊が総指揮官に担ごうとした陸軍大将は誰ですか）",
            "answer": "真崎甚三郎",
            "choices": ["真崎甚三郎", "荒木貞夫", "林銑十郎", "寺内寿一"],
            "explanation": "真崎甚三郎（1876〜1956）は皇道派の陸軍大将で、1936年2月26日の二・二六事件で反乱部隊が担ごうとした人物の一人とされる。事件では陸軍内の皇道派青年将校約1400人が首相官邸・警視庁などを占拠し、斎藤実内大臣・高橋是清蔵相らを殺害した。事件後、皇道派は粛清され、統制派が主導権を握った。",
            "era": "昭和時代（戦前）",
            "tags": ["テロ", "軍部"]
        },
        # 難易度4
        {
            "difficulty": 4,
            "question": "江戸幕府が異国船打払令を発令したのは1825年ですが、この前年に日本沿岸に現れてトラブルとなったイギリス船の名前は何ですか？（その事件名は？）",
            "answer": "フェートン号事件",
            "choices": ["フェートン号事件", "モリソン号事件", "シーボルト事件", "ゴローウニン事件"],
            "explanation": "フェートン号事件は1808年（文化5年）に起きた。イギリス船フェートン号が長崎に入港し、オランダ船員を人質に取って食料・水の補給を要求した。当時の長崎奉行は切腹して責任を取り、幕府は海防強化を迫られた。この事件と1824年の常陸国大津浜へのイギリス船員上陸事件などを背景に、1825年に異国船打払令が出された。",
            "era": "江戸時代後期",
            "tags": ["外交", "海防"]
        },
        {
            "difficulty": 4,
            "question": "鎌倉時代に後嵯峨天皇が二人の皇子に皇位を分け与えたことが原因で生まれた二つの系統とは何ですか？（南北朝の対立のきっかけとなった持明院統と何統ですか）",
            "answer": "大覚寺統",
            "choices": ["大覚寺統", "花山院統", "亀山院統", "伏見院統"],
            "explanation": "後嵯峨天皇が後深草天皇（持明院統）と亀山天皇（大覚寺統）の二系統に分かれ、鎌倉幕府の仲裁で両統から交互に天皇を出す「両統迭立」が行われた。しかし争いは続き、後醍醐天皇（大覚寺統）が倒幕を試みたことで南北朝の動乱（1336〜92）へと発展した。後醍醐天皇が吉野に逃れて南朝、光明天皇（持明院統）が京都で北朝を立てた。",
            "era": "鎌倉〜南北朝時代",
            "tags": ["皇室", "南北朝"]
        },
        {
            "difficulty": 4,
            "question": "明治時代に実施された地方制度改革で、1888年の市制・町村制、1890年の府県制・郡制を立案した内務官僚は誰ですか？",
            "answer": "山県有朋",
            "choices": ["山県有朋", "伊藤博文", "井上馨", "松方正義"],
            "explanation": "山県有朋（1838〜1922）は長州藩出身で、軍制整備（徴兵令・軍人勅諭）とともに地方自治制度の整備に尽力した。1888年の市制・町村制と1890年の府県制・郡制（いわゆる明治の地方自治制度）を内務卿として立案・施行した。山県は「藩閥政治家」として桂太郎ら官僚・軍人を養成し、明治後期〜大正初期の政界に長く影響力を持った。",
            "era": "明治時代",
            "tags": ["地方制度", "行政"]
        },
        {
            "difficulty": 4,
            "question": "江戸時代初期にキリシタン弾圧の中で起きた島原の乱（1637〜38年）で一揆軍の総大将となった少年は誰ですか？",
            "answer": "天草四郎（益田時貞）",
            "choices": ["天草四郎（益田時貞）", "小西行長", "有馬晴信", "鍋島直茂"],
            "explanation": "天草四郎（1621頃〜1638）、本名・益田時貞は、島原藩・唐津藩の過酷な年貢徴収とキリシタン弾圧に苦しむ農民たちに推戴されて一揆の総大将となった。わずか16歳前後だったが、「天の使者」として信仰を集めた。原城に籠城した一揆軍約3万7千人は4ヶ月後に幕府軍12万に攻め落とされ、ほぼ全員が討ち死にした。",
            "era": "江戸時代初期",
            "tags": ["キリシタン", "一揆"]
        },
        {
            "difficulty": 4,
            "question": "奈良時代に鑑真が来日を果たしたのは何度目の挑戦でしたか？その最終来日年は？（何年に来日したか）",
            "answer": "753年",
            "choices": ["753年", "741年", "745年", "759年"],
            "explanation": "鑑真（688〜763）は唐（中国）の高僧で、日本側の招きに応じて渡航を試みたが嵐・難破・失明などで5回失敗し、6回目の挑戦でようやく753年に来日を果たした。759年に奈良に唐招提寺を創建し、正式な戒律（授戒制度）を日本に伝えた。盲目となった鑑真の像（唐招提寺鑑真和上像）は日本最古の肖像彫刻として国宝に指定されている。",
            "era": "奈良時代",
            "tags": ["仏教", "外交"]
        },
    ]
}


# ─────────────────────────────────────────────
# ページ設定
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="日本史クイズ",
    page_icon="⛩️",
    layout="wide"
)

# ─────────────────────────────────────────────
# カスタムCSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&family=Noto+Sans+JP:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
}

h1, h2, h3 {
    font-family: 'Noto Serif JP', serif;
}

.main-title {
    text-align: center;
    font-size: 2.8rem;
    font-family: 'Noto Serif JP', serif;
    color: #2c1810;
    margin-bottom: 0.2em;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}

.subtitle {
    text-align: center;
    color: #8b4513;
    font-size: 1.1rem;
    margin-bottom: 2em;
}

.question-card {
    background: linear-gradient(135deg, #fdf6e3 0%, #fef9f0 100%);
    border: 2px solid #d4a96a;
    border-radius: 12px;
    padding: 1.5em;
    margin-bottom: 1em;
    box-shadow: 3px 3px 10px rgba(139,69,19,0.15);
}

.question-text {
    font-family: 'Noto Serif JP', serif;
    font-size: 1.25rem;
    color: #2c1810;
    line-height: 1.7;
}

.difficulty-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: bold;
    margin-right: 8px;
    margin-bottom: 8px;
}

.diff-1 { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.diff-2 { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
.diff-3 { background: #ffe5d0; color: #c05621; border: 1px solid #ffcc9d; }
.diff-4 { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }

.correct-box {
    background: #d4edda;
    border: 2px solid #28a745;
    border-radius: 8px;
    padding: 1em;
    margin: 0.5em 0;
    color: #155724;
}

.wrong-box {
    background: #f8d7da;
    border: 2px solid #dc3545;
    border-radius: 8px;
    padding: 1em;
    margin: 0.5em 0;
    color: #721c24;
}

.explanation-box {
    background: #e8f4fd;
    border-left: 4px solid #2980b9;
    border-radius: 0 8px 8px 0;
    padding: 1em 1.2em;
    margin: 0.7em 0;
    color: #1a4a6b;
    line-height: 1.8;
    font-size: 0.97rem;
}

.note-card {
    background: #fffdf5;
    border: 1px solid #e8c97a;
    border-radius: 8px;
    padding: 1em;
    margin-bottom: 0.7em;
    border-left: 4px solid #e8962a;
}

.stats-box {
    background: linear-gradient(135deg, #2c1810 0%, #5c2d0a 100%);
    border-radius: 12px;
    padding: 1.2em;
    color: white;
    text-align: center;
    margin-bottom: 1em;
}

.mode-card {
    background: white;
    border: 2px solid #d4a96a;
    border-radius: 12px;
    padding: 1.2em;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 0.5em;
}

.mode-card:hover {
    border-color: #8b4513;
    box-shadow: 0 4px 12px rgba(139,69,19,0.2);
}

.progress-bar-container {
    background: #e8d5b5;
    border-radius: 10px;
    height: 12px;
    margin: 0.5em 0;
}

.progress-bar-fill {
    background: linear-gradient(90deg, #8b4513, #d4a96a);
    border-radius: 10px;
    height: 12px;
    transition: width 0.3s;
}

.stButton>button {
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 1rem;
    border-radius: 8px;
    transition: all 0.2s;
}

.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.era-tag {
    display: inline-block;
    background: #f0e6d3;
    color: #6b3a1f;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.8rem;
    border: 1px solid #d4a96a;
    margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# セッション状態の初期化
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "page": "home",
        "mode": None,
        "difficulty": None,
        "questions": [],
        "current_idx": 0,
        "score": 0,
        "answered": False,
        "selected": None,
        "wrong_notes": [],  # 間違えた問題のリスト
        "session_results": [],  # このセッションの結果
        "total_answered": 0,
        "total_correct": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ─────────────────────────────────────────────
# ユーティリティ関数
# ─────────────────────────────────────────────
def get_difficulty_label(d):
    labels = {1: "⭐ 易しい", 2: "⭐⭐ 普通", 3: "⭐⭐⭐ 難しい", 4: "⭐⭐⭐⭐ 超難問"}
    return labels.get(d, "不明")

def get_difficulty_class(d):
    return f"diff-{d}"

def get_mode_emoji(m):
    emojis = {"人物": "👤", "年号": "📅", "できごと": "⚔️"}
    return emojis.get(m, "❓")

def build_quiz(mode, difficulty, n=10):
    pool = [q for q in QUESTIONS[mode] if q["difficulty"] == difficulty]
    random.shuffle(pool)
    return pool[:min(n, len(pool))]

def go_to(page):
    st.session_state.page = page

def start_quiz(mode, difficulty):
    st.session_state.mode = mode
    st.session_state.difficulty = difficulty
    st.session_state.questions = build_quiz(mode, difficulty)
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.session_results = []
    st.session_state.page = "quiz"


# ─────────────────────────────────────────────
# ホーム画面
# ─────────────────────────────────────────────
def page_home():
    st.markdown('<h1 class="main-title">⛩️ 日本史クイズ</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">人物・年号・できごとの3モード ／ 難易度4段階</p>', unsafe_allow_html=True)

    # 統計表示
    if st.session_state.total_answered > 0:
        rate = int(st.session_state.total_correct / st.session_state.total_answered * 100)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("累計回答数", st.session_state.total_answered)
        with col2:
            st.metric("累計正解数", st.session_state.total_correct)
        with col3:
            st.metric("正解率", f"{rate}%")

    st.divider()

    # モード選択
    st.subheader("📚 モードを選んでください")
    mode_descriptions = {
        "人物": "歴史上の重要人物を答える問題。武将・天皇・偉人など幅広く出題！",
        "年号": "出来事が起きた西暦年を答える問題。歴史の流れをしっかり押さえよう！",
        "できごと": "ある出来事や業績から関連人物を答える問題。応用力が試される！"
    }

    selected_mode = st.session_state.get("selected_mode", None)
    cols = st.columns(3)
    for i, (mode, desc) in enumerate(mode_descriptions.items()):
        with cols[i]:
            emoji = get_mode_emoji(mode)
            if st.button(f"{emoji} {mode}モード", key=f"mode_{mode}", use_container_width=True):
                st.session_state.selected_mode = mode
                st.rerun()
            st.caption(desc)

    st.divider()

    # 難易度選択
    if st.session_state.get("selected_mode"):
        mode = st.session_state.selected_mode
        st.subheader(f"🎯 {get_mode_emoji(mode)} {mode}モード ─ 難易度を選んでください")

        diff_labels = [
            (1, "⭐ 易しい", "基本的な知識。教科書レベル", "#d4edda", "#155724"),
            (2, "⭐⭐ 普通", "高校入試・センター試験レベル", "#fff3cd", "#856404"),
            (3, "⭐⭐⭐ 難しい", "大学入試・歴史検定2〜3級レベル", "#ffe5d0", "#c05621"),
            (4, "⭐⭐⭐⭐ 超難問", "歴史マニア・検定1級レベル", "#f8d7da", "#721c24"),
        ]

        col1, col2 = st.columns(2)
        for idx, (d, label, desc, bg, fg) in enumerate(diff_labels):
            n = len([q for q in QUESTIONS[mode] if q["difficulty"] == d])
            with (col1 if idx < 2 else col2):
                if st.button(f"{label}　（{n}問）\n{desc}", key=f"diff_{d}", use_container_width=True):
                    start_quiz(mode, d)
                    st.rerun()

    st.divider()

    # ノート確認ボタン
    note_count = len(st.session_state.wrong_notes)
    if note_count > 0:
        st.info(f"📓 間違えた問題が {note_count} 件あります")
        if st.button("📓 間違いノートを見る", use_container_width=True):
            go_to("notes")
            st.rerun()
    else:
        st.caption("📓 間違えた問題は「間違いノート」に自動保存されます")


# ─────────────────────────────────────────────
# クイズ画面
# ─────────────────────────────────────────────
def page_quiz():
    questions = st.session_state.questions
    idx = st.session_state.current_idx

    if not questions or idx >= len(questions):
        go_to("result")
        st.rerun()
        return

    q = questions[idx]
    total = len(questions)

    # ヘッダー
    col_head1, col_head2, col_head3 = st.columns([1, 2, 1])
    with col_head1:
        if st.button("🏠 ホームへ"):
            go_to("home")
            st.session_state.selected_mode = None
            st.rerun()
    with col_head2:
        progress = (idx) / total
        st.markdown(f"""
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width:{int(progress*100)}%"></div>
        </div>
        <p style="text-align:center; margin:0; font-size:0.9rem; color:#666;">
            問題 {idx+1} / {total} ｜ 正解: {st.session_state.score}
        </p>
        """, unsafe_allow_html=True)
    with col_head3:
        st.markdown(
            f'<span class="difficulty-badge {get_difficulty_class(q["difficulty"])}">'
            f'{get_difficulty_label(q["difficulty"])}</span>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 問題文
    mode_emoji = get_mode_emoji(st.session_state.mode)
    st.markdown(f"""
    <div class="question-card">
        <span class="era-tag">{q["era"]}</span>
        <p class="question-text">
            <strong>{mode_emoji} 問題 {idx+1}</strong><br><br>
            {q["question"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 選択肢
    choices = q["choices"][:]
    answered = st.session_state.answered
    selected = st.session_state.selected

    if not answered:
        st.write("**選択肢を選んでください：**")
        for choice in choices:
            if st.button(f"　{choice}　", key=f"choice_{choice}", use_container_width=True):
                st.session_state.selected = choice
                st.session_state.answered = True
                st.session_state.total_answered += 1
                if choice == q["answer"]:
                    st.session_state.score += 1
                    st.session_state.total_correct += 1
                    st.session_state.session_results.append({"q": q, "correct": True, "selected": choice})
                else:
                    # 間違いノートに追加（重複チェック）
                    existing_ids = [n["question"] for n in st.session_state.wrong_notes]
                    if q["question"] not in existing_ids:
                        st.session_state.wrong_notes.append({
                            **q,
                            "wrong_answer": choice,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                    st.session_state.session_results.append({"q": q, "correct": False, "selected": choice})
                st.rerun()
    else:
        # 回答後の表示
        is_correct = selected == q["answer"]

        if is_correct:
            st.markdown(f'<div class="correct-box">✅ <strong>正解！</strong>　{q["answer"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wrong-box">❌ <strong>不正解</strong>　あなたの回答: {selected}<br>正解: <strong>{q["answer"]}</strong></div>', unsafe_allow_html=True)

        # 選択肢を色分け表示
        st.write("**選択肢：**")
        for choice in choices:
            if choice == q["answer"]:
                st.success(f"✅ {choice}（正解）")
            elif choice == selected and not is_correct:
                st.error(f"❌ {choice}（あなたの回答）")
            else:
                st.write(f"　　{choice}")

        # 解説
        st.markdown(f"""
        <div class="explanation-box">
            <strong>📖 解説</strong><br><br>
            {q["explanation"]}
        </div>
        """, unsafe_allow_html=True)

        # 時代タグ
        if q.get("tags"):
            tags_html = "".join([f'<span class="era-tag">#{t}</span>' for t in q["tags"]])
            st.markdown(f"**関連キーワード：** {tags_html}", unsafe_allow_html=True)

        st.markdown("")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            label = "次の問題 ▶" if idx + 1 < total else "結果を見る 🏆"
            if st.button(label, use_container_width=True, type="primary"):
                st.session_state.current_idx += 1
                st.session_state.answered = False
                st.session_state.selected = None
                if idx + 1 >= total:
                    go_to("result")
                st.rerun()
        with col_btn2:
            if st.button("📓 ノートを見る", use_container_width=True):
                go_to("notes")
                st.rerun()


# ─────────────────────────────────────────────
# 結果画面
# ─────────────────────────────────────────────
def page_result():
    st.markdown('<h2 style="text-align:center; font-family: Noto Serif JP, serif; color:#2c1810;">🏆 クイズ終了！</h2>', unsafe_allow_html=True)

    results = st.session_state.session_results
    score = st.session_state.score
    total = len(results) if results else len(st.session_state.questions)
    rate = int(score / total * 100) if total > 0 else 0

    # スコア表示
    if rate >= 80:
        emoji, msg = "🥇", "素晴らしい！"
        color = "#28a745"
    elif rate >= 60:
        emoji, msg = "🥈", "よくできました！"
        color = "#17a2b8"
    elif rate >= 40:
        emoji, msg = "🥉", "もう少し頑張ろう！"
        color = "#ffc107"
    else:
        emoji, msg = "📚", "復習が必要です！"
        color = "#dc3545"

    st.markdown(f"""
    <div style="text-align:center; padding:2em; background:linear-gradient(135deg, #fdf6e3, #fef9f0);
    border:2px solid #d4a96a; border-radius:16px; margin-bottom:1.5em;">
        <div style="font-size:4rem;">{emoji}</div>
        <div style="font-size:2rem; font-weight:bold; color:{color};">{score} / {total}</div>
        <div style="font-size:1.5rem; color:{color};">{rate}% 正解</div>
        <div style="font-size:1.2rem; color:#666; margin-top:0.5em;">{msg}</div>
        <div style="font-size:0.9rem; color:#888; margin-top:0.3em;">
            モード: {get_mode_emoji(st.session_state.mode)} {st.session_state.mode}　
            難易度: {get_difficulty_label(st.session_state.difficulty)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 問題別結果
    if results:
        st.subheader("📋 問題別結果")
        for i, r in enumerate(results):
            q = r["q"]
            icon = "✅" if r["correct"] else "❌"
            bg = "#d4edda" if r["correct"] else "#f8d7da"
            with st.expander(f"{icon} Q{i+1}: {q['question'][:40]}..."):
                st.markdown(f"""
                <div style="background:{bg}; padding:1em; border-radius:8px; margin-bottom:0.5em;">
                    <b>あなたの回答:</b> {r['selected']}<br>
                    <b>正解:</b> {q['answer']}
                </div>
                <div class="explanation-box">{q['explanation']}</div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 もう一度同じ設定", use_container_width=True, type="primary"):
            start_quiz(st.session_state.mode, st.session_state.difficulty)
            st.rerun()
    with col2:
        if st.button("📓 間違いノート", use_container_width=True):
            go_to("notes")
            st.rerun()
    with col3:
        if st.button("🏠 ホームへ", use_container_width=True):
            go_to("home")
            st.session_state.selected_mode = None
            st.rerun()


# ─────────────────────────────────────────────
# 間違いノート画面
# ─────────────────────────────────────────────
def page_notes():
    st.markdown('<h2 style="font-family: Noto Serif JP, serif; color:#2c1810;">📓 間違いノート</h2>', unsafe_allow_html=True)
    st.caption("間違えた問題が自動的にここに保存されます。復習に活用しましょう！")

    notes = st.session_state.wrong_notes

    if not notes:
        st.info("まだ間違えた問題はありません。クイズを頑張りましょう！")
        if st.button("🏠 ホームへ"):
            go_to("home")
            st.rerun()
        return

    # フィルタ
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mode_filter = st.selectbox("モードで絞り込み", ["すべて"] + list(QUESTIONS.keys()))
    with col_f2:
        diff_filter = st.selectbox("難易度で絞り込み", ["すべて", "1: 易しい", "2: 普通", "3: 難しい", "4: 超難問"])

    filtered = notes
    if mode_filter != "すべて":
        # モードでフィルタ（問題がどのモードに属するかチェック）
        filtered = [n for n in filtered if n["question"] in [q["question"] for q in QUESTIONS[mode_filter]]]
    if diff_filter != "すべて":
        d = int(diff_filter[0])
        filtered = [n for n in filtered if n["difficulty"] == d]

    st.markdown(f"**{len(filtered)} 件の間違いが記録されています**")
    st.markdown("---")

    # ノートの表示
    for i, note in enumerate(filtered):
        diff_label = get_difficulty_label(note["difficulty"])
        diff_cls = get_difficulty_class(note["difficulty"])

        with st.expander(f"📌 {note['question'][:50]}...", expanded=False):
            st.markdown(f"""
            <div class="note-card">
                <span class="difficulty-badge {diff_cls}">{diff_label}</span>
                <span class="era-tag">{note['era']}</span>
                <br><br>
                <strong>❓ 問題：</strong><br>
                {note['question']}
                <br><br>
                <strong>❌ あなたの回答：</strong> {note.get('wrong_answer', '不明')}<br>
                <strong>✅ 正解：</strong> <span style="color:#155724; font-size:1.1em; font-weight:bold;">{note['answer']}</span>
                <br><br>
                <div style="background:#e8f4fd; border-left:4px solid #2980b9; padding:0.8em 1em; border-radius:0 6px 6px 0; line-height:1.8;">
                    <strong>📖 解説</strong><br><br>
                    {note['explanation']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if note.get("tags"):
                tags_html = "".join([f'<span class="era-tag">#{t}</span>' for t in note["tags"]])
                st.markdown(f"**関連キーワード：** {tags_html}", unsafe_allow_html=True)

            col_del, _ = st.columns([1, 3])
            with col_del:
                if st.button(f"🗑️ 削除", key=f"del_note_{i}_{note['question'][:10]}"):
                    st.session_state.wrong_notes = [n for n in st.session_state.wrong_notes if n["question"] != note["question"]]
                    st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 ホームへ", use_container_width=True):
            go_to("home")
            st.rerun()
    with col2:
        if st.button("🗑️ ノートをすべて削除", use_container_width=True):
            st.session_state.wrong_notes = []
            st.rerun()

    # 印刷用テキスト出力
    st.markdown("---")
    st.subheader("📄 ノートをテキストでエクスポート")
    if st.button("テキスト形式で出力"):
        text_out = "# 日本史クイズ 間違いノート\n\n"
        for i, note in enumerate(notes):
            text_out += f"## 問題{i+1}（{get_difficulty_label(note['difficulty'])} ／ {note['era']}）\n"
            text_out += f"**Q:** {note['question']}\n"
            text_out += f"**誤答:** {note.get('wrong_answer', '不明')}\n"
            text_out += f"**正解:** {note['answer']}\n\n"
            text_out += f"**解説:**\n{note['explanation']}\n\n"
            text_out += "---\n\n"
        st.text_area("コピーしてご利用ください", text_out, height=300)


# ─────────────────────────────────────────────
# ルーティング
# ─────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    page_home()
elif page == "quiz":
    page_quiz()
elif page == "result":
    page_result()
elif page == "notes":
    page_notes()