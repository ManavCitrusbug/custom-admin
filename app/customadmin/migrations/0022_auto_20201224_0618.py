# Generated by Django 3.1.4 on 2020-12-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0021_auto_20201224_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='../static/assets/images/profile.jpg', null=True, upload_to='profile_image', verbose_name='Profile Image'),
        ),
    ]
