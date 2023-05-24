from django import forms
from .models import Publication, Author, Publisher, Journal, Editor
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from dal import autocomplete

from ajax_select.fields import AutoCompleteSelectMultipleField
from ajax_select import make_ajax_field

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ['name']

# class PublisherForm(forms.ModelForm):
#     name = forms.ModelChoiceField(
#         queryset=Publisher.objects.all(),
#         widget=autocomplete.ModelSelect2(url='publisher-autocomplete')
#     )
#     class Meta:
#         model = Publisher
#         fields = ['name']

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
    author = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='author-autocomplete')
    )
    editor = forms.ModelMultipleChoiceField(
        queryset=Editor.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(url='editor-autocomplete')
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='publisher-autocomplete')
    )
    journal = forms.ModelChoiceField(
        queryset=Journal.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='journal-autocomplete')
    )
    # author = AutoCompleteSelectMultipleField('author')
    # editor = AutoCompleteSelectMultipleField('editor')
    class Meta:
        model = Publication
        # author = make_ajax_field(Contributor,'author','person')
        fields = [
            # 'date_posted',
            'public',
            'file_path',
            'keyword',
            'publication_type',
            'citation_key',

            'author',
            'abstract',
            'annote',
            'booktitle',
            'chapter',
            'editor',
            'edition',
            'howpublished',
            'ISBN',
            'journal',
            'language',
            'month',
            'note',
            'number',
            'page',
            'publisher',
            'title',
            'URL',
            'volume',
            'year',

            'issue',
            'DOI',
            'bibtex'
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
