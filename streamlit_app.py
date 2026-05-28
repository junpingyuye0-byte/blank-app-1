import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
import os
from datetime import datetime
from quiz_data import QUIZ_DATA

# ==============================
# 保存ファイルパス
# ==============================
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_data")
os.makedirs(SAVE_DIR, exist_ok=True)
HISTORY_FILE = os.path.join(SAVE_DIR, "history.json")
NOTES_FILE = os.path.join(SAVE_DIR, "notes.json")

# ==============================
# カラーパレット
# ==============================
BG_MAIN      = "#1a1a2e"
BG_CARD      = "#16213e"
BG_ACCENT    = "#0f3460"
COLOR_GOLD   = "#e2b96a"
COLOR_RED    = "#e55353"
COLOR_GREEN  = "#4caf7d"
COLOR_WHITE  = "#f0eadc"
COLOR_GRAY   = "#8a8fa8"
COLOR_BTN    = "#e2b96a"
COLOR_BTN_FG = "#1a1a2e"
FONT_TITLE   = ("Georgia", 22, "bold")
FONT_HEAD    = ("Georgia", 15, "bold")
FONT_BODY    = ("Yu Gothic UI", 13)
FONT_SMALL   = ("Yu Gothic UI", 11)
FONT_BTN     = ("Yu Gothic UI", 12, "bold")

# ==============================
# データ管理
# ==============================
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==============================
# メインアプリ
# ==============================
class HistoryQuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌍 世界史クイズ")
        self.geometry("900x680")
        self.resizable(True, True)
        self.configure(bg=BG_MAIN)
        self.history_records = load_json(HISTORY_FILE)
        self.notes = load_json(NOTES_FILE)
        self._show_home()

    # ---- 画面切り替え共通 ----
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_home(self):
        self._clear()
        HomeScreen(self)

    def _show_quiz(self, mode):
        self._clear()
        QuizScreen(self, mode)

    def _show_history(self):
        self._clear()
        HistoryScreen(self)

    def _show_notes(self):
        self._clear()
        NotesScreen(self)

# ==============================
# ホーム画面
# ==============================
class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        # タイトル
        tk.Label(self, text="🌍 世界史クイズ", font=FONT_TITLE,
                 bg=BG_MAIN, fg=COLOR_GOLD).pack(pady=(40, 5))
        tk.Label(self, text="モードを選んでスタート！",
                 font=FONT_BODY, bg=BG_MAIN, fg=COLOR_GRAY).pack(pady=(0, 30))

        # モードボタン
        modes = [
            ("📅  年号クイズ",        "年号",        "重要な出来事が起きた年を答えよう"),
            ("👤  人物名クイズ",       "人物名",      "歴史上の偉人を当てよう"),
            ("📖  出来事クイズ",       "出来事",      "歴史的事件・出来事を答えよう"),
            ("🏆  人物がやったことクイズ","人物がやったこと","歴史上の人物の業績を覚えよう"),
            ("🔀  やり直し（間違い復習）","retry",    "これまでに間違えた問題だけ"),
        ]
        for label, mode, desc in modes:
            self._mode_btn(label, mode, desc)

        # 区切り
        tk.Frame(self, height=2, bg=BG_ACCENT).pack(fill="x", padx=80, pady=20)

        # サブボタン
        sub_frame = tk.Frame(self, bg=BG_MAIN)
        sub_frame.pack()
        self._sub_btn(sub_frame, "📋 履歴",  self.master._show_history)
        self._sub_btn(sub_frame, "📝 ノート", self.master._show_notes)

    def _mode_btn(self, label, mode, desc):
        frame = tk.Frame(self, bg=BG_CARD, bd=0, relief="flat", cursor="hand2")
        frame.pack(fill="x", padx=100, pady=6)
        inner = tk.Frame(frame, bg=BG_CARD)
        inner.pack(fill="x", padx=20, pady=12)
        tk.Label(inner, text=label, font=FONT_BTN,
                 bg=BG_CARD, fg=COLOR_GOLD, anchor="w").pack(side="left")
        tk.Label(inner, text=desc, font=FONT_SMALL,
                 bg=BG_CARD, fg=COLOR_GRAY, anchor="e").pack(side="right")
        for w in (frame, inner):
            w.bind("<Button-1>", lambda e, m=mode: self.master._show_quiz(m))
            w.bind("<Enter>",    lambda e, f=frame: f.config(bg="#1e2d50"))
            w.bind("<Leave>",    lambda e, f=frame: f.config(bg=BG_CARD))

    def _sub_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, font=FONT_BTN, bg=BG_ACCENT,
                        fg=COLOR_WHITE, bd=0, padx=24, pady=8,
                        activebackground=COLOR_GOLD, activeforeground=BG_MAIN,
                        cursor="hand2", command=cmd)
        btn.pack(side="left", padx=10)

