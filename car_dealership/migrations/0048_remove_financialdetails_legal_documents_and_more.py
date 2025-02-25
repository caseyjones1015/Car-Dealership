# Generated by Django 4.2.3 on 2023-12-04 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealership', '0047_financialdetails_legal_documents_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialdetails',
            name='legal_documents',
        ),
        migrations.CreateModel(
            name='LegalDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_documents', models.ImageField(upload_to='legal_documents/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_dealership.car')),
            ],
        ),
    ]
