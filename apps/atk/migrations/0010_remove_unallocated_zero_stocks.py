from django.db import migrations


POOL_NAMES = ('Administrator', 'Admin')


def remove_unallocated_zero_stocks(apps, schema_editor):
    ATKDivisionStock = apps.get_model('atk', 'ATKDivisionStock')

    ATKDivisionStock.objects.filter(
        current_stock=0,
        minimum_stock=0,
    ).exclude(
        division__name__in=POOL_NAMES,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('atk', '0009_atkrequest_stock_applied_at_and_more'),
    ]

    operations = [
        migrations.RunPython(
            remove_unallocated_zero_stocks,
            migrations.RunPython.noop,
        ),
    ]
