# Mid-Proyek-AP5
Tema : Gamifikasi;
Judul : ALTER EGO (ALTERnativE Game Oriented);

## Struktur Folder & Arsitektur MVC
_* Project ini menggunakan arsitektur MVC (Model-View-Controller) untuk memisahkan logika aplikasi, tampilan, dan pengendali alur data._

- models/ (Logika Database) : Berisi file-file yang mengatur struktur data, penyimpanan, dan operasi database. Setiap file model merepresentasikan satu entitas data.
- controllers/ (Penghubung Logic & Tampilan) : Berisi file yang mengatur alur antara models dan views, seperti mengambil data dari model lalu menampilkannya ke view. Controller juga menangani input user dari view sebelum dikirim ke model.
- views/ (Antarmuka Terminal) : Berisi kode tampilan teks dan menu interaktif untuk user di terminal. Semua input maupun output ke pengguna terjadi di sini.

## Cara menambahkan file pada folder controllers / models / views
Jadi, gunakan perintah berikut di terminal:
python manage.py make:model|controller|view <name>

Contoh :
python manage.py make:view user

_* File manage.py digunakan untuk membuat file baru (model, controller, atau view) secara otomatis agar struktur project tetap rapi dan konsisten._

## Setup Database (Local MySQL)
_* Project ini menggunakan MySQL lokal untuk menyimpan data user, karakter, dan item game._

### Lokasi File
Semua pengaturan database ada di:
utils/database.py

### Konfigurasi awal
Sebelum menjalankan program:
1. Pastikan kamu sudah menginstall MySQL Server (XAMPP) dan mysql-connector-python. Jalankan di terminal:
pip install mysql-connector-python
2. Pastikan juga sudah menginstall python-dotenv yang digunakan untuk mengelola konfigurasi sensitif dengan file .env. Jalankan di terminal:
pip install python-dotenv
3. Pastikan server MySQL sudah aktif dengan menggunakan XAMPP (Jalankan Apache dan MySQL).
4. Buat file .env berdasarkan .env.example dengan cara jalankan perintah di terminal:
copy .env.example .env

## Membuat Database & Tabel
_* Di dalam file database.py, semua perintah SQL untuk membuat database dan tabel sudah disiapkan, tapi dalam keadaan dikomentari agar bisa dijalankan satu per satu secara manual.
Tujuannya supaya bisa mengontrol tiap tahap pembuatan, dan tahu kalau ada error di bagian tertentu._

1. Buat Database
- Buka database.py
- Un-comment bagian line 22-23
- Jalankan di terminal:
python utils/database.py
- Setelah muncul pesan "Database berhasil dibuat", kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.
- Kemudian pada line 12, ubah menjadi seperti ini:
database=os.getenv("DB_NAME"),

2. Buat Tabel Users
- Un-comment bagian line 27-33
- Jalankan kembali:
python utils/database.py
- Cek di localhost untuk memastikan tabel users sudah ada.
- Jika sudah ada, kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.

3. Buat Tabel Characters
- Un-comment bagian line 36-51
- Jalankan kembali:
python utils/database.py
- Cek di localhost untuk memastikan tabel users sudah ada.
- Jika sudah ada, kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.

3. Buat Tabel Inventory
- Un-comment bagian line 54-62
- Jalankan kembali:
python utils/database.py
- Cek di localhost untuk memastikan tabel users sudah ada.
- Jika sudah ada, kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.

### Catatan :
- Ubah isi atau struktur tabel jika diperlukan, misalnya menambahkan dan menghapus kolom baru, mengubah tipe data, atau menyesuaikan relasi sesuai kebutuhan fiturnya.
- Jalankan satu per satu agar mudah mendeteksi error.
- Setelah tabel berhasil dibuat, biarkan semua dalam kondisi dikomentari agar tidak duplikat saat file di-run ulang.
- Kalau ada error seperti "database doesn't exist", pastikan database-nya sudah dibuat di langkah pertama.

# Cara Menjalankan Program :
Jalankan di terminal:
python main.py