# ==============================
# クイズ画面
# ==============================
class QuizScreen(tk.Frame):
    def __init__(self, master, mode):
        super().__init__(master, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self.mode = mode
        self.questions = self._load_questions()
        self.idx = 0
        self.score = 0
        self.total = len(self.questions)
        self.wrong_list = []
        self.answered = False
        if not self.questions:
            messagebox.showinfo("情報", "間違えた問題がありません！通常モードで練習しましょう。")
            master._show_home()
            return
        self._build()
        self._show_question()

    def _load_questions(self):
        if self.mode == "retry":
            history = load_json(HISTORY_FILE)
            wrong = [r for r in history if not r["correct"]]
            if not wrong:
                return []
            # 重複除去して最近の間違いを最大20問
            seen = set()
            qs = []
            for r in reversed(wrong):
                key = r["question"]
                if key not in seen:
                    seen.add(key)
                    qs.append({
                        "question": r["question"],
                        "answer": r["answer"],
                        "choices": r.get("choices", [r["answer"]]),
                        "explanation": r.get("explanation", ""),
                        "category": r.get("category", ""),
                    })
                if len(qs) >= 20:
                    break
            random.shuffle(qs)
            return qs
        else:
            qs = QUIZ_DATA.get(self.mode, []).copy()
            random.shuffle(qs)
            return qs

    def _build(self):
        # ヘッダー
        hdr = tk.Frame(self, bg=BG_ACCENT)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← ホーム", font=FONT_SMALL, bg=BG_ACCENT,
                  fg=COLOR_WHITE, bd=0, padx=12, pady=6, cursor="hand2",
                  activebackground=COLOR_GOLD, activeforeground=BG_MAIN,
                  command=self.master._show_home).pack(side="left", padx=8, pady=6)

        mode_label = self.mode if self.mode != "retry" else "やり直し（間違い復習）"
        tk.Label(hdr, text=f"📚 {mode_label}", font=FONT_SMALL,
                 bg=BG_ACCENT, fg=COLOR_GOLD).pack(side="left", padx=4)

        self.score_label = tk.Label(hdr, text="", font=FONT_SMALL,
                                    bg=BG_ACCENT, fg=COLOR_WHITE)
        self.score_label.pack(side="right", padx=16, pady=6)

        # プログレスバー
        self.prog_var = tk.DoubleVar(value=0)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Gold.Horizontal.TProgressbar",
                        troughcolor=BG_CARD, background=COLOR_GOLD, thickness=6)
        self.prog = ttk.Progressbar(self, variable=self.prog_var, maximum=self.total,
                                    style="Gold.Horizontal.TProgressbar")
        self.prog.pack(fill="x")

        # 問題エリア
        self.q_frame = tk.Frame(self, bg=BG_MAIN)
        self.q_frame.pack(fill="both", expand=True, padx=60, pady=20)

        self.q_num_label = tk.Label(self.q_frame, text="", font=FONT_SMALL,
                                    bg=BG_MAIN, fg=COLOR_GRAY)
        self.q_num_label.pack(anchor="w")

        self.q_label = tk.Label(self.q_frame, text="", font=FONT_HEAD, wraplength=750,
                                bg=BG_MAIN, fg=COLOR_WHITE, justify="left", anchor="w")
        self.q_label.pack(anchor="w", pady=(4, 20))

        self.choice_frame = tk.Frame(self.q_frame, bg=BG_MAIN)
        self.choice_frame.pack(fill="x")

        self.exp_label = tk.Label(self.q_frame, text="", font=FONT_SMALL, wraplength=750,
                                  bg=BG_CARD, fg=COLOR_WHITE, justify="left",
                                  padx=16, pady=12, anchor="w")

        self.next_btn = tk.Button(self.q_frame, text="次の問題 →", font=FONT_BTN,
                                  bg=COLOR_GOLD, fg=COLOR_BTN_FG, bd=0,
                                  padx=24, pady=10, cursor="hand2",
                                  activebackground="#c9a04e",
                                  command=self._next_question)

        # 間違いタブ（下部）
        self.wrong_frame = tk.Frame(self, bg=BG_MAIN)
        self.wrong_frame.pack(fill="x", padx=60, pady=(0, 10))

        self.wrong_tab_outer = tk.Frame(self.wrong_frame, bg=BG_MAIN)
        self.wrong_tab_outer.pack(fill="x")
        self.wrong_tab_label = tk.Label(self.wrong_tab_outer,
                                        text="❌ 間違い: 0問", font=FONT_SMALL,
                                        bg=COLOR_RED, fg=COLOR_WHITE,
                                        padx=10, pady=4, cursor="hand2")
        self.wrong_tab_label.pack(side="left")
        self.wrong_tab_label.bind("<Button-1>", self._toggle_wrong_list)
        self.wrong_list_frame = tk.Frame(self.wrong_frame, bg=BG_CARD)

    def _show_question(self):
        for w in self.choice_frame.winfo_children():
            w.destroy()
        self.exp_label.pack_forget()
        self.next_btn.pack_forget()
        self.answered = False

        q = self.questions[self.idx]
        self.prog_var.set(self.idx)
        self.score_label.config(text=f"✅ {self.score} / {self.total}")
        self.q_num_label.config(text=f"問 {self.idx + 1} / {self.total}  [{q.get('category','')}]")
        self.q_label.config(text=q["question"])

        choices = q.get("choices", [q["answer"]])
        if len(choices) < 2:
            choices = [q["answer"]]
        random.shuffle(choices)

        colors = ["#2d4a7a", "#2d4a7a", "#2d4a7a", "#2d4a7a"]
        for i, c in enumerate(choices):
            row = i // 2
            col = i % 2
            btn = tk.Button(self.choice_frame, text=c, font=FONT_BODY,
                            bg=BG_CARD, fg=COLOR_WHITE, bd=0,
                            wraplength=320, justify="center",
                            padx=10, pady=14, cursor="hand2",
                            activebackground=BG_ACCENT,
                            command=lambda ans=c: self._check_answer(ans))
            btn.grid(row=row, column=col, padx=8, pady=6, sticky="ew")
            self.choice_frame.columnconfigure(col, weight=1)

    def _check_answer(self, selected):
        if self.answered:
            return
        self.answered = True
        q = self.questions[self.idx]
        correct = q["answer"]
        is_correct = selected == correct

        # ボタン色更新
        for btn in self.choice_frame.winfo_children():
            txt = btn.cget("text")
            if txt == correct:
                btn.config(bg=COLOR_GREEN, fg=COLOR_WHITE)
            elif txt == selected and not is_correct:
                btn.config(bg=COLOR_RED, fg=COLOR_WHITE)
            btn.config(state="disabled", cursor="arrow")

        # 解説
        icon = "✅ 正解！" if is_correct else "❌ 不正解"
        exp_text = f"{icon}\n\n{q.get('explanation', '')}"
        self.exp_label.config(text=exp_text,
                              bg=COLOR_GREEN if is_correct else COLOR_RED)
        self.exp_label.pack(fill="x", pady=(12, 8))
        self.next_btn.pack(anchor="e", pady=(0, 8))

        if is_correct:
            self.score += 1
        else:
            self.wrong_list.append(q)
            self._update_wrong_tab()
            # ノートへ自動追加
            self._auto_add_note(q)

        # 履歴保存
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mode": self.mode,
            "question": q["question"],
            "answer": correct,
            "selected": selected,
            "correct": is_correct,
            "choices": q.get("choices", []),
            "explanation": q.get("explanation", ""),
            "category": q.get("category", ""),
        }
        history = load_json(HISTORY_FILE)
        history.append(record)
        save_json(HISTORY_FILE, history)
        self.master.history_records = history

    def _next_question(self):
        self.idx += 1
        if self.idx >= self.total:
            self._show_result()
        else:
            self._show_question()

    def _show_result(self):
        for w in self.winfo_children():
            w.destroy()
        ResultScreen(self.master, self.score, self.total, self.wrong_list, self.mode)

    def _update_wrong_tab(self):
        n = len(self.wrong_list)
        self.wrong_tab_label.config(text=f"❌ 間違い: {n}問")
        # リスト再描画
        for w in self.wrong_list_frame.winfo_children():
            w.destroy()
        for q in self.wrong_list:
            tk.Label(self.wrong_list_frame,
                     text=f"• {q['question'][:40]}…  → 答: {q['answer']}",
                     font=FONT_SMALL, bg=BG_CARD, fg=COLOR_WHITE,
                     anchor="w", padx=10, pady=3).pack(fill="x")

    def _toggle_wrong_list(self, event=None):
        if self.wrong_list_frame.winfo_ismapped():
            self.wrong_list_frame.pack_forget()
        else:
            self.wrong_list_frame.pack(fill="x")

    def _auto_add_note(self, q):
        notes = load_json(NOTES_FILE)
        # 重複チェック
        for n in notes:
            if n.get("question") == q["question"]:
                return
        notes.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "question": q["question"],
            "answer": q["answer"],
            "explanation": q.get("explanation", ""),
            "category": q.get("category", ""),
            "memo": "",
        })
        save_json(NOTES_FILE, notes)
        self.master.notes = notes

