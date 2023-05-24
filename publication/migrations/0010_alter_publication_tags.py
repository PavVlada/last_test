# Generated by Django 3.2.19 on 2023-05-18 05:27

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('publication', '0009_alter_publication_bibtex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
