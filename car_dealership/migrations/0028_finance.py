# Generated by Django 4.2.3 on 2023-12-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0027_additionalcarimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.IntegerField()),
                ('Particulars', models.CharField(max_length=100)),
                ('CO', models.CharField(max_length=100)),
                ('Amount', models.IntegerField()),
                ('Additional', models.IntegerField(max_length=100)),
                ('Total', models.IntegerField()),
            ],
        ),
    ]