# ==============================
# 結果画面
# ==============================
class ResultScreen(tk.Frame):
    def __init__(self, master, score, total, wrong_list, mode):
        super().__init__(master, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self.score = score
        self.total = total
        self.wrong_list = wrong_list
        self.mode = mode
        self._build()

    def _build(self):
        pct = int(self.score / self.total * 100) if self.total else 0
        stars = "⭐" * min(5, max(1, pct // 20))
        result_color = COLOR_GREEN if pct >= 70 else COLOR_GOLD if pct >= 40 else COLOR_RED

        tk.Label(self, text="結果発表", font=FONT_TITLE,
                 bg=BG_MAIN, fg=COLOR_GOLD).pack(pady=(50, 10))
        tk.Label(self, text=f"{self.score} / {self.total}  ({pct}%)",
                 font=("Georgia", 36, "bold"), bg=BG_MAIN, fg=result_color).pack()
        tk.Label(self, text=stars, font=("Arial", 28),
                 bg=BG_MAIN, fg=COLOR_GOLD).pack(pady=10)

        msg = ("完璧！素晴らしい！🎉" if pct == 100 else
               "よくできました！😊" if pct >= 70 else
               "もう少しで合格！💪" if pct >= 40 else
               "復習しよう！📚")
        tk.Label(self, text=msg, font=FONT_HEAD, bg=BG_MAIN, fg=COLOR_WHITE).pack(pady=6)

        # 間違い一覧
        if self.wrong_list:
            tk.Label(self, text="── 間違えた問題 ──",
                     font=FONT_SMALL, bg=BG_MAIN, fg=COLOR_GRAY).pack(pady=(20, 6))
            canvas = tk.Canvas(self, bg=BG_CARD, height=160, highlightthickness=0)
            sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y", padx=(0, 40))
            canvas.pack(fill="x", padx=60)
            inner = tk.Frame(canvas, bg=BG_CARD)
            canvas.create_window((0, 0), window=inner, anchor="nw")
            for q in self.wrong_list:
                tk.Label(inner,
                         text=f"❌  {q['question'][:55]}　→ {q['answer']}",
                         font=FONT_SMALL, bg=BG_CARD, fg=COLOR_WHITE,
                         anchor="w", padx=12, pady=4).pack(fill="x")
            inner.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        # ボタン
        btn_frame = tk.Frame(self, bg=BG_MAIN)
        btn_frame.pack(pady=30)

        def make_btn(text, cmd, bg=BG_ACCENT, fg=COLOR_WHITE):
            tk.Button(btn_frame, text=text, font=FONT_BTN, bg=bg, fg=fg, bd=0,
                      padx=20, pady=10, cursor="hand2",
                      activebackground=COLOR_GOLD, activeforeground=BG_MAIN,
                      command=cmd).pack(side="left", padx=8)

        make_btn("🔄 同じモードで再挑戦", lambda: self.master._show_quiz(self.mode),
                 COLOR_GOLD, COLOR_BTN_FG)
        make_btn("📝 ノートを見る", self.master._show_notes)
        make_btn("🏠 ホームへ", self.master._show_home)

# ==============================
# 履歴画面
# ==============================
class HistoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self.records = load_json(HISTORY_FILE)
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_ACCENT)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← ホーム", font=FONT_SMALL, bg=BG_ACCENT,
                  fg=COLOR_WHITE, bd=0, padx=12, pady=6, cursor="hand2",
                  activebackground=COLOR_GOLD, activeforeground=BG_MAIN,
                  command=self.master._show_home).pack(side="left", padx=8, pady=6)
        tk.Label(hdr, text="📋 解答履歴", font=FONT_HEAD,
                 bg=BG_ACCENT, fg=COLOR_GOLD).pack(side="left")

        if not self.records:
            tk.Label(self, text="まだ解答履歴がありません。", font=FONT_BODY,
                     bg=BG_MAIN, fg=COLOR_GRAY).pack(pady=60)
            return

        # 統計
        total = len(self.records)
        correct = sum(1 for r in self.records if r["correct"])
        tk.Label(self, text=f"総問数: {total}問 　✅ 正解: {correct}問 　❌ 不正解: {total - correct}問",
                 font=FONT_BODY, bg=BG_MAIN, fg=COLOR_WHITE).pack(pady=12)

        # テーブル
        cols = ("日時", "モード", "問題", "答え", "選択", "結果")
        frame = tk.Frame(self, bg=BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        style = ttk.Style()
        style.configure("Dark.Treeview", background=BG_CARD, fieldbackground=BG_CARD,
                        foreground=COLOR_WHITE, rowheight=28, font=FONT_SMALL)
        style.configure("Dark.Treeview.Heading", background=BG_ACCENT,
                        foreground=COLOR_GOLD, font=FONT_SMALL)
        style.map("Dark.Treeview", background=[("selected", "#2d4a7a")])

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="Dark.Treeview", height=18)
        sb = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        widths = [120, 120, 280, 140, 140, 60]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if col in ("モード", "結果") else "w")

        for r in reversed(self.records):
            result = "✅" if r["correct"] else "❌"
            tree.insert("", "end", values=(
                r.get("date", ""),
                r.get("mode", ""),
                r.get("question", "")[:35],
                r.get("answer", ""),
                r.get("selected", ""),
                result,
            ))

        # クリアボタン
        tk.Button(self, text="🗑 履歴を全消去", font=FONT_SMALL, bg=COLOR_RED,
                  fg=COLOR_WHITE, bd=0, padx=14, pady=6, cursor="hand2",
                  command=self._clear_history).pack(pady=8)

    def _clear_history(self):
        if messagebox.askyesno("確認", "履歴をすべて消去しますか？"):
            save_json(HISTORY_FILE, [])
            self.master.history_records = []
            self.master._show_history()

