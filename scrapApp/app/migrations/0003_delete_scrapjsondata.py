# Generated by Django 3.1.3 on 2021-05-18 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_storejsondata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScrapJsonData',
        ),
    ]