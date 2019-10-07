# Generated by Django 2.2.5 on 2019-09-09 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registerd',
            old_name='registered_name',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='registerd',
            name='match',
        ),
        migrations.RemoveField(
            model_name='registerd',
            name='team',
        ),
        migrations.CreateModel(
            name='Registered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=100)),
                ('first', models.CharField(max_length=100)),
                ('second', models.CharField(max_length=100)),
                ('third', models.CharField(max_length=100)),
                ('fourth', models.CharField(max_length=100)),
                ('fifth', models.CharField(max_length=100)),
                ('hoketsu', models.CharField(max_length=100)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Match')),
            ],
        ),
    ]
