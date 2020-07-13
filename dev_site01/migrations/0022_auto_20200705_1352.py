# Generated by Django 3.0.8 on 2020-07-05 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dev_site01', '0021_auto_20200705_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group_project',
            name='lead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_of_project', to=settings.AUTH_USER_MODEL),
        ),
    ]