# Generated by Django 4.2.5 on 2023-09-23 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0004_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcaption',
            name='product',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductCaption',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]
