from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment
import socket

class Command(BaseCommand):
    help = 'Test QR code system dan tampilkan contoh URL'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Testing QR Code System...\n')
        
        # Get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "192.168.1.1"
        
        self.stdout.write(f'🌐 IP Server Terdeteksi: {local_ip}:8000')
        
        # Ambil beberapa contoh equipment
        sample_equipment = Equipment.objects.all()[:5]
        
        if not sample_equipment.exists():
            self.stdout.write(self.style.ERROR('❌ Tidak ada data equipment untuk test!'))
            return
        
        self.stdout.write('\n📱 Contoh URL QR Code yang akan di-generate:')
        self.stdout.write('=' * 60)
        
        for equipment in sample_equipment:
            qr_url = f"http://{local_ip}:8000/item/{equipment.inventory_code}/"
            self.stdout.write(f'📦 {equipment.name}')
            self.stdout.write(f'   Kode: {equipment.inventory_code}')
            self.stdout.write(f'   URL:  {qr_url}')
            self.stdout.write('')
        
        self.stdout.write('=' * 60)
        self.stdout.write('✅ QR Code System siap digunakan!')
        self.stdout.write('\n📋 Cara test:')
        self.stdout.write('1. Buka inventory di browser komputer')
        self.stdout.write('2. Klik tombol QR hijau pada salah satu barang')
        self.stdout.write('3. Download file PNG QR code')
        self.stdout.write('4. Scan QR code dengan HP (pastikan 1 jaringan WiFi)')
        self.stdout.write('5. Browser HP akan membuka halaman detail barang')
        
        self.stdout.write(f'\n🔧 Test URL manual: http://{local_ip}:8000/inventory/test-mobile/')
        self.stdout.write('   (Buka di HP untuk test koneksi jaringan)')