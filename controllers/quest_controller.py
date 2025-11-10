# Controller for quest
import random
from models.quest_model import QuestData
from controllers.leaderboard_controller import update_player_score

class QuestController:
    def __init__(self, character):
        self.character = character
        self.active_quest = None

    # Membuat quest baru
    def bikin_quest(self):
        # Jika sudah menyelesaikan 3 quest biasa, munculkan quest boss
        if self.character.quest_selesai >= 3:
            self.buat_quest_boss()
            self.character.quest_selesai = 0  # reset counter setelah boss
            return

        tipe_quest = random.choice(["berburu", "pengumpulan"])
        kesulitan = random.choice(["mudah", "sedang", "sulit"])
        pengali = {"mudah": 1, "sedang": 1.5, "sulit": 2}[kesulitan]

        if tipe_quest == "berburu":
            musuh = random.choice(["goblin", "serigala", "bandit", "orc", "naga kecil"])
            gold_reward = int(random.randint(5, 15) * pengali)
            exp_reward = int(random.randint(10, 25) * pengali)
            quest = QuestData("berburu", f"Lawan {musuh}", gold_reward, exp_reward, kesulitan)
        else:
            material = random.choice(["kayu", "batu sihir", "herbal", "kulit binatang", "biji besi"])
            gold_reward = int(random.randint(3, 10) * pengali)
            exp_reward = int(random.randint(8, 20) * pengali)
            quest = QuestData("pengumpulan", f"Kumpulkan {material}", gold_reward, exp_reward, kesulitan)

        self.active_quest = quest
        print("\n🧭 Quest Baru Diterima!")
        quest.tampilkan_info_quest()

    # Membuat quest boss
    def buat_quest_boss(self):
        bos = random.choice(["Naga Api", "Raja Orc", "Iblis Kegelapan", "Hydra"])
        print("\n🔥 QUEST BOSS TERBUKA! 🔥")
        hadiah_uang = random.randint(50, 100)
        hadiah_exp = random.randint(150, 250)
        quest_boss = QuestData("boss", f"Kalahkan {bos}", hadiah_uang, hadiah_exp, "epik")
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
            self.character.uang += self.active_quest.hadiah_uang
            self.character.pengalaman += self.active_quest.hadiah_exp
            print(f"✅ Quest berhasil! Kamu mendapat {self.active_quest.hadiah_uang} gold dan {self.active_quest.hadiah_exp} exp.")

            # Update skor setelah quest selesai
            update_score_after_quest(self.character, self.active_quest.kesulitan)

            # Tambahkan logika level up & boss
            if self.active_quest.tipe == "boss":
                self.level_up_setelah_boss()
            else:
                self.character.quest_selesai += 1
                print(f"📜 Quest selesai: {self.character.quest_selesai}/3 sebelum boss muncul.")
                print(f"🏆 Total Skor: {self.character.skor}")

            # Update skor ke leaderboard
            update_player_score(self.character.user_id, self.character.skor)

        else:
            print("❌ Quest gagal! Tidak mendapat hadiah.")

        self.active_quest = None
        print(f"💰 Gold: {self.character.uang} | ⭐ EXP: {self.character.pengalaman} | 🏆 Skor: {self.character.skor}\n")

    # Naik level setelah boss dikalahkan
    def level_up_setelah_boss(self):
        print("👑 Kamu mengalahkan BOS! Pengalaman dan hadiah besar diterima.")
        self.character.level += 1
        self.character.gelar = random.choice(["Pahlawan", "Sang Penakluk", "Kesatria Agung", "Pembasmi Kegelapan"])
        self.character.bisa_lawan_boss = False
        print(f"🎉 LEVEL UP! Sekarang Level {self.character.level} - Gelar: {self.character.gelar}")
        print(f"🏆 Bonus Skor +100 (Total: {self.character.skor})\n")

# Fungsi tambahan untuk perhitungan skor otomatis
def update_score_after_quest(character, kesulitan_quest):
    """
    Fungsi untuk update score setelah quest selesai berdasarkan kesulitan
    """
    score_map = {
        "mudah": 15,
        "sedang": 40,
        "sulit": 80,
        "epik": 300
    }

    score_gained = score_map.get(kesulitan_quest, 10)

    # Pastikan karakter punya atribut ID dan skor
    if hasattr(character, 'user_id'):
        if not hasattr(character, 'skor'):
            character.skor = 0

        character.skor += score_gained
        update_player_score(character.user_id, character.skor)
        print(f"🏆 Skor +{score_gained} (Total: {character.skor})")
    else:
        print("⚠️ Character ID tidak ditemukan, skor tidak dapat diupdate.")
