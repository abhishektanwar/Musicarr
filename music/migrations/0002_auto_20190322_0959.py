# Generated by Django 2.1.4 on 2019-03-22 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='aritst',
            new_name='artist',
        ),
    ]