# Generated by Django 2.2.6 on 2019-12-30 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_tournament_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='Past',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(default='-', max_length=100)),
                ('team2', models.CharField(default='-', max_length=100)),
                ('team3', models.CharField(default='-', max_length=100)),
                ('team4', models.CharField(default='-', max_length=100)),
                ('team5', models.CharField(default='-', max_length=100)),
                ('team6', models.CharField(default='-', max_length=100)),
                ('player1', models.CharField(default='-', max_length=100)),
                ('r1', models.CharField(default='-', max_length=100)),
                ('player2', models.CharField(default='-', max_length=100)),
                ('r2', models.CharField(default='-', max_length=100)),
                ('player3', models.CharField(default='-', max_length=100)),
                ('r3', models.CharField(default='-', max_length=100)),
                ('player4', models.CharField(default='-', max_length=100)),
                ('r4', models.CharField(default='-', max_length=100)),
                ('player5', models.CharField(default='-', max_length=100)),
                ('r5', models.CharField(default='-', max_length=100)),
                ('player6', models.CharField(default='-', max_length=100)),
                ('r6', models.CharField(default='-', max_length=100)),
                ('player7', models.CharField(default='-', max_length=100)),
                ('r7', models.CharField(default='-', max_length=100)),
                ('player8', models.CharField(default='-', max_length=100)),
                ('r8', models.CharField(default='-', max_length=100)),
                ('player9', models.CharField(default='-', max_length=100)),
                ('r9', models.CharField(default='-', max_length=100)),
                ('player10', models.CharField(default='-', max_length=100)),
                ('r10', models.CharField(default='-', max_length=100)),
            ],
        ),
    ]