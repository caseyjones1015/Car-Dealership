# Generated by Django 4.2.3 on 2023-11-07 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0006_alter_car_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
