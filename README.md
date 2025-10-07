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

このプロジェクトは **MIT License** のもとで公開されています。ライセンスの全文については、[LICENSE](LICENSE) ファイルをご覧ください。

また、このプロジェクトはサードパーティ製のライブラリを利用しています。これらのライブラリのライセンス情報については、[NOTICE.md](NOTICE.md) ファイルに記載しています。

## 作成者
[Samurai-Human-Go](https://samurai-human-go.com/%e9%81%8b%e5%96%b6%e8%80%85%e6%83%85%e5%a0%b1/)

**ブログ記事**: [【Python/PySide6】ユーザーと共に育てる！パターン記憶ゲーム開発の全ステップまとめ](https://samurai-human-go.com/python-pyside6-iterative-development-story/)