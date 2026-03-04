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
# Jika error, gunakan: pip install -r requirements-minimal.txt

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

## 🎯 Fitur Utama

1. **Manajemen Email Karyawan** - Track email dengan password terenkripsi
2. **Inventaris IT** - Monitor laptop, monitor, peralatan IT
3. **Sistem Tiketing** - User buat tiket, admin kelola
4. **Reminder Jaringan** - Pengingat cek jaringan dengan log history

## 🔧 Troubleshooting

### Error: "no such table"
```bash
# Jalankan migrasi:
python manage.py makemigrations
python manage.py migrate

# Atau double-click:
MIGRATE_NOW.bat
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

## 📚 Dokumentasi Lengkap

- **README.md** (file ini) - Quick start & troubleshooting
- **QUICK_START.md** - Panduan instalasi detail
- **PANDUAN_PENGGUNAAN.md** - User manual lengkap (Bahasa Indonesia)
- **FAQ.md** - Pertanyaan umum
- **COMMON_ISSUES.md** - Masalah umum & solusi
- **PYTHON_VERSION_GUIDE.md** - Panduan versi Python
- **INSTALL_TROUBLESHOOTING.md** - Troubleshooting instalasi

## 🛠️ Scripts Bantuan

- **setup.bat** - Setup otomatis
- **run.bat** - Jalankan server
- **MIGRATE_NOW.bat** - Fix database
- **fix_database.bat** - Fix database (alternatif)
- **check_setup.py** - Validasi setup

## 📞 Butuh Bantuan?

1. Baca **COMMON_ISSUES.md** untuk masalah umum
2. Baca **FAQ.md** untuk pertanyaan umum
3. Jalankan `python check_setup.py` untuk diagnosa
4. Baca error message dengan teliti

## 📝 Teknologi

- Django 5.0.1
- Bootstrap 5
- SQLite (development) / PostgreSQL (production)
- Python 3.8 - 3.12

## 📄 License

MIT License - Gratis untuk digunakan dan dimodifikasi

---

**Dibuat dengan ❤️ untuk Tim IT**
