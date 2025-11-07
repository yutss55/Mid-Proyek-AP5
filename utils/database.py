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

# # 2. Tabel karakter dalam game
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS characters (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         user_id INT NOT NULL UNIQUE,
#         role VARCHAR(50) NOT NULL,
#         hp INT NOT NULL,
#         max_hp INT NOT NULL,
#         energi INT NOT NULL,
#         max_energi INT NOT NULL,
#         deff INT NOT NULL,
#         damage INT NOT NULL,
#         gold INT DEFAULT 10,
#         exp INT DEFAULT 0,
#         score INT DEFAULT 0,
#         title VARCHAR(100) DEFAULT 'Newbie',
#         current_floor INT DEFAULT 1,
#         FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#     ) ENGINE=InnoDB;
# ''')

# # 3. Tabel item untuk karakter
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS inventory (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         character_id INT NOT NULL,
#         item_name VARCHAR(100) NOT NULL,
#         quantity INT NOT NULL,
#         FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
#     ) ENGINE=InnoDB;
# ''')