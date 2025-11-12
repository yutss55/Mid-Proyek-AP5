from models.user_model import UserModel
from views.user_view import show_message, delete_account_menu
from views.menu_view import main_menu
import hashlib
from utils.database import db, cursor

def register_user(username, password):
    if UserModel.find_by_username(username):
        show_message("\nUsername sudah digunakan.\nSilakan pilih username yang lain.")
        input("Tekan Enter untuk lanjut...")
        return False
    UserModel.insert(username, password)
    show_message("\nRegistrasi berhasil!✅")
    show_message("Masuklah untuk memulai petualanganmu.⚔️")
    return True

def login_user(username, password):
    user = UserModel.find_by_username(username)
    if not user:
        show_message("\nUsername tidak ditemukan!")
        input("Tekan Enter untuk lanjut...")
        return False

    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user["password_hash"] == password_hash:
        show_message(f"\nLogin berhasil! Sistem mengenali {username}.")
        show_message(f"Selamat datang di dunia ALTER EGO.⚔️")
        main_menu(user)
        return True
    else:
        show_message("\nPassword Anda salah!")
        input("Tekan Enter untuk lanjut...")
        return False

import hashlib
from utils.database import db, cursor

def delete_account(username):
    try:
        # Ambil data user dari database
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            print("❌ User tidak ditemukan.")
            return False

        user_id = user["id"]
        password_hash = user["password_hash"]

        # Konfirmasi awal (y/n)
        print("\n=== HAPUS AKUN ===")
        confirm = input(f"⚠️ Yakin ingin menghapus akun '{username}'? (y/n): ").strip().lower()
        if confirm != "y":
            print("❎ Penghapusan akun dibatalkan.")
            return False

        # Verifikasi password sebelum hapus
        password = input("Masukkan password untuk konfirmasi: ").strip()
        hashed_input = hashlib.sha256(password.encode()).hexdigest()

        if hashed_input != password_hash:
            print("❌ Password salah! Penghapusan dibatalkan.")
            return False

        # Hapus inventory berdasarkan karakter user
        cursor.execute("""
            DELETE FROM inventory
            WHERE character_id IN (
                SELECT id FROM characters WHERE user_id = %s
            )
        """, (user_id,))

        # Hapus karakter
        cursor.execute("DELETE FROM characters WHERE user_id = %s", (user_id,))

        # Hapus user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

        db.commit()
        print("✅ Akun berhasil dihapus. Sampai jumpa!")
        return True

    except Exception as e:
        db.rollback()
        print(f"⚠️ Gagal menghapus akun. Error: {e}")
        return False