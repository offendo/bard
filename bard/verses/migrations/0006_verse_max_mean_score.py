# Generated by Django 2.2.7 on 2019-12-01 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verses', '0005_auto_20191201_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='verse',
            name='max_mean_score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
