# Generated by Django 3.2.16 on 2022-12-17 04:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('managment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='time')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle_start', models.DateField(verbose_name='start of the cycle')),
                ('cycle_end', models.DateField(verbose_name='end of the cycle')),
                ('frequency', models.PositiveIntegerField(verbose_name='frequency')),
                ('timesheet', models.ManyToManyField(to='medicine.TimeTable', verbose_name='time')),
            ],
        ),
        migrations.CreateModel(
            name='Cure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('dose', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='dose')),
                ('dose_type', models.CharField(choices=[('PCS', 'PCS'), ('ml', 'ml')], max_length=255, verbose_name='dose type')),
                ('type', models.CharField(choices=[('injection', 'injection'), ('ampule', 'ampule'), ('pill', 'pill'), ('SUSPENSION', 'SUSPENSION')], max_length=255, verbose_name='type')),
                ('strict_status', models.BooleanField(default=False, max_length=255, null=True, verbose_name='strict')),
                ('food', models.CharField(choices=[('Before meals', 'Before meals'), ('While eating', 'While eating'), ('After meal', 'After meal'), ('No matter', 'No matter')], max_length=255, null=True, verbose_name='food')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managment.patient')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicine.schedule', verbose_name='schedule')),
            ],
        ),
    ]
