# controller_character.py
from utils.database import db, cursor
from models.character_model import Character
from utils.database import db, cursor

class Archmage(Character):
    def __init__(self, user_id: int):
        super().__init__(user_id, "Archmage", hp=200, energy=250, defense=100, damage=75)
    def special_attack(self, target):
        if self.energy >= 30:
            dmg = int(self.damage * 1.5)
            target.hp -= dmg
            self.energy -= 30
            print(f"{self.class_name} melempar bola api ({dmg} dmg)")
        else:
            print("Energi tidak cukup!")

class Guardian(Character):
    def __init__(self, user_id: int):
        super().__init__(user_id, "Guardian", hp=350, energy=100, defense=200, damage=40)

class Marksman(Character):
    def __init__(self, user_id: int):
        super().__init__(user_id, "Marksman", hp=220, energy=120, defense=120, damage=90)

class Assassin(Character):
    def __init__(self, user_id: int):
        super().__init__(user_id, "Assassin", hp=180, energy=150, defense=80, damage=100)

class Fighter(Character):
    def __init__(self, user_id: int):
        super().__init__(user_id, "Fighter", hp=250, energy=130, defense=150, damage=80)

    
def create_character(user_id: int):
    print("\n=== PEMBUATAN KARAKTER BARU ===")
    print("Pilih class karakter:")
    print("1. Archmage  - Penyihir kuat dengan energi besar")
    print("2. Guardian  - Pelindung tangguh dengan pertahanan tinggi")
    print("3. Marksman  - Pemanah cepat dengan serangan tajam")
    print("4. Assassin  - Pembunuh lincah dengan serangan mematikan")
    print("5. Fighter   - Petarung seimbang dengan daya tahan baik")

    choice = input("Masukkan pilihan (1-5): ").strip()

    # Pemilihan class berdasarkan input
    if choice == "1":
        char = Archmage(user_id)
    elif choice == "2":
        char = Guardian(user_id)
    elif choice == "3":
        char = Marksman(user_id)
    elif choice == "4":
        char = Assassin(user_id)
    elif choice == "5":
        char = Fighter(user_id)
    else:
        print("Pilihan tidak valid! Silakan coba lagi.\n")
        return create_character(user_id)

    # Simpan karakter ke database
    cursor.execute("""
        INSERT INTO characters (user_id, class_name, hp, energy, defense, damage, gold, exp, floor, title, score, inventory)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        char.user_id, char.class_name, char.hp, char.energy, char.defense, char.damage,
        char.gold, char.exp, char.floor, char.title, char.score, "{}"
    ))
    db.commit()

    print(f"\nKarakter '{char.class_name}' berhasil dibuat untuk User ID {user_id}!")
    print("Detail karakter:")
    char.show_status()
    return char

