import sys
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# --- 定数設定 ---
# ボタンの色と、点灯時の明るい色の定義
COLORS = {
    "green":  {"normal": "#34a853", "light": "#81c995"},
    "red":    {"normal": "#ea4335", "light": "#f28b82"},
    "yellow": {"normal": "#fbbc05", "light": "#fdd663"},
    "blue":   {"normal": "#4285f4", "light": "#8ab4f8"},
}
# ボタンの点灯時間 (ミリ秒)
FLASH_DURATION = 400
# 次のレベルに進むまでの待ち時間 (ミリ秒)
LEVEL_DELAY = 1000

class SimonGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("パターン記憶ゲーム")
        self.setFixedSize(400, 450)

        # --- ゲームの状態管理用変数 ---
        self.sequence = []          # コンピューターが生成した色の順番
        self.player_sequence_pos = 0 # プレイヤーが現在入力中の順番
        self.is_player_turn = False  # プレイヤーの入力受付中か
        self.buttons = {}           # 色の名前とボタンウィジェットを紐付ける辞書

        # --- UIのセットアップ ---
        main_layout = QVBoxLayout()
        
        # ステータス表示用ラベル
        self.status_label = QLabel("スタートボタンを押してください")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.status_label.font()
        font.setPointSize(14)
        self.status_label.setFont(font)
        
        # 色ボタンを配置するグリッドレイアウト
        grid_layout = QGridLayout()
        
        # 色ボタンの作成
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        color_names = list(COLORS.keys())
        for i, pos in enumerate(positions):
            color = color_names[i]
            button = QPushButton()
            button.setMinimumSize(150, 150)
            button.setStyleSheet(f"background-color: {COLORS[color]['normal']}; border-radius: 10px;")
            # functools.partialの代わりにlambdaを使ってクリック時の色を渡す
            button.clicked.connect(lambda c=color: self.on_color_button_clicked(c))
            self.buttons[color] = button
            grid_layout.addWidget(button, pos[0], pos[1])

        # スタートボタン
        self.start_button = QPushButton("スタート")
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.start_game)

        # レイアウトの組み立て
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.start_button)
        self.setLayout(main_layout)

    def start_game(self):
        """ゲームを開始またはリセットする"""
        self.sequence = []
        self.start_button.setEnabled(False)
        self.status_label.setText("レベル 1")
        self.next_level()

    def next_level(self):
        """新しい色をシーケンスに追加し、再生する"""
        self.is_player_turn = False
        self.player_sequence_pos = 0
        # ランダムな色をシーケンスに追加
        new_color = random.choice(list(COLORS.keys()))
        self.sequence.append(new_color)
        
        self.status_label.setText(f"レベル {len(self.sequence)}")
        
        # プレイヤーの操作を一旦無効化
        for button in self.buttons.values():
            button.setEnabled(False)

        # 0.5秒後にシーケンスの再生を開始
        QTimer.singleShot(500, self.play_sequence)

    def play_sequence(self):
        """シーケンスを順番に点灯させる"""
        self._flash_index = 0
        self._flash_timer = QTimer()
        self._flash_timer.setInterval(FLASH_DURATION * 2) # 点灯時間＋消灯時間
        self._flash_timer.timeout.connect(self.flash_next_color)
        self._flash_timer.start()
        self.flash_next_color() # 最初の色をすぐに点灯

    def flash_next_color(self):
        """シーケンスの次の色を点灯させる"""
        if self._flash_index < len(self.sequence):
            color = self.sequence[self._flash_index]
            button = self.buttons[color]
            
            # ボタンを明るい色にする
            button.setStyleSheet(f"background-color: {COLORS[color]['light']}; border-radius: 10px;")
            # 一定時間後に元の色に戻す
            QTimer.singleShot(FLASH_DURATION, lambda: button.setStyleSheet(f"background-color: {COLORS[color]['normal']}; border-radius: 10px;"))
            
            self._flash_index += 1
        else:
            # 再生終了
            self._flash_timer.stop()
            self.is_player_turn = True
            self.status_label.setText("あなたの番です")
            # プレイヤーの操作を有効化
            for button in self.buttons.values():
                button.setEnabled(True)

    def on_color_button_clicked(self, color):
        """色ボタンがクリックされたときの処理"""
        if not self.is_player_turn:
            return

        # 押されたボタンがシーケンスと一致しているかチェック
        if color == self.sequence[self.player_sequence_pos]:
            self.player_sequence_pos += 1
            # プレイヤーがシーケンスをすべて入力し終えたか
            if self.player_sequence_pos == len(self.sequence):
                self.status_label.setText("正解！")
                # 一定時間後に次のレベルへ
                QTimer.singleShot(LEVEL_DELAY, self.next_level)
        else:
            # 間違えた場合
            self.game_over()

    def game_over(self):
        """ゲームオーバー処理"""
        self.is_player_turn = False
        final_level = len(self.sequence) -1
        self.status_label.setText(f"ゲームオーバー！ スコア: {final_level}")
        self.start_button.setEnabled(True)
        self.start_button.setText("もう一度挑戦")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SimonGame()
    game.show()
    sys.exit(app.exec())