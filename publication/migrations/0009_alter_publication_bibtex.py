# Generated by Django 3.2.19 on 2023-05-18 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0008_publication_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='bibtex',
            field=models.TextField(blank=True),
        ),
    ]