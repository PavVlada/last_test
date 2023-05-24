# Generated by Django 3.2.19 on 2023-05-17 17:12

from django.db import migrations, models
import publication.models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0004_publication_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='file_path',
            field=models.FileField(blank=True, null=True, upload_to=publication.models.user_directory_path, verbose_name='PDF'),
        ),
    ]