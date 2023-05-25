from django.contrib import admin
from .models import Publication, Contributor, Publisher, Journal
# Register your models here.

admin.site.register(Publication)
admin.site.register(Contributor)
admin.site.register(Publisher)
admin.site.register(Journal)