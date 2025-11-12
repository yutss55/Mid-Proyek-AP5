from utils.database import cursor, db
from controllers.leaderboard_controller import update_player_score
import random

# ==================================================
# DAFTAR MONSTER DAN BOSS
# ==================================================
MONSTERS = {
    "1": {"name": "Slime", "hp": 50, "attack": 8, "reward": {"gold": 20, "exp": 30, "score": 10}},
    "2": {"name": "Goblin", "hp": 80, "attack": 15, "reward": {"gold": 35, "exp": 50, "score": 20}},
    "3": {"name": "Werewolf", "hp": 120, "attack": 25, "reward": {"gold": 60, "exp": 90, "score": 30}},
    "4": {"name": "Orc", "hp": 150, "attack": 30, "reward": {"gold": 80, "exp": 120, "score": 40}},
}

BOSSES = {
    "1": {"name": "Minotaur", "hp": 250, "attack": 45, "reward": {"gold": 200, "exp": 250, "score": 100}, "title": "Minotaur Conqueror"},
    "2": {"name": "Dark Knight", "hp": 350, "attack": 60, "reward": {"gold": 300, "exp": 400, "score": 150}, "title": "Dark Knight Slayer"},
    "3": {"name": "Hydra", "hp": 500, "attack": 75, "reward": {"gold": 450, "exp": 600, "score": 200}, "title": "Hydra Vanquisher"},
    "4": {"name": "Dragon King", "hp": 700, "attack": 90, "reward": {"gold": 700, "exp": 900, "score": 300}, "title": "Dragon Slayer"},
}


# ==================================================
# HELPER: AMBIL INVENTORY USER DARI DATABASE
# ==================================================
def get_inventory(character_id):
    cursor.execute("""
        SELECT si.item_name, si.item_type, i.quantity
        FROM inventory i
        JOIN shop_items si ON si.id = i.item_id
        WHERE i.character_id = %s
    """, (character_id,))
    return cursor.fetchall()


# ==================================================
# AKSI PERTEMPURAN (TURN-BASED)
# ==================================================
def quest_action_menu(character, enemy, is_boss=False):
    print(f"\n⚔️ Kamu menghadapi {'Boss ' if is_boss else ''}{enemy['name']}!")
    current_enemy_hp = enemy["hp"]

    sword_active = False
    armor_active = False

    while current_enemy_hp > 0 and character.hp > 0:
        print(f"\n=== STATUS ===")
        print(f"❤️ HP Kamu   : {character.hp}")
        print(f"💀 HP Musuh  : {current_enemy_hp}")

        print("\n=== AKSI ===")
        print("1. Menyerang")
        print("2. Gunakan Potion")
        print("3. Gunakan Armor (kurangi damage musuh)")
        print("4. Gunakan Sword (tambah damage serangan)")
        print("5. Menghindar (50% peluang berhasil)")

        action = input("Pilih aksi: ").strip()
        inventory = get_inventory(character.character_id)

        # =====================================
        # 1. MENYERANG
        # =====================================
        if action == "1":
            base_damage = character.damage + random.randint(-5, 10)
            total_damage = base_damage
            if sword_active:
                total_damage += 15  # efek Iron Sword aktif
                print("🗡️ Efek Sword aktif! Damage +15")

            current_enemy_hp -= total_damage
            print(f"\n🗡️ Kamu menyerang dan memberikan {total_damage} damage!")

            if current_enemy_hp <= 0:
                print(f"{enemy['name']} dikalahkan! 🎉")
                gain_rewards(character, enemy, is_boss)
                if is_boss:
                    level_up_floor(character, enemy["reward"], enemy["title"])
                break

        # =====================================
        # 2. GUNAKAN POTION
        # =====================================
        elif action == "2":
            potions = [item for item in inventory if item["item_type"] == "potion" and item["quantity"] > 0]
            if not potions:
                print("❌ Kamu tidak memiliki potion apa pun.")
                continue

            print("\n=== PILIH POTION ===")
            for idx, p in enumerate(potions, start=1):
                print(f"[{idx}] {p['item_name']} (x{p['quantity']})")

            try:
                potion_choice = int(input("Pilih potion: "))
                selected = potions[potion_choice - 1]
            except (ValueError, IndexError):
                print("Pilihan tidak valid.")
                continue

            heal = 50 if selected["item_name"] == "Health Potion" else 150
            character.hp += heal
            print(f"🧪 Kamu menggunakan {selected['item_name']} dan memulihkan {heal} HP!")

            cursor.execute("""
                UPDATE inventory 
                SET quantity = quantity - 1 
                WHERE character_id = %s 
                AND item_id = (SELECT id FROM shop_items WHERE item_name = %s)
            """, (character.character_id, selected["item_name"]))
            db.commit()

        # =====================================
        # 3. GUNAKAN ARMOR
        # =====================================
        elif action == "3":
            armor_items = [item for item in inventory if item["item_type"] == "armor" and item["quantity"] > 0]
            if not armor_items:
                print("❌ Kamu tidak memiliki armor apa pun.")
                continue

            for armor in armor_items:
                if armor["item_name"] == "Steel Armor":
                    armor_active = True
                    print("🛡️ Kamu mengenakan Steel Armor! Damage musuh berkurang 40.")
                    break
            else:
                print("⚠️ Kamu tidak memiliki armor yang bisa digunakan.")

        # =====================================
        # 4. GUNAKAN SWORD (aktifkan efek, tapi monster tetap menyerang)
        # =====================================
        elif action == "4":
            sword_items = [item for item in inventory if item["item_type"] == "weapon" and item["quantity"] > 0]
            if not sword_items:
                print("❌ Kamu tidak memiliki sword apa pun.")
            else:
                for sword in sword_items:
                    if sword["item_name"] == "Iron Sword":
                        sword_active = True
                        print("⚔️ Kamu mengaktifkan Iron Sword! Damage serangan meningkat 15.")
                        break
                else:
                    print("⚠️ Kamu tidak memiliki sword yang cocok.")

        # =====================================
        # 5. MENGHINDAR
        # =====================================
        elif action == "5":
            if random.random() < 0.5:
                print("💨 Kamu berhasil menghindari serangan musuh!")
                continue
            else:
                print("⚠️ Kamu gagal menghindar!")

        else:
            print("❌ Aksi tidak valid! Pilih 1-5.")
            continue

        # =====================================
        # SERANGAN BALIK MUSUH
        # =====================================
        if current_enemy_hp > 0:
            enemy_damage = enemy["attack"] + random.randint(-3, 5)
            if armor_active:
                enemy_damage = max(0, enemy_damage - 40)
                print("🛡️ Armor aktif! Damage musuh berkurang 40.")
            character.hp -= enemy_damage
            print(f"💥 {enemy['name']} menyerang dan memberikan {enemy_damage} damage!")

            if character.hp <= 0:
                print("\n💀 Kamu kalah dalam pertarungan! HP-mu tersisa 1.")
                character.hp = 1
                break

    cursor.execute("UPDATE characters SET hp = %s WHERE id = %s", (character.hp, character.character_id))
    db.commit()


