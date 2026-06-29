from django.db import migrations, models


def backfill_division_stock(apps, schema_editor):
    ATKItem = apps.get_model('atk', 'ATKItem')
    ATKDivisionStock = apps.get_model('atk', 'ATKDivisionStock')
    Division = apps.get_model('users', 'Division')

    admin, _ = Division.objects.get_or_create(
        name='Admin',
        defaults={'description': ''}
    )

    for item in ATKItem.objects.all():
        ATKDivisionStock.objects.update_or_create(
            item=item,
            division=admin,
            defaults={
                'current_stock': item.current_stock,
                'minimum_stock': item.minimum_stock,
            }
        )
        totals = ATKDivisionStock.objects.filter(item=item).aggregate(
            total_stock=models.Sum('current_stock'),
            total_minimum=models.Sum('minimum_stock'),
        )
        item.current_stock = totals['total_stock'] or 0
        item.minimum_stock = totals['total_minimum'] or 0
        item.save(update_fields=['current_stock', 'minimum_stock', 'updated_at'])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_seed_initial_divisions'),
        ('atk', '0007_atkdivisionstock'),
    ]

    operations = [
        migrations.RunPython(backfill_division_stock, noop_reverse),
    ]
