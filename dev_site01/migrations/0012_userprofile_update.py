# Generated by Django 3.0.8 on 2020-07-02 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0011_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='update',
            field=models.BooleanField(default=False),
        ),
    ]
