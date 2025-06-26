import os
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
import json

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/password_generator')

engine = sa.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class PasswordRecord(Base):
    """パスワード生成履歴のモデル"""
    __tablename__ = "password_records"
    
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(256), nullable=False)
    length = Column(Integer, nullable=False)
    character_sets = Column(Text)  # JSON形式で保存
    strength_score = Column(Integer)
    strength_level = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_session = Column(String(100))  # セッション識別用

class UserPreferences(Base):
    """ユーザー設定のモデル"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_session = Column(String(100), unique=True, index=True)
    default_length = Column(Integer, default=16)
    default_count = Column(Integer, default=50)
    use_numbers = Column(Boolean, default=True)
    use_lowercase = Column(Boolean, default=True)
    use_uppercase = Column(Boolean, default=True)
    use_basic_symbols = Column(Boolean, default=False)
    use_brackets = Column(Boolean, default=False)
    use_punctuation = Column(Boolean, default=False)
    use_math_symbols = Column(Boolean, default=False)
    use_hiragana = Column(Boolean, default=False)
    use_katakana = Column(Boolean, default=False)
    use_kanji = Column(Boolean, default=False)
    custom_chars = Column(String(256), default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database functions
def init_database():
    """データベースを初期化"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_password_record(db: Session, password: str, length: int, char_sets: dict, 
                        strength_score: int, strength_level: str, user_session: str):
    """パスワード生成履歴を保存"""
    record = PasswordRecord(
        password=password,
        length=length,
        character_sets=json.dumps(char_sets),
        strength_score=strength_score,
        strength_level=strength_level,
        user_session=user_session
    )
    db.add(record)
    db.commit()
    return record

def get_password_history(db: Session, user_session: str, limit: int = 10):
    """パスワード履歴を取得"""
    return db.query(PasswordRecord).filter(
        PasswordRecord.user_session == user_session
    ).order_by(PasswordRecord.created_at.desc()).limit(limit).all()

def save_user_preferences(db: Session, user_session: str, preferences: dict):
    """ユーザー設定を保存"""
    existing = db.query(UserPreferences).filter(
        UserPreferences.user_session == user_session
    ).first()
    
    if existing:
        for key, value in preferences.items():
            setattr(existing, key, value)
    else:
        preferences['user_session'] = user_session
        existing = UserPreferences(**preferences)
        db.add(existing)
    
    db.commit()
    return existing

def get_user_preferences(db: Session, user_session: str):
    """ユーザー設定を取得"""
    return db.query(UserPreferences).filter(
        UserPreferences.user_session == user_session
    ).first()

def get_password_statistics(db: Session, user_session: str):
    """パスワード統計を取得"""
    total_generated = db.query(PasswordRecord).filter(
        PasswordRecord.user_session == user_session
    ).count()
    
    avg_strength = db.query(sa.func.avg(PasswordRecord.strength_score)).filter(
        PasswordRecord.user_session == user_session
    ).scalar() or 0
    
    recent_passwords = db.query(PasswordRecord).filter(
        PasswordRecord.user_session == user_session
    ).order_by(PasswordRecord.created_at.desc()).limit(10).all()
    
    return {
        'total_generated': total_generated,
        'average_strength': round(avg_strength, 1),
        'recent_count': len(recent_passwords)
    }

def clear_user_history(db: Session, user_session: str):
    """ユーザーの履歴をクリア"""
    db.query(PasswordRecord).filter(
        PasswordRecord.user_session == user_session
    ).delete()
    db.commit()