# 🚀 Panduan Menjalankan IT Dashboard Server

## 📁 File-file Penting

Di folder project ini ada 3 file batch yang memudahkan Anda:

- **`START_SERVER.bat`** - Untuk nyalain server
- **`STOP_SERVER.bat`** - Untuk matiin server
- **`CHECK_SERVER.bat`** - Untuk cek status server

## 🔥 Cara Nyalain Server (MUDAH!)

### Metode 1: Double-click File Batch
1. **Double-click `START_SERVER.bat`**
2. **Tunggu sampai muncul**: "Starting development server at http://0.0.0.0:8000/"
3. **Server siap digunakan!**

### Metode 2: Manual via Command Prompt
1. Buka **Command Prompt** atau **PowerShell**
2. Ketik: `cd "D:\Project Coding\company-it-helpdesk"`
3. Ketik: `python manage.py runserver 0.0.0.0:8000`
4. Tekan **Enter**

## 🛑 Cara Matiin Server

### Metode 1: Double-click File Batch
- **Double-click `STOP_SERVER.bat`**

### Metode 2: Manual
- Di window server yang terbuka, tekan **Ctrl + C**
- Atau tutup window command prompt

## 🔍 Cara Cek Status Server

### Metode 1: Double-click File Batch
- **Double-click `CHECK_SERVER.bat`**

### Metode 2: Manual
- Buka browser, ketik: `http://localhost:8000`
- Jika muncul halaman login = server aktif
- Jika error/tidak bisa akses = server mati

## 📱 URL Penting Setelah Server Nyala

| Fungsi | URL |
|--------|-----|
| **Dashboard Utama** | `http://192.168.1.11:8000` |
| **Inventory** | `http://192.168.1.11:8000/inventory/` |
| **Test Mobile** | `http://192.168.1.11:8000/inventory/test-mobile/` |
| **Admin Panel** | `http://192.168.1.11:8000/admin/` |

## 🔧 Troubleshooting

### Problem: "python tidak dikenali"
**Solusi**: Install Python atau tambahkan Python ke PATH

### Problem: "Port 8000 sudah digunakan"
**Solusi**: 
1. Jalankan `STOP_SERVER.bat`
2. Atau restart komputer
3. Atau ganti port: `python manage.py runserver 0.0.0.0:8001`

### Problem: "ModuleNotFoundError"
**Solusi**: Install dependencies:
```cmd
pip install django qrcode pillow openpyxl
```

### Problem: Server jalan tapi tidak bisa diakses dari HP
**Solusi**:
1. Pastikan HP dan laptop di WiFi yang sama
2. Cek Windows Firewall (matikan sementara untuk test)
3. Pastikan IP address benar (cek dengan `ipconfig`)

## 🎯 Tips Penting

1. **Jangan tutup window server** selama mau digunakan
2. **Server otomatis mati** kalau laptop dimatikan
3. **Setelah restart laptop**, jalankan lagi `START_SERVER.bat`
4. **Untuk akses dari HP**, pastikan WiFi sama
5. **IP bisa berubah** setelah restart router

## 🚨 Jika Ada Masalah

1. **Cek status** dengan `CHECK_SERVER.bat`
2. **Stop server** dengan `STOP_SERVER.bat`
3. **Start ulang** dengan `START_SERVER.bat`
4. **Restart laptop** jika masih bermasalah

## 📞 Quick Commands

```cmd
# Cek IP komputer
ipconfig

# Test server lokal
curl http://localhost:8000

# Lihat proses Python yang jalan
tasklist | findstr python
```

---
**💡 Tip**: Bookmark file ini untuk referensi cepat!