# ==============================
# ノート画面
# ==============================
class NotesScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self.notes = load_json(NOTES_FILE)
        self.selected_idx = None
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_ACCENT)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← ホーム", font=FONT_SMALL, bg=BG_ACCENT,
                  fg=COLOR_WHITE, bd=0, padx=12, pady=6, cursor="hand2",
                  activebackground=COLOR_GOLD, activeforeground=BG_MAIN,
                  command=self.master._show_home).pack(side="left", padx=8, pady=6)
        tk.Label(hdr, text="📝 ノート（間違い問題まとめ）", font=FONT_HEAD,
                 bg=BG_ACCENT, fg=COLOR_GOLD).pack(side="left")
        tk.Button(hdr, text="＋ 手動追加", font=FONT_SMALL, bg=COLOR_GOLD,
                  fg=COLOR_BTN_FG, bd=0, padx=12, pady=4, cursor="hand2",
                  command=self._add_manual).pack(side="right", padx=8, pady=6)

        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # 左: ノート一覧
        left = tk.Frame(main, bg=BG_CARD, width=300)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(left, text="ノート一覧", font=FONT_SMALL,
                 bg=BG_CARD, fg=COLOR_GOLD).pack(pady=8)

        self.listbox = tk.Listbox(left, bg=BG_CARD, fg=COLOR_WHITE,
                                  selectbackground=BG_ACCENT, font=FONT_SMALL,
                                  bd=0, highlightthickness=0, activestyle="none")
        sb_l = tk.Scrollbar(left, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb_l.set)
        sb_l.pack(side="right", fill="y")
        self.listbox.pack(fill="both", expand=True, padx=6, pady=(0, 8))
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # 右: 詳細・メモ編集
        right = tk.Frame(main, bg=BG_MAIN)
        right.pack(side="left", fill="both", expand=True)

        self.detail_q = tk.Label(right, text="", font=FONT_HEAD, wraplength=520,
                                 bg=BG_MAIN, fg=COLOR_WHITE, justify="left", anchor="w")
        self.detail_q.pack(anchor="w", pady=(0, 6))

        self.detail_a = tk.Label(right, text="", font=FONT_BODY, wraplength=520,
                                 bg=BG_MAIN, fg=COLOR_GOLD, justify="left", anchor="w")
        self.detail_a.pack(anchor="w", pady=(0, 6))

        self.detail_exp = tk.Label(right, text="", font=FONT_SMALL, wraplength=520,
                                   bg=BG_CARD, fg=COLOR_WHITE, justify="left",
                                   padx=12, pady=10, anchor="w")
        self.detail_exp.pack(fill="x", pady=(0, 10))

        tk.Label(right, text="📌 自分のメモ", font=FONT_SMALL,
                 bg=BG_MAIN, fg=COLOR_GRAY).pack(anchor="w")
        self.memo_text = scrolledtext.ScrolledText(right, font=FONT_SMALL,
                                                   bg=BG_CARD, fg=COLOR_WHITE,
                                                   insertbackground=COLOR_WHITE,
                                                   height=5, wrap="word", bd=0)
        self.memo_text.pack(fill="x", pady=6)

        btn_row = tk.Frame(right, bg=BG_MAIN)
        btn_row.pack(anchor="w", pady=6)
        tk.Button(btn_row, text="💾 メモを保存", font=FONT_SMALL, bg=COLOR_GOLD,
                  fg=COLOR_BTN_FG, bd=0, padx=14, pady=6, cursor="hand2",
                  command=self._save_memo).pack(side="left", padx=(0, 8))
        tk.Button(btn_row, text="🗑 このノートを削除", font=FONT_SMALL, bg=COLOR_RED,
                  fg=COLOR_WHITE, bd=0, padx=14, pady=6, cursor="hand2",
                  command=self._delete_note).pack(side="left")

        self._refresh_list()

    def _refresh_list(self):
        self.listbox.delete(0, "end")
        if not self.notes:
            self.listbox.insert("end", "（ノートが空です）")
        for n in self.notes:
            self.listbox.insert("end", f"  {n.get('category','')}: {n['question'][:28]}…")

    def _on_select(self, event):
        sel = self.listbox.curselection()
        if not sel or not self.notes:
            return
        self.selected_idx = sel[0]
        n = self.notes[self.selected_idx]
        self.detail_q.config(text=f"Q: {n['question']}")
        self.detail_a.config(text=f"答え: {n['answer']}")
        self.detail_exp.config(text=n.get("explanation", ""))
        self.memo_text.delete("1.0", "end")
        self.memo_text.insert("1.0", n.get("memo", ""))

    def _save_memo(self):
        if self.selected_idx is None:
            return
        self.notes[self.selected_idx]["memo"] = self.memo_text.get("1.0", "end").strip()
        save_json(NOTES_FILE, self.notes)
        messagebox.showinfo("保存", "メモを保存しました！")

    def _delete_note(self):
        if self.selected_idx is None:
            return
        if messagebox.askyesno("確認", "このノートを削除しますか？"):
            self.notes.pop(self.selected_idx)
            save_json(NOTES_FILE, self.notes)
            self.selected_idx = None
            self._refresh_list()
            self.detail_q.config(text="")
            self.detail_a.config(text="")
            self.detail_exp.config(text="")
            self.memo_text.delete("1.0", "end")

    def _add_manual(self):
        win = tk.Toplevel(self)
        win.title("ノートを手動追加")
        win.configure(bg=BG_MAIN)
        win.geometry("480x380")

        def row(label):
            tk.Label(win, text=label, font=FONT_SMALL, bg=BG_MAIN, fg=COLOR_GOLD
                     ).pack(anchor="w", padx=20, pady=(10, 2))

        row("問題文")
        q_entry = tk.Entry(win, font=FONT_BODY, bg=BG_CARD, fg=COLOR_WHITE,
                           insertbackground=COLOR_WHITE, bd=0)
        q_entry.pack(fill="x", padx=20)

        row("答え")
        a_entry = tk.Entry(win, font=FONT_BODY, bg=BG_CARD, fg=COLOR_WHITE,
                           insertbackground=COLOR_WHITE, bd=0)
        a_entry.pack(fill="x", padx=20)

        row("説明・解説")
        e_entry = scrolledtext.ScrolledText(win, font=FONT_SMALL, bg=BG_CARD,
                                            fg=COLOR_WHITE, insertbackground=COLOR_WHITE,
                                            height=4, wrap="word", bd=0)
        e_entry.pack(fill="x", padx=20)

        row("カテゴリ（任意）")
        c_entry = tk.Entry(win, font=FONT_BODY, bg=BG_CARD, fg=COLOR_WHITE,
                           insertbackground=COLOR_WHITE, bd=0)
        c_entry.pack(fill="x", padx=20)

        def save():
            note = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "question": q_entry.get().strip(),
                "answer": a_entry.get().strip(),
                "explanation": e_entry.get("1.0", "end").strip(),
                "category": c_entry.get().strip(),
                "memo": "",
            }
            if not note["question"]:
                messagebox.showwarning("入力エラー", "問題文を入力してください。")
                return
            self.notes.append(note)
            save_json(NOTES_FILE, self.notes)
            self._refresh_list()
            win.destroy()

        tk.Button(win, text="💾 追加", font=FONT_BTN, bg=COLOR_GOLD, fg=COLOR_BTN_FG,
                  bd=0, padx=20, pady=8, cursor="hand2", command=save).pack(pady=12)

# ==============================
# 起動
# ==============================
if __name__ == "__main__":
    app = HistoryQuizApp()
    app.mainloop()