from django.db import migrations


TARGET_DIVISIONS = [
    ('Finance', ''),
    ('IT', ''),
    ('GA', ''),
    ('HR', ''),
    ('Project', ''),
    ('Admin', ''),
    ('Purchasing', ''),
]


def normalize_divisions(apps, schema_editor):
    Division = apps.get_model('users', 'Division')

    rename_map = {
        'Umum': 'Admin',
        'HRD': 'HR',
        'Operasional': 'Project',
    }

    for old_name, new_name in rename_map.items():
        old_division = Division.objects.filter(name=old_name).first()
        if not old_division:
            continue

        existing = Division.objects.filter(name=new_name).exclude(pk=old_division.pk).first()
        if existing:
            old_division.members.update(division=existing)
            old_division.atk_stocks.update(division=existing)
            old_division.delete()
        else:
            old_division.name = new_name
            old_division.save(update_fields=['name'])

    for name, description in TARGET_DIVISIONS:
        Division.objects.get_or_create(name=name, defaults={'description': description})

    target_names = [name for name, _ in TARGET_DIVISIONS]
    for division in Division.objects.exclude(name__in=target_names):
        if not division.members.exists() and not division.atk_stocks.exists():
            division.delete()


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_seed_initial_divisions'),
    ]

    operations = [
        migrations.RunPython(normalize_divisions, noop_reverse),
    ]
