import tkinter as tk
from tkinter import messagebox
import random

WORDS = [
    'APPLE','BRAIN','CHAIR','DANCE','EAGLE','FLAME','GRACE','HEART','IMAGE','JUDGE',
    'KNIFE','LIGHT','MOUSE','NOBLE','OCEAN','PAINT','QUEST','RIVER','STONE','TABLE',
    'UNDER','VALVE','WATER','XENON','YOUTH','ZEBRA','ABOUT','BEACH','CROWN','DREAM'
]

# 顏色設定
BG_EMPTY = '#d1d5db'   # 未填滿格子淺灰
BG_FILLED = '#ffffff'  # 已填字白
BG_GRAY = '#9aa0a6'    # 錯誤灰
BG_YELLOW = '#f5c137'  # 黃
BG_GREEN = '#6aaa64'   # 綠
KEY_BG = '#ffffff'
KEY_USED_BG = BG_GRAY

class WordleGUI:
    def __init__(self, master):
        self.master = master
        master.title('Wordle - Python GUI')
        self.answer = random.choice(WORDS)
        self.board = [['' for _ in range(5)] for _ in range(6)]
        self.colors = [['empty' for _ in range(5)] for _ in range(6)]
        self.current_row = 0
        self.current_col = 0
        self.game_over = False

        self.setup_ui()
        master.bind('<Key>', self.on_key)

    def setup_ui(self):
        # 主區域
        main = tk.Frame(self.master, padx=12, pady=12)
        main.pack()

        top = tk.Frame(main)
        top.pack(side=tk.LEFT)

        title = tk.Label(top, text='WORDLE', font=('Helvetica', 20, 'bold'))
        title.pack(pady=(0,8))

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
        self.status_lbl.pack(side=tk.LEFT, padx=(0,12))
        restart_btn = tk.Button(ctrl, text='重新開始', command=self.restart)
        restart_btn.pack(side=tk.LEFT)

        # 右側鍵表
        side = tk.Frame(main, padx=16)
        side.pack(side=tk.LEFT, anchor='n')
        ktitle = tk.Label(side, text='字母表', font=('Helvetica', 14))
        ktitle.pack()
        keys_frame = tk.Frame(side, pady=8)
        keys_frame.pack()

        self.key_labels = {}
        letters = [chr(ord('A')+i) for i in range(26)]
        # 使用矩形排列：4 欄
        cols = 4
        rows = (len(letters) + cols - 1) // cols
        idx = 0
        for r in range(rows):
            rowf = tk.Frame(keys_frame)
            rowf.pack()
            for c in range(cols):
                if idx >= len(letters):
                    break
                ch = letters[idx]
                lbl = tk.Label(rowf, text=ch, width=3, height=1, bg=KEY_BG, relief='raised',
                               font=('Helvetica', 10, 'bold'))
                lbl.pack(side=tk.LEFT, padx=3, pady=3)
                lbl.bind('<Button-1>', lambda e, ch=ch: self.on_letter_click(ch))
                self.key_labels[ch] = lbl
                idx += 1

        hint = tk.Label(side, text='被猜過的字母會變灰', font=('Helvetica', 9), fg='#555')
        hint.pack(pady=(8,0))

        # 初始渲染
        self.render()

    def on_letter_click(self, ch):
        if self.game_over:
            return
        self.add_letter(ch)

    def on_key(self, event):
        if self.game_over:
            return
        key = event.keysym
        if key == 'Return':
            self.submit_word()
        elif key == 'BackSpace':
            self.remove_letter()
        else:
            char = event.char.upper()
            if len(char) == 1 and 'A' <= char <= 'Z':
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

    def submit_word(self):
        if self.current_col < 5:
            self.status_lbl.config(text='請輸入完整五個字母')
            return
        guess = ''.join(self.board[self.current_row])
        # 檢查與標記顏色
        answer_counts = {}
        for ch in self.answer:
            answer_counts[ch] = answer_counts.get(ch, 0) + 1
        # 先設為灰
        for c in range(5):
            self.colors[self.current_row][c] = 'gray'
        # 綠色優先
        for c in range(5):
            g = self.board[self.current_row][c]
            if g == self.answer[c]:
                self.colors[self.current_row][c] = 'green'
                answer_counts[g] -= 1
        # 黃色
        for c in range(5):
            g = self.board[self.current_row][c]
            if self.colors[self.current_row][c] == 'gray' and answer_counts.get(g,0) > 0:
                self.colors[self.current_row][c] = 'yellow'
                answer_counts[g] -= 1

        # 標記該列
        self.render_row(self.current_row)
        # 更新右側鍵表（已被猜過的字母變灰）
        self.update_keys()

        if guess == self.answer:
            self.status_lbl.config(text=f'恭喜答對！答案：{self.answer}')
            self.game_over = True
            messagebox.showinfo('勝利', f'恭喜！你答對了：{self.answer}')
            return
        self.current_row += 1
        self.current_col = 0
        if self.current_row >= 6:
            self.game_over = True
            self.status_lbl.config(text=f'遊戲結束，答案：{self.answer}')
            messagebox.showinfo('遊戲結束', f'遊戲結束，答案是：{self.answer}')
            return
        self.status_lbl.config(text='')

    def update_keys(self):
        # 若任一已提交行包含該字母, 將 key 變為 used
        for ch, lbl in self.key_labels.items():
            used = False
            # 檢查所有已提交的列：若該列已被評分（colors 不全為 'empty'）就視為已提交，
            # 包含剛送出但尚未 self.current_row+1 的那一列。
            for r in range(0, self.current_row + 1):
                # 判斷此列是否為已提交（有任何一格被標記為非 empty）
                row_submitted = any(self.colors[r][c] != 'empty' for c in range(5))
                if not row_submitted:
                    continue
                for c in range(5):
                    if self.board[r][c] == ch:
                        used = True
                        break
                if used:
                    break
            if used:
                lbl.config(bg=KEY_USED_BG, fg='#fff', relief='sunken')
            else:
                lbl.config(bg=KEY_BG, fg='#000', relief='raised')

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
                # 若該格是空的但在當前行輸入中，顯示 filled 背景
                if val == '' and r == self.current_row:
                    lbl.config(bg=BG_EMPTY, fg='#000')
                else:
                    lbl.config(bg=BG_GRAY, fg='#fff')
            else:
                # empty
                if val == '':
                    lbl.config(bg=BG_EMPTY, fg='#000')
                else:
                    lbl.config(bg=BG_FILLED, fg='#000')

    def render(self):
        for r in range(6):
            for c in range(5):
                self.render_row(r)
        self.update_keys()

    def restart(self):
        self.answer = random.choice(WORDS)
        self.board = [['' for _ in range(5)] for _ in range(6)]
        self.colors = [['empty' for _ in range(5)] for _ in range(6)]
        self.current_row = 0
        self.current_col = 0
        self.game_over = False
        self.status_lbl.config(text='')
        self.render()

if __name__ == '__main__':
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()
