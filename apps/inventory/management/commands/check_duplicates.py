from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment
from collections import Counter

class Command(BaseCommand):
    help = 'Cek dan perbaiki kode inventaris yang duplikat'

    def handle(self, *args, **options):
        # Ambil semua kode inventaris
        all_codes = list(Equipment.objects.values_list('inventory_code', flat=True))
        
        # Cari duplikat
        code_counts = Counter(all_codes)
        duplicates = [code for code, count in code_counts.items() if count > 1]
        
        if duplicates:
            self.stdout.write(self.style.WARNING(f'🚨 Ditemukan {len(duplicates)} kode duplikat:'))
            for code in duplicates:
                items = Equipment.objects.filter(inventory_code=code)
                self.stdout.write(f'   {code} ({items.count()} item):')
                for item in items:
                    self.stdout.write(f'     - ID: {item.id}, Nama: {item.name}, Kategori: {item.category.name}')
            
            # Perbaiki duplikat
            self.stdout.write('\n🔧 Memperbaiki duplikat...')
            for code in duplicates:
                items = Equipment.objects.filter(inventory_code=code).order_by('id')
                for index, item in enumerate(items):
                    if index > 0:  # Skip item pertama
                        # Generate kode baru
                        category_code = item.category.name.split()[0].upper()
                        
                        # Cari nomor urut yang belum dipakai
                        counter = 1
                        while True:
                            new_code = f"APM/{category_code}/{counter:03d}"
                            if not Equipment.objects.filter(inventory_code=new_code).exists():
                                break
                            counter += 1
                        
                        old_code = item.inventory_code
                        item.inventory_code = new_code
                        item.save()
                        self.stdout.write(f'   ✅ ID {item.id}: {old_code} → {new_code}')
        else:
            self.stdout.write(self.style.SUCCESS('✅ Tidak ada kode duplikat ditemukan!'))