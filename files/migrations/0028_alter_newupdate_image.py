# Generated by Django 4.2.20 on 2025-05-08 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0027_dailynewsletter_newslettersubscriber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newupdate',
            name='image',
            field=models.ImageField(blank=True, help_text='Optional – You may leave this empty.', null=True, upload_to='new_updates/'),
        ),
    ]
