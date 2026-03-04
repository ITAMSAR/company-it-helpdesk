# Quick Start Guide - IT Hub Internal

## Instalasi Cepat (Windows)

### Cara Termudah - Gunakan Script Otomatis

1. **Install Python** (jika belum ada)
   - Download dari: https://www.python.org/downloads/
   - Centang "Add Python to PATH" saat install

2. **Jalankan Setup**
   - Double-click file `setup.bat`
   - Ikuti instruksi untuk membuat akun admin
   - Tunggu sampai selesai

3. **Jalankan Server**
   - Double-click file `run.bat`
   - Buka browser: http://127.0.0.1:8000

### Cara Manual

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python manage.py makemigrations
python manage.py migrate

# 3. Buat admin
python manage.py createsuperuser
# CATATAN: Password tidak terlihat saat diketik (ini normal untuk keamanan)

# 4. (Opsional) Buat data sample
python manage.py create_sample_data

# 5. Jalankan server
python manage.py runserver
```

## Login Pertama Kali

1. Buka: http://127.0.0.1:8000
2. Login dengan username dan password admin yang dibuat
3. Selesai! Anda sudah bisa menggunakan aplikasi

## Akses Admin Panel

- URL: http://127.0.0.1:8000/admin
- Gunakan akun superuser untuk login
- Di sini Anda bisa mengelola semua data

## Fitur Utama

### 1. Dashboard
- Lihat ringkasan data
- Statistik tiket dan inventaris

### 2. Inventaris
- Tambah/Edit peralatan IT
- Track status dan pengguna

### 3. Tiket
- Buat tiket pengaduan
- Monitor status penyelesaian

### 4. Reminder Jaringan
- Catat pengecekan jaringan
- Lihat riwayat pengecekan

## Tips

- **Admin**: Bisa akses semua fitur
- **User Biasa**: Hanya bisa buat dan lihat tiket sendiri
- **Buat User Baru**: Lewat Admin Panel → Users → Add

## Butuh Bantuan?

Lihat dokumentasi lengkap di:
- `README.md` - Instalasi detail
- `PANDUAN_PENGGUNAAN.md` - Cara pakai aplikasi
- `DEPLOYMENT.md` - Deploy ke production

## Troubleshooting Cepat

**Error: Python not found**
→ Install Python dan pastikan ada di PATH

**Error: No module named 'django'**
→ Jalankan: `pip install -r requirements.txt`

**Lupa password admin**
→ Jalankan: `python manage.py changepassword username`

**Port 8000 sudah dipakai**
→ Jalankan: `python manage.py runserver 8001`
