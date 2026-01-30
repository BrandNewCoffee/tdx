import tkinter as tk
from tkinter import messagebox
import random

# 答案庫（用於隨機選擇答案）
ANSWER_WORDS = [
    'APPLE', 'BRAIN', 'CHAIR', 'DANCE', 'EAGLE', 'FLAME', 'GRACE', 'HEART', 'IMAGE', 'JUDGE',
    'KNIFE', 'LIGHT', 'MOUSE', 'NOBLE', 'OCEAN', 'PAINT', 'QUEST', 'RIVER', 'STONE', 'TABLE',
    'UNDER', 'VALVE', 'WATER', 'XENON', 'YOUTH', 'ZEBRA', 'ABOUT', 'BEACH', 'CROWN', 'DREAM',
    'FIELD', 'GIANT', 'HOUSE', 'JOINT', 'LAUGH', 'MUSIC', 'NIGHT', 'ORBIT', 'PHONE', 'QUIET',
    'RIGHT', 'SMART', 'THINK', 'VALID', 'WHALE', 'YIELD', 'ANGEL', 'BLEND', 'CLIMB', 'DEPTH'
]

# 選項庫（擴充的單詞庫，與答案庫錯開，用於右側選項，確保涵蓋所有 26 個字母）
OPTION_WORDS = [
    'ANGRY', 'BLAZE', 'CHARM', 'DEBUT', 'EVOKE', 'FLOOD', 'GRAFT', 'HELLO', 'IVORY', 'JOKER',
    'KNOWN', 'LOCAL', 'MAGIC', 'NICHE', 'OFFER', 'PLUMB', 'QUAKE', 'ROCKY', 'SEVEN', 'TOWER',
    'URBAN', 'VIRUS', 'WORLD', 'YACHT', 'ZEBRA', 'ADMIN', 'BONUS', 'CHEEK', 'DIRGE', 'EMPTY',
    'FAINT', 'GLOBE', 'HABIT', 'INPUT', 'JEANS', 'KARMA', 'LEGAL', 'MAPLE', 'NAILS', 'ORBIT',
    'PLANK', 'QUEEN', 'RANCH', 'SAUCE', 'TOAST', 'ULTRA', 'VENOM', 'WRIST', 'YANKS', 'ZIPPY',
    'ASTER', 'BOXER', 'CRAFT', 'DYING', 'EASEL', 'FLYER', 'GRAZE', 'HAPPY', 'ICING', 'JAZZY',
    'KIOSK', 'LEMON', 'MIXER', 'NOBLE', 'OZONE', 'POKER', 'QUIRK', 'RISKY', 'SUNNY', 'TOXIC',
    'UNZIP', 'VIVID', 'WEARY', 'YACHT', 'ZEBRA'
]

# 顏色設定
BG_EMPTY = '#d1d5db'   # 未填滿格子淺灰
BG_FILLED = '#ffffff'  # 已填字白
BG_GRAY = '#9aa0a6'    # 錯誤灰
BG_YELLOW = '#f5c137'  # 黃
BG_GREEN = '#6aaa64'   # 綠
OPTION_BG = '#ffffff'
OPTION_USED_BG = BG_GRAY

