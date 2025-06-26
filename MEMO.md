# Random String Generator プロジェクト完全ガイド

## プロジェクト概要
日本語対応の高度なパスワード生成ツールを、StreamlitとGitHub Pages両対応で開発したプロジェクト。

## 開発経緯
1. **要求分析**: https://apps.hayu.io/random を参考に、より使いやすいパスワード生成ツールの開発
2. **UI改善要求**: 
   - 生成数を1-1000に拡張（デフォルト50）
   - 個別シンボル選択機能
   - レスポンシブデザイン（PC/モバイル対応）
   - 一括コピー機能、個別強度表示の削除
3. **デプロイ要求**: GitHub Pages対応の静的版作成

## 完成した機能
- 多様な文字セット選択（数字、英字、記号、日本語文字）
- 1-1000個の一括パスワード生成
- PostgreSQL履歴管理（Streamlit版）
- レスポンシブデザイン
- GitHub Pages自動デプロイ
- TXT/CSV形式エクスポート

---

# 同じアプリを再作成するための完全指示

以下の指示に従って、同じ機能を持つパスワード生成アプリを作成してください：

## ステップ1: 環境セットアップ
```
1. Streamlit環境を構築
2. PostgreSQLデータベースを作成
3. 必要なPythonライブラリをインストール：
   - streamlit
   - psycopg2-binary
   - sqlalchemy
```

## ステップ2: コアファイル作成

### password_generator.py
- PasswordGeneratorクラス
- 文字セット構築機能（数字、英字大小、基本記号、括弧、句読点、数学記号、ひらがな、カタカナ、漢字、カスタム文字）
- generate_password(), generate_batch()メソッド
- 文字種類保証機能（ensure_character_types）

### strength_checker.py  
- PasswordStrengthCheckerクラス
- エントロピー計算機能
- 強度レベル判定（弱い/普通/強い/非常に強い）
- 一般的なパターンチェック
- 詳細分析機能

### utils.py
- プリセットテンプレート機能
- エクスポート形式対応（TXT/CSV）
- 文字セット妥当性チェック
- クラック時間推定
- セキュリティ推奨事項生成

### database.py
- SQLAlchemyベースのデータベース設計
- PasswordRecordテーブル（履歴管理）
- UserPreferencesテーブル（設定保存）
- CRUD操作関数群

## ステップ3: Streamlitアプリ (app.py)
```python
# 主要機能要件:
- サイドバーで文字セット選択UI
- 生成数：1-1000（デフォルト50）
- 文字数：4-256（デフォルト16）
- 個別シンボルカテゴリ選択
- 一括表示テキストエリア
- 全パスワード一括コピーボタン
- エクスポート機能（TXT/CSV）
- 履歴表示（最新10件）
- ユーザー設定保存
- セッション管理
```

## ステップ4: 静的HTML版 (index.html)
```html
<!-- GitHub Pages対応の完全機能版 -->
- 同等のUI/UX
- JavaScript実装のパスワード生成
- レスポンシブCSSデザイン
- ローカルストレージ活用
- 暗号学的に安全な乱数生成
```

## ステップ5: GitHub Pages設定
```yaml
# .github/workflows/deploy.yml
- mainブランチへのプッシュで自動デプロイ
- GitHub Pagesへの静的サイト公開
```

## ステップ6: 設定ファイル
```toml
# .streamlit/config.toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## UI/UX要件
1. **文字セット選択**: チェックボックスで個別選択可能
2. **生成設定**: スライダーとテキスト入力の組み合わせ
3. **結果表示**: 単一テキストエリアで全パスワード表示
4. **操作性**: 一括コピー、個別エクスポート対応
5. **履歴機能**: セッション別履歴管理
6. **レスポンシブ**: PC/モバイル両対応

## データベーススキーマ
```sql
-- password_records テーブル
id, password, length, character_sets, strength_score, 
strength_level, created_at, user_session

-- user_preferences テーブル  
id, user_session, default_length, default_count,
各文字セットのBoolean設定, custom_chars, updated_at
```

## 特記要項
- 個別パスワード強度表示は不要（ユーザー要求）
- 統計表示機能は削除（ユーザー要求）
- 日本語文字対応は必須
- セキュリティを重視した実装
- 両バージョン（Streamlit/静的HTML）の機能同等性維持

この指示に従えば、同一機能のパスワード生成アプリを再作成できます。
