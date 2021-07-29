# Generated by Django 3.2.5 on 2021-07-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('player_id', models.IntegerField()),
                ('media_id', models.IntegerField()),
                ('media_type', models.CharField(max_length=2)),
            ],
            options={
                'unique_together': {('date', 'time', 'player_id')},
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('register', models.ManyToManyField(blank=True, to='base.Register')),
            ],
        ),
    ]
