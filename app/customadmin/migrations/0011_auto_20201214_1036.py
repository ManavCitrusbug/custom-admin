# Generated by Django 3.1.4 on 2020-12-14 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0010_auto_20201214_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalchart',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]