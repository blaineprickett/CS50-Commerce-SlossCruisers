# Generated by Django 4.1.7 on 2023-05-09 21:26

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]

