# Generated by Django 2.2.7 on 2019-12-01 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verses', '0003_auto_20191201_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verse',
            options={'ordering': ['num_vote_up']},
        ),
    ]
