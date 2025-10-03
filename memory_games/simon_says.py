import sys
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout,
    QStackedWidget, QHBoxLayout
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
CLICK_FEEDBACK_DURATION = 150
LEVEL_DELAY = 1000

class SimonGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("パターン記憶ゲーム (v4)")
        self.setFixedSize(400, 500)

        self.sequence = []
        self.player_input = []
        self.player_sequence_pos = 0
        self.is_player_turn = False
        self.buttons = {}

        # --- 画面切り替えのためのStackedWidget ---
        self.stacked_widget = QStackedWidget()
        
        # ページを作成
        self.welcome_page = self.create_welcome_page()
        self.game_page = self.create_game_page()

        # StackedWidgetにページを追加
        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.game_page)

        # メインレイアウトにStackedWidgetを配置
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        
        self.stacked_widget.setCurrentIndex(0) # 最初にルール説明ページを表示

    def create_welcome_page(self):
        """ルール説明ページのUIを作成する"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title_font = QFont(); title_font.setPointSize(24); title_font.setBold(True)
        rule_font = QFont(); rule_font.setPointSize(14)
        button_font = QFont(); button_font.setPointSize(16)

        title_label = QLabel("パターン記憶ゲーム")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        rule_text = (
            "<h3>遊び方</h3>"
            "<p>光った色の順番を記憶し、<br>"
            "最初から同じ順番でクリックしてください。</p>"
            "<p>レベルが上がると、順番の最後に<br>"
            "新しい色が１つ追加されます。</p>"
        )
        rule_label = QLabel(rule_text)
        rule_label.setFont(rule_font)
        rule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rule_label.setWordWrap(True)

        start_game_button = QPushButton("ゲーム開始")
        start_game_button.setFont(button_font)
        start_game_button.setFixedSize(200, 50)
        start_game_button.clicked.connect(self.show_game_page_and_start)

        layout.addWidget(title_label)
        layout.addWidget(rule_label)
        layout.addWidget(start_game_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return page

    def create_game_page(self):
        """ゲーム画面のUIを作成する"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.status_label = QLabel("ステータス")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        font = self.status_label.font(); font.setPointSize(14)
        self.status_label.setFont(font)
        
        grid_layout = QGridLayout()
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        color_names = list(COLORS.keys())
        for i, pos in enumerate(positions):
            color = color_names[i]
            button = QPushButton()
            button.setMinimumSize(150, 150)
            button.setStyleSheet(f"background-color: {COLORS[color]['normal']}; border-radius: 10px; border: none;")
            button.clicked.connect(lambda checked=False, c=color: self.on_color_button_clicked(c))
            self.buttons[color] = button
            grid_layout.addWidget(button, pos[0], pos[1])

        # ゲームオーバー時のボタンを配置する水平レイアウト
        self.game_over_layout = QHBoxLayout()
        self.retry_button = QPushButton("もう一度挑戦")
        self.back_to_rules_button = QPushButton("ルールに戻る")
        self.retry_button.setFont(font)
        self.back_to_rules_button.setFont(font)
        self.retry_button.clicked.connect(self.start_game)
        self.back_to_rules_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.game_over_layout.addWidget(self.retry_button)
        self.game_over_layout.addWidget(self.back_to_rules_button)
        self.retry_button.hide(); self.back_to_rules_button.hide()

        layout.addWidget(self.status_label)
        layout.addLayout(grid_layout)
        layout.addLayout(self.game_over_layout)
        
        return page

    def show_game_page_and_start(self):
        """ゲームページに切り替えてゲームを開始する"""
        self.stacked_widget.setCurrentIndex(1)
        self.start_game()

    def start_game(self):
        self.retry_button.hide(); self.back_to_rules_button.hide()
        self.sequence = []
        self.player_input = []
        self.next_level()

    def next_level(self):
        # ... (next_level以降のメソッドは変更なし)
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
        if self._flash_index < len(self.sequence):
            color = self.sequence[self._flash_index]
            self.flash_button(color, FLASH_DURATION)
            
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

        self.flash_button(color, CLICK_FEEDBACK_DURATION)
        self.player_input.append(color)

        if color == self.sequence[self.player_sequence_pos]:
            self.player_sequence_pos += 1
            if self.player_sequence_pos == len(self.sequence):
                self.status_label.setText("正解！")
                self.is_player_turn = False
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
        self.retry_button.show()
        self.back_to_rules_button.show()
        
    def flash_button(self, color, duration):
        button = self.buttons[color]
        normal_style = f"background-color: {COLORS[color]['normal']}; border-radius: 10px; border: none;"
        light_style = f"background-color: {COLORS[color]['light']}; border-radius: 10px; border: 4px solid white;"
        
        button.setStyleSheet(light_style)
        QTimer.singleShot(duration, lambda: button.setStyleSheet(normal_style))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SimonGame()
    game.show()
    sys.exit(app.exec())