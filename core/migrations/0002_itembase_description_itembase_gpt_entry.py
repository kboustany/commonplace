# Generated by Django 5.2.4 on 2025-07-24 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itembase',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='itembase',
            name='gpt_entry',
            field=models.TextField(null=True),
        ),
    ]
