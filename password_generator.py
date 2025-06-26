import secrets
import string

class PasswordGenerator:
    """高度なパスワード生成クラス"""
    
    def __init__(self):
        # 日本語文字セット
        self.hiragana = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
        self.katakana = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
        self.basic_kanji = '一二三四五六七八九十百千万円年月日時分秒人名前後左右上下大小中高低新古好悪美醜'
        
        # 基本文字セット
        self.numbers = string.digits
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        
        # 記号を種類別に分類
        self.basic_symbols = '!@#$%^&*'
        self.brackets = '()[]{}|'
        self.punctuation = '.,;:'
        self.math_symbols = '+-*/<>=_~'
    
    def build_character_set(self, char_sets):
        """文字セットを構築"""
        charset = ''
        
        if char_sets.get('numbers', False):
            charset += self.numbers
        if char_sets.get('lowercase', False):
            charset += self.lowercase
        if char_sets.get('uppercase', False):
            charset += self.uppercase
        if char_sets.get('basic_symbols', False):
            charset += self.basic_symbols
        if char_sets.get('brackets', False):
            charset += self.brackets
        if char_sets.get('punctuation', False):
            charset += self.punctuation
        if char_sets.get('math_symbols', False):
            charset += self.math_symbols
        if char_sets.get('hiragana', False):
            charset += self.hiragana
        if char_sets.get('katakana', False):
            charset += self.katakana
        if char_sets.get('kanji', False):
            charset += self.basic_kanji
        if char_sets.get('custom', ''):
            charset += char_sets['custom']
        
        if not charset:
            raise ValueError("少なくとも1つの文字種類を選択してください")
        
        # 重複文字を除去
        return ''.join(set(charset))
    
    def generate_password(self, char_sets, length):
        """単一のパスワードを生成"""
        charset = self.build_character_set(char_sets)
        
        if length < 1:
            raise ValueError("パスワードの長さは1文字以上である必要があります")
        
        # セキュアな乱数生成器を使用
        password = ''.join(secrets.choice(charset) for _ in range(length))
        return password
    
    def generate_batch(self, char_sets, length, count):
        """複数のパスワードを一括生成"""
        if count < 1 or count > 1000:
            raise ValueError("生成数は1-1000の範囲で指定してください")
        
        passwords = []
        for _ in range(count):
            password = self.generate_password(char_sets, length)
            passwords.append(password)
        
        return passwords
    
    def ensure_character_types(self, password, char_sets):
        """指定された文字種類が含まれることを保証（オプション機能）"""
        # この機能は必要に応じて実装可能
        # 各文字種類から最低1文字は含まれるようにする高度な機能
        pass
