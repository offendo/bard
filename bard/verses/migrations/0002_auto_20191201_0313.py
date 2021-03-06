# Generated by Django 2.2.7 on 2019-12-01 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verse',
            name='score',
        ),
        migrations.AddField(
            model_name='verse',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='verse',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='verse',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
