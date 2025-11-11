# Controller untuk Quest
import random
from models.quest_model import QuestData
from controllers.leaderboard_controller import update_player_score
from utils.database import db, cursor

class QuestController:
    def __init__(self, character):
        self.character = character
        self.active_quest = None

    # Membuat quest baru
    def buat_quest(self):
        # Jika sudah menyelesaikan 3 quest biasa, munculkan quest boss
        if self.character.quest_selesai >= 3:
            self.buat_quest_boss()
            self.character.quest_selesai = 0  # reset setelah boss
            return

        tipe_quest = input("Pilih tipe quest (berburu/pengumpulan): ").strip().lower()
        kesulitan = random.choice(["mudah", "sedang", "sulit"])
        pengali = {"mudah": 1, "sedang": 1.5, "sulit": 2}[kesulitan]

        if tipe_quest == "berburu":
            musuh = random.choice(["goblin", "serigala", "bandit", "orc", "naga kecil"])
            reward_gold = int(random.randint(5, 15) * pengali)
            reward_exp = int(random.randint(10, 25) * pengali)
            quest = QuestData("berburu", f"Lawan {musuh}", reward_gold, reward_exp, kesulitan)
        else:
            material = random.choice(["kayu", "batu sihir", "herbal", "kulit binatang", "biji besi"])
            reward_gold = int(random.randint(3, 10) * pengali)
            reward_exp = int(random.randint(8, 20) * pengali)
            quest = QuestData("pengumpulan", f"Kumpulkan {material}", reward_gold, reward_exp, kesulitan)

        self.active_quest = quest
        print("\n🧭 Quest Baru Diterima!")
        quest.tampilkan_info_quest()

    # Membuat quest boss
    def buat_quest_boss(self):
        boss = random.choice(["Naga Api", "Raja Orc", "Iblis Kegelapan", "Hydra"])
        print("\n🔥 QUEST BOSS TERBUKA! 🔥")
        reward_gold = random.randint(50, 100)
        reward_exp = random.randint(150, 250)
        quest_boss = QuestData("boss", f"Kalahkan {boss}", reward_gold, reward_exp, "epik")
        self.active_quest = quest_boss
        self.character.bisa_lawan_boss = True
        quest_boss.tampilkan_info_quest()

    # Menyelesaikan quest
    def selesaikan_quest(self):
        if not self.active_quest:
            print("❌ Tidak ada quest aktif!\n")
            return

        print(f"Menjalankan quest: {self.active_quest.nama}...")
        hasil = random.choices(["berhasil", "gagal"], weights=[0.8, 0.2])[0]

        if hasil == "berhasil":
            # Tambahkan gold & exp
            self.character.gold += self.active_quest.reward_gold
            self.character.exp += self.active_quest.reward_exp
            print(f"✅ Quest berhasil! Kamu mendapat {self.active_quest.reward_gold} gold dan {self.active_quest.reward_exp} exp.")

            # Update skor setelah quest selesai
            update_score_after_quest(self.character, self.active_quest.kesulitan)

            # Cek apakah quest boss atau biasa
            if self.active_quest.tipe == "boss":
                self.level_up_setelah_boss()
            else:
                self.character.quest_selesai += 1
                print(f"📜 Quest selesai: {self.character.quest_selesai}/3 sebelum boss muncul.")
                print(f"🏆 Total Skor: {self.character.score}")

            # Simpan hasil perubahan karakter ke database
            self.update_character_database()

            # Update skor ke leaderboard
            update_player_score(self.character.user_id, self.character.score)

        else:
            print("❌ Quest gagal! Tidak mendapat hadiah.")

        self.active_quest = None
        print(f"💰 Gold: {self.character.gold} | ⭐ EXP: {self.character.exp} | 🏆 Skor: {self.character.score}\n")

    # Naik level setelah boss dikalahkan
    def level_up_setelah_boss(self):
        print("👑 Kamu mengalahkan BOS! Pengalaman dan hadiah besar diterima.")
        self.character.floor += 1
        self.character.title = random.choice(["Pahlawan", "Sang Penakluk", "Kesatria Agung", "Pembasmi Kegelapan"])
        self.character.bisa_lawan_boss = False
        print(f"🎉 LEVEL UP! Sekarang Floor {self.character.floor} - Gelar: {self.character.title}")
        print(f"🏆 Bonus Skor +100 (Total: {self.character.score})\n")

        # Update database setelah boss dikalahkan
        self.update_character_database()

    # Simpan hasil perubahan karakter ke database
    def update_character_database(self):
        try:
            sql = """
                UPDATE characters
                SET gold = %s,
                    exp = %s,
                    score = %s,
                    floor = %s,
                    title = %s
                WHERE user_id = %s
            """
            values = (
                self.character.gold,
                self.character.exp,
                self.character.score,
                self.character.floor,
                self.character.title,
                self.character.user_id
            )
            cursor.execute(sql, values)
            db.commit()
            print("💾 Data karakter berhasil diperbarui ke database.\n")
        except Exception as e:
            db.rollback()
            print(f"⚠️ Gagal memperbarui database: {e}\n")


# Fungsi tambahan untuk perhitungan skor otomatis
def update_score_after_quest(character, kesulitan_quest):
# Fungsi untuk memperbarui skor setelah menyelesaikan quest berdasarkan tingkat kesulitan
    score_map = {
        "mudah": 15,
        "sedang": 40,
        "sulit": 80,
        "epik": 300
    }

    score_gained = score_map.get(kesulitan_quest, 10)

    if hasattr(character, 'user_id'):
        character.score += score_gained
        update_player_score(character.user_id, character.score)
        print(f"🏆 Skor +{score_gained} (Total: {character.score})")

        try:
            cursor.execute(
                "UPDATE characters SET score = %s WHERE user_id = %s",
                (character.score, character.user_id)
            )
            db.commit()
            print("💾 Skor karakter berhasil disimpan ke database.\n")
        except Exception as e:
            db.rollback()
            print(f"⚠️ Gagal menyimpan skor ke database: {e}")
    else:
        print("⚠️ Character ID tidak ditemukan, skor tidak dapat diperbarui.")
