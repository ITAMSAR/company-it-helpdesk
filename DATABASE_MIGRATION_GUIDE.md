# 📚 Panduan Migration Database

## 🎯 Kapan Perlu Migration?

Migration diperlukan saat ada perubahan pada **model** (file `models.py`):
- ✅ Tambah field baru
- ✅ Hapus field
- ✅ Ubah tipe field
- ✅ Tambah/hapus model
- ✅ Ubah constraint (unique, null, dll)

Migration **TIDAK** diperlukan saat:
- ❌ Ubah views
- ❌ Ubah templates
- ❌ Ubah URLs
- ❌ Ubah static files

---

## 🔄 Cara Update Database (Tanpa Hapus Data)

### **Metode 1: Gunakan Script (Recommended)**

```bash
UPDATE_DATABASE.bat
```

Script akan:
1. Backup database otomatis
2. Buat migration files
3. Apply migrations
4. Jaga data lama tetap aman

---

### **Metode 2: Manual**

#### **Step 1: Backup Database**
```bash
copy db.sqlite3 db.sqlite3.backup
```

#### **Step 2: Buat Migration**
```bash
python manage.py makemigrations
```

Output contoh:
```
Migrations for 'inventory':
  apps\inventory\migrations\0003_equipment_warranty_status.py
    - Add field warranty_status to equipment
```

#### **Step 3: Apply Migration**
```bash
python manage.py migrate
```

Output contoh:
```
Running migrations:
  Applying inventory.0003_equipment_warranty_status... OK
```

---

## 📝 Contoh Kasus

### **Kasus 1: Tambah Field Baru (Opsional)**

**Model:**
```python
class Equipment(models.Model):
    # ... field lama ...
    notes = models.TextField(blank=True, null=True)  # Field baru
```

**Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

✅ **Data lama tetap aman!** Field baru akan kosong (NULL) untuk data lama.

---

### **Kasus 2: Tambah Field Baru (Required)**

**Model:**
```python
class Equipment(models.Model):
    # ... field lama ...
    location = models.CharField(max_length=100)  # Required, no default!
```

**Migration akan error!** Karena data lama tidak punya nilai untuk field ini.

**Solusi 1: Tambah default value**
```python
location = models.CharField(max_length=100, default='Kantor Pusat')
```

**Solusi 2: Buat nullable dulu**
```python
location = models.CharField(max_length=100, blank=True, null=True)
```

---

### **Kasus 3: Ubah Field Type**

**Dari:**
```python
price = models.IntegerField()
```

**Ke:**
```python
price = models.DecimalField(max_digits=10, decimal_places=2)
```

**Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

✅ Django akan convert data otomatis (jika kompatibel).

---

### **Kasus 4: Hapus Field**

**Model:**
```python
class Equipment(models.Model):
    name = models.CharField(max_length=200)
    # old_field dihapus
```

**Migration:**
```bash
python manage.py makemigrations
# Django akan tanya: "Are you sure you want to delete field 'old_field'?"
# Ketik: yes
python manage.py migrate
```

⚠️ **Data di field tersebut akan hilang!**

---

## 🚨 Troubleshooting

### **Error: "You are trying to add a non-nullable field"**

**Penyebab:** Field baru required tapi data lama tidak punya nilai.

**Solusi:**
1. Tambah `default` value:
   ```python
   new_field = models.CharField(max_length=100, default='default_value')
   ```

2. Atau buat nullable:
   ```python
   new_field = models.CharField(max_length=100, blank=True, null=True)
   ```

---

### **Error: "Constraint failed"**

**Penyebab:** Data lama melanggar constraint baru (unique, foreign key, dll).

**Solusi:**
1. Bersihkan data yang bermasalah dulu
2. Atau ubah constraint (hapus unique, tambah null=True)

---

### **Migration Conflict**

**Penyebab:** Ada migration yang bentrok.

**Solusi:**
```bash
python manage.py makemigrations --merge
python manage.py migrate
```

---

## 💾 Backup & Restore

### **Backup Database**
```bash
# Manual
copy db.sqlite3 db.sqlite3.backup

# Dengan timestamp
copy db.sqlite3 db.sqlite3.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%
```

### **Restore Database**
```bash
copy db.sqlite3.backup db.sqlite3
```

---

## 🎯 Best Practices

### **1. Selalu Backup Sebelum Migrate**
```bash
copy db.sqlite3 db.sqlite3.backup
```

### **2. Test di Development Dulu**
Jangan langsung migrate di production!

### **3. Gunakan Default Value untuk Field Baru**
```python
# Good
new_field = models.CharField(max_length=100, default='')

# Bad (akan error jika ada data lama)
new_field = models.CharField(max_length=100)
```

### **4. Buat Field Nullable Jika Tidak Wajib**
```python
optional_field = models.CharField(max_length=100, blank=True, null=True)
```

### **5. Review Migration Files**
Cek file di `apps/*/migrations/` sebelum apply.

---

## 📋 Checklist Migration

- [ ] Backup database (`copy db.sqlite3 db.sqlite3.backup`)
- [ ] Stop server (Ctrl+C)
- [ ] Ubah model di `models.py`
- [ ] Buat migration (`python manage.py makemigrations`)
- [ ] Review migration files
- [ ] Apply migration (`python manage.py migrate`)
- [ ] Test aplikasi
- [ ] Hapus backup jika sukses

---

## 🔧 Commands Berguna

```bash
# Lihat status migrations
python manage.py showmigrations

# Lihat SQL yang akan dijalankan
python manage.py sqlmigrate app_name migration_number

# Rollback migration
python manage.py migrate app_name previous_migration_number

# Reset migrations (DANGER!)
python manage.py migrate app_name zero
```

---

## 📞 Kapan Harus Hapus Database?

Hapus database hanya jika:
- ❌ Migration conflict yang tidak bisa di-resolve
- ❌ Perubahan struktur database yang sangat besar
- ❌ Masih development dan data tidak penting

**Jangan hapus database jika:**
- ✅ Sudah ada data production
- ✅ Perubahan bisa di-handle dengan migration
- ✅ Hanya tambah/ubah field biasa

---

**Ingat: Migration adalah teman, bukan musuh! 🚀**
