# Generated by Django 3.1.3 on 2020-11-29 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20201129_1338'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='upload_images',
            new_name='uploadImage',
        ),
    ]