# Generated manually for adding photo field to Equipment model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_equipmentdeletionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='inventory/photos/', verbose_name='Foto Barang'),
        ),
    ]
