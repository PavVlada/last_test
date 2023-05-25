import django_filters
from django_filters import CharFilter,ChoiceFilter,MultipleChoiceFilter

from .models import Publication

class PublicationFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    # authors = CharFilter(field_name='authors', lookup_expr='icontains')
    # publisher = CharFilter(field_name='publisher', lookup_expr='icontains')
    keyword__name = CharFilter(field_name='keyword__name', lookup_expr='icontains')
    class Meta:
        model = Publication
        fields = [
            # 'keyword',
            'publication_type',
            'citation_key',

            'author',

            'ISBN',
            
            'language',

            'journal',
            'publisher',
            'event',

            'title',
            'year',
            'DOI',
        ]