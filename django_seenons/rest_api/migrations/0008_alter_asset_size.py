# Generated by Django 4.2.7 on 2023-11-29 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0007_remove_asset_created_at_remove_asset_update_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='size',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
