# Generated by Django 3.0.5 on 2021-01-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_uploadgoogledatalink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semrush',
            name='volume',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]