# Panduan Penggunaan IT Hub Internal

## Untuk Admin IT

### 1. Login sebagai Admin
- Gunakan akun superuser yang dibuat saat setup
- Akses: http://127.0.0.1:8000

### 2. Mengelola Email Karyawan
- Buka Admin Panel: http://127.0.0.1:8000/admin
- Pilih "Email Karyawan"
- Klik "Add Email Karyawan" untuk menambah data baru
- Isi semua field yang diperlukan
- Password email akan tersimpan terenkripsi

### 3. Mengelola Inventaris
- Dari dashboard, klik menu "Inventaris"
- Klik tombol "Tambah Peralatan"
- Isi form dengan data peralatan:
  - Nama Barang (contoh: Dell Latitude 5420)
  - Kode Inventaris (contoh: LAP001)
  - Kategori (Laptop, Monitor, dll)
  - Spesifikasi
  - Status (Tersedia, Dipinjam, Rusak, Servis)
  - Tanggal Pembelian
  - Garansi Sampai
- Klik "Simpan"

### 4. Mengelola Tiket
- Admin dapat melihat SEMUA tiket dari semua user
- Klik menu "Tiket" untuk melihat daftar
- Klik "Detail" untuk melihat informasi lengkap tiket
- Update status tiket melalui Admin Panel

### 5. Reminder Jaringan
- Klik menu "Reminder Jaringan"
- Setelah melakukan pengecekan, klik "Saya Sudah Cek"
- Tambahkan catatan jika diperlukan
- Riwayat pengecekan akan tersimpan

## Untuk User Biasa

### 1. Login
- Gunakan username dan password yang diberikan admin
- Akses: http://127.0.0.1:8000

### 2. Membuat Tiket
- Dari dashboard, klik menu "Tiket"
- Klik tombol "Buat Tiket Baru"
- Isi form:
  - Judul Tiket (ringkas dan jelas)
  - Deskripsi Masalah (detail masalah yang dialami)
  - Prioritas (Rendah, Sedang, Tinggi, Darurat)
  - Lampiran (opsional, untuk screenshot atau foto)
- Klik "Kirim Tiket"

### 3. Melihat Status Tiket
- Klik menu "Tiket"
- Anda hanya bisa melihat tiket yang Anda buat sendiri
- Klik "Detail" untuk melihat informasi lengkap
- Status tiket: Baru, Diproses, Selesai, Ditolak

### 4. Melihat Inventaris
- User biasa hanya bisa melihat inventaris (read-only)
- Tidak bisa menambah atau mengedit data

## Tips & Trik

### Pencarian Cepat
- Gunakan fitur search di halaman Tiket dan Inventaris
- Ketik kata kunci dan klik "Filter"

### Filter Data
- Gunakan dropdown filter untuk menyaring data berdasarkan status
- Kombinasikan dengan pencarian untuk hasil lebih spesifik

### Prioritas Tiket
- **Rendah**: Masalah minor, tidak urgent
- **Sedang**: Masalah normal, perlu ditangani
- **Tinggi**: Masalah penting, segera ditangani
- **Darurat**: Masalah kritis, harus segera ditangani

## Troubleshooting

### Lupa Password
- Hubungi admin IT untuk reset password
- Admin dapat reset melalui Admin Panel

### Tiket Tidak Muncul
- Pastikan Anda sudah login
- User biasa hanya bisa melihat tiket sendiri
- Refresh halaman atau logout-login kembali

### Upload Lampiran Gagal
- Pastikan ukuran file tidak terlalu besar (max 10MB)
- Format yang didukung: jpg, png, pdf, doc, docx

## Kontak Support
Jika ada masalah atau pertanyaan, hubungi:
- Email: it-support@company.com
- Extension: 1234
