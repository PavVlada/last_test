# Generated by Django 3.2.19 on 2023-05-25 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='ISSN',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
