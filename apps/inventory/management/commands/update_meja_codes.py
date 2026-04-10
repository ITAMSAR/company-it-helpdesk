from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Update semua kode meja menjadi format APM/MEJA/XXX'

    def handle(self, *args, **options):
        # Cari kategori meja
        try:
            meja_category = EquipmentCategory.objects.filter(name__icontains='meja').first()
            if not meja_category:
                self.stdout.write(self.style.ERROR('Kategori meja tidak ditemukan!'))
                return
            
            # Ambil semua meja
            meja_items = Equipment.objects.filter(category=meja_category).order_by('id')
            
            if not meja_items.exists():
                self.stdout.write(self.style.WARNING('Tidak ada data meja ditemukan!'))
                return
            
            self.stdout.write(f'🪑 Ditemukan {meja_items.count()} meja')
            self.stdout.write(f'📂 Kategori: {meja_category.name}')
            self.stdout.write('=' * 50)
            
            # Update kode satu per satu dengan pengecekan duplikat
            updated_count = 0
            for index, meja in enumerate(meja_items, 1):
                old_code = meja.inventory_code
                new_code = f"APM/MEJA/{index:03d}"
                
                # Cek apakah kode sudah ada
                if Equipment.objects.filter(inventory_code=new_code).exclude(id=meja.id).exists():
                    self.stdout.write(f'{index:2d}. {old_code:15s} → {new_code} (SKIP - sudah ada)')
                    continue
                
                meja.inventory_code = new_code
                meja.save()
                
                self.stdout.write(f'{index:2d}. {old_code:15s} → {new_code}')
                updated_count += 1
            
            self.stdout.write('=' * 50)
            self.stdout.write(
                self.style.SUCCESS(f'✅ Berhasil update {updated_count} kode meja!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )