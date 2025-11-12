# titik awal program
import time
import sys
from controllers.user_controller import register_user, login_user
from views.user_view import register_menu, login_menu
from utils.database import close_connection
# from views.user_view import clear_screen

def slow_print(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

while True:
    print("\n=========================================")
    print(" ALTER EGO  —  ALTERnativE Game Oriented ")
    print("=========================================\n")
    slow_print("Bangun karaktermu. Tentukan jalanmu.")
    slow_print("Petualanganmu dimulai di sini!\n")
    time.sleep(0.5)
    print("=========================================")
    print(">>> AKSES SISTEM")
    print("1. Register (Mulai perjalanan baru)")
    print("2. Login (Lanjutkan perjalananmu)")
    print("3. Keluar (Beristirahat sejenak)")
    print("=========================================")
    pilihan = input("Pilih aksi (1/2/3): ")
    
    try:
        if pilihan == "1":
            while True:
                username, password = register_menu()
                if username is None or password is None:
                    break
                success = register_user(username, password)
                if success:
                    time.sleep(2)
                    break
        elif pilihan == "2":
            while True:
                username, password = login_menu()
                if username is None or password is None:
                    break
                success = login_user(username, password)
                if success:
                    time.sleep(2)
                    break
        elif pilihan == "3":
            print("\nKeluar dari game... sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")
    except Exception as e:
        print("Terjadi error:", e)
    
close_connection()