# ❓ Masalah Umum & Solusi Cepat

## 🔐 Password Tidak Terlihat Saat Diketik

### ❓ Pertanyaan:
"Saat buat superuser, saya tidak bisa mengetik password. Keyboard tidak berfungsi?"

### ✅ Jawaban:
**Ini NORMAL!** Password memang tidak terlihat saat diketik untuk keamanan.

### Cara yang Benar:
1. Ketik username → Enter
2. Ketik email (opsional) → Enter
3. Ketik password → **TIDAK TERLIHAT** → Enter
4. Ketik password lagi (konfirmasi) → **TIDAK TERLIHAT** → Enter
5. Selesai!

### Contoh:
```
Username: admin
Email address: admin@company.com
Password: ************  ← Anda ketik tapi tidak terlihat
Password (again): ************  ← Ketik lagi untuk konfirmasi
Superuser created successfully.
```

**Tips:**
- Ketik dengan hati-hati karena tidak terlihat
- Gunakan password yang mudah diingat untuk development
- Jika salah, ulangi dengan: `python manage.py createsuperuser`

---

## 🐍 Python 3.14 - Pillow Error

### ❓ Pertanyaan:
"Error: Failed to build 'Pillow'"

### ✅ Solusi:
Python 3.14 terlalu baru. Pilih salah satu:

**Opsi 1 (RECOMMENDED):**
Install Python 3.11 atau 3.12 dari python.org

**Opsi 2 (Quick Fix):**
```bash
pip install -r requirements-minimal.txt
```

**Opsi 3:**
```bash
pip install Django==5.0.1
pip install Pillow --upgrade
pip install django-crontab python-decouple
```

Baca: [PYTHON_VERSION_GUIDE.md](PYTHON_VERSION_GUIDE.md)

---

## 🚫 Port 8000 Already in Use

### ❓ Pertanyaan:
"Error: That port is already in use"

### ✅ Solusi:

**Opsi 1: Gunakan port lain**
```bash
python manage.py runserver 8001
```
Akses: http://127.0.0.1:8001

**Opsi 2: Kill process yang menggunakan port 8000**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Contoh:
# netstat -ano | findstr :8000
# TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING    12345
# taskkill /PID 12345 /F
```

---

## 📦 Module Not Found

### ❓ Pertanyaan:
"ModuleNotFoundError: No module named 'django'"

### ✅ Solusi:
```bash
# Install dependencies
pip install -r requirements.txt

# Atau install manual
pip install Django==5.0.1
```

---

## 🗄️ No Such Table

### ❓ Pertanyaan:
"OperationalError: no such table: users_employeeemail"

### ✅ Solusi:
Database belum di-migrate. Jalankan:

```bash
# Buat migration files
python manage.py makemigrations

