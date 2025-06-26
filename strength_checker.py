import re
import math

class PasswordStrengthChecker:
    """パスワード強度チェッククラス"""
    
    def __init__(self):
        self.strength_levels = {
            0: "非常に弱い",
            1: "弱い", 
            2: "普通",
            3: "強い",
            4: "非常に強い"
        }
    
    def check_strength(self, password):
        """パスワード強度を文字列で返す"""
        score = self.get_strength_score(password)
        
        if score < 1:
            return "非常に弱い"
        elif score < 2:
            return "弱い"
        elif score < 3:
            return "普通"
        elif score < 4:
            return "強い"
        else:
            return "非常に強い"
    
    def get_strength_score(self, password):
        """パスワード強度スコア（0-5）を計算"""
        if not password:
            return 0
        
        score = 0
        
        # 長さによるスコア
        length = len(password)
        if length >= 8:
            score += 1
        if length >= 12:
            score += 0.5
        if length >= 16:
            score += 0.5
        
        # 文字種類の多様性
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        has_hiragana = bool(re.search(r'[あ-ん]', password))
        has_katakana = bool(re.search(r'[ア-ン]', password))
        has_kanji = bool(re.search(r'[一-龯]', password))
        
        char_types = sum([has_lower, has_upper, has_digit, has_symbol, 
                         has_hiragana, has_katakana, has_kanji])
        
        if char_types >= 2:
            score += 1
        if char_types >= 3:
            score += 0.5
        if char_types >= 4:
            score += 0.5
        
        # エントロピーの計算
        entropy = self.calculate_entropy(password)
        if entropy >= 40:
            score += 0.5
        if entropy >= 60:
            score += 0.5
        if entropy >= 80:
            score += 0.5
        
        # 一般的な弱いパスワードパターンのチェック
        if self.has_common_patterns(password):
            score -= 1
        
        return max(0, min(5, score))
    
    def calculate_entropy(self, password):
        """パスワードのエントロピーを計算"""
        if not password:
            return 0
        
        # 文字セットサイズを推定
        charset_size = 0
        
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            charset_size += 32
        if re.search(r'[あ-ん]', password):
            charset_size += 46  # ひらがな
        if re.search(r'[ア-ン]', password):
            charset_size += 46  # カタカナ
        if re.search(r'[一-龯]', password):
            charset_size += 100  # 基本漢字の推定
        
        if charset_size == 0:
            return 0
        
        # エントロピー = log2(charset_size) * length
        entropy = math.log2(charset_size) * len(password)
        return entropy
    
    def has_common_patterns(self, password):
        """一般的な弱いパターンをチェック"""
        password_lower = password.lower()
        
        # 連続する文字のチェック
        if re.search(r'(.)\1{2,}', password):  # 同じ文字が3回以上
            return True
        
        # 順次パターン（123, abc等）
        sequences = ['0123456789', 'abcdefghijklmnopqrstuvwxyz', 'qwertyuiop']
        for seq in sequences:
            for i in range(len(seq) - 2):
                if seq[i:i+3] in password_lower or seq[i:i+3][::-1] in password_lower:
                    return True
        
        # 一般的な弱いパスワード
        common_weak = ['password', 'admin', 'login', '111111', '000000', 'qwerty']
        for weak in common_weak:
            if weak in password_lower:
                return True
        
        return False
    
    def get_detailed_analysis(self, password):
        """詳細な分析結果を返す"""
        analysis = {
            'length': len(password),
            'entropy': self.calculate_entropy(password),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_digits': bool(re.search(r'[0-9]', password)),
            'has_symbols': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
            'has_hiragana': bool(re.search(r'[あ-ん]', password)),
            'has_katakana': bool(re.search(r'[ア-ン]', password)),
            'has_kanji': bool(re.search(r'[一-龯]', password)),
            'has_common_patterns': self.has_common_patterns(password),
            'strength_score': self.get_strength_score(password),
            'strength_level': self.check_strength(password)
        }
        
        return analysis
