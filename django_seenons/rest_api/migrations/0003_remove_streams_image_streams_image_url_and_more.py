# Generated by Django 4.2.7 on 2023-11-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0002_alter_lsptimeslots_weekday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streams',
            name='image',
        ),
        migrations.AddField(
            model_name='streams',
            name='image_url',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='assets',
            name='image_url',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='lsptimeslots',
            name='timeslot_end',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='lsptimeslots',
            name='timeslot_start',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='streams',
            name='details_url',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
