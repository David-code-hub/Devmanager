# Generated by Django 3.0.8 on 2020-07-09 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0034_userprofile_group_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborators',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dev_site01.UserProfile'),
        ),
    ]
