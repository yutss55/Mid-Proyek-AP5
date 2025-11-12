# Model for user
from utils.database import db, cursor
import hashlib
import mysql.connector

class UserModel:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def insert(username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (username, password_hash))
        db.commit()

    @staticmethod
    def find_by_username(username):
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        return cursor.fetchone()
    
    @staticmethod
    def delete_by_username(username):
        """Menghapus akun dari tabel users berdasarkan username."""
        from utils.database import db, cursor  # pastikan pakai koneksi global
        query = "DELETE FROM users WHERE username = %s"
        cursor.execute(query, (username))
        db.commit()
