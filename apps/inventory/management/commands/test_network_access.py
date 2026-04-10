from django.core.management.base import BaseCommand
import socket
import subprocess
import platform

class Command(BaseCommand):
    help = 'Test network access dan berikan instruksi lengkap'

    def handle(self, *args, **options):
        self.stdout.write('🔍 TESTING NETWORK ACCESS UNTUK QR CODE...\n')
        
        # Get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "192.168.1.1"
        
        self.stdout.write(f'🌐 IP Komputer: {local_ip}')
        self.stdout.write(f'🚀 Server harus berjalan di: {local_ip}:8000')
        
        # Test if port is open
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(1)
            result = test_socket.connect_ex((local_ip, 8000))
            test_socket.close()
            
            if result == 0:
                self.stdout.write(self.style.SUCCESS('✅ Port 8000 terbuka dan siap diakses!'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  Port 8000 tidak terbuka atau server belum jalan'))
        except:
            self.stdout.write(self.style.WARNING('⚠️  Tidak bisa test port 8000'))
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('📋 INSTRUKSI LENGKAP UNTUK QR CODE:')
        self.stdout.write('='*60)
        
        self.stdout.write('\n1️⃣ STOP SERVER YANG SEDANG BERJALAN:')
        self.stdout.write('   - Tekan Ctrl+C di terminal yang menjalankan server')
        self.stdout.write('   - Atau tutup command prompt yang menjalankan server')
        
        self.stdout.write('\n2️⃣ JALANKAN SERVER DENGAN NETWORK MODE:')
        self.stdout.write('   - Double click file: run_network.bat')
        self.stdout.write('   - ATAU jalankan command: python manage.py runserver 0.0.0.0:8000')
        self.stdout.write(f'   - Server akan berjalan di: {local_ip}:8000')
        
        self.stdout.write('\n3️⃣ CEK FIREWALL WINDOWS:')
        self.stdout.write('   - Buka Windows Defender Firewall')
        self.stdout.write('   - Allow Python atau Django melalui firewall')
        self.stdout.write('   - Atau disable firewall sementara untuk test')
        
        self.stdout.write('\n4️⃣ TEST KONEKSI DARI HP:')
        self.stdout.write(f'   - Buka browser HP, ketik: http://{local_ip}:8000/inventory/test-mobile/')
        self.stdout.write('   - Jika berhasil, akan muncul halaman "SERVER BERHASIL DIAKSES"')
        self.stdout.write('   - Jika gagal, cek jaringan WiFi dan firewall')
        
        self.stdout.write('\n5️⃣ GENERATE DAN TEST QR CODE:')
        self.stdout.write('   - Buka inventory di komputer')
        self.stdout.write('   - Klik tombol QR hijau pada barang')
        self.stdout.write('   - Download QR code PNG')
        self.stdout.write('   - Scan dengan HP')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('🔧 TROUBLESHOOTING:')
        self.stdout.write('='*60)
        
        self.stdout.write('\n❌ Jika HP tidak bisa akses:')
        self.stdout.write('   1. Pastikan HP dan komputer di WiFi yang sama')
        self.stdout.write('   2. Restart router WiFi')
        self.stdout.write('   3. Disable firewall Windows sementara')
        self.stdout.write('   4. Coba IP lain jika ada (ipconfig /all)')
        
        self.stdout.write('\n❌ Jika QR code tidak bisa dibuka:')
        self.stdout.write('   1. Generate QR code baru setelah server network jalan')
        self.stdout.write('   2. Pastikan URL di QR code menggunakan IP yang benar')
        self.stdout.write('   3. Test manual dengan ketik URL di browser HP')
        
        self.stdout.write(f'\n🎯 URL TEST MANUAL: http://{local_ip}:8000/inventory/test-mobile/')
        self.stdout.write('   Buka URL ini di HP untuk test koneksi!')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('✅ Setelah server network jalan, QR code akan berfungsi!')
        self.stdout.write('='*60)