# Generated by Django 4.2.5 on 2023-09-30 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article_module.articlecategory', verbose_name='دسته بندی والد'),
        ),
        migrations.AlterField(
            model_name='articlecategory',
            name='url_title',
            field=models.CharField(max_length=100, unique=True, verbose_name='عنوان لینک'),
        ),
    ]
