# Generated by Django 3.0.8 on 2020-07-03 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0019_group_project_project_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group_project',
            old_name='users',
            new_name='collaborators',
        ),
    ]
