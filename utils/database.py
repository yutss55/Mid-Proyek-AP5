# koneksi MySQL
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)
cursor = db.cursor()

# Mengecek koneksi database ke Python
#if db.is_connected():
#   print("berhasil.")

# Buat database
# cursor.execute("CREATE DATABASE game_adventure")
# print("Database berhasil dibuat")

# Buat tabel dalam database
# 1. Tabel user
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         username VARCHAR(100) NOT NULL UNIQUE,
#         password_hash VARCHAR(255) NOT NULL
#     )
# ''')

# 2. Tabel karakter dalam game
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS characters (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     class_name VARCHAR(30) NOT NULL,
#     hp INT DEFAULT 0,
#     energy INT DEFAULT 0,
#     defense INT DEFAULT 0,
#     damage INT DEFAULT 0,
#     gold INT DEFAULT 0,
#     exp INT DEFAULT 0,
#     floor INT DEFAULT 1,
#     title VARCHAR(50) DEFAULT 'Novice',
#     score INT DEFAULT 0,
#     inventory TEXT DEFAULT '{}',
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# )
# ''')