# Jalankan migrasi
python manage.py migrate
```

**Penjelasan:**
- `makemigrations` = Buat file migrasi dari models
- `migrate` = Terapkan migrasi ke database (buat tabel)

**Setelah migrate, refresh browser Anda.**

---

## 🔑 Lupa Password Admin

### ❓ Pertanyaan:
"Saya lupa password admin yang saya buat"

### ✅ Solusi:

**Opsi 1: Reset password**
```bash
python manage.py changepassword admin
# Ganti 'admin' dengan username Anda
```

**Opsi 2: Buat admin baru**
```bash
python manage.py createsuperuser
```

---

## 🌐 Tidak Bisa Akses dari Browser

### ❓ Pertanyaan:
"Server running tapi browser tidak bisa akses"

### ✅ Solusi:

**Cek 1: Server benar-benar running?**
```bash
python manage.py runserver
# Harus muncul: Starting development server at http://127.0.0.1:8000/
```

**Cek 2: URL yang benar**
- ✅ http://127.0.0.1:8000
- ✅ http://localhost:8000
- ❌ http://127.0.0.1:8000/ (tanpa http)

**Cek 3: Firewall**
- Pastikan firewall tidak block port 8000
- Coba disable firewall sementara untuk test

---

## 📁 Static Files Tidak Muncul

### ❓ Pertanyaan:
"CSS/JS tidak load, tampilan berantakan"

### ✅ Solusi:

**Development:**
```bash
# Pastikan DEBUG=True di settings.py
# Restart server
python manage.py runserver
```

**Production:**
```bash
python manage.py collectstatic
```

---

## 🔐 CSRF Verification Failed

### ❓ Pertanyaan:
"CSRF verification failed. Request aborted."

### ✅ Solusi:

1. **Clear browser cookies**
   - Ctrl+Shift+Delete
   - Clear cookies untuk localhost

2. **Cek template**
   - Pastikan ada `{% csrf_token %}` di semua form

3. **Cek ALLOWED_HOSTS**
   - Di settings.py, pastikan ada `'localhost'` dan `'127.0.0.1'`

---

## 💾 Database Locked

### ❓ Pertanyaan:
"OperationalError: database is locked"

### ✅ Solusi:

**Opsi 1: Restart server**
```bash
# Ctrl+C untuk stop
# Jalankan lagi
python manage.py runserver
```

**Opsi 2: Tutup aplikasi lain yang akses database**
- Tutup DB Browser atau tools database lain
- Restart server

---

## 🖼️ Upload File Gagal

### ❓ Pertanyaan:
"File upload tidak berfungsi"

### ✅ Solusi:

**Cek 1: Folder media exists**
```bash
# Pastikan folder media/ ada
# Jika tidak, buat manual atau restart server
```

**Cek 2: Form encoding**
```html
<!-- Pastikan form punya enctype -->
<form method="post" enctype="multipart/form-data">
```

**Cek 3: File size**
- Default max: 2.5MB
- Untuk file lebih besar, update settings.py

---

## 🔄 Perubahan Code Tidak Muncul

### ❓ Pertanyaan:
"Saya sudah edit code tapi tidak berubah"

### ✅ Solusi:

1. **Restart server**
   ```bash
   # Ctrl+C untuk stop
   python manage.py runserver
   ```

2. **Hard refresh browser**
   - Ctrl+F5 (Windows)
   - Cmd+Shift+R (Mac)

3. **Clear browser cache**
   - Ctrl+Shift+Delete

4. **Cek file yang diedit**
   - Pastikan edit file yang benar
   - Cek path file

---

## 🐛 Error Setelah Update Code

### ❓ Pertanyaan:
"Setelah edit model, muncul error"

### ✅ Solusi:
```bash
# Buat dan jalankan migrasi
python manage.py makemigrations
python manage.py migrate
```

---

## 📱 Tampilan Mobile Berantakan

### ❓ Pertanyaan:
"Di HP tampilan tidak responsive"

### ✅ Solusi:

**Cek 1: Viewport meta tag**
```html
<!-- Harus ada di base.html -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Cek 2: Bootstrap loaded**
- Cek di browser console (F12)
- Pastikan tidak ada error loading CSS

**Cek 3: Clear cache**
- Clear browser cache di HP
- Hard refresh

---

## 🔍 Cara Debug Error

### Langkah-langkah Debug:

1. **Baca error message lengkap**
   - Jangan skip, baca dari atas sampai bawah
   - Cari line number dan file name

2. **Cek terminal/command prompt**
   - Error biasanya muncul di sini
   - Copy error message untuk search

3. **Cek browser console**
   - Tekan F12
   - Lihat tab Console
   - Cek error JavaScript atau network

4. **Jalankan check_setup.py**
   ```bash
   python check_setup.py
   ```

5. **Test satu-satu**
   - Isolate masalah
   - Test fitur satu per satu

---

## 📞 Masih Butuh Bantuan?

Jika masalah Anda tidak ada di sini:

1. ✅ Baca [FAQ.md](FAQ.md)
2. ✅ Baca [INSTALL_TROUBLESHOOTING.md](INSTALL_TROUBLESHOOTING.md)
3. ✅ Baca [PYTHON_VERSION_GUIDE.md](PYTHON_VERSION_GUIDE.md)
4. ✅ Jalankan `python check_setup.py`
5. ✅ Google error message lengkap
6. ✅ Buat issue di repository

---

## 💡 Tips Menghindari Masalah

1. ✅ Gunakan Python 3.11 atau 3.12
2. ✅ Update pip: `python -m pip install --upgrade pip`
3. ✅ Gunakan virtual environment
4. ✅ Backup database sebelum update
5. ✅ Baca dokumentasi sebelum mulai
6. ✅ Test di development dulu sebelum production
7. ✅ Commit code ke Git secara berkala

---

**Semoga membantu! 🚀**
