# Generated by Django 4.2.20 on 2025-04-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_alter_pdfupload_company_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfupload',
            name='company_location',
            field=models.CharField(max_length=255),
        ),
    ]
