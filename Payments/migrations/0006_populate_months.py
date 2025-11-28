# Generated manually to populate Month table with all 12 months

from django.db import migrations


def populate_months(apps, schema_editor):
    """Create all 12 months in the Month table."""
    Month = apps.get_model('Payments', 'Month')
    
    months = [
        {'name': 'January', 'order': 1},
        {'name': 'February', 'order': 2},
        {'name': 'March', 'order': 3},
        {'name': 'April', 'order': 4},
        {'name': 'May', 'order': 5},
        {'name': 'June', 'order': 6},
        {'name': 'July', 'order': 7},
        {'name': 'August', 'order': 8},
        {'name': 'September', 'order': 9},
        {'name': 'October', 'order': 10},
        {'name': 'November', 'order': 11},
        {'name': 'December', 'order': 12},
    ]
    
    for month_data in months:
        Month.objects.get_or_create(
            name=month_data['name'],
            defaults={'order': month_data['order']}
        )


def remove_months(apps, schema_editor):
    """Remove all months from the Month table."""
    Month = apps.get_model('Payments', 'Month')
    
    # Only delete the months we created
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    Month.objects.filter(name__in=month_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0005_payment_student_alter_payment_months_paid_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_months, reverse_code=remove_months),
    ]
