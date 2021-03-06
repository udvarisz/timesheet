# Generated by Django 3.0.7 on 2020-06-28 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('time_sheet', '0002_auto_20200627_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_type', models.CharField(blank=True, max_length=150, null=True, verbose_name='Típus')),
                ('car_plate', models.CharField(max_length=6, unique=True, verbose_name='Rendszám')),
                ('fuel_type', models.CharField(choices=[('B', 'Benzin'), ('D', 'Gázolaj'), ('G', 'Gáz')], default='O', max_length=1, verbose_name='Üzemanyag típusa')),
                ('ccm', models.PositiveSmallIntegerField(verbose_name='Lökettérfogat')),
            ],
        ),
        migrations.AlterField(
            model_name='duty',
            name='plate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='time_sheet.Car', verbose_name='Rendszám'),
        ),
    ]
