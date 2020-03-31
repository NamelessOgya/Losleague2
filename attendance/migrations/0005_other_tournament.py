# Generated by Django 2.2.6 on 2020-03-31 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20200331_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Other_tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_name', models.CharField(default='-', max_length=100)),
                ('prize', models.IntegerField(blank=True, default=0, null=True, verbose_name='4th')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Player')),
            ],
        ),
    ]