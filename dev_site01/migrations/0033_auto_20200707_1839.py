# Generated by Django 3.0.8 on 2020-07-07 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0032_group_project_collaborators'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group_project',
            old_name='done',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='collaborators',
            name='label_colour',
            field=models.CharField(choices=[('primary', 'primary'), ('dark', 'dark'), ('warning', 'warning'), ('info', 'info'), ('secondary', 'secondary'), ('danger', 'danger'), ('light', 'light'), ('success', 'success')], default='warning', max_length=90),
        ),
    ]
