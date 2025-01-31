# Generated by Django 4.2.3 on 2023-12-04 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0033_finance_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financedetail',
            name='finance',
        ),
        migrations.AlterField(
            model_name='finance',
            name='car',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finance', to='car_dealership.car'),
        ),
        migrations.AlterField(
            model_name='finance',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financedetail',
            name='particulars',
            field=models.CharField(choices=[('BUY', 'Buy'), ('REPAIRS', 'Repairs'), ('SOLD', 'Sold'), ('BROKERAGE', 'Brokerage')], max_length=9),
        ),
    ]
