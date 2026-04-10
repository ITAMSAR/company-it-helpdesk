from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment
import qrcode
import socket
import os

class Command(BaseCommand):
    help = 'Generate QR code untuk test dengan IP yang benar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--code',
            type=str,
            help='Kode inventaris untuk generate QR (opsional)',
        )

    def handle(self, *args, **options):
        # Get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "192.168.1.11"
        
        code = options.get('code')
        
        if code:
            # Generate QR untuk kode tertentu
            try:
                equipment = Equipment.objects.get(inventory_code=code)
                self.generate_qr_for_item(equipment, local_ip)
            except Equipment.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Barang dengan kode {code} tidak ditemukan!'))
                return
        else:
            # Generate QR untuk beberapa contoh
            sample_items = Equipment.objects.all()[:3]
            
            if not sample_items.exists():
                self.stdout.write(self.style.ERROR('❌ Tidak ada data equipment!'))
                return
            
            self.stdout.write(f'🔍 Generate QR code untuk test dengan IP: {local_ip}:8000\n')
            
            for item in sample_items:
                self.generate_qr_for_item(item, local_ip)
        
        self.stdout.write(f'\n✅ QR code berhasil di-generate!')
        self.stdout.write(f'📱 Test dengan buka: http://{local_ip}:8000/inventory/test-mobile/ di HP')
        self.stdout.write('🔧 Pastikan server berjalan dengan: START_NETWORK_SERVER.bat')
    
    def generate_qr_for_item(self, equipment, local_ip):
        # Create URL
        item_url = f"http://{local_ip}:8000/item/{equipment.inventory_code}/"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        
        qr.add_data(item_url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to file
        filename = f"QR-{equipment.inventory_code.replace('/', '_')}-{equipment.name.replace(' ', '_')[:20]}.png"
        img.save(filename)
        
        self.stdout.write(f'📦 {equipment.name}')
        self.stdout.write(f'   Kode: {equipment.inventory_code}')
        self.stdout.write(f'   URL:  {item_url}')
        self.stdout.write(f'   File: {filename}')
        self.stdout.write('')