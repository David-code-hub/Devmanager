# Generated by Django 3.0.8 on 2020-07-06 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0028_remove_group_project_collaborators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assign_user_to_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dev_site01.Collaborators'),
        ),
    ]