# Generated by Django 4.0.5 on 2022-06-01 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=None, null=True, verbose_name='Las time login'),
        ),
    ]
