# Generated by Django 3.0.8 on 2020-07-01 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dev_site01', '0003_auto_20200701_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dev_site01.Projects'),
            preserve_default=False,
        ),
    ]
