# Generated by Django 2.2.5 on 2019-09-13 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_auto_20190912_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registered',
            name='hoketsu',
        ),
        migrations.AddField(
            model_name='registered',
            name='fifthl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='fifthwl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='firstl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='firstwl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='fourthl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='fourthwl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='secondl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='secondwl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='thirdl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registered',
            name='thirdwl',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='team_point',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='registerd',
            name='date',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='registered',
            name='fifth',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='registered',
            name='first',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='registered',
            name='fourth',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='registered',
            name='second',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='registered',
            name='team',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='registered',
            name='third',
            field=models.CharField(default='', max_length=100),
        ),
    ]
