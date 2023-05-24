# Generated by Django 3.2.19 on 2023-05-19 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0013_auto_20230519_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='publication_type',
            field=models.CharField(choices=[('article', 'Статья из журнала'), ('book', 'Книга'), ('booklet', 'Печатная работа, которая не содержит имя издателя'), ('inbook', 'Часть книги'), ('incollection', 'Часть книги, имеющая собственное название'), ('inproceedings', 'Труд конференции'), ('manual', 'Техническая документация'), ('mastersthesis', 'Магистерская диссертация'), ('misc', 'Если другие типы не подходят'), ('phdthesis', 'Кандидатская диссертация'), ('proceedings', 'Сборник трудов конференции'), ('techreport', 'Отчет'), ('unpublished', 'Не опубликовано')], default='article', max_length=200, verbose_name='Тип'),
        ),
        migrations.DeleteModel(
            name='PublicationType',
        ),
    ]
