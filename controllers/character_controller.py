from models.character_model import Character
from utils.database import db, cursor
import string

# ==================================================
# 🔹 CLASS KARAKTER
# ==================================================
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


# ==================================================
# 🔹 PEMBUATAN KARAKTER BARU
# ==================================================
def create_character(user_id: int):
    print("\n=== PEMBUATAN KARAKTER BARU ===")
    print("1. Archmage  - Penyihir kuat dengan energi besar")
    print("2. Guardian  - Pelindung tangguh dengan pertahanan tinggi")
    print("3. Marksman  - Pemanah cepat dengan serangan tajam")
    print("4. Assassin  - Pembunuh lincah dengan serangan mematikan")
    print("5. Fighter   - Petarung seimbang dengan daya tahan baik")

    choice = input("Masukkan pilihan (1-5): ").strip()

    class_map = {
        "1": Archmage,
        "2": Guardian,
        "3": Marksman,
        "4": Assassin,
        "5": Fighter
    }

    if choice not in class_map:
        print("Pilihan tidak valid! Silakan coba lagi.\n")
        return create_character(user_id)

    char = class_map[choice](user_id)

    try:
        cursor.execute("SELECT id FROM characters WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            print("\n❌ User ini sudah memiliki karakter!")
            return None

        cursor.execute("""
            INSERT INTO characters 
            (user_id, class_name, hp, energy, defense, damage, gold, exp, floor, title, score)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            char.user_id, char.class_name, char.hp, char.energy, 
            char.defense, char.damage, char.gold, char.exp, 
            char.floor, char.title, char.score
        ))
        db.commit()

        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        char_id = cursor.fetchone()["id"]
        char.character_id = char_id

        cursor.execute("SELECT id FROM shop_items WHERE item_name = 'Health Potion'")
        potion_id = cursor.fetchone()["id"]
        cursor.execute("SELECT id FROM shop_items WHERE item_name = 'Iron Sword'")
        sword_id = cursor.fetchone()["id"]

        starter_items = [
            (char_id, potion_id, 3),
            (char_id, sword_id, 1)
        ]
        cursor.executemany(
            "INSERT INTO inventory (character_id, item_id, quantity) VALUES (%s,%s,%s)",
            starter_items
        )
        db.commit()

        print(f"\n✅ Karakter '{char.class_name}' berhasil dibuat untuk User ID {user_id}!")
        print("🎒 Item awal: Health Potion x3, Iron Sword x1")
        char.show_status()

    except Exception as e:
        db.rollback()
        print(f"⚠️ Terjadi kesalahan: {e}")
        return None

    return char


# ==================================================
# 🔹 LOAD KARAKTER DARI DATABASE
# ==================================================
def load_character_by_user_id(user_id: int):
    try:
        cursor.execute("SELECT * FROM characters WHERE user_id = %s", (user_id,))
        char_data = cursor.fetchone()
        if not char_data:
            return None

        class_map = {
            "Archmage": Archmage,
            "Guardian": Guardian,
            "Marksman": Marksman,
            "Assassin": Assassin,
            "Fighter": Fighter
        }

        KarakterClass = class_map.get(char_data["class_name"])
        char = KarakterClass(user_id)

        for key in ["id", "hp", "energy", "defense", "damage", "gold", "exp", "floor", "title", "score"]:
            setattr(char, key if key != "id" else "character_id", char_data[key])
            
        cursor.execute("""
            SELECT s.item_name AS item_name, i.quantity
            FROM inventory i
            JOIN shop_items s ON i.item_id = s.id
            WHERE i.character_id = %s
        """, (char.character_id,))
        char.inventory = {row["item_name"]: row["quantity"] for row in cursor.fetchall()}

        print(f"\nKarakter '{char.class_name}' (Floor {char.floor}) berhasil dimuat.")
        return char

    except Exception as e:
        print(f"⚠️ Terjadi kesalahan saat memuat karakter: {e}")
        return None


# ==================================================
# 🔹 INVENTORY (Sinkron dengan Shop)
# ==================================================
def show_inventory(character_id: int):
    try:
        cursor.execute("""
            SELECT 
                i.id AS inventory_id,
                s.id AS item_id,
                s.item_name,
                s.description,
                s.item_type,
                s.price,
                i.quantity
            FROM inventory i
            JOIN shop_items s ON i.item_id = s.id
            WHERE i.character_id = %s
            ORDER BY s.item_type, s.price ASC;
        """, (character_id,))
        items = cursor.fetchall()

        if not items:
            print("\n📦 Inventory kamu kosong.")
            return []

        print("\n=== 🎒 INVENTORY KAMU ===")
        for idx, item in enumerate(items):
            huruf = string.ascii_lowercase[idx]
            print(f"[{huruf}] {item['item_name']} ({item['item_type']}) "
                  f"x{item['quantity']} — {item['description']}")
        return items

    except Exception as e:
        print(f"⚠️ Gagal memuat inventory: {e}")
        return []


def use_item(character_id: int, inventory_id: int):
    try:
        cursor.execute("""
            SELECT s.item_name, s.item_type, s.description, i.quantity
            FROM inventory i
            JOIN shop_items s ON i.item_id = s.id
            WHERE i.character_id = %s AND i.id = %s
        """, (character_id, inventory_id))
        item = cursor.fetchone()

        if not item:
            print("❌ Item tidak ditemukan di inventory.")
            return

        if item["quantity"] <= 0:
            print("⚠️ Kamu tidak memiliki item ini lagi.")
            return

        # Ambil status karakter
        cursor.execute("SELECT hp, energy, defense, damage FROM characters WHERE id = %s;", (character_id,))
        char = cursor.fetchone()
        if not char:
            print("Karakter tidak ditemukan.")
            return

        hp, energy, defense, damage = char["hp"], char["energy"], char["defense"], char["damage"]

        # Efek item
        if item["item_type"] == "potion":
            if "HP" in item["description"]:
                tambah = 150 if "Heavenly" in item["item_name"] else 50
                hp += tambah
                print(f"💖 {item['item_name']} digunakan! HP bertambah +{tambah}.")
            elif "Energy" in item["description"]:
                energy += 50
                print(f"⚡ {item['item_name']} digunakan! Energy bertambah +50.")
        elif item["item_type"] == "weapon":
            damage += 10
            print(f"🗡️ {item['item_name']} meningkatkan damage!")
        elif item["item_type"] == "armor":
            defense += 10
            print(f"🛡️ {item['item_name']} meningkatkan defense!")
        else:
            print(f"{item['item_name']} tidak memiliki efek khusus.")

        # Update database
        cursor.execute("""
            UPDATE characters 
            SET hp = %s, energy = %s, defense = %s, damage = %s 
            WHERE id = %s;
        """, (hp, energy, defense, damage, character_id))
        cursor.execute("UPDATE inventory SET quantity = quantity - 1 WHERE id = %s;", (inventory_id,))
        cursor.execute("DELETE FROM inventory WHERE id = %s AND quantity <= 0;", (inventory_id,))
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"⚠️ Gagal menggunakan item: {e}")


def sell_item(character_id: int, inventory_id: int):
    try:
        cursor.execute("""
            SELECT s.item_name, s.price, i.quantity
            FROM inventory i
            JOIN shop_items s ON i.item_id = s.id
            WHERE i.character_id = %s AND i.id = %s
        """, (character_id, inventory_id))
        item = cursor.fetchone()

        if not item:
            print("Item tidak ditemukan di inventory.")
            return

        if item["quantity"] <= 0:
            print("Tidak ada item yang bisa dijual.")
            return

        sell_price = item["price"] // 2
        cursor.execute("UPDATE inventory SET quantity = quantity - 1 WHERE id = %s;", (inventory_id,))
        cursor.execute("UPDATE characters SET gold = gold + %s WHERE id = %s;", (sell_price, character_id))
        cursor.execute("DELETE FROM inventory WHERE id = %s AND quantity <= 0;", (inventory_id,))
        db.commit()

        print(f"💰 Kamu menjual {item['item_name']} dan mendapat {sell_price} gold.")

    except Exception as e:
        db.rollback()
        print(f"⚠️ Gagal menjual item: {e}")


def inventory_menu(character_id: int):
    while True:
        items = show_inventory(character_id)
        if not items:
            return

        print("\n[1] Gunakan item")
        print("[2] Jual item")
        print("[3] Kembali")

        choice = input("Pilih aksi: ").strip()

        if choice == "1":
            huruf = input("Masukkan huruf item yang ingin digunakan: ").lower().strip()
            index = string.ascii_lowercase.find(huruf)
            if 0 <= index < len(items):
                inventory_id = items[index]["inventory_id"]
                use_item(character_id, inventory_id)
            else:
                print("Huruf tidak valid.")
        elif choice == "2":
            huruf = input("Masukkan huruf item yang ingin dijual: ").lower().strip()
            index = string.ascii_lowercase.find(huruf)
            if 0 <= index < len(items):
                inventory_id = items[index]["inventory_id"]
                sell_item(character_id, inventory_id)
            else:
                print("Huruf tidak valid.")
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")


def show_character_stats(character_id):
    try:
        cursor.execute("""
            SELECT 
                class_name, hp, energy, defense, damage, gold, exp, floor, score, title
            FROM characters
            WHERE id = %s
        """, (character_id,))
        data = cursor.fetchone()

        if not data:
            print("❌ Karakter tidak ditemukan.")
            return

        print("\n=== STATUS KARAKTER TERKINI ===")
        print(f"Kelas   : {data['class_name']}")
        print(f"HP      : {data['hp']}")
        print(f"Energy  : {data['energy']}")
        print(f"Defense : {data['defense']}")
        print(f"Damage  : {data['damage']}")
        print(f"Gold    : {data['gold']}")
        print(f"EXP     : {data['exp']}")
        print(f"Floor   : {data['floor']}")
        print(f"Score   : {data['score']}")
        print(f"Title   : {data['title']}")
        print("===============================")

    except Exception as e:
        print(f"⚠️ Terjadi kesalahan saat menampilkan stats: {e}")


def delete_character(user_id: int):
    print("\n============ HAPUS KARAKTER ============")
    confirm = input("Yakin ingin menghapus karakter Anda? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Penghapusan dibatalkan.")
        return
    try:
        cursor.execute("DELETE FROM characters WHERE user_id = %s", (user_id,))
        db.commit()
        if cursor.rowcount > 0:
            print("Karakter berhasil dihapus.")
        else:
            print("Tidak ditemukan karakter untuk User ID tersebut.")
    except Exception as e:
        db.rollback()
        print(f"Gagal menghapus karakter. Error: {e}")