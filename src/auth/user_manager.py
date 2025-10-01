import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import logging

class UserManager:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize user database with proper schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                roles TEXT NOT NULL DEFAULT 'user',
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                failed_login_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user if not exists
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, roles)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@sovereign-osint.com', 
              self.hash_password('Admin123!'), 'admin,analyst,user'))
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        return salt + ':' + hashlib.sha256((salt + password).encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = password_hash.split(':')
            return hashlib.sha256((salt + password).encode()).hexdigest() == hash_value
        except:
            return False
    
    def create_user(self, username: str, email: str, password: str, 
                   roles: str = "user", full_name: str = None) -> bool:
        """Create new user account"""
        if not self.is_strong_password(password):
            return False
            
        password_hash = self.hash_password(password)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, roles, full_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, roles, full_name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and update login stats"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash, roles, full_name, 
                   is_active, locked_until, failed_login_attempts
            FROM users WHERE username = ?
        ''', (username,))
        
        user_data = cursor.fetchone()
        
        if not user_data:
            conn.close()
            return None
        
        (user_id, username, email, password_hash, roles, full_name, 
         is_active, locked_until, failed_attempts) = user_data
        
        # Check if account is locked
        if locked_until and datetime.fromisoformat(locked_until) > datetime.now():
            conn.close()
            return None
        
        # Verify password
        if self.verify_password(password, password_hash):
            # Successful login - reset failed attempts and update last login
            cursor.execute('''
                UPDATE users 
                SET last_login = ?, failed_login_attempts = 0, locked_until = NULL
                WHERE id = ?
            ''', (datetime.now(), user_id))
            
            user = {
                'id': user_id,
                'username': username,
                'email': email,
                'roles': roles.split(','),
                'full_name': full_name,
                'is_active': bool(is_active)
            }
        else:
            # Failed login - increment attempts and potentially lock account
            failed_attempts += 1
            locked_until = None
            
            if failed_attempts >= 5:
                locked_until = datetime.now() + timedelta(minutes=30)
            
            cursor.execute('''
                UPDATE users 
                SET failed_login_attempts = ?, locked_until = ?
                WHERE id = ?
            ''', (failed_attempts, locked_until, user_id))
            
            user = None
        
        conn.commit()
        conn.close()
        return user
    
    def create_session(self, user_id: int, expires_hours: int = 24) -> str:
        """Create user session"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_sessions (user_id, session_token, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, session_token, expires_at))
        
        conn.commit()
        conn.close()
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Validate session token and return user data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.roles, u.full_name, u.is_active
            FROM users u
            JOIN user_sessions s ON u.id = s.user_id
            WHERE s.session_token = ? AND s.expires_at > ? AND u.is_active = 1
        ''', (session_token, datetime.now()))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'roles': user_data[3].split(','),
                'full_name': user_data[4],
                'is_active': bool(user_data[5])
            }
        return None
    
    def is_strong_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            return False
        return True

# Global user manager instance
user_manager = UserManager()