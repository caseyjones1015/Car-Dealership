# Generated by Django 4.2.3 on 2023-12-04 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0043_delete_legaldocuments'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ImageField(upload_to='legal_documents/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_dealership.car')),
            ],
        ),
    ]
