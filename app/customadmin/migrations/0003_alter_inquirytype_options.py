# Generated by Django 3.2.10 on 2022-05-19 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0002_auto_20220519_1454'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inquirytype',
            options={'ordering': ['-created_at'], 'verbose_name': 'InquiryType', 'verbose_name_plural': 'InquiryTypes'},
        ),
    ]
