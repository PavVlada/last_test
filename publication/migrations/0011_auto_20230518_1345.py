# Generated by Django 3.2.19 on 2023-05-18 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0010_alter_publication_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='keywords',
        ),
        migrations.AddField(
            model_name='publication',
            name='issue',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]