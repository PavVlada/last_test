from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


from taggit.managers import TaggableManager



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Author(models.Model):
    name = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return str(self.name)
    def create(self, text):
        author = self.create(name=text)
        return author

class Editor(models.Model):
    name = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return str(self.name)
    def create(self, text):
        editor = self.create(name=text)
        return editor


class Publisher(models.Model):
    name = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.name}. Город: {self.address}"
    def create(self, text):
        name, address = text.split('|')
        publisher = self.create(name=name.strip(), address=address.strip())
        return publisher


class Journal(models.Model):
    name = models.CharField(max_length=100, blank=True)
    ISSN = models.CharField(max_length=8, blank=True,)
    def __str__(self):
        return f"{self.name}. ISSN: {self.ISSN}"
    def create(self, text):
        name, issn = text.split('|')
        journal = self.create(name=name.strip(), ISSN=issn.strip())
        return journal


class Publication(models.Model):
    class PublicationType(models.TextChoices):
        ARTICLE = "article", "Article (Статья из журнала)"
        BOOK = "book", "Book (Книга)"
        BOOKLET = "booklet", "Booklet (Печатная работа, которая не содержит имя издателя)"
        INBOOK = "inbook", "Inbook (Часть книги)"
        INCOLLECTION = "incollection", "Incollection (Часть книги, имеющая собственное название)"
        INPROCEEDINGS = "inproceedings", "Inproceedings (Труд конференции)"
        MANUAL = "manual", "Manual (Техническая документация)"
        MASTERSTHESIS = "mastersthesis", "Mastersthesis (Магистерская диссертация)"
        MISC = "misc", "Misc (Если другие типы не подходят)"
        PHDTHESIS = "phdthesis", "Phdthesis (Кандидатская диссертация)"
        PROCEEDINGS = "proceedings", "Proceedings (Сборник трудов конференции)"
        TECHREPORT = "techreport", "Techreport (Отчет)"
        UNPUBLISHED = "unpublished", "Unpublished (Не опубликовано)"

    class Month(models.IntegerChoices):
        JAN = 1, "Январь"
        FEB = 2, "Февраль"
        MAR = 3, "Март"
        APR = 4, "Апрель"
        MAY = 5, "Май"
        JUN = 6, "Июнь"
        JUL = 7, "Июль"
        AUG = 8, "Август"
        SEP = 9, "Сентябрь"
        OCT = 10, "Октябрь"
        NOV = 11, "Ноябрь"
        DEC = 12, "Декабрь"

    public = models.BooleanField(default=True, help_text="Публикация доступна всем")
    date_posted=models.DateTimeField(auto_now_add=True, help_text='Дата публикации на этом сайте')
    file_path = models.FileField(upload_to=user_directory_path, verbose_name='PDF', blank=True, null=True)
    keyword = TaggableManager(blank=True, help_text='Ключевые слова (записываются через запятую)')
    publication_type = models.CharField(choices=PublicationType.choices, max_length=200, verbose_name='Тип', default=PublicationType.ARTICLE)
    citation_key = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    author = models.ManyToManyField(Author, blank=False)
    editor = models.ManyToManyField(Editor, blank=True)
    # author = models.ManyToManyField(Contributor, through='PublicationContributor', blank=True)

    abstract = models.TextField(blank=True, null=True)
    annote = models.TextField(blank=True, null=True, help_text='Аннотация для библиографической записи')
    authority =  models.CharField(max_length=256, blank=True)
    booktitle = models.CharField(max_length=256, blank=True, help_text='Наименование книги, содержащей данную работу')
    chapter = models.CharField(max_length=50, blank=True, help_text='Номер главы')
    edition = models.CharField(max_length=256, blank=True, help_text='Издание (полная строка, например, «1-е, стереотипное»)')
    howpublished = models.CharField(max_length=256, blank=True)

    ISBN = models.CharField(max_length=32, blank=True, help_text='Только для книг')
    # journal = models.ManyToManyField(Journal, blank=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True, blank=True)
    language = models.CharField(max_length=5, blank=True)
    month = models.PositiveIntegerField(choices=Month.choices, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, help_text='Любые заметки')
    number = models.IntegerField(blank=True, null=True, help_text='Номер журнала')
    # organization = models.CharField(max_length=256, blank=True)
    page = models.CharField(max_length=50, blank=True)
    # publisher = models.ManyToManyField(Publisher, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    # series = models.CharField(max_length=256, blank=True)
    title = models.CharField(max_length=256, blank=True)
    URL = models.URLField(blank=True, help_text='Ссылка на оригинальную публикацию')
    volume = models.IntegerField(blank=True, null=True, help_text='Том журнала или книги')
    year = models.PositiveIntegerField(blank=True, null=True)
   
    issue = models.PositiveIntegerField(blank=True, null=True)
    issued = models.CharField(max_length=256, blank=True)
    DOI = models.CharField(max_length=128, verbose_name='DOI', blank=True)
    bibtex= models.TextField(blank=True, null=True)


    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['date_posted']
