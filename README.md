# 🤖 Spammer-BotV1

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge&logo=github">
  <img src="https://img.shields.io/badge/Node.js-18.x-green?style=for-the-badge&logo=node.js">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram">
  <img src="https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase">
  <img src="https://img.shields.io/badge/License-ISC-orange?style=for-the-badge">
</p>

<p align="center">
  <b>Bot Spammer Telegram V1</b>
</p>

---

## 📖 Tentang Proyek

**Spammer-BotV1** adalah aplikasi manajemen bot Telegram berbasis Node.js yang dilengkapi dengan dashboard web interaktif. Proyek ini dirancang untuk memudahkan pengujian dan pengelolaan bot Telegram, dengan sistem keamanan autentikasi berbasis Supabase dan fitur obfuskasi HTML tambahan.

**Teknologi Utama:**
- 🟢 **Backend:** Node.js, Telegraf
- 🗄️ **Database:** Supabase (PostgreSQL)
- 🎨 **Frontend:** HTML5, CSS3, Vanilla JavaScript
- 🐍 **Keamanan Tambahan:** Python (untuk obfuskasi HTML)

---

## ✨ Fitur Unggulan

### 🔐 Sistem Autentikasi & Manajemen Akses
Dashboard dilindungi oleh sistem autentikasi yang terintegrasi dengan Supabase. Pengguna dapat:
- Mengirimkan **permintaan akses** ke bot owner.
- **Login** menggunakan password yang telah ditentukan.
- Mendapatkan **session ID** unik untuk setiap sesi.
- Memiliki batas waktu akses (*expiry*) yang dapat diatur.
- Melakukan **logout** secara aman dari dashboard.

### 🤖 Bot Telegram Client (Owner Only)
Bot Telegram berfungsi sebagai antarmuka utama bagi owner untuk mengelola pengguna dan akses.

**Command yang tersedia:**
- `/setpassword <unique_id> <password_baru>` — Mengatur password pengguna.
- `/setexpiry <unique_id> <jumlah_hari>` — Mengatur masa aktif akses (gunakan `0` untuk akses tanpa batas).
- `/deluser <unique_id>` — Menghapus user dari database.
- `/help` — Menampilkan daftar perintah.

### 🖥️ Web Dashboard Kontrol Penuh
Dashboard web menyediakan antarmuka visual untuk mengontrol bot secara real-time:

- Mengatur **Bot Token** dan **Target Chat ID**.
- Memilih **Parse Mode** (HTML / Markdown).
- Menyusun **Pesan** yang akan dikirim.
- Mengunggah **Foto** untuk dikirim bersama pesan.
- Mengatur **Interval Pengiriman** dan **Jumlah Pesan**.
- **Change Bot** untuk mengganti akun bot.
- **Update Informasi Bot** secara langsung.

### 🔒 HTML Obfuscator (Opsional)
Proyek ini menyertakan script Python untuk melakukan obfuskasi sederhana pada file HTML.

```bash
python obf_html.py input.html output.html
```

Hasilnya adalah file HTML yang diubah menjadi kode hexadecimal escape sequence dan Base64, yang akan didecode ulang oleh browser menggunakan atob() dan document.write().

Catatan: Obfuskasi bukan enkripsi. Jangan menganggap HTML yang di-obfuscate sebagai data yang benar-benar rahasia. Ini hanya metode untuk menyulitkan pembacaan kode secara kasual.

---

📂 Struktur Direktori

```
Spammer-BotV1/
│
├── BotClient.js                # Main bot logic (Node.js)
├── package.json                # Dependencies & metadata
├── obf_html.py                 # Python script untuk obfuskasi HTML
├── index.html                  # Halaman login / landing
├── dashboard.html              # Halaman utama dashboard
│
├── config/
│   └── config.js               # Konfigurasi lokal
│
└── vid/
    ├── vid.mp4                 # Video pendukung (opsional)
```

---

⚙️ Instalasi & Persiapan

1. Prasyarat

· Node.js versi 18 atau lebih baru.
· npm (Node Package Manager).
· Python 3.x (jika ingin menggunakan obfuscator).

2. Clone Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd Spammer-BotV1
```

3. Install Dependencies

```bash
npm install
```

Dependency utama:

· telegraf — Framework bot Telegram.
· @supabase/supabase-js — Client Supabase untuk Node.js.

---

🚨 Peringatan Penggunaan

Fitur pada proyek ini dapat mengirimkan pesan berulang ke target Telegram. Harap gunakan dengan bijak.

Dilarang menggunakan proyek ini untuk:

* Spam ke pengguna tanpa persetujuan.
* Mengganggu grup/channel milik orang lain.
* Flooding layanan Telegram.
* Bypass sistem pembatasan Telegram.
* Aktivitas ilegal atau melanggar ketentuan layanan Telegram.

Developer tidak bertanggung jawab atas penyalahgunaan proyek ini. Gunakan hanya pada bot, chat, grup, atau lingkungan yang Anda miliki atau telah mendapatkan izin.

---

🔑 Keamanan Kredensial

JANGAN PERNAH mengunggah file konfigurasi yang berisi:

· BOT_TOKEN
· OWNER_ID
· Kredensial Supabase (URL & ANON_KEY)
· Password atau API key lainnya

Jika token bot Anda bocor:

1. Segera revoke/rotate token melalui BotFather.
2. Hapus credential dari riwayat Git (jika sudah terlanjur push).
3. Jangan hanya menghapus commit terakhir — pastikan token lama sudah tidak aktif.

---

📜 Lisensi

Proyek ini dilisensikan di bawah MIT License.
Pengguna bebas memodifikasi asal pencantumkan nana pemilik/copyright/hak cipta

---

⚠️ Disclaimer:

Proyek ini dibuat untuk tujuan pembelajaran, pengembangan, dan pengujian pada lingkungan yang memiliki izin resmi.

Dengan menggunakan proyek ini, pengguna bertanggung jawab penuh atas seluruh aktivitas yang dilakukan.
Gunakan dengan akal sehat.

---

<p align="center">
  <b>Spammer-BotV1</b><br>
  © By Sketchware™ All Rights Reserved
</p>