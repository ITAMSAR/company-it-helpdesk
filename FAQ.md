# Frequently Asked Questions (FAQ)

## Instalasi & Setup

### Q: Password tidak terlihat saat membuat superuser, apakah keyboard saya rusak?
**A:** Tidak rusak! Ini fitur keamanan standar. Saat Anda mengetik password, karakter memang tidak akan terlihat di layar. Ketik saja password Anda (meskipun tidak terlihat) lalu tekan Enter. Anda akan diminta mengetik 2 kali untuk konfirmasi.

**Tips:** Gunakan password yang mudah diingat untuk development, atau ketik di notepad dulu lalu copy-paste.

### Q: Apakah saya perlu install database terpisah?
**A:** Tidak untuk development. Aplikasi menggunakan SQLite yang sudah built-in di Python. Untuk production, disarankan menggunakan PostgreSQL.

### Q: Berapa lama proses instalasi?
**A:** Sekitar 5-10 menit, tergantung kecepatan internet untuk download dependencies.

### Q: Apakah bisa dijalankan di Mac/Linux?
**A:** Ya! Aplikasi ini cross-platform. Untuk Mac/Linux, gunakan command manual di README.md (skip file .bat).

### Q: Error "Python not found" saat menjalankan setup.bat
**A:** Install Python dari python.org dan pastikan centang "Add Python to PATH" saat instalasi.

## Penggunaan

### Q: Bagaimana cara menambah user baru?
**A:** 
1. Login sebagai admin
2. Buka http://127.0.0.1:8000/admin
3. Klik "Users" → "Add User"
4. Isi username dan password
5. Save

### Q: User biasa bisa lihat tiket user lain?
**A:** Tidak. User biasa hanya bisa melihat tiket yang mereka buat sendiri. Hanya admin yang bisa melihat semua tiket.

### Q: Bagaimana cara mengubah status tiket?
**A:** Saat ini hanya bisa melalui Admin Panel. Login sebagai admin, buka Admin Panel, pilih tiket, dan ubah statusnya.

### Q: Apakah ada batasan ukuran file untuk lampiran tiket?
**A:** Default Django adalah 2.5MB. Bisa diubah di settings.py dengan menambahkan `DATA_UPLOAD_MAX_MEMORY_SIZE`.

### Q: Bagaimana cara backup data?
**A:** 
- Development (SQLite): Copy file `db.sqlite3`
- Production (PostgreSQL): Gunakan `pg_dump` (lihat DEPLOYMENT.md)

## Fitur

### Q: Apakah ada notifikasi email otomatis?
**A:** Belum ada di versi 1.0. Fitur ini ada di roadmap untuk versi 1.1.

### Q: Bisa export data ke Excel?
**A:** Belum ada di versi 1.0. Sementara bisa export dari Admin Panel atau copy-paste dari tabel.

### Q: Apakah ada mobile app?
**A:** Belum ada. Tapi web interface sudah responsive dan bisa diakses dari mobile browser.

### Q: Bagaimana cara mengaktifkan reminder otomatis?
**A:** Jalankan command: `python manage.py crontab add`. Ini akan setup cron job yang berjalan setiap Senin jam 09:00.

## Keamanan

### Q: Apakah password email tersimpan dengan aman?
**A:** Ya, password disimpan dalam field CharField. Untuk keamanan maksimal, disarankan menggunakan enkripsi tambahan atau vault service di production.

### Q: Bagaimana cara mengubah SECRET_KEY?
**A:** Edit file `itdashboard/settings.py`, ubah nilai `SECRET_KEY`. Untuk production, gunakan environment variable.

### Q: Apakah ada rate limiting untuk login?
**A:** Belum ada di versi 1.0. Bisa ditambahkan dengan package seperti `django-ratelimit`.

## Performance

### Q: Berapa banyak user yang bisa ditangani?
**A:** Untuk SQLite (development): ~100 concurrent users. Untuk PostgreSQL (production): ribuan users tergantung spesifikasi server.

### Q: Apakah perlu Redis atau Celery?
**A:** Tidak wajib untuk versi 1.0. Tapi disarankan untuk production dengan traffic tinggi.

### Q: Database semakin besar, bagaimana cara optimize?
**A:** 
1. Buat index di field yang sering di-query
2. Archive tiket lama
3. Compress lampiran
4. Gunakan PostgreSQL untuk performa lebih baik

## Troubleshooting

### Q: Error "CSRF verification failed"
**A:** 
1. Clear browser cookies
2. Pastikan `{% csrf_token %}` ada di semua form
3. Cek ALLOWED_HOSTS di settings.py

### Q: Static files tidak muncul setelah deploy
**A:** Jalankan `python manage.py collectstatic` dan pastikan Nginx/Apache dikonfigurasi dengan benar.

### Q: Error "OperationalError: no such table"
**A:** Jalankan migrasi: `python manage.py migrate`

### Q: Lupa password admin
**A:** Jalankan: `python manage.py changepassword username`

### Q: Port 8000 sudah digunakan
**A:** Gunakan port lain: `python manage.py runserver 8001`

## Development

### Q: Bagaimana cara menambah fitur baru?
**A:** 
1. Buat branch baru
2. Tambahkan model/view/template sesuai kebutuhan
3. Buat migration jika ada perubahan model
4. Test fitur
5. Commit dan buat pull request

### Q: Apakah ada API documentation?
**A:** Belum ada REST API di versi 1.0. Planned untuk versi 1.2.

### Q: Bisa integrate dengan sistem lain?
**A:** Ya, bisa. Untuk versi 1.0 bisa menggunakan Django signals atau custom management commands. Versi 1.2 akan ada REST API.

## Lisensi & Support

### Q: Apakah aplikasi ini gratis?
**A:** Ya, menggunakan MIT License. Gratis untuk digunakan dan dimodifikasi.

### Q: Dimana saya bisa dapat support?
**A:** Hubungi tim IT internal atau buat issue di repository project.

### Q: Boleh dimodifikasi untuk kebutuhan perusahaan?
**A:** Ya, silakan! MIT License memperbolehkan modifikasi dan distribusi.

---

**Tidak menemukan jawaban?** Buka issue di repository atau hubungi tim IT internal.