# Deskripsi Program :
_* Proyek ini merupakan game berbasis console dengan sistem login, karakter, misi, shop, dan leaderboard.
User dapat membuat karakter, menjalankan misi, membeli item, mengelola inventory, serta bersaing di papan peringkat.
Game ini menggunakan struktur MVC (Model-View-Controller) dan terhubung dengan database MySQL._

# Fitur yang tersedia :

## 1. Login & Register
Fitur ini memungkinkan user untuk:
- Membuat akun baru (Register) dengan menginput username dan password.
- Masuk ke akun (Login) untuk melanjutkan progres permainan.
- Sistem melakukan validasi agar username tidak duplikat dan password tidak kosong.
- Setelah login berhasil, sistem akan mengenali user dan menampilkan menu utama.

## 2. Character Creation & Management
Pada fitur ini, user dapat membuat dan mengelola karakter utama. Terdapat lima kelas karakter dengan statistik unik masing-masing:
- Archmage
- Guardian
- Marksman
- Assassin
- Fighter

Saat karakter baru dibuat:
- Sistem otomatis memberikan item awal (Health Potion ×3 dan Iron Sword ×1).
- Data karakter tersimpan ke database (characters table).
- User hanya dapat memiliki satu karakter aktif pada satu akun.

_* Fitur ini juga mencakup untuk menampilkan status karakter (HP, Energy, Defense, Damage, dll)._

## 3. Quest
Fitur misi memungkinkan user untuk menjalankan pertempuran melawan musuh.
Tersedia dua jenis misi:
- Monster Biasa — pertempuran standar untuk mendapatkan exp dan gold.
- Boss Battle — tantangan lebih berat dengan hadiah lebih besar.

_* Setiap misi akan meningkatkan experience (EXP), floor, dan gold sesuai hasil pertempuran. Semakin tinggi floor yang dicapai, semakin banyak fitur dan item yang terbuka._

## 4. Shop
Di fitur ini user dapat membeli item menggunakan gold yang dimiliki karakter.
Beberapa ketentuan:
- Item yang tersedia berbeda tiap floor.
- Contoh:
Floor 1: hanya 2 item tersedia.
Floor 2 ke atas: item baru muncul secara bertahap.
- Setiap pembelian item otomatis menambah stok di inventory user.

## 5. Inventory
Menampilkan seluruh item yang dimiliki oleh karakter.
Fitur yang tersedia:
- Melihat daftar item beserta jenis dan deskripsinya.
- Menggunakan item, misalnya potion untuk menambah HP atau Energy.
- Menjual item ke toko dengan harga setengah dari harga beli.
Item disimpan dalam tabel inventory, terhubung dengan characters dan shop_items

## 6. Leaderboard
Fitur Leaderboard berfungsi untuk menampilkan 10 pemain terbaik berdasarkan peringkat skor (score) dan tingkat lantai (floor) tertinggi yang telah dicapai.
Sistem akan secara otomatis mengambil data dari tabel characters di database, kemudian:
- Mengurutkan pemain dari score tertinggi ke terendah.
- Jika terdapat skor yang sama, maka floor tertinggi digunakan sebagai penentu urutan berikutnya.
- Hanya 10 pemain teratas yang akan ditampilkan pada papan peringkat.

_* Tujuan dari fitur ini adalah untuk memberikan elemen kompetitif di antara pemain serta memotivasi user untuk terus meningkatkan kemampuan karakternya dan naik ke floor yang lebih tinggi._

## 7. Delete character & account
User memiliki dua opsi penghapusan:
- Delete Character — hanya menghapus karakter aktif beserta datanya (inventory, progress, dll).
- Delete Account — menghapus akun secara permanen dari database (termasuk karakter dan semua data terkait).
Sebelum penghapusan, sistem meminta konfirmasi agar tidak terjadi kesalahan.

# Komponen
- Gold : Mata uang untuk beli item (dari quest)
- EXP : Pengalaman dari quest (untuk future leveling)
- Floor : Level dungeon (naik setiap kalahkan boss)
- Title : Gelar karakter (berubah tiap naik floor)
- Score : Total skor untuk leaderboard
- Dari menyelesaikan quest
- Makin sulit quest, makin besar score

# Selamat bekerja guyss