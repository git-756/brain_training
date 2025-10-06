# Brain Training Games Collection 🧠

PythonとPySide6を使って作成した、さまざまな脳トレゲームのコレクションです。

## 🎮 ゲーム一覧

現在、以下のゲームをプレイできます。

### 1. 色読み (Iroyomi)
文字の意味と色が異なる漢字を素早く読み解く、注意力と判断力を鍛えるゲームです。
- **ディレクトリ**: [`/iroyomi`](./iroyomi)

### 2. パターン記憶 (Simon Says)
光った色の順番を記憶し、正確に再現する、短期記憶と集中力を鍛えるゲームです。
- **ディレクトリ**: [`/memory_games`](./memory_games)


## 🛠️ セットアップと実行方法
このプロジェクトは[Rye](https://rye-up.com/)で管理されています。
### 1. 必要なライブラリのインストール
```bash
rye sync
```

### 2. ゲームの実行
各ゲームは、対応するPythonスクリプトを実行することで起動します。

**例：色読みを起動する場合**
```bash
rye run python iroyomi/iroyomi.py
```
**例：パターン記憶ゲームを起動する場合**
```bash
rye run python memory_games/simon_says.py
```

## 📜 ライセンス
このプロジェクトは [MIT License](LICENSE) の下で公開されています。

# 作成者
Samurai-Human-Go
https://samurai-human-go.com