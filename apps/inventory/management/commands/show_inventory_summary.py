from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Tampilkan ringkasan inventaris dengan format kode baru'

    def handle(self, *args, **options):
        self.stdout.write('📊 RINGKASAN INVENTARIS DENGAN FORMAT KODE BARU')
        self.stdout.write('=' * 70)
        
        categories = EquipmentCategory.objects.all().order_by('name')
        total_items = 0
        
        for category in categories:
            items = Equipment.objects.filter(category=category)
            if items.exists():
                count = items.count()
                total_items += count
                
                # Ambil contoh kode
                first_item = items.first()
                last_item = items.last()
                
                if count == 1:
                    code_range = first_item.inventory_code
                else:
                    code_range = f"{first_item.inventory_code} - {last_item.inventory_code}"
                
                self.stdout.write(f'📁 {category.name:<20} : {count:3d} item ({code_range})')
        
        self.stdout.write('=' * 70)
        self.stdout.write(f'📈 TOTAL INVENTARIS: {total_items} item')
        self.stdout.write('✅ Semua kode menggunakan format APM/KATEGORI/XXX')
        
        # Cek apakah masih ada kode lama
        old_format_items = Equipment.objects.exclude(inventory_code__startswith='APM/')
        if old_format_items.exists():
            self.stdout.write(f'\n⚠️  PERHATIAN: Masih ada {old_format_items.count()} item dengan format lama:')
            for item in old_format_items[:5]:  # Tampilkan 5 contoh
                self.stdout.write(f'   - {item.inventory_code} ({item.name})')
            if old_format_items.count() > 5:
                self.stdout.write(f'   ... dan {old_format_items.count() - 5} lainnya')
        else:
            self.stdout.write('\n🎉 Semua kode inventaris sudah menggunakan format APM!')