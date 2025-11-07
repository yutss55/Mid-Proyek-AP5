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
```python manage.py make:model|controller|view <name>```

Contoh :
```python manage.py make:view user```

_* File manage.py digunakan untuk membuat file baru (model, controller, atau view) secara otomatis agar struktur project tetap rapi dan konsisten._

## Setup Database (Local MySQL)
_* Project ini menggunakan MySQL lokal untuk menyimpan data user, karakter, dan item game._

### Lokasi File
Semua pengaturan database ada di:
utils/database.py

### Konfigurasi awal
Sebelum menjalankan program:
1. Pastikan kamu sudah menginstall MySQL Server (XAMPP) dan mysql-connector-python. Jalankan di terminal:
```pip install mysql-connector-python```
2. Pastikan juga sudah menginstall python-dotenv yang digunakan untuk mengelola konfigurasi sensitif dengan file .env. Jalankan di terminal:
```pip install python-dotenv```
3. Pastikan server MySQL sudah aktif dengan menggunakan XAMPP (Jalankan Apache dan MySQL).
4. Buat file `.env` berdasarkan `.env.example` dengan cara jalankan perintah di terminal:
```copy .env.example .env```

## Membuat Database & Tabel
_* Di dalam file database.py, semua perintah SQL untuk membuat database dan tabel sudah disiapkan, tapi dalam keadaan dikomentari agar bisa dijalankan satu per satu secara manual.
Tujuannya supaya bisa mengontrol tiap tahap pembuatan, dan tahu kalau ada error di bagian tertentu._

1. Buat Database
- Buka database.py
- Un-comment bagian line 22-23
- Jalankan di terminal:
```python utils/database.py```
- Setelah muncul pesan "Database berhasil dibuat", kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.
- Kemudian pada line 12, ubah menjadi seperti ini:
```database=os.getenv("DB_NAME"),```

2. Buat Tabel Users
- Un-comment bagian line 27-33
- Jalankan kembali:
```python utils/database.py```
- Cek di phpMyAdmin untuk memastikan tabel users sudah ada.
- Jika sudah ada, kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.

3. Buat Tabel Characters
- Un-comment bagian line 36-53
- Un-comment bagian line 36-54
- Jalankan kembali:
```python utils/database.py```
- Cek di phpMyAdmin untuk memastikan tabel users sudah ada.
- Jika sudah ada, kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.

3. Buat Tabel Inventory
- Un-comment bagian line 57-65
- Jalankan kembali:
```python utils/database.py```
- Cek di phpMyAdmin untuk memastikan tabel users sudah ada.
- Jika sudah ada, kembalikan komentar (#) agar tidak terbuat ulang setiap kali dijalankan.

### Catatan :
- Ubah isi atau struktur tabel jika diperlukan, misalnya menambahkan dan menghapus kolom baru, mengubah tipe data, atau menyesuaikan relasi sesuai kebutuhan fiturnya.
- Jalankan satu per satu agar mudah mendeteksi error.
- Setelah tabel berhasil dibuat, biarkan semua dalam kondisi dikomentari agar tidak duplikat saat file di-run ulang.
- Kalau ada error seperti "database doesn't exist", pastikan database-nya sudah dibuat di langkah pertama.

# Selamat bekerja guyss