from django.contrib import admin
from .models import Publication, Author, Publisher, Journal
# Register your models here.

admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Journal)