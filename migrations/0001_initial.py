# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 01:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.CharField(max_length=4)),
                ('stop_id', models.IntegerField(verbose_name='Stop ID')),
                ('direction', models.CharField(choices=[('INBOUND', 'Inbound'), ('OUTBOUND', 'Outbound')], max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='TickerStation',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100, verbose_name="Location (store's name, etc)")),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='Address for Location')),
                ('contact_notes', models.TextField(blank=True, verbose_name='Contact details (phone, email, etc) of Location')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('width', models.IntegerField(default=4, verbose_name='Width (in 8x8 matrices)')),
                ('brightness', models.FloatField(default=1)),
                ('speed', models.FloatField(default=5)),
                ('last_message', models.CharField(editable=False, max_length=1000)),
                ('status', models.CharField(editable=False, max_length=400)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='prediction',
            name='ticker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticker.TickerStation'),
        ),
    ]
