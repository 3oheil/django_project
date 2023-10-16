# Generated by Django 4.2.5 on 2023-10-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setting', '0007_sitebanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitebanner',
            name='position',
            field=models.CharField(choices=[('product_list', 'صفحه لیست محصولات'), ('product_detail', 'صفحه توضیحات محصولات'), ('about_us', 'درباره ما'), ('contact_us', 'تماس با ما')], max_length=250, verbose_name='جایگاه نمایش'),
        ),
    ]