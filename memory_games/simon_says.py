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
FLASH_DURATION = 400  # コンピュータの点灯時間
CLICK_FEEDBACK_DURATION = 150 # プレイヤーのクリック時の点灯時間
LEVEL_DELAY = 1000

class SimonGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("パターン記憶ゲーム (v3)")
        self.setFixedSize(400, 500)

        self.sequence = []
        self.player_input = []
        self.player_sequence_pos = 0
        self.is_player_turn = False
        self.buttons = {}

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
            # <<< 変更: スタイルに 'border: none' を追加
            button.setStyleSheet(f"background-color: {COLORS[color]['normal']}; border-radius: 10px; border: none;")
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
        self.flash_color_in_sequence()

    def flash_color_in_sequence(self):
        """コンピュータのシーケンスを1つずつ点灯させる"""
        if self._flash_index < len(self.sequence):
            color = self.sequence[self._flash_index]
            self.flash_button(color, FLASH_DURATION) # <<< 変更: 共通の点灯メソッドを呼ぶ
            
            self._flash_index += 1
            QTimer.singleShot(FLASH_DURATION * 2, self.flash_color_in_sequence)
        else:
            self.is_player_turn = True
            self.status_label.setText("あなたの番です")
            for button in self.buttons.values():
                button.setEnabled(True)

    def on_color_button_clicked(self, color):
        if not self.is_player_turn:
            return

        self.flash_button(color, CLICK_FEEDBACK_DURATION) # <<< 追加: クリックフィードバック
        self.player_input.append(color)

        if color == self.sequence[self.player_sequence_pos]:
            self.player_sequence_pos += 1
            if self.player_sequence_pos == len(self.sequence):
                self.status_label.setText("正解！")
                self.is_player_turn = False # <<< 追加: 次のレベルに行くまで入力を無効化
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
        
    def flash_button(self, color, duration):
        """ <<< 新設: ボタンを点灯させる共通メソッド >>> """
        button = self.buttons[color]
        normal_style = f"background-color: {COLORS[color]['normal']}; border-radius: 10px; border: none;"
        # 点灯時のスタイルに太い白枠を追加
        light_style = f"background-color: {COLORS[color]['light']}; border-radius: 10px; border: 4px solid white;"
        
        button.setStyleSheet(light_style)
        QTimer.singleShot(duration, lambda: button.setStyleSheet(normal_style))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SimonGame()
    game.show()
    sys.exit(app.exec())