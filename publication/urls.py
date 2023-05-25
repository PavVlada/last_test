from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from ajax_select import urls as ajax_select_urls
from .views import PublicationList, PublicationDetail, PublicationCreate, PublicationUpdate, PublicationDelete, MyPublicationList, PublicationUpload
from .views import ContributorAutocomplete, PublisherAutocomplete, EventAutocomplete, JournalAutocomplete, PublicationAutocomplete

# admin.autodiscover()

urlpatterns = [
    path('', PublicationList.as_view(), name='publications'),
    path('publications-my', MyPublicationList.as_view(), name='publications-my'),
    path('publication/<int:pk>/', PublicationDetail.as_view(), name='publication'),
    path('publication-create/', PublicationCreate.as_view(), name='publication-create'),
    path('publication-upload/', PublicationUpload.as_view(), name='publication-upload'),
    path('publication-update/<int:pk>/', PublicationUpdate.as_view(), name='publication-update'),
    path('publication-delete/<int:pk>/', PublicationDelete.as_view(), name='publication-delete'),


    # path('author-create/', AuthorCreate.as_view(), name='author-create'),
    # path('author-update/<int:pk>/', AuthorUpdate.as_view(), name='author-update'),
    # path('author-delete/<int:pk>/', AuthorDelete.as_view(), name='author-delete'),


    path('contributor-autocomplete/', ContributorAutocomplete.as_view(create_field='name'), name='contributor-autocomplete'),
    path('publisher-autocomplete/', PublisherAutocomplete.as_view(create_field='name|address'), name='publisher-autocomplete'),
    path('journal-autocomplete/', JournalAutocomplete.as_view(create_field='name|ISSN'), name='journal-autocomplete'),
    path('event-autocomplete/', EventAutocomplete.as_view(create_field='name'), name='event-autocomplete'),
    path('publication-autocomplete/', PublicationAutocomplete.as_view(), name='publication-autocomplete'),

    # url(r'^ajax_select/', include(ajax_select_urls)),
    # url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.SHARED_STATIC)