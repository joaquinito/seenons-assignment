# Generated by Django 4.2.7 on 2023-11-28 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_remove_streams_image_streams_image_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='image_url',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
