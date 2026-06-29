from django.db import migrations


INITIAL_DIVISIONS = [
    ('Finance', ''),
    ('GA', ''),
    ('HR', ''),
    ('IT', ''),
    ('Project', ''),
    ('Admin', ''),
    ('Purchasing', ''),
]


def seed_divisions(apps, schema_editor):
    Division = apps.get_model('users', 'Division')
    for name, description in INITIAL_DIVISIONS:
        Division.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )


def unseed_divisions(apps, schema_editor):
    Division = apps.get_model('users', 'Division')
    Division.objects.filter(name__in=[name for name, _ in INITIAL_DIVISIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_division_userprofile'),
    ]

    operations = [
        migrations.RunPython(seed_divisions, unseed_divisions),
    ]
