# Generated by Django 4.2.20 on 2025-05-25 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0035_fileupload_uploaded_image_alter_aboutpage_image1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileupload',
            name='uploaded_image',
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='uploaded_file',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
