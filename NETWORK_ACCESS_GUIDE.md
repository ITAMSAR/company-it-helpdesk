# Panduan Akses dari Jaringan Lokal

## Cara Akses IT Hub Internal dari Laptop/Device Lain

### Langkah 1: Setup Firewall (Hanya Sekali)

1. **Klik kanan** file `SETUP_FIREWALL.bat`
2. Pilih **"Run as administrator"**
3. Klik **Yes** pada UAC prompt
4. Tunggu sampai muncul pesan "SUCCESS!"

### Langkah 2: Jalankan Server dalam Mode Network

1. Double-click file `run_network.bat`
2. Server akan berjalan di `0.0.0.0:8000`
3. Jangan tutup window command prompt

### Langkah 3: Akses dari Laptop

Dari laptop/device lain di jaringan yang sama, buka browser dan ketik:

```
http://192.168.1.4:8000
```

**PENTING:** Ganti `192.168.1.4` dengan IP address PC kamu jika berbeda!

## Cara Cek IP Address PC

Jika IP address PC berubah, cek dengan cara:

1. Buka Command Prompt
2. Ketik: `ipconfig`
3. Cari "IPv4 Address" di bagian adapter yang aktif
4. Gunakan IP tersebut untuk akses dari laptop

## Troubleshooting

### Tidak Bisa Akses dari Laptop

**Problem 1: Connection Timeout**
- Pastikan firewall sudah di-setup (jalankan SETUP_FIREWALL.bat as admin)
- Cek apakah PC dan laptop di jaringan WiFi/LAN yang sama
- Coba matikan antivirus sementara untuk test

**Problem 2: IP Address Berubah**
- IP address bisa berubah setiap restart PC
- Cek IP terbaru dengan `ipconfig`
- Update URL di browser laptop

**Problem 3: Server Not Running**
- Pastikan `run_network.bat` masih berjalan di PC
- Jangan tutup window command prompt
- Cek apakah ada error di console

### Cek Koneksi dari Laptop

Buka Command Prompt di laptop dan test:

```bash
ping 192.168.1.4
```

Jika berhasil ping, berarti koneksi network OK.

## Akses URL

### Dari PC (Host):
- http://127.0.0.1:8000
- http://localhost:8000
- http://192.168.1.4:8000

### Dari Laptop/Device Lain:
- http://192.168.1.4:8000

## Keamanan

**CATATAN PENTING:**
- Server ini hanya untuk development/internal use
- Jangan expose ke internet publik
- Hanya bisa diakses dari jaringan lokal (LAN/WiFi yang sama)
- Untuk production, gunakan proper web server (Apache/Nginx)

## Static Files

Jika CSS/JS tidak load dari laptop, jalankan:

```bash
python manage.py collectstatic --noinput
```

## Tips

1. **IP Statis:** Untuk menghindari IP berubah-ubah, set static IP di router untuk PC kamu
2. **Bookmark:** Save URL `http://192.168.1.4:8000` di bookmark laptop
3. **Auto-start:** Bisa buat shortcut `run_network.bat` di Startup folder untuk auto-run saat PC nyala

## File Penting

- `run_network.bat` - Jalankan server dalam mode network
- `SETUP_FIREWALL.bat` - Setup firewall (run as admin, sekali saja)
- `run.bat` - Jalankan server normal (hanya localhost)
