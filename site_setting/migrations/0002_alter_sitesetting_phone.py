# Generated by Django 4.2.5 on 2023-09-30 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetting',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='تلفن'),
        ),
    ]