# ==================================================
# HADIAH SETELAH MENANG
# ==================================================
def gain_rewards(character, enemy, is_boss=False):
    reward = enemy["reward"]
    character.gold += reward["gold"]
    character.exp += reward["exp"]
    character.score += reward["score"]

    cursor.execute("""
        UPDATE characters 
        SET gold = %s, exp = %s, score = %s
        WHERE id = %s
    """, (character.gold, character.exp, character.score, character.character_id))
    db.commit()

    update_player_score(character.character_id, reward["score"])

    print(f"\n🎁 Kamu mendapatkan hadiah:")
    print(f"  🪙 Gold : +{reward['gold']}")
    print(f"  ✨ EXP  : +{reward['exp']}")
    print(f"  🏅 Score: +{reward['score']}")
    if is_boss:
        print("  👑 Gelar (Title): Akan diberikan setelah Boss dikalahkan!")


# ==================================================
# LEVEL UP FLOOR & TITLE
# ==================================================
def level_up_floor(character, reward, title):
    character.floor += 1
    character.title = title
    cursor.execute("""
        UPDATE characters 
        SET floor = %s, title = %s
        WHERE id = %s
    """, (character.floor, title, character.character_id))
    db.commit()

    print(f"\n🏆 Selamat! Kamu naik ke Floor {character.floor}!")
    print(f"👑 Gelar baru: '{title}'")


# ==================================================
# MEMULAI QUEST
# ==================================================
def start_quest(character):
    while True:
        print("\n=== QUEST DIMULAI ===")
        print("Pilih jenis pertempuran:")
        print("[1] Monster biasa")
        print("[2] Boss battle")
        print("[0] Kembali")

        battle_choice = input("Pilih jenis quest: ").strip()

        if battle_choice == "1":
            print("\n=== PILIH MONSTER ===")
            for key, mon in MONSTERS.items():
                r = mon["reward"]
                print(f"[{key}] {mon['name']} (HP: {mon['hp']}, ATK: {mon['attack']}) "
                      f"=> Reward: +{r['exp']} EXP, +{r['gold']} Gold, +{r['score']} Score")

            choice = input("Pilih monster: ").strip()
            enemy = MONSTERS.get(choice)
            if not enemy:
                print("Pilihan tidak valid.")
                continue

            print(f"\n⚔️ Kamu melawan {enemy['name']}!")
            quest_action_menu(character, enemy, is_boss=False)

        elif battle_choice == "2":
            print("\n=== PILIH BOSS ===")
            for key, boss in BOSSES.items():
                r = boss["reward"]
                print(f"[{key}] {boss['name']} (HP: {boss['hp']}, ATK: {boss['attack']}) "
                      f"=> Reward: +{r['exp']} EXP, +{r['gold']} Gold, +{r['score']} Score, Title: '{boss['title']}'")

            choice = input("Pilih boss: ").strip()
            boss = BOSSES.get(choice)
            if not boss:
                print("Pilihan tidak valid.")
                continue

            print(f"\n🔥 Kamu menantang Boss {boss['name']}! Bersiaplah!")
            quest_action_menu(character, boss, is_boss=True)

        elif battle_choice == "0":
            break
        else:
            print("⚠ Input tidak valid.")