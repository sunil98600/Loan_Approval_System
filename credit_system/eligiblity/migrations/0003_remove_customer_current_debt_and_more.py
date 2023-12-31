# Generated by Django 5.0 on 2023-12-16 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eligiblity', '0002_customer_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='current_debt',
        ),
        migrations.AlterField(
            model_name='customer',
            name='approved_limit',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='monthly_salary',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.IntegerField(max_length=15),
        ),
        migrations.AlterField(
            model_name='loan',
            name='interest_rate',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='loan',
            name='monthly_repayment',
            field=models.ImageField(upload_to=''),
        ),
    ]
