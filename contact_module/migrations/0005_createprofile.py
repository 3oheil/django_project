# Generated by Django 4.2.5 on 2023-09-27 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_module', '0004_alter_contactus_response'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='profile')),
            ],
        ),
    ]
