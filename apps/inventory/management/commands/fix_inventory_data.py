from django.core.management.base import BaseCommand
from apps.inventory.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Fix inventory data: ubah bangku jadi kursi, update kode AC dan Router'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Memulai perbaikan data inventaris...\n')
        
        # 1. Ubah semua nama "Bangku" menjadi "Kursi"
        self.stdout.write('1️⃣ Mengubah nama "Bangku" menjadi "Kursi"...')
        bangku_items = Equipment.objects.filter(name__icontains='bangku')
        bangku_count = 0
        
        for item in bangku_items:
            old_name = item.name
            item.name = item.name.replace('Bangku', 'Kursi').replace('bangku', 'kursi')
            item.save()
            self.stdout.write(f'   {old_name} → {item.name}')
            bangku_count += 1
        
        if bangku_count > 0:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Berhasil mengubah {bangku_count} bangku menjadi kursi\n'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️  Tidak ada data bangku ditemukan\n'))
        
        # 2. Update kode AC
        self.stdout.write('2️⃣ Mengupdate kode AC...')
        ac_category = EquipmentCategory.objects.filter(name__icontains='ac').first()
        
        if ac_category:
            ac_items = Equipment.objects.filter(category=ac_category).order_by('id')
            self.stdout.write(f'   Ditemukan {ac_items.count()} AC')
            
            ac_count = 0
            for index, ac in enumerate(ac_items, 1):
                old_code = ac.inventory_code
                new_code = f"APM/AC/{index:03d}"
                ac.inventory_code = new_code
                ac.save()
                self.stdout.write(f'   {index}. {old_code} → {new_code}')
                ac_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'   ✅ Berhasil update {ac_count} kode AC\n'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️  Kategori AC tidak ditemukan\n'))
        
        # 3. Update kode Router
        self.stdout.write('3️⃣ Mengupdate kode Router...')
        router_category = EquipmentCategory.objects.filter(name__icontains='router').first()
        
        if router_category:
            router_items = Equipment.objects.filter(category=router_category).order_by('id')
            self.stdout.write(f'   Ditemukan {router_items.count()} Router')
            
            router_count = 0
            for index, router in enumerate(router_items, 1):
                old_code = router.inventory_code
                new_code = f"APM/ROUTER/{index:03d}"
                router.inventory_code = new_code
                router.save()
                self.stdout.write(f'   {index}. {old_code} → {new_code}')
                router_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'   ✅ Berhasil update {router_count} kode Router\n'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️  Kategori Router tidak ditemukan\n'))
        
        # 4. Cari dan update kategori lain yang mungkin ada
        self.stdout.write('4️⃣ Mencari kategori lain yang perlu diupdate...')
        
        # Cari kategori yang mengandung kata-kata tertentu
        other_categories = EquipmentCategory.objects.filter(
            name__iregex=r'.*(printer|monitor|keyboard|mouse|speaker|webcam|headset).*'
        ).exclude(name__icontains='ac').exclude(name__icontains='router')
        
        for category in other_categories:
            items = Equipment.objects.filter(category=category).order_by('id')
            if items.exists():
                category_code = category.name.split()[0].upper()
                self.stdout.write(f'   Kategori: {category.name} ({items.count()} item)')
                
                for index, item in enumerate(items, 1):
                    old_code = item.inventory_code
                    new_code = f"APM/{category_code}/{index:03d}"
                    item.inventory_code = new_code
                    item.save()
                    self.stdout.write(f'     {index}. {old_code} → {new_code}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 SELESAI! Semua data inventaris berhasil diperbaiki!'))