# Generated by Django 4.0.3 on 2022-04-09 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idgenerator', '0002_idinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='idinfo',
            name='id_number',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
