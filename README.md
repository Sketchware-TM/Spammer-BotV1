# 🤖 Spammer-BotV1.2

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.2-blue?style=for-the-badge&logo=github">
  <img src="https://img.shields.io/badge/Node.js-18+-green?style=for-the-badge&logo=node.js">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram">
  <img src="https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase">
  <img src="https://img.shields.io/badge/License-MIT-orange?style=for-the-badge">
</p>

---

## 📖 Tentang Proyek

**Spammer-BotV1.2** adalah sistem lengkap untuk mengelola bot spam Telegram, dilengkapi dengan dashboard web yang aman dan obfuscator HTML berbasis AES‑GCM. Proyek ini terdiri dari:

- **Bot Telegram (Client)** – untuk owner mengelola user akses.
- **Web Dashboard** – antarmuka untuk mengirim spam, mengatur bot, dan melihat status.
- **Halaman Login** – autentikasi dengan sistem request ke owner.
- **Obfuscator HTML** – menyembunyikan kode sumber HTML dengan enkripsi AES‑GCM.

---

## ✨ Fitur Unggulan

### 🔐 Sistem Autentikasi & Manajemen Akses
- Pengguna dapat **meminta akses** ke owner melalui dashboard (index.html).
- Owner menerima notifikasi via bot, lalu mengatur password dan masa aktif.
- **Login** menggunakan password yang ditentukan.
- **Polling otomatis** untuk mendeteksi perubahan password atau masa aktif.
- **Logout paksa** jika password diubah atau akun dihapus.

### 🤖 Bot Telegram Client (Owner Only)
Bot berfungsi sebagai antarmuka admin untuk mengelola user di Supabase.

**Command yang tersedia:**
- `/listuser` – menampilkan daftar user (5 per halaman, dengan navigasi).
- `/setpassword <unique_id> <password_baru>` – mengatur password user.
- `/setexpiry <unique_id> <jumlah_hari>` – mengatur masa aktif (0 = unlimited).
- `/deluser <unique_id>` – menghapus user dari database.
- `/help` – menampilkan panduan.

### 🖥️ Web Dashboard Kontrol Penuh
Dashboard (`dashboard.html`) menyediakan antarmuka visual:

- **Spam Control**: atur token, chat ID, pesan, interval, jumlah, dan upload foto (max 3).
- **Tombol Start/Stop** dengan notifikasi realtime.
- **Change Bot Panel** – ubah nama, deskripsi, dan short description bot (menggunakan API Telegram).
- **Load Info Bot** – ambil data bot secara otomatis.
- **Reset Settings** – kembalikan ke default.

### 🔒 HTML Obfuscator (AES‑GCM)
Script Python `obf_html_v2.py` mengenkripsi file HTML dengan AES‑GCM dan menyisipkan kunci yang di-shuffle serta integrity check (SHA‑256).

```bash
python obf_html_v2.py input.html output.html <password>
```

Hasilnya adalah file HTML yang hanya bisa didekripsi oleh browser dengan password yang benar. Ini menyulitkan pembacaan kode sumber secara kasual.

⚠️ Obfuskasi bukan enkripsi permanen. Jangan gunakan untuk data yang benar-benar rahasia.

---

📂 Struktur Direktori

```
Spammer-BotV1/
├── BotClient.js                
├── package.json                
├── obf_html_v2.py              
├── index.html                  
├── dashboard.html             
├── config/
│   └── config.js               
└── vid/
    └ vid.mp4
```

---

⚙️ Instalasi & Persiapan

1. Prasyarat
   · Node.js 18+
   · npm
   · Python 3.x (untuk obfuscator)
   · Akun Supabase (PostgreSQL)
2. Clone Repository
   ```bash
   git clone https://github.com/Sketchware-TM/Spammer-BotV1.git
   cd Spammer-BotV1
   ```
3. Install Dependencies Node.js
   ```bash
   npm install
   ```
   Dependencies utama: telegraf, @supabase/supabase-js
4. Setup Supabase
   · Buat tabel users dengan kolom: id (uuid), unique_id (text), password (text), expires_at (timestamp), created_at (timestamp).
   · Buat tabel configbot dengan kolom: id (int), bot_token (text), owner_id (text) – isi id=1.
   · Salin URL dan anon key Supabase.
5. Konfigurasi
   · Buat file config/config.js (contoh):
     ```javascript
     const CONFIG = {
         SUPABASE_URL: 'https://your-project.supabase.co',
         SUPABASE_ANON_KEY: 'eyJhbGciOiJ...'
     };
     ```
   · Di BotClient.js, isi BOT_TOKEN dan OWNER_ID (atau ambil dari Supabase).

---

🚀 Cara Penggunaan

· Jalankan Bot
  ```bash
  node BotClient.js
  ```
  Bot akan online dan menerima perintah dari owner.
· Akses Dashboard
  Buka index.html di browser (atau hosting). Pengguna baru bisa request auth, owner akan menerima notifikasi dan mengatur password. Setelah login, akan diarahkan ke dashboard.html untuk mengirim spam.
· Obfuskasi HTML
  ```bash
  python obf_html_v2.py index.html index_obf.html "passwordku"
  python obf_html_v2.py dashboard.html dashboard_obf.html "passwordku"
  ```

---

🚨 Peringatan Penggunaan

Fitur spam dapat mengirim banyak pesan ke target. Gunakan dengan bijak dan hanya pada bot/grup yang Anda miliki atau memiliki izin.

Dilarang menggunakan untuk:

* Spam ke pengguna tanpa persetujuan.
* Mengganggu grup/channel orang lain.
* Aktivitas ilegal atau melanggar ketentuan Telegram.

Developer tidak bertanggung jawab atas penyalahgunaan.

---

📜 Lisensi

MIT License – bebas dimodifikasi dengan tetap mencantumkan hak cipta.

---

⚠️ Disclaimer
Proyek ini dibuat untuk tujuan pembelajaran dan pengujian pada lingkungan yang memiliki izin resmi. Pengguna bertanggung jawab penuh atas aktivitas yang dilakukan.

---

<p align="center">
  <b>Spammer-BotV1.2</b><br>
  © By Sketchware™ – All Rights Reserved
</p>