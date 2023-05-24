# Generated by Django 3.2.19 on 2023-05-23 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0018_auto_20230523_0425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='publicationcontributor',
            name='contributor',
        ),
        migrations.RemoveField(
            model_name='publicationcontributor',
            name='publication',
        ),
        migrations.DeleteModel(
            name='Contributor',
        ),
        migrations.DeleteModel(
            name='PublicationContributor',
        ),
        migrations.AddField(
            model_name='publication',
            name='editor',
            field=models.ManyToManyField(to='publication.Editor'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='author',
            field=models.ManyToManyField(to='publication.Author'),
        ),
    ]
