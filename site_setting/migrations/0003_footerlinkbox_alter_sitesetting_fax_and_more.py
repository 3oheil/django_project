# Generated by Django 4.2.5 on 2023-09-30 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_setting', '0002_alter_sitesetting_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterLinkBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'دسته یندی لینک های فوتر',
                'verbose_name_plural': 'لینک های فوتر',
            },
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='fax',
            field=models.CharField(blank=True, max_length=18, null=True, verbose_name='فکس'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='تلفن'),
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('url_title', models.CharField(max_length=100, verbose_name='لینک')),
                ('footer_link_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_setting.footerlinkbox', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'لینک فوتر',
                'verbose_name_plural': 'لینک های فوتر',
            },
        ),
    ]
