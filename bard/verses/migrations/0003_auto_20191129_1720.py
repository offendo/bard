# Generated by Django 2.2.7 on 2019-11-29 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verses', '0002_auto_20191129_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verse',
            name='genre',
            field=models.ManyToManyField(to='verses.Genre'),
        ),
    ]
