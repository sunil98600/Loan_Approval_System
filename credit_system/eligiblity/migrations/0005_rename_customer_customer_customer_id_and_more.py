# Generated by Django 5.0 on 2023-12-17 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eligiblity', '0004_alter_customer_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customer',
            new_name='customer_id',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='customer',
            new_name='customer_id',
        ),
    ]
