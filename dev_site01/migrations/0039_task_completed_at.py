# Generated by Django 3.0.8 on 2020-07-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0038_auto_20200709_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
