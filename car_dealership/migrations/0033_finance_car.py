# Generated by Django 4.2.3 on 2023-12-04 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0032_remove_finance_additional_remove_finance_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance',
            name='car',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='car_dealership.car'),
            preserve_default=False,
        ),
    ]
