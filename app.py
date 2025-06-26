import streamlit as st
import secrets
import string
import base64
import json
from password_generator import PasswordGenerator
from strength_checker import PasswordStrengthChecker
from utils import get_preset_templates, format_passwords_for_export

# Page configuration
st.set_page_config(
    page_title="ランダム文字列ジェネレーター",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for responsive design
st.markdown("""
<style>
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    .stCheckbox > label {
        font-size: 14px;
    }
    
    .password-display {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-family: monospace;
        word-break: break-all;
    }
    
    .symbol-group {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 10px 0;
    }
    
    .symbol-item {
        min-width: 150px;
    }
    
    @media (max-width: 768px) {
        .main-container {
            padding: 0.5rem;
        }
        
        .stColumns > div {
            margin-bottom: 1rem;
        }
        
        .symbol-item {
            min-width: 120px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_passwords' not in st.session_state:
    st.session_state.generated_passwords = []
if 'password_history' not in st.session_state:
    st.session_state.password_history = []

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Main title
st.title("🔐 ランダム文字列ジェネレーター")
st.markdown("**高度なパスワード生成ツール - セキュアで使いやすい**")

# Create responsive columns
is_mobile = st.container()
with is_mobile:
    # For mobile, use single column layout
    col1, col2 = st.columns([1, 1])

with col1:
    st.header("⚙️ 設定")
    
    # Character set selection
    st.subheader("使用文字")
    
    # Basic character types
    char_col1, char_col2 = st.columns(2)
    with char_col1:
        use_numbers = st.checkbox("数字 (0-9)", value=True)
        use_lowercase = st.checkbox("小文字 (a-z)", value=True)
    with char_col2:
        use_uppercase = st.checkbox("大文字 (A-Z)", value=True)
        use_symbols_any = st.checkbox("記号を使用", value=False)
    
    # Symbol selection (when symbols are enabled)
    if use_symbols_any:
        st.markdown("**記号の種類を選択:**")
        symbol_col1, symbol_col2 = st.columns(2)
        with symbol_col1:
            use_basic_symbols = st.checkbox("基本記号 (!@#$%)", value=True)
            use_brackets = st.checkbox("括弧 ()[]{}|", value=True)
        with symbol_col2:
            use_punctuation = st.checkbox("句読点 .,;:", value=False)
            use_math_symbols = st.checkbox("演算子 +-*/<>", value=False)
    else:
        use_basic_symbols = False
        use_brackets = False
        use_punctuation = False
        use_math_symbols = False
    
    # Japanese characters
    st.markdown("**日本語文字:**")
    jp_col1, jp_col2 = st.columns(2)
    with jp_col1:
        use_hiragana = st.checkbox("ひらがな", value=False)
        use_katakana = st.checkbox("カタカナ", value=False)
    with jp_col2:
        use_kanji = st.checkbox("漢字 (基本)", value=False)
    
    # Custom characters
    custom_chars = st.text_input("カスタム文字", placeholder="追加したい文字を入力")
    
    # Password length
    st.subheader("文字数")
    password_length = st.slider("パスワードの長さ", min_value=4, max_value=128, value=16)
    
    # Batch generation
    st.subheader("生成数")
    batch_count = st.number_input("一度に生成する数", min_value=1, max_value=1000, value=50)
    
    # Preset templates
    st.subheader("プリセット")
    templates = get_preset_templates()
    selected_template = st.selectbox("テンプレートを選択", ["カスタム"] + list(templates.keys()))
    
    if selected_template != "カスタム":
        if st.button("テンプレートを適用"):
            template = templates[selected_template]
            st.session_state.template_applied = template
            st.rerun()
    
    # Apply template if selected
    if hasattr(st.session_state, 'template_applied'):
        template = st.session_state.template_applied
        use_numbers = template.get('numbers', use_numbers)
        use_lowercase = template.get('lowercase', use_lowercase)
        use_uppercase = template.get('uppercase', use_uppercase)
        use_basic_symbols = template.get('symbols', use_basic_symbols)
        password_length = template.get('length', password_length)
        del st.session_state.template_applied

with col2:
    st.header("🎯 生成結果")
    
    # Generate button
    if st.button("🎲 パスワード生成", type="primary", use_container_width=True):
        # Create character set
        char_sets = {
            'numbers': use_numbers,
            'lowercase': use_lowercase,
            'uppercase': use_uppercase,
            'basic_symbols': use_basic_symbols,
            'brackets': use_brackets,
            'punctuation': use_punctuation,
            'math_symbols': use_math_symbols,
            'hiragana': use_hiragana,
            'katakana': use_katakana,
            'kanji': use_kanji,
            'custom': custom_chars
        }
        
        generator = PasswordGenerator()
        try:
            passwords = generator.generate_batch(
                char_sets=char_sets,
                length=password_length,
                count=batch_count
            )
            st.session_state.generated_passwords = passwords
            st.session_state.password_history.extend(passwords)
                
        except ValueError as e:
            st.error(f"エラー: {str(e)}")
    
    # Display generated passwords
    if st.session_state.generated_passwords:
        st.subheader("生成されたパスワード")
        
        # Show count
        st.info(f"✅ {len(st.session_state.generated_passwords)}個のパスワードを生成しました")
        
        # Display all passwords in a single text area for easy viewing and copying
        all_passwords = '\n'.join(st.session_state.generated_passwords)
        
        # Text area for all passwords
        st.text_area(
            "生成されたパスワード一覧",
            value=all_passwords,
            height=min(300, len(st.session_state.generated_passwords) * 25 + 50),
            help="すべてのパスワードをまとめて表示しています。テキストエリア内で全選択（Ctrl+A）してコピー（Ctrl+C）できます。"
        )
        
        # Bulk copy button - using Streamlit's built-in copy functionality
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📋 すべてのパスワードをコピー", use_container_width=True, type="secondary"):
                st.code(all_passwords, language=None)
                st.success("👆 上のコードボックスの右上のコピーボタンをクリックしてください")
        
        # Export options
        st.subheader("エクスポート")
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📄 テキストファイルとしてダウンロード"):
                text_content = format_passwords_for_export(st.session_state.generated_passwords, 'txt')
                st.download_button(
                    label="💾 passwords.txt をダウンロード",
                    data=text_content,
                    file_name="passwords.txt",
                    mime="text/plain"
                )
        
        with col_export2:
            if st.button("📊 CSVファイルとしてダウンロード"):
                csv_content = format_passwords_for_export(st.session_state.generated_passwords, 'csv')
                st.download_button(
                    label="💾 passwords.csv をダウンロード",
                    data=csv_content,
                    file_name="passwords.csv",
                    mime="text/csv"
                )

# Sidebar for additional features  
with st.sidebar:
    st.header("🔍 パスワード履歴")
    
    if st.session_state.password_history:
        st.info(f"📊 合計 {len(st.session_state.password_history)} 個生成済み")
        
        # Show last 5 passwords
        recent_passwords = st.session_state.password_history[-5:]
        for pwd in reversed(recent_passwords):
            with st.expander(f"{pwd[:8]}..."):
                st.code(pwd)
                checker = PasswordStrengthChecker()
                strength = checker.check_strength(pwd)
                st.write(f"強度: {strength}")
    else:
        st.info("まだパスワードが生成されていません")
    
    if st.button("📝 履歴をクリア"):
        st.session_state.password_history = []
        st.session_state.generated_passwords = []
        st.rerun()
    
    st.header("ℹ️ 使い方")
    st.markdown("""
    1. **文字種類を選択** - 使用したい文字の種類をチェック
    2. **長さを設定** - 4-128文字の範囲で設定
    3. **生成数を選択** - 一度に生成するパスワード数
    4. **生成ボタンをクリック** - パスワードを生成
    5. **コピー** - 📋ボタンでクリップボードにコピー
    6. **エクスポート** - ファイルとして保存
    """)
    
    st.header("🛡️ セキュリティ")
    st.markdown("""
    - 暗号学的に安全な乱数生成器を使用
    - ブラウザ上で生成、サーバーに保存されません
    - 生成されたパスワードは一時的にのみ表示
    """)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        © 2024 ランダム文字列ジェネレーター | セキュアなパスワード生成ツール
    </div>
    """, 
    unsafe_allow_html=True
)
