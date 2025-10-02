import sys
import random
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# --- 定数設定 ---
# 使用する漢字と色のマッピング
KANJI_COLORS = {
    "赤": "red",
    "青": "blue",
    "緑": "green",
    "黄": "yellow",
}

# グリッドの行数と列数
ROWS = 5
COLS = 6

# ウィンドウのサイズ (HD)
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


class IroyomiWindow(QWidget):
    """
    「色読み」トレーニング風の表示を行うメインウィンドウクラス
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("色読み (3連続防止版)")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.populate_grid()

    def populate_grid(self):
        """
        グリッドに色と文字が一致せず、かつ水平方向に同じ色が3連続しないように
        ランダムなラベルを配置する
        """
        kanji_list = list(KANJI_COLORS.keys())
        
        cell_height = self.height() / ROWS
        font_pixel_size = int(cell_height * 0.5)

        font = QFont()
        font.setPointSize(font_pixel_size)
        font.setBold(True)

        for row in range(ROWS):
            # <<< 変更点 >>> 行ごとに直前の色を記録するリストを初期化
            previous_colors = [] 
            
            for col in range(COLS):
                # 1. 表示する文字をランダムに選択
                display_kanji = random.choice(kanji_list)

                # 2. 色の候補リストを作成（文字の意味と一致しない色）
                allowed_colors = [k for k in kanji_list if k != display_kanji]

                # <<< 変更点 >>> 3連続を避けるためのロジック
                # 列が2つ以上進んでいて、かつ直前2つの色が同じ場合
                if len(previous_colors) >= 2 and previous_colors[-1] == previous_colors[-2]:
                    color_to_avoid = previous_colors[-1]
                    # 候補リストから、避けるべき色を削除
                    if color_to_avoid in allowed_colors:
                        allowed_colors.remove(color_to_avoid)
                
                # エッジケース対応: もし候補がなくなったら全候補から選ぶ
                if not allowed_colors:
                    allowed_colors = [k for k in kanji_list if k != display_kanji]


                # 3. 最終的な色を候補リストからランダムに選択
                color_kanji = random.choice(allowed_colors)
                color_name = KANJI_COLORS[color_kanji]
                
                # <<< 変更点 >>> 決定した色を記録リストに追加
                previous_colors.append(color_kanji)

                # 4. ラベルを作成して設定
                label = QLabel(display_kanji)
                label.setFont(font)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet(f"color: {color_name};")

                # 5. グリッドレイアウトにラベルを追加
                self.grid_layout.addWidget(label, row, col)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IroyomiWindow()
    window.show()
    sys.exit(app.exec())