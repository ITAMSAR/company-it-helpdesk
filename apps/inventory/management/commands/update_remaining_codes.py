from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Update kode untuk router, lemari, telepon, lemari rak, tablet'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Memulai update kode inventaris untuk kategori lainnya...\n')
        
        # Daftar kategori yang akan diupdate
        categories_to_update = [
            {'search': 'router', 'code': 'ROUTER'},
            {'search': 'lemari', 'code': 'LEMARI'},
            {'search': 'telepon', 'code': 'TELEPON'},
            {'search': 'rak', 'code': 'RAK'},
            {'search': 'tablet', 'code': 'TABLET'},
        ]
        
        total_updated = 0
        
        for cat_info in categories_to_update:
            search_term = cat_info['search']
            code_prefix = cat_info['code']
            
            self.stdout.write(f'📂 Mencari kategori: {search_term}...')
            
            # Cari kategori berdasarkan nama
            categories = EquipmentCategory.objects.filter(name__icontains=search_term)
            
            if not categories.exists():
                self.stdout.write(self.style.WARNING(f'   ⚠️  Kategori "{search_term}" tidak ditemukan\n'))
                continue
            
            for category in categories:
                self.stdout.write(f'   📁 Kategori ditemukan: {category.name}')
                
                # Ambil semua item di kategori ini
                items = Equipment.objects.filter(category=category).order_by('id')
                
                if not items.exists():
                    self.stdout.write(f'   ⚠️  Tidak ada item di kategori {category.name}\n')
                    continue
                
                self.stdout.write(f'   📊 Ditemukan {items.count()} item')
                self.stdout.write('   ' + '=' * 60)
                
                # Update kode satu per satu
                updated_count = 0
                for index, item in enumerate(items, 1):
                    old_code = item.inventory_code
                    new_code = f"APM/{code_prefix}/{index:03d}"
                    
                    # Cek apakah kode sudah ada
                    if Equipment.objects.filter(inventory_code=new_code).exclude(id=item.id).exists():
                        # Cari nomor yang belum dipakai
                        counter = index
                        while Equipment.objects.filter(inventory_code=f"APM/{code_prefix}/{counter:03d}").exclude(id=item.id).exists():
                            counter += 1
                        new_code = f"APM/{code_prefix}/{counter:03d}"
                    
                    item.inventory_code = new_code
                    item.save()
                    
                    self.stdout.write(f'   {index:2d}. {old_code:20s} → {new_code}')
                    updated_count += 1
                
                self.stdout.write('   ' + '=' * 60)
                self.stdout.write(self.style.SUCCESS(f'   ✅ Berhasil update {updated_count} item di kategori {category.name}\n'))
                total_updated += updated_count
        
        # Update kategori lain yang mungkin terlewat
        self.stdout.write('🔍 Mencari kategori lain yang belum diupdate...')
        
        # Cari semua kategori yang itemnya belum menggunakan format APM
        all_categories = EquipmentCategory.objects.all()
        
        for category in all_categories:
            # Skip kategori yang sudah diproses
            if any(search in category.name.lower() for search in ['kursi', 'meja', 'ac', 'printer', 'router', 'lemari', 'telepon', 'rak', 'tablet']):
                continue
            
            # Cek apakah ada item yang belum menggunakan format APM
            old_format_items = Equipment.objects.filter(
                category=category
            ).exclude(inventory_code__startswith='APM/').order_by('id')
            
            if old_format_items.exists():
                category_code = category.name.split()[0].upper()
                self.stdout.write(f'   📁 Kategori: {category.name} ({old_format_items.count()} item)')
                
                for index, item in enumerate(old_format_items, 1):
                    old_code = item.inventory_code
                    
                    # Cari nomor urut yang belum dipakai
                    counter = 1
                    while Equipment.objects.filter(inventory_code=f"APM/{category_code}/{counter:03d}").exists():
                        counter += 1
                    
                    new_code = f"APM/{category_code}/{counter:03d}"
                    item.inventory_code = new_code
                    item.save()
                    
                    self.stdout.write(f'     {index}. {old_code} → {new_code}')
                    total_updated += 1
        
        self.stdout.write(f'\n🎉 SELESAI! Total {total_updated} kode inventaris berhasil diupdate!')
        self.stdout.write('📋 Semua kode inventaris sekarang menggunakan format APM/KATEGORI/XXX')