from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Update semua kode inventaris menjadi format APM/KATEGORI/XXX'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            help='Nama kategori yang ingin diupdate (opsional, kosongkan untuk semua kategori)',
        )

    def handle(self, *args, **options):
        category_name = options.get('category')
        
        if category_name:
            # Update kategori tertentu
            categories = EquipmentCategory.objects.filter(name__icontains=category_name)
            if not categories.exists():
                self.stdout.write(self.style.ERROR(f'Kategori "{category_name}" tidak ditemukan!'))
                return
        else:
            # Update semua kategori
            categories = EquipmentCategory.objects.all()
        
        total_updated = 0
        
        for category in categories:
            self.stdout.write(f'\n=== Memproses kategori: {category.name} ===')
            
            # Ambil semua equipment di kategori ini
            equipment_items = Equipment.objects.filter(category=category).order_by('id')
            
            if not equipment_items.exists():
                self.stdout.write(self.style.WARNING(f'Tidak ada data di kategori {category.name}'))
                continue
            
            # Generate kode kategori dari nama
            category_code = category.name.split()[0].upper()
            
            self.stdout.write(f'Ditemukan {equipment_items.count()} item')
            self.stdout.write(f'Kode kategori: {category_code}')
            
            # Update kode satu per satu
            updated_count = 0
            for index, item in enumerate(equipment_items, 1):
                old_code = item.inventory_code
                new_code = f"APM/{category_code}/{index:03d}"
                
                item.inventory_code = new_code
                item.save()
                
                self.stdout.write(f'{index}. {old_code} → {new_code}')
                updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Berhasil update {updated_count} item di kategori {category.name}!')
            )
            total_updated += updated_count
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 SELESAI! Total {total_updated} kode inventaris berhasil diupdate!')
        )