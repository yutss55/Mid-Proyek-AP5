# View for user
import os
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def register_menu():
    clear_screen()
    print("\n=========== REGISTER ACCOUNT ============")
    print("Ketik 'keluar' kapan saja untuk kembali.\n")
    username = input("Masukkan username: ")
    if username == "keluar":
        return None, None
    password = input("Masukkan password: ")
    if password == "keluar":
        return None, None
    return username, password

def login_menu():
    clear_screen()
    print("\n================= LOGIN =================")
    print("Ketik 'keluar' kapan saja untuk kembali.\n")
    username = input("Masukkan username: ")
    if username == "keluar":
        return None, None
    password = input("Masukkan password: ")
    if password == "keluar":
        return None, None
    return username, password

def delete_account_menu():
    print("\n=== HAPUS AKUN ===")
    confirm = input("Yakin ingin menghapus akun ini? (y/n): ")
    return confirm.lower() == 'y'

def show_message(message):
    print(message)