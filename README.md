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
setup.bat

# 2. Ikuti instruksi, buat admin
# 3. Double-click:
run.bat

# 4. Buka browser:
http://127.0.0.1:8000
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
http://127.0.0.1:8000
```

## 🌐 Akses dari Jaringan Lokal

Untuk akses dari laptop/device lain di jaringan yang sama:

```bash
# 1. Setup firewall (sekali saja, run as admin):
SETUP_FIREWALL.bat

# 2. Jalankan server dalam mode network:
run_network.bat

# 3. Akses dari device lain:
http://[IP-ADDRESS-PC]:8000
```

Lihat **NETWORK_ACCESS_GUIDE.md** untuk panduan lengkap.

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
# Atau: UPDATE_DATABASE.bat
```

### Error: "Pillow failed to build"
Python 3.14 terlalu baru. Solusi:
1. Install Python 3.11 atau 3.12 (recommended)
2. Atau: `pip install -r requirements-minimal.txt`

### Password tidak terlihat saat buat admin
Ini NORMAL untuk keamanan. Ketik saja (meskipun tidak terlihat) lalu Enter.

### Port 8000 sudah dipakai
```bash
python manage.py runserver 8001
```

### Lupa password admin
```bash
python manage.py changepassword admin
```

### Tidak bisa akses dari laptop
1. Pastikan firewall sudah di-setup (SETUP_FIREWALL.bat as admin)
2. Pastikan PC dan laptop di jaringan yang sama
3. Gunakan `run_network.bat` bukan `run.bat`
4. Lihat NETWORK_ACCESS_GUIDE.md

## 📚 Dokumentasi

- **README.md** - Quick start & overview
- **QUICK_START.md** - Panduan instalasi detail
- **PANDUAN_PENGGUNAAN.md** - User manual lengkap
- **FAQ.md** - Pertanyaan umum
- **COMMON_ISSUES.md** - Masalah umum & solusi
- **INSTALL_TROUBLESHOOTING.md** - Troubleshooting instalasi
- **DATABASE_MIGRATION_GUIDE.md** - Panduan update database
- **NETWORK_ACCESS_GUIDE.md** - Akses dari jaringan lokal

## 🛠️ Scripts

**Setup & Run:**
- `setup.bat` - Setup otomatis (first time)
- `run.bat` - Jalankan server (localhost only)
- `run_network.bat` - Jalankan server (network access)

**Database:**
- `UPDATE_DATABASE.bat` - Update database schema
- `UPDATE_TICKET_STATUS.bat` - Update ticket status fields
- `RESTART_FRESH.bat` - Reset database (WARNING: hapus semua data!)

**Firewall:**
- `SETUP_FIREWALL.bat` - Setup firewall untuk network access (run as admin)

## 📦 Dependencies

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
