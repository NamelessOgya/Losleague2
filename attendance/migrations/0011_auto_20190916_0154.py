# Generated by Django 2.2.5 on 2019-09-16 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_team_grosspoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamresult',
            name='point',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=''),
        ),
    ]
