# IT Hub Internal - Dashboard Internal IT

Dashboard internal untuk manajemen IT yang mencakup manajemen email karyawan, inventaris peralatan, sistem tiketing, dan reminder pengecekan jaringan.

## ⚠️ PENTING: Cek Python Version Dulu!

**Aplikasi ini butuh Python 3.8 - 3.12**

```bash
python --version
```

- ✅ Python 3.10, 3.11, 3.12 → **PERFECT!**
- ⚠️ Python 3.14 → **Terlalu baru!** Install Python 3.11 atau 3.12
- ❌ Python 3.7 atau lebih lama → **Upgrade Python**

**Download Python:** https://www.python.org/downloads/

## 🚀 Quick Start

### Windows (Termudah):
```bash
# 1. Double-click:
scripts\IT_DASHBOARD.bat

# 2. Untuk setup pertama kali, pilih menu:
6

# 3. Untuk menjalankan server, pilih menu:
1

# 4. Buka browser:
http://127.0.0.1:9000
```

### Manual:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Migrasi database (PENTING!)
python manage.py makemigrations
python manage.py migrate

# 3. Buat admin
python manage.py createsuperuser
# Password tidak terlihat saat diketik - ini normal!

# 4. Jalankan server
python manage.py runserver

# 5. Buka browser
http://127.0.0.1:9000
```

## 🌐 Akses dari Jaringan Lokal

Untuk akses dari laptop/device lain di jaringan yang sama:

```bash
# 1. Setup firewall (sekali saja, run as admin):
scripts\IT_DASHBOARD.bat
# lalu pilih menu 12

# 2. Jalankan server dalam mode network:
scripts\IT_DASHBOARD.bat
# lalu pilih menu 2

# 3. Akses dari device lain:
http://[IP-ADDRESS-PC]:9000
```

Lihat **docs/NETWORK_ACCESS_GUIDE.md** untuk panduan lengkap.

## 🎯 Fitur Utama

1. **Manajemen Email Karyawan**
   - Track email dengan password protection
   - Password hanya bisa dilihat admin dengan verifikasi
   - Export ke Excel (tanpa password)

2. **Inventaris IT**
   - Kategori dinamis (CPU, Laptop, Monitor, dll)
   - Filter by kategori dan status
   - Export ke Excel

3. **Sistem Tiketing**
   - User buat tiket, admin kelola
   - Status: Baru, Sedang Dikerjakan, Selesai, Tidak Selesai
   - Catatan untuk setiap perubahan status
   - Export ke Excel

4. **Reminder Jaringan**
   - Pengingat cek jaringan harian
   - Statistik pengecekan (hari ini, minggu ini, total)
   - Filter riwayat
   - Export ke Excel

## 🔧 Troubleshooting

### Error: "no such table"
```bash
python manage.py migrate
# Atau: scripts\IT_DASHBOARD.bat
```

### Error: "Pillow failed to build"
Python 3.14 terlalu baru. Solusi:
1. Install Python 3.11 atau 3.12 (recommended)
2. Atau: `pip install -r requirements-minimal.txt`

### Password tidak terlihat saat buat admin
Ini NORMAL untuk keamanan. Ketik saja (meskipun tidak terlihat) lalu Enter.

### Port 9000 sudah dipakai
```bash
python manage.py runserver 8001
```

### Lupa password admin
```bash
python manage.py changepassword admin
```

### Tidak bisa akses dari laptop
1. Pastikan firewall sudah di-setup (scripts\IT_DASHBOARD.bat as admin)
2. Pastikan PC dan laptop di jaringan yang sama
3. Pilih menu `2` untuk server network / LAN
4. Lihat docs/NETWORK_ACCESS_GUIDE.md

## 📚 Dokumentasi

- **README.md** - Quick start & overview
- **docs/QUICK_START.md** - Panduan instalasi detail
- **docs/PANDUAN_PENGGUNAAN.md** - User manual lengkap
- **docs/FAQ.md** - Pertanyaan umum
- **docs/COMMON_ISSUES.md** - Masalah umum & solusi
- **docs/DATABASE_MIGRATION_GUIDE.md** - Panduan update database
- **docs/NETWORK_ACCESS_GUIDE.md** - Akses dari jaringan lokal

## Tools

Semua command Windows sekarang digabung di satu launcher:

- `scripts\IT_DASHBOARD.bat` - menu setup, start server, migrate, user management, firewall, dan reset database

## Dependencies

- Django >= 5.0, < 5.1
- Pillow >= 10.0
- django-crontab >= 0.7.1
- python-decouple >= 3.8
- openpyxl >= 3.1.0

## 📝 Teknologi

- Django 5.0.1
- Bootstrap 5
- SQLite (development)
- Python 3.8 - 3.12

## 🔒 Keamanan

- Password email terenkripsi
- Admin password verification untuk lihat password
- CSRF protection
- Session-based authentication
- Network access hanya untuk LAN (tidak untuk internet publik)

## 📄 License

MIT License - Gratis untuk digunakan dan dimodifikasi

---

**Dibuat dengan ❤️ untuk Tim IT**
