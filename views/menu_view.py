# View for menu
from controllers.character_controller import create_character, load_character_by_user_id, inventory_menu, delete_character, show_character_stats
from controllers.leaderboard_controller import get_leaderboard
from controllers.quest_controller import start_quest
from views.leaderboard_view import display_leaderboard
from controllers.shop_controller import open_shop
from views.user_view import clear_screen
import time

def main_menu(user):
    while True:
        print("\n=========================================")
        print(f"👤 Pemain: {user["username"].upper()}")
        print("-----------------------------------------")
        print(f">>> MENU UTAMA")
        print("1. Buat Karakter🧙")
        print("2. Lihat Stats Karakter⚔")
        print("3. Selesaikan Misi🎯")
        print("4. Beli Item💎")
        print("5. Penyimpanan Item🎒")
        print("6. Papan Peringkat🏆")
        print("7. Hapus Karakter☠")
        print("8. Hapus Akun⚠")
        print("9. Kembali🚪")
        print("=========================================")
        pilihan = input("Pilih menu (1-8): ")
        
        try:
            if pilihan == "1":
                create_character(user["id"])
                time.sleep(1.5)
            elif pilihan == "2":
                character = load_character_by_user_id(user["id"])
                if character:
                    clear_screen()
                    show_character_stats(character.character_id)
                    time.sleep(1.5)
                else:
                    print("⚠ Kamu belum memiliki karakter! Buat dulu sebelum melihat stats.")
            elif pilihan == "3":
                character = load_character_by_user_id(user["id"])
                if character:
                    clear_screen()
                    start_quest(character)
                else:
                    print("⚠ Kamu belum memiliki karakter! Buat dulu sebelum mulai quest.")
            elif pilihan == "4":
                character = load_character_by_user_id(user["id"])
                if character:
                    clear_screen()
                    open_shop(character)
                else:
                    print("⚠ Kamu belum memiliki karakter! Buat dulu sebelum membuka shop.")
            elif pilihan == "5":
                character = load_character_by_user_id(user["id"])
                if character:
                    clear_screen()
                    inventory_menu(character.character_id)
                else:
                    print("⚠ Kamu belum memiliki karakter! Buat dulu sebelum membuka inventory.")
            elif pilihan == "6":
                clear_screen()
                leaderboard_data = get_leaderboard()
                display_leaderboard(leaderboard_data)
            elif pilihan == "7":
                clear_screen()
                delete_character(user["id"])
            elif pilihan == "8":
                clear_screen()
                from controllers.user_controller import delete_account
                status = delete_account(user["username"])
                if status == True :
                    break
            elif pilihan == "9":
                clear_screen()
                break
            else:
                print("Pilihan menu tidak valid.")
        except Exception as e:
            print("Terjadi error:", e)