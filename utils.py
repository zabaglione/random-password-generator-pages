import csv
import io
from datetime import datetime

def get_preset_templates():
    """プリセットテンプレートを返す"""
    templates = {
        "基本セキュア": {
            "numbers": True,
            "lowercase": True,
            "uppercase": True,
            "symbols": False,
            "length": 12
        },
        "高セキュリティ": {
            "numbers": True,
            "lowercase": True,
            "uppercase": True,
            "symbols": True,
            "length": 16
        },
        "シンプル": {
            "numbers": True,
            "lowercase": True,
            "uppercase": False,
            "symbols": False,
            "length": 8
        },
        "日本語混合": {
            "numbers": True,
            "lowercase": True,
            "uppercase": True,
            "hiragana": True,
            "katakana": True,
            "length": 12
        },
        "記号なし長文": {
            "numbers": True,
            "lowercase": True,
            "uppercase": True,
            "symbols": False,
            "length": 20
        },
        "WiFiパスワード": {
            "numbers": True,
            "lowercase": True,
            "uppercase": True,
            "symbols": False,
            "length": 16
        },
        "PIN風数字": {
            "numbers": True,
            "lowercase": False,
            "uppercase": False,
            "symbols": False,
            "length": 6
        }
    }
    
    return templates

def format_passwords_for_export(passwords, format_type='txt'):
    """パスワードをエクスポート用にフォーマット"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if format_type == 'txt':
        content = f"# Generated Passwords - {timestamp}\n"
        content += f"# Total: {len(passwords)} passwords\n\n"
        
        for i, password in enumerate(passwords, 1):
            content += f"{i:3d}. {password}\n"
        
        return content
    
    elif format_type == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        
        # ヘッダー
        writer.writerow(['No', 'Password', 'Length', 'Generated_At'])
        
        # データ
        for i, password in enumerate(passwords, 1):
            writer.writerow([i, password, len(password), timestamp])
        
        return output.getvalue()
    
    elif format_type == 'json':
        import json
        data = {
            'generated_at': timestamp,
            'total_count': len(passwords),
            'passwords': [
                {
                    'id': i,
                    'password': password,
                    'length': len(password)
                }
                for i, password in enumerate(passwords, 1)
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    return str(passwords)

def validate_character_set(char_sets):
    """文字セット設定の妥当性をチェック"""
    has_any_charset = any([
        char_sets.get('numbers', False),
        char_sets.get('lowercase', False),
        char_sets.get('uppercase', False),
        char_sets.get('symbols', False),
        char_sets.get('hiragana', False),
        char_sets.get('katakana', False),
        char_sets.get('kanji', False),
        bool(char_sets.get('custom', ''))
    ])
    
    if not has_any_charset:
        return False, "少なくとも1つの文字種類を選択してください"
    
    return True, "OK"

def estimate_crack_time(password):
    """パスワードのクラック時間を推定"""
    from strength_checker import PasswordStrengthChecker
    
    checker = PasswordStrengthChecker()
    entropy = checker.calculate_entropy(password)
    
    # 1秒間に10億回の試行を仮定
    attempts_per_second = 1e9
    
    # 平均的には全組み合わせの半分を試行する必要がある
    total_combinations = 2 ** entropy
    average_attempts = total_combinations / 2
    
    seconds = average_attempts / attempts_per_second
    
    # 時間単位に変換
    if seconds < 60:
        return f"{seconds:.1f} 秒"
    elif seconds < 3600:
        return f"{seconds/60:.1f} 分"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} 時間"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} 日"
    else:
        return f"{seconds/31536000:.1f} 年"

def get_security_recommendations(char_sets, length):
    """セキュリティ推奨事項を生成"""
    recommendations = []
    
    if length < 8:
        recommendations.append("⚠️ パスワードの長さを8文字以上にすることを推奨します")
    
    if length < 12:
        recommendations.append("💡 より高いセキュリティのために12文字以上を推奨します")
    
    char_type_count = sum([
        char_sets.get('numbers', False),
        char_sets.get('lowercase', False),
        char_sets.get('uppercase', False),
        char_sets.get('symbols', False)
    ])
    
    if char_type_count < 3:
        recommendations.append("💡 数字、小文字、大文字、記号のうち3種類以上使用することを推奨します")
    
    if not char_sets.get('symbols', False):
        recommendations.append("🔒 より高いセキュリティのために記号の使用を推奨します")
    
    if not recommendations:
        recommendations.append("✅ 良好なパスワード設定です")
    
    return recommendations
