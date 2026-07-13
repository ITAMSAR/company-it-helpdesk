# 📦 IT Hub Inventory Management System

Django inventory management dengan QR code scanning dan multiple photos.

## 🚀 Quick Setup

```bash
# 1. Run migrations
python manage.py migrate inventory

# 2. Start server
python manage.py runserver 0.0.0.0:9000

# 3. Access system
# Web: http://localhost:9000/inventory/
# Mobile test: http://192.168.100.89:9000/inventory/test-mobile/
```

## ✨ Features

### Multiple Photos
- Upload multiple photos per item
- Positions: Depan, Belakang, Kiri, Kanan, Atas, Bawah, Detail
- Auto-compress (~400KB per photo)
- Gallery slider dengan swipe support

### QR Code System  
- Auto-generate QR per item
- Mobile scanning interface
- Auto IP detection (no manual config)

### Inventory Management
- Categories, status tracking
- Bulk operations
- Admin interface

## 📱 Usage

**Upload Photos:**
1. Create/edit item → Click "Tambah Foto"
2. Select position & add caption
3. Repeat for multiple photos

**QR Scanning:**
1. Generate QR (green button)
2. Scan dengan HP (same WiFi)
3. View gallery dengan swipe

## 🔧 Tech Stack

- Django 5.0, Python 3.11+
- Pillow (image compression)
- Bootstrap 5, JavaScript
- Auto IP detection system

## 🌐 Network Setup

System auto-detects IP untuk QR codes. For static IP:

**Router DHCP Reservation (Recommended):**
1. Get MAC: `ipconfig /all`
2. Router admin → DHCP → Reservation
3. Add MAC-to-IP mapping

## 🐛 Troubleshooting

**QR tidak bisa diakses:** Check same WiFi, test `/inventory/test-mobile/`  
**Upload gagal:** Max 3MB per photo, use JPG format  
**IP berubah:** System auto-detects (no action needed)

---

**Version:** 2.0 | **Updated:** July 2026