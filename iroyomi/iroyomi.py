import sys
import random
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
)
from PySide6.QtGui import QFont, QColor
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
        self.setWindowTitle("色読み")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # メインのレイアウトとしてグリッドレイアウトを設定
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.populate_grid()

    def populate_grid(self):
        """
        グリッドに色と文字が一致しないようにランダムなラベルを配置する
        """
        kanji_list = list(KANJI_COLORS.keys())

        # フォントサイズをセルの高さに基づいて動的に計算
        # ウィンドウの高さを行数で割り、セルの高さを算出
        # その高さの約半分をフォントのピクセルサイズとする
        cell_height = self.height() / ROWS
        font_pixel_size = int(cell_height * 0.5)

        font = QFont()
        font.setPointSize(font_pixel_size)
        font.setBold(True)

        for row in range(ROWS):
            for col in range(COLS):
                # 1. 表示する文字をランダムに選択
                display_kanji = random.choice(kanji_list)

                # 2. 表示する色をランダムに選択（ただし、文字の意味と一致しないように）
                #    色の候補リストから、表示する文字を除外する
                possible_colors = [k for k in kanji_list if k != display_kanji]
                color_kanji = random.choice(possible_colors)
                color_name = KANJI_COLORS[color_kanji]

                # 3. ラベルを作成して設定
                label = QLabel(display_kanji)
                label.setFont(font)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # 4. スタイルシートで文字色を設定
                label.setStyleSheet(f"color: {color_name};")

                # 5. グリッドレイアウトにラベルを追加
                self.grid_layout.addWidget(label, row, col)


if __name__ == "__main__":
    # PySide6アプリケーションの実行
    app = QApplication(sys.argv)
    window = IroyomiWindow()
    window.show()
    sys.exit(app.exec())