class WordleGUI:
    def __init__(self, master):
        self.master = master
        master.title('Wordle - 單詞選擇版')
        self.answer = random.choice(ANSWER_WORDS)
        self.board = [['' for _ in range(5)] for _ in range(6)]
        self.colors = [['empty' for _ in range(5)] for _ in range(6)]
        self.current_row = 0
        self.current_col = 0  # 用於第 6 排手動輸入
        self.game_over = False
        self.used_words = set()  # 追蹤已使用過的選項單詞

        self.setup_ui()
        self.master.bind('<Key>', self.on_key)

    def setup_ui(self):
        # 主區域
        main = tk.Frame(self.master, padx=12, pady=12)
        main.pack()

        top = tk.Frame(main)
        top.pack(side=tk.LEFT)

        title = tk.Label(top, text='WORDLE', font=('Helvetica', 20, 'bold'))
        title.pack(pady=(0, 8))

        # board
        self.tiles = []
        board_frame = tk.Frame(top)
        board_frame.pack()
        for r in range(6):
            row_frame = tk.Frame(board_frame)
            row_frame.pack(pady=4)
            row_tiles = []
            for c in range(5):
                lbl = tk.Label(row_frame, text='', width=4, height=2, relief='ridge',
                               bg=BG_EMPTY, font=('Helvetica', 20, 'bold'))
                lbl.pack(side=tk.LEFT, padx=4)
                row_tiles.append(lbl)
            self.tiles.append(row_tiles)

        ctrl = tk.Frame(top, pady=8)
        ctrl.pack()
        self.status_lbl = tk.Label(ctrl, text='', font=('Helvetica', 12))
        self.status_lbl.pack(side=tk.LEFT, padx=(0, 12))
        restart_btn = tk.Button(ctrl, text='重新開始', command=self.restart)
        restart_btn.pack(side=tk.LEFT)

        # 右側單詞選項
        side = tk.Frame(main, padx=16)
        side.pack(side=tk.LEFT, anchor='n')
        ktitle = tk.Label(side, text='單詞選項', font=('Helvetica', 14))
        ktitle.pack()
        options_frame = tk.Frame(side, pady=8)
        options_frame.pack()

        self.option_labels = {}
        # 每次遊戲隨機選擇 20 個選項單詞（從選項庫中），確保包含所有 26 個字母
        available_options = [w for w in OPTION_WORDS if w != self.answer]
        self.current_options = self._select_options_with_all_letters(available_options, 20)

        # 5 欄排列，適合 20 個選項（4 列 × 5 欄）
        cols = 5
        idx = 0
        for i, word in enumerate(self.current_options):
            r = i // cols
            c = i % cols
            if c == 0:
                rowf = tk.Frame(options_frame)
                rowf.pack()
            lbl = tk.Label(rowf, text=word, width=7, height=1, bg=OPTION_BG, relief='raised',
                           font=('Helvetica', 9, 'bold'), cursor='hand2')
            lbl.pack(side=tk.LEFT, padx=2, pady=2)
            lbl.bind('<Button-1>', lambda e, w=word: self.on_word_click(w))
            self.option_labels[word] = lbl

        hint = tk.Label(side, text='點擊單詞以提交', font=('Helvetica', 9), fg='#555')
        hint.pack(pady=(8, 0))
        # 字母表（顯示 A~Z，已出現的字母會變灰）
        alpha_frame = tk.Frame(side, pady=8)
        alpha_frame.pack()
        self.alpha_labels = {}
        alpha_cols = 7
        letters = [chr(ord('A') + i) for i in range(26)]
        for i, ch in enumerate(letters):
            if i % alpha_cols == 0:
                rowf = tk.Frame(alpha_frame)
                rowf.pack()
            albl = tk.Label(rowf, text=ch, width=3, height=1, bg=OPTION_BG, relief='raised',
                            font=('Helvetica', 9, 'bold'))
            albl.pack(side=tk.LEFT, padx=2, pady=2)
            self.alpha_labels[ch] = albl

        # 規則說明
        rules_frame = tk.Frame(side, pady=12)
        rules_frame.pack()
        rules_title = tk.Label(rules_frame, text='規則', font=('Helvetica', 11, 'bold'))
        rules_title.pack()
        rules_text = tk.Label(rules_frame, text='行1~5：點擊右側單詞\n行6：手動輸入字母\n綠色：位置正確\n黃色：字母存在\n灰色：不在答案中',
                              font=('Helvetica', 8), fg='#555', justify=tk.LEFT)
        rules_text.pack()

        # 初始渲染
        self.render()

    def _select_options_with_all_letters(self, available_options, num_options):
        """選擇選項，確保包含所有 26 個字母"""
        all_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        selected = []
        covered_letters = set()

        # 首先挑選覆蓋缺少字母的單詞
        remaining = list(available_options)
        while remaining and len(covered_letters) < 26 and len(selected) < num_options:
            # 找到能覆蓋最多未覆蓋字母的單詞
            best_word = None
            best_score = -1
            for word in remaining:
                word_letters = set(word)
                new_letters = word_letters - covered_letters
                if len(new_letters) > best_score:
                    best_score = len(new_letters)
                    best_word = word
            
            if best_word:
                selected.append(best_word)
                covered_letters.update(set(best_word))
                remaining.remove(best_word)
        
        # 如果還需要更多選項，隨機添加剩餘單詞
        if len(selected) < num_options and remaining:
            additional = random.sample(remaining, min(num_options - len(selected), len(remaining)))
            selected.extend(additional)
        
        return selected[:num_options]

    def on_key(self, event):
        if self.game_over:
            return
        # 只有第 6 排（index 5）才支援手動輸入
        if self.current_row != 5:
            return
        key = event.keysym
        if key == 'Return':
            self.submit_manual_word()
        elif key == 'BackSpace':
            self.remove_letter()
        else:
            char = event.char.upper()
            if len(char) == 1 and 'A'<= char <= 'Z':
                self.add_letter(char)

    def add_letter(self, ch):
        if self.current_col < 5:
            self.board[self.current_row][self.current_col] = ch
            self.current_col += 1
            self.render_row(self.current_row)

    def remove_letter(self):
        if self.current_col > 0:
            self.current_col -= 1
            self.board[self.current_row][self.current_col] = ''
            self.render_row(self.current_row)

    def submit_manual_word(self):
        """提交手動輸入的單詞（第 6 排）"""
        if self.current_col < 5:
            self.status_lbl.config(text='請輸入完整五個字母')
            return
        guess = ''.join(self.board[self.current_row])
        self.submit_word(guess)

    def on_word_click(self, word):
        if self.game_over or self.current_row >= 6:
            return
        # 只有行 1~5 才支援點擊選擇（current_row 0~4）
        if self.current_row >= 5:
            return
        self.submit_word(word)

    def submit_word(self, word):
        """提交選定的單詞（行 1~5 選擇或行 6 手動輸入）"""
        if self.current_row >= 6:
            return

        # 更新當前行為該單詞
        word = word.upper()
        for c in range(5):
            self.board[self.current_row][c] = word[c]

        # 追蹤使用過的單詞（立即變灰）
        self.used_words.add(word)

        # 評分邏輯（綠色優先；黃色只要答案包含該字母即標示，不以次數限制）
        # 先設為灰
        for c in range(5):
            self.colors[self.current_row][c] = 'gray'

        # 綠色優先
        for c in range(5):
            g = self.board[self.current_row][c]
            if g == self.answer[c]:
                self.colors[self.current_row][c] = 'green'

        # 黃色：若此字母在答案任一位置出現（不受數量限制），且尚未標成綠色
        answer_letters = set(self.answer)
        for c in range(5):
            if self.colors[self.current_row][c] == 'gray':
                g = self.board[self.current_row][c]
                if g in answer_letters:
                    self.colors[self.current_row][c] = 'yellow'

        # 標記該列
        self.render_row(self.current_row)
        # 更新右側選項（已被猜過的單詞變灰）
        self.update_options()

        if word == self.answer:
            self.status_lbl.config(text=f'恭喜答對！答案：{self.answer}')
            self.game_over = True
            messagebox.showinfo('勝利', f'恭喜！你答對了：{self.answer}')
            return

        self.current_row += 1
        self.current_col = 0  # 重置列位置用於下一行
        if self.current_row >= 6:
            self.game_over = True
            self.status_lbl.config(text=f'遊戲結束，答案：{self.answer}')
            messagebox.showinfo('遊戲結束', f'遊戲結束，答案是：{self.answer}')
            return
        self.status_lbl.config(text='')

    def update_options(self):
        """更新右側選項按鈕的外觀"""
        for word, lbl in self.option_labels.items():
            if word in self.used_words:
                lbl.config(bg=OPTION_USED_BG, fg='#fff', relief='sunken')
            else:
                lbl.config(bg=OPTION_BG, fg='#000', relief='raised')
        # 同步更新字母表，若字母在任何已提交列中出現，該字母變灰
        self.update_alphabet()

    def update_alphabet(self):
        letters_used = set()
        # 檢查所有已評分的列（顏色不是 'empty'）
        for r in range(0, self.current_row + 1):
            row_submitted = any(self.colors[r][c] != 'empty' for c in range(5))
            if not row_submitted:
                continue
            for c in range(5):
                ch = self.board[r][c]
                if ch:
                    letters_used.add(ch.upper())

        for ch, lbl in self.alpha_labels.items():
            if ch in letters_used:
                lbl.config(bg=OPTION_USED_BG, fg='#fff', relief='sunken')
            else:
                lbl.config(bg=OPTION_BG, fg='#000', relief='raised')

    def render_row(self, r):
        for c in range(5):
            val = self.board[r][c]
            lbl = self.tiles[r][c]
            lbl.config(text=val)
            color = self.colors[r][c]
            if color == 'green':
                lbl.config(bg=BG_GREEN, fg='#000')
            elif color == 'yellow':
                lbl.config(bg=BG_YELLOW, fg='#000')
            elif color == 'gray':
                lbl.config(bg=BG_GRAY, fg='#fff')
            else:
                # empty
                lbl.config(bg=BG_EMPTY, fg='#000')

    def render(self):
        for r in range(6):
            for c in range(5):
                self.render_row(r)
        self.update_options()

    def restart(self):
        self.answer = random.choice(ANSWER_WORDS)
        self.board = [['' for _ in range(5)] for _ in range(6)]
        self.colors = [['empty' for _ in range(5)] for _ in range(6)]
        self.current_row = 0
        self.current_col = 0
        self.game_over = False
        self.used_words = set()
        self.status_lbl.config(text='')

        # 重新生成選項，確保包含所有 26 個字母
        available_options = [w for w in OPTION_WORDS if w != self.answer]
        self.current_options = self._select_options_with_all_letters(available_options, 20)

        self.render()

if __name__ == '__main__':
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()
