# Generated by Django 4.2.3 on 2023-11-22 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0020_delete_carimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
