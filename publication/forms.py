from django import forms
from .models import Publication, Contributor, Event, Publisher, Journal
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from dal import autocomplete

from ajax_select.fields import AutoCompleteSelectMultipleField


class PublicationListForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            'title',
            'author',
            'keyword',
            # 'date_posted'
        ]

class PublicationForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Contributor.objects.all(),
        # requiered=False,
        widget=autocomplete.ModelSelect2(url='contributor-autocomplete')
    )
    coauthor = forms.ModelMultipleChoiceField(
        queryset=Contributor.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='contributor-autocomplete')
    )
    editor = forms.ModelMultipleChoiceField(
        queryset=Contributor.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='contributor-autocomplete')
    )
    collectioneditor = forms.ModelMultipleChoiceField(
        queryset=Contributor.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='contributor-autocomplete')
    )
    reviewedauthor = forms.ModelMultipleChoiceField(
        queryset=Contributor.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='contributor-autocomplete')
    )
    translator = forms.ModelMultipleChoiceField(
        queryset=Contributor.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='contributor-autocomplete')
    )

    journal = forms.ModelChoiceField(
        queryset=Journal.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='journal-autocomplete')
    )
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='event-autocomplete')
    )
    book = forms.ModelChoiceField(
        queryset=Publication.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='publication-autocomplete')
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='publisher-autocomplete')
    )

    class Meta:
        model = Publication
        fields = [
            # 'date_posted',
            'public',
            'file_path',
            'keyword',
            'publication_type',
            'citation_key',

            'author',
            'coauthor',
            'editor',
            'collectioneditor',
            'reviewedauthor',
            'translator',

            'journal',
            'event',
            'book',
            'publisher',

            'abstract',
            'archive',
            'archive_location',
            'call_number',
            'collection_number',
            'collection_title',
            'container_title',
            'edition',
            'genre',
            'issue',

            'day',
            'year',
            'month',

            'language',
            'medium',
            'number_of_pages',
            'number_of_volumes',
            'page',
            'section',
            'source',
            'title',
            'title_short',
            'version',
            'volume',
            
            'ISBN',
            'note',
            'URL',
            'DOI',
            'bibtex',
            'gost2018'
    ]

# class PublicationUploadForm(forms.ModelForm):
    # # def __init__(self, user = None, *args, **kwargs):
    # #     super(PublicationUploadForm, self).__init__(*args, **kwargs)
    # #     print(f"!!!!!!!!!!1USERRRR ISSSS!!!!!")
    # #     print(f"USERNAME = {user}")
    # #     print(f"!!!!!!!!!!1USERRRR ISSSS!!!!!")
    # #     if user:
    # #         self.user = user
    # #         self.fields['user'].queryset = user

    
    # # def __init__(self, *args, **kwargs):
    # #     print(self)
    #     # user_id = kwargs.pop('user_id', False)
    #     # # self.pid = kwargs.pop('pid', None)
    #     # super(PublicationUploadForm, self).__init__(*args, **kwargs)
    #     # if user_id:
    #     #     self.fields['user'] = forms.CharField(max_length=256)
    # class Meta:
    #     model = Publication
    #     fields = [
    #     'public',
    #     'file_path',
    #     'type',
    #     'title',
    #     'authors',
    #     'year',
    #     'month',
    #     'journal',
    #     'book_title',
    #     'publisher',
    #     'institution',
    #     'volume',
    #     'number',
    #     'pages',
    #     'note',
    #     'issue',
    #     # 'keywords',
    #     'url',
    #     'code',
    #     'doi',
    #     'abstract',
    #     'isbn'
    # ]
