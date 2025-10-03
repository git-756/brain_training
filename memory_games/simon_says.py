import sys
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# --- 定数設定 ---
COLORS = {
    "green":  {"normal": "#34a853", "light": "#81c995", "jp": "緑"},
    "red":    {"normal": "#ea4335", "light": "#f28b82", "jp": "赤"},
    "yellow": {"normal": "#fbbc05", "light": "#fdd663", "jp": "黄"},
    "blue":   {"normal": "#4285f4", "light": "#8ab4f8", "jp": "青"},
}
FLASH_DURATION = 400
LEVEL_DELAY = 1000

class SimonGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("パターン記憶ゲーム (修正版)")
        self.setFixedSize(400, 500)

        # --- ゲームの状態管理用変数 ---
        self.sequence = []
        self.player_input = []
        self.player_sequence_pos = 0
        self.is_player_turn = False
        self.buttons = {}

        # --- UIのセットアップ ---
        main_layout = QVBoxLayout()
        
        self.status_label = QLabel("スタートボタンを押してください")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        font = self.status_label.font()
        font.setPointSize(14)
        self.status_label.setFont(font)
        
        grid_layout = QGridLayout()
        
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        color_names = list(COLORS.keys())
        for i, pos in enumerate(positions):
            color = color_names[i]
            button = QPushButton()
            button.setMinimumSize(150, 150)
            button.setStyleSheet(f"background-color: {COLORS[color]['normal']}; border-radius: 10px;")
            
            # <<< ここを修正 >>>
            button.clicked.connect(lambda checked=False, c=color: self.on_color_button_clicked(c))
            
            self.buttons[color] = button
            grid_layout.addWidget(button, pos[0], pos[1])

        self.start_button = QPushButton("スタート")
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.start_game)

        main_layout.addWidget(self.status_label)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.start_button)
        self.setLayout(main_layout)

    def start_game(self):
        self.sequence = []
        self.player_input = []
        self.start_button.setEnabled(False)
        self.next_level()

    def next_level(self):
        self.is_player_turn = False
        self.player_sequence_pos = 0
        self.player_input = []
        new_color = random.choice(list(COLORS.keys()))
        self.sequence.append(new_color)
        
        self.status_label.setText(f"覚えてください: レベル {len(self.sequence)}")
        
        for button in self.buttons.values():
            button.setEnabled(False)

        QTimer.singleShot(500, self.play_sequence)

    def play_sequence(self):
        self._flash_index = 0
        self.flash_color()

    def flash_color(self):
        if self._flash_index < len(self.sequence):
            color = self.sequence[self._flash_index]
            button = self.buttons[color]
            
            button.setStyleSheet(f"background-color: {COLORS[color]['light']}; border-radius: 10px;")
            QTimer.singleShot(FLASH_DURATION, lambda b=button, c=color: b.setStyleSheet(f"background-color: {COLORS[c]['normal']}; border-radius: 10px;"))
            
            self._flash_index += 1
            QTimer.singleShot(FLASH_DURATION * 2, self.flash_color)
        else:
            self.is_player_turn = True
            self.status_label.setText("あなたの番です")
            for button in self.buttons.values():
                button.setEnabled(True)

    def on_color_button_clicked(self, color):
        if not self.is_player_turn:
            return

        self.player_input.append(color)

        if color == self.sequence[self.player_sequence_pos]:
            self.player_sequence_pos += 1
            if self.player_sequence_pos == len(self.sequence):
                self.status_label.setText("正解！")
                QTimer.singleShot(LEVEL_DELAY, self.next_level)
        else:
            self.game_over()

    def game_over(self):
        self.is_player_turn = False
        
        correct_str = " → ".join([COLORS[c]['jp'] for c in self.sequence])
        your_input_str = " → ".join([COLORS[c]['jp'] for c in self.player_input])
        
        final_level = len(self.sequence) -1
        
        message = (f"ゲームオーバー！ (スコア: {final_level})\n\n"
                   f"正解: {correct_str}\n"
                   f"あなたの入力: {your_input_str}")
                   
        self.status_label.setText(message)
        self.start_button.setEnabled(True)
        self.start_button.setText("もう一度挑戦")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SimonGame()
    game.show()
    sys.exit(app.exec())