# Generated by Django 3.0.8 on 2020-07-06 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0027_collaborators'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group_project',
            name='collaborators',
        ),
    ]
