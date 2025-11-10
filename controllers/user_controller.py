from models.user_model import UserModel
from views.user_view import show_message

def register_user(username, password):
    if UserModel.find_by_username(username):
        show_message("Username sudah digunakan. Silakan pilih username yang lain.")
        return
    UserModel.insert(username, password)
    show_message("Registrasi berhasil!")

def login_user(username, password):
    user = UserModel.find_by_username(username)
    if not user:
        show_message("Username tidak ditemukan!")
        return False
    
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user[2] == password_hash:
        show_message(f"Login berhasil! Selamat datang, {username}!")
        return True
    else:
        show_message("Password Anda salah!")
        return False
    
def delete_account(username, password):
    user = UserModel.find_by_username(username)
    if not user:
        show_message("Username tidak ditemukan!")
        return False

    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user[2] != password_hash:
        show_message("Password salah! Penghapusan akun dibatalkan.")
        return False

    confirm = input("Yakin ingin menghapus akun Anda secara permanen? (y/n): ").strip().lower()
    if confirm != 'y':
        show_message("Penghapusan akun dibatalkan.")
        return False
    
    try:
        db = UserModel.get_db() 
        db.start_transaction()
    
        user_id = user[0]

        UserModel.delete_by_username(username)
        
        db.commit()
        show_message("Akun berhasil dihapus. Sampai jumpa!")
        return True
    
    except Exception as e:
        db.rollback()
        show_message(f"Gagal menghapus akun. Error: {str(e)}")
        return False
