# ランダム文字列ジェネレーター

GitHub Pages対応の高度なパスワード生成ツール

## 機能

- **高度な文字セット選択**: 数字、英字、記号（個別選択可能）、日本語文字対応
- **大量生成**: 1〜1000個のパスワードを一度に生成
- **レスポンシブデザイン**: PC・スマートフォン対応
- **エクスポート機能**: TXT・CSV形式でのダウンロード
- **まとめてコピー**: 全パスワードを一度にクリップボードにコピー
- **セキュア**: 暗号学的に安全な乱数生成器を使用

## GitHub Pagesでの公開方法

1. このリポジトリをGitHubにプッシュ
2. GitHubリポジトリの Settings > Pages に移動
3. Source を "Deploy from a branch" に設定
4. Branch を "main" (または "master") に設定
5. Save をクリック

## ローカルでの実行

HTMLファイルを直接ブラウザで開くか、ローカルサーバーで実行:

```bash
# Python 3の場合
python -m http.server 8000

# Node.jsの場合
npx serve .
```

## ファイル構成

- `index.html` - メインのHTMLファイル（GitHub Pages用）
- `app.py` - Streamlitアプリケーション（開発用）
- `password_generator.py` - パスワード生成ロジック
- `strength_checker.py` - パスワード強度チェック
- `utils.py` - ユーティリティ関数
- `database.py` - データベース機能

## 技術仕様

- フロントエンド: HTML5, CSS3, JavaScript (ES6+)
- バックエンド（開発用）: Python, Streamlit, PostgreSQL
- セキュリティ: クライアントサイド生成、データ非送信

## ライセンス

© 2024 ランダム文字列ジェネレーター# random-string-generator
