# Generated by Django 5.0.7 on 2024-07-21 11:20

import django.contrib.postgres.indexes
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField()),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
                'indexes': [django.contrib.postgres.indexes.BrinIndex(fields=['created_at'], name='advert_cate_created_bb3d6f_brin')],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField()),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
                'indexes': [django.contrib.postgres.indexes.BrinIndex(fields=['created_at'], name='advert_city_created_2b0511_brin')],
            },
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField()),
                ('description', models.TextField()),
                ('views', models.PositiveBigIntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='talk_price_data', to='advert.category')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='talk_price_data', to='advert.city')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
                'indexes': [django.contrib.postgres.indexes.BrinIndex(fields=['created_at'], name='advert_adve_created_7d99e3_brin')],
            },
        ),
    ]