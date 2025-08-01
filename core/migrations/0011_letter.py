# Generated by Django 5.2.4 on 2025-07-31 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_quotation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.item')),
                ('date_sent', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('sender', models.CharField(max_length=200)),
                ('recipient', models.CharField(max_length=200)),
                ('salutation', models.CharField(blank=True, max_length=200)),
                ('body', models.TextField()),
                ('closing', models.CharField(blank=True, max_length=200)),
                ('signature', models.CharField(blank=True, max_length=200)),
                ('postscript', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.item',),
        ),
    ]
