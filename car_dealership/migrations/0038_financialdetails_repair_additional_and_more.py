# Generated by Django 4.2.3 on 2023-12-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0037_remove_financialdetails_brokage_additional_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialdetails',
            name='repair_additional',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financialdetails',
            name='repair_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financialdetails',
            name='repair_co',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financialdetails',
            name='repair_total',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
