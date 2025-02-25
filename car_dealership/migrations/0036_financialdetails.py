# Generated by Django 4.2.3 on 2023-12-04 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0035_remove_finance_car_delete_financedetail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_co', models.CharField(blank=True, max_length=100, null=True)),
                ('buy_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('buy_additional', models.CharField(blank=True, max_length=100, null=True)),
                ('buy_total', models.CharField(blank=True, max_length=100, null=True)),
                ('repairs_co', models.CharField(blank=True, max_length=100, null=True)),
                ('repairs_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('repairs_additional', models.CharField(blank=True, max_length=100, null=True)),
                ('repairs_total', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_co', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_additional', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_total', models.CharField(blank=True, max_length=100, null=True)),
                ('brokage_co', models.CharField(blank=True, max_length=100, null=True)),
                ('brokage_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('brokage_additional', models.CharField(blank=True, max_length=100, null=True)),
                ('brokage_total', models.CharField(blank=True, max_length=100, null=True)),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='car_dealership.car')),
            ],
        ),
    ]
