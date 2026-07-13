# Generated for adding EquipmentPhoto model for multiple photos

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_equipment_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='inventory/photos/', verbose_name='Foto')),
                ('position', models.CharField(choices=[('front', 'Tampak Depan'), ('back', 'Tampak Belakang'), ('left', 'Tampak Kiri'), ('right', 'Tampak Kanan'), ('top', 'Tampak Atas'), ('bottom', 'Tampak Bawah'), ('detail', 'Detail/Close-up'), ('other', 'Lainnya')], default='other', max_length=20, verbose_name='Posisi Foto')),
                ('caption', models.CharField(blank=True, max_length=200, verbose_name='Keterangan')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Urutan')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='inventory.equipment', verbose_name='Peralatan')),
            ],
            options={
                'verbose_name': 'Foto Peralatan',
                'verbose_name_plural': 'Foto Peralatan',
                'ordering': ['equipment', 'order', 'uploaded_at'],
                'indexes': [
                    models.Index(fields=['equipment', 'order'], name='equip_photo_order_idx'),
                ],
            },
        ),
    ]
