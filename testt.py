import os
import sys

# ANSI 顏色代碼
RESET = '\033[0m'
GRAY_BG = '\033[40m'  # 黑色背景作為灰色
GRAY_TEXT = '\033[90m'  # 灰色文字
WHITE_TEXT = '\033[97m'  # 白色文字
YELLOW_BG = '\033[43m'  # 黃色背景
YELLOW_TEXT = '\033[33m'  # 黃色文字
GREEN_BG = '\033[42m'  # 綠色背景
GREEN_TEXT = '\033[32m'  # 綠色文字
BLACK_TEXT = '\033[30m'  # 黑色文字

class WordleGame:
    def __init__(self):
        # 預設答案列表
        self.word_list = [
            'APPLE', 'BRA'
            'IN', 'CHAIR', 'DANCE', 'EAGLE',
            'FLAME', 'GRACE', 'HEART', 'IMAGE', 'JUDGE',
            'KNIFE', 'LIGHT', 'MOUSE', 'NOBLE', 'OCEAN',
            'PAINT', 'QUEST', 'RIVER', 'STONE', 'TABLE',
            'UNDER', 'VALVE', 'WATER', 'XENON', 'YOUTH',
            'ZEBRA', 'ABOUT', 'BEACH', 'CROWN', 'DREAM'
        ]
        
        # 隨機選擇一個詞語作為答案
        import random
        self.answer = random.choice(self.word_list).upper()
        
        # 遊戲狀態
        self.board = [['' for _ in range(5)] for _ in range(6)]  # 遊戲板
        self.colors = [[0 for _ in range(5)] for _ in range(6)]  # 0: 灰色, 1: 黃色, 2: 綠色
        self.current_row = 0  # 當前行
        self.current_col = 0  # 當前列
        self.game_over = False
        self.won = False
        
    def clear_screen(self):
        """清除螢幕"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_board(self):
        """顯示遊戲板"""
        self.clear_screen()
        print("\n" + " " * 20 + "WORDLE 遊戲\n")
        
        for row in range(6):
            for col in range(5):
                letter = self.board[row][col]
                color = self.colors[row][col]
                
                # 根據顏色設置背景
                if row < self.current_row or (row == self.current_row and col < self.current_col):
                    # 已提交的格子
                    if color == 0:  # 灰色
                        bg = GRAY_BG
                        text_color = GRAY_TEXT
                    elif color == 1:  # 黃色
                        bg = YELLOW_BG
                        text_color = BLACK_TEXT
                    elif color == 2:  # 綠色
                        bg = GREEN_BG
                        text_color = BLACK_TEXT
                    print(f"{bg}{text_color} {letter} {RESET}", end=" ")
                elif row == self.current_row and col < self.current_col:
                    # 當前行已輸入的格子
                    print(f"{GRAY_BG}{WHITE_TEXT} {letter} {RESET}", end=" ")
                elif row == self.current_row and col == self.current_col:
                    # 當前游標位置
                    print(f"{GRAY_BG}{WHITE_TEXT} {letter} {RESET}", end=" ")
                else:
                    # 未使用的格子
                    print(f"{GRAY_BG}{GRAY_TEXT}   {RESET}", end=" ")
            print()
        
        print("\n" + "=" * 40)
        if self.won:
            print(f"🎉 恭喜！你答對了！答案是：{self.answer}")
        elif self.game_over:
            print(f"遊戲結束！答案是：{self.answer}")
        else:
            print(f"第 {self.current_row + 1} 排 / 6 排")
        print("=" * 40)
    
    def check_word(self):
        """檢查輸入的詞語"""
        guessed_word = ''.join(self.board[self.current_row]).upper()
        
        if guessed_word == self.answer:
            # 全部正確
            for col in range(5):
                self.colors[self.current_row][col] = 2  # 綠色
            self.won = True
            return True
        
        # 檢查每個字母
        answer_counts = {}
        for letter in self.answer:
            answer_counts[letter] = answer_counts.get(letter, 0) + 1
        
        # 先標記綠色
        for col in range(5):
            letter = self.board[self.current_row][col].upper()
            if letter == self.answer[col]:
                self.colors[self.current_row][col] = 2  # 綠色
                answer_counts[letter] -= 1
        
        # 再標記黃色
        for col in range(5):
            letter = self.board[self.current_row][col].upper()
            if self.colors[self.current_row][col] == 0:  # 還沒被標記
                if letter in answer_counts and answer_counts[letter] > 0:
                    self.colors[self.current_row][col] = 1  # 黃色
                    answer_counts[letter] -= 1
        
        return False
    
    def add_letter(self, letter):
        """添加字母"""
        if self.current_col < 5:
            self.board[self.current_row][self.current_col] = letter.upper()
            self.current_col += 1
    
    def remove_letter(self):
        """刪除字母"""
        if self.current_col > 0:
            self.current_col -= 1
            self.board[self.current_row][self.current_col] = ''
    
    def submit_word(self):
        """提交詞語"""
        if self.current_col < 5:
            print("請輸入完整的五個字母！")
            input("按 Enter 繼續...")
            return
        
        if self.check_word():
            self.game_over = True
            return
        
        # 移動到下一行
        self.current_row += 1
        self.current_col = 0
        
        if self.current_row >= 6:
            self.game_over = True
    
    def play(self):
        """遊戲主迴圈"""
        while not self.game_over:
            self.display_board()
            
            # 獲取使用者輸入
            try:
                # 在 Windows 上使用 msvcrt 來獲取單個字符
                import msvcrt
                
                while True:
                    key = msvcrt.getch().decode('utf-8', errors='ignore').upper()
                    
                    if key == '\r':  # Enter 鍵
                        self.submit_word()
                        break
                    elif key == '\x08':  # Backspace 鍵
                        self.remove_letter()
                        break
                    elif key.isalpha() and len(key) == 1:
                        self.add_letter(key)
                        break
                    elif key == '\x1b':  # Escape 鍵
                        print("遊戲已退出。")
                        return
                    
                    self.display_board()
            except ImportError:
                # 如果在非 Windows 系統上，使用替代方法
                self.display_board()
                user_input = input("輸入字母或按 Enter 提交 (Backspace 刪除, Esc 退出): ").upper()
                
                if user_input == '':
                    self.submit_word()
                elif user_input == 'BACKSPACE':
                    self.remove_letter()
                elif user_input == 'ESC':
                    print("遊戲已退出。")
                    return
                elif len(user_input) == 1 and user_input.isalpha():
                    self.add_letter(user_input)
        
        # 顯示最終結果
        self.display_board()
        print("\n遊戲結束！")


def main():
    """主程式入口"""
    print("歡迎來到 WORDLE 遊戲！")
    print("規則：")
    print("- 輸入五個英文字母")
    print("- 按 Enter 提交答案")
    print("- 綠色 = 正確位置")
    print("- 黃色 = 正確字母，錯誤位置")
    print("- 灰色 = 不在答案中")
    print("- 你有 6 次機會猜測")
    input("\n按 Enter 開始遊戲...")
    
    game = WordleGame()
    game.play()


if __name__ == "__main__":
    main()
