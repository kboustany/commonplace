# Generated by Django 5.2.4 on 2025-07-31 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_letter_recipient_remove_letter_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
