from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Update semua kode kursi menjadi format APM/KURSI/XXX'

    def handle(self, *args, **options):
        # Cari kategori kursi
        try:
            kursi_category = EquipmentCategory.objects.filter(name__icontains='kursi').first()
            if not kursi_category:
                self.stdout.write(self.style.ERROR('Kategori kursi tidak ditemukan!'))
                return
            
            # Ambil semua kursi
            kursi_items = Equipment.objects.filter(category=kursi_category).order_by('id')
            
            if not kursi_items.exists():
                self.stdout.write(self.style.WARNING('Tidak ada data kursi ditemukan!'))
                return
            
            self.stdout.write(f'Ditemukan {kursi_items.count()} kursi')
            self.stdout.write(f'Kategori: {kursi_category.name}')
            
            # Update kode satu per satu
            updated_count = 0
            for index, kursi in enumerate(kursi_items, 1):
                old_code = kursi.inventory_code
                new_code = f"APM/KURSI/{index:03d}"
                
                kursi.inventory_code = new_code
                kursi.save()
                
                self.stdout.write(f'{index}. {old_code} → {new_code}')
                updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Berhasil update {updated_count} kode kursi!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )