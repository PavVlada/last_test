from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


from taggit.managers import TaggableManager



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Contributor(models.Model):
    name = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return str(self.name)
    # def create(self, text):
    #     author = self.create(name=text)
    #     return author


class Event(models.Model):
    name = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return str(self.name)
    # def create(self, text):
    #     event = self.create(name=text)
    #     return event

class Publisher(models.Model):
    name = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.name}. Город: {self.address}"
    # def create(self, text):
    #     name, address = text.split('|')
    #     publisher = self.create(name=name.strip(), address=address.strip())
    #     return publisher


class Journal(models.Model):
    name = models.CharField(max_length=100, blank=True)
    ISSN = models.CharField(max_length=15, blank=True,)
    def __str__(self):
        return f"{self.name}. ISSN: {self.ISSN}"
    # def create(self, text):
    #     name, issn = text.split('|')
    #     journal = self.create(name=name.strip(), ISSN=issn.strip())
    #     return journal


class Publication(models.Model):
    class PublicationType(models.TextChoices):
        CHOOSE = "choose", "Выберите тип"

        WEBPAGE = "webpage", "Веб-страница (Электронный ресурс удаленного доступа)"
        BOOK = "book", "Книга (Book)"
        THESIS = "thesis", "Диссертация и автореферат диссертации (Thesis)"

        CHAPTER = "chapter", "Раздел книги (BookSection)"
        PAPER_CONFERENCE = "paper-conference", "Статья из сборника (Документ конференции) (Conference Paper)"
        # ARTICLE_NEWSPAPER = "article-newspaper", "Газетная статья (Newspaper Article)"
        # ENTRY_ENCYCLOPEDIA = "entry-encyclopedia", "Статья из энциклопедии (Encyclopedia Article)"
        ARTICLE_JOURNAL = "article-journal", "Статья из периодики (Journal Article)"

        # SOFTWARE = "software", "Электронный ресурс локального доступа (Компьютерная программа) (Computer Program)"
     

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
    keyword = TaggableManager(blank=True, help_text='Ключевые слова (записываются через запятую)', verbose_name='Ключевые словаf')
    publication_type = models.CharField(choices=PublicationType.choices, max_length=200, verbose_name='Тип', default=PublicationType.CHOOSE)
    citation_key = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, null=True, blank=True, related_name='author_publications', verbose_name='Автор')
    coauthor = models.ManyToManyField(Contributor, blank=True, related_name='coauthor_publications')
    editor = models.ManyToManyField(Contributor, blank=True, related_name='editor_publications')
    collectioneditor = models.ManyToManyField(Contributor, blank=True, related_name='collectioneditor_publications')
    reviewedauthor = models.ManyToManyField(Contributor, blank=True, related_name='reviewedauthor_publications')
    translator = models.ManyToManyField(Contributor, blank=True, related_name='translator_publications')

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Журнал')
    book = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Конференция')

    abstract = models.TextField(blank=True, null=True)
    archive = models.CharField(max_length=100, blank=True)
    archive_location = models.CharField(max_length=100, blank=True)
    call_number = models.CharField(max_length=100, blank=True)
    collection_number = models.CharField(max_length=100, blank=True)
    collection_title = models.CharField(max_length=100, blank=True)
    container_title = models.CharField(max_length=100, blank=True)
    edition = models.CharField(max_length=50, blank=True, help_text='Издание (полная строка, например, «1-е, стереотипное»)')
    genre = models.CharField(max_length=100, blank=True)
    issue = models.PositiveIntegerField(blank=True, null=True)

    # ISSUED
    day = models.PositiveIntegerField(blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    month = models.PositiveIntegerField(choices=Month.choices, blank=True, null=True)

    language = models.CharField(max_length=10, blank=True)
    medium = models.CharField(max_length=100, blank=True)
    number_of_pages = models.PositiveIntegerField(blank=True, null=True)
    number_of_volumes = models.PositiveIntegerField(blank=True, null=True)
    page = models.CharField(max_length=10, blank=True)
    section = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True, verbose_name='Заглавие')
    title_short = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=50, blank=True)
    volume = models.IntegerField(blank=True, null=True, help_text='Том журнала или книги')

    note = models.CharField(max_length=256, blank=True, help_text='Любые заметки')
    ISBN = models.CharField(max_length=20, blank=True, help_text='Только для книг')
    URL = models.URLField(blank=True, help_text='Ссылка на оригинальную публикацию')
    DOI = models.CharField(max_length=128, verbose_name='DOI', blank=True)
    bibtex= models.TextField(blank=True, null=True)
    gost2018= models.TextField(blank=True, null=True)


    # def get_fields(self):
    #     return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['date_posted']
