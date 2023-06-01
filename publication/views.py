from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Publication, Contributor, Event, Publisher, Journal
from .forms import PublicationForm
from .bibtex_helpers import create_bibtex, test, make_bibtex
from .cite_helpers import *
from django.conf import settings

from .filters import PublicationFilter

from taggit.models import Tag

from ajax_select import register, LookupChannel

from dal import autocomplete

    

class PublicationList(ListView):
    model = Publication
    # publications = Publication.objects.order_by('-date_posted')
    context_object_name = 'publications'
    # form = PublicationListForm()
    # listFilter = PublicationFilter()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['publications'] = context['publications'].filter(public=True) | context['publications'].filter(user=self.request.user)
        else:
            context['publications'] = context['publications'].filter(public=True)

        context['list_filter'] = PublicationFilter(self.request.GET, queryset=context['publications'])
        context['publications'] = context['list_filter'].qs
        # context['has_filter'] = any(field in self.request.GET for field in set(context['list_filter'].get_fields()))
        context['has_filter'] = len(context['publications']._has_filters().__dict__['children']) > 0
        
        # search_input = self.request.GET.get('search-area') or ''
        # if search_input: 
        #     if self.request.user.is_authenticated:
        #         context['publications'] = context['publications'].filter(public=True, title__icontains=search_input) | context['publications'].filter(user=self.request.user, title__icontains=search_input)
        #     else:
        #         context['publications'] = context['publications'].filter(public=True, title__icontains=search_input)
        
        # context['search_input'] = search_input
        return context


class MyPublicationList(LoginRequiredMixin, ListView):
    model = Publication
    context_object_name = 'publications'
    template_name = 'publication/publication_list_my.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['publications'] = context['publications'].filter(user=self.request.user)
        return context


class PublicationDetail(DetailView):
    model = Publication
    template_name = 'publication/publication.html'
    context_object_name = 'publication'
    form_class = PublicationForm
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['media'] = settings.MEDIA_URL
        return context


class PublicationCreate(LoginRequiredMixin, CreateView):
    # publication = Publication.objects.all()
    # common_keyword = Publication.keyword.most_common()[:4]
    model = Publication
    context_object_name = 'publication'
    template_name = 'publication/publication_create.html'
    success_url = reverse_lazy('publications')
    form_class = PublicationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)

        data = form.cleaned_data.copy()
        new_data = dict()
        new_data['author'] = str(data['author'])
        for contributor_type in ['coauthor', 'editor', 'collectioneditor', 'reviewedauthor', 'translator']:
            if data[contributor_type]:
                new_data[contributor_type] = [str(contributor) for contributor in data[contributor_type]]
        

        if data['journal']:
            new_data['journal'] = data['journal'].name
            new_data['ISSN'] = data['journal'].ISSN

        if data['publisher']:
            new_data['publisher'] = data['publisher'].name
            new_data['address'] = data['publisher'].address

        if data['book']:
            new_data['book'] = data['book'].title
        
        if data['event']:
            new_data['event'] = data['event'].title

        
        for value in [
            'publication_type',
            'citation_key', 

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
            'note',

            'URL',
            'ISBN', 
            'DOI',
            'note']:
            if data[value]:
                new_data[value] = data[value]
        csl_data = make_csl(new_data)
        bibtex_result = make_bibtex(csl_data)
        self.object.bibtex = bibtex_result['bibtex']
        result_cite = make_cite(csl_data)
        print(f"RESULT CITE:\n{result_cite}")
        self.object.gost2018 = result_cite

        # tmp = make_bibtex(new_data)
        # self.object.bibtex = tmp['bibtex']
        # self.object.citation_key = tmp['id']
        self.object.save()

        form.save_m2m()

        return super(PublicationCreate, self).form_valid(form)
    
    def view_form(request):
        form = PublicationForm(request.POST)
        if form.is_valid():
            new_publication = form.save(commit=False)
            new_publication.save()
            form.save_m2m()

            

class PublicationUpload(LoginRequiredMixin, CreateView):
    model = Publication
    context_object_name = 'publication'
    template_name = 'publication/publication_upload.html'
    form_class = PublicationForm

    # success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        # result = create_bibtex(str(self.object.file_path))

        # form.instance.bibtex = result['bibtex']

        # metadata = result['metadata']

        # if metadata is None:
        #     metadata = result['metadata']


        # form.instance.title = metadata['title']
        # form.instance.pages = metadata['page']
        # form.instance.type = 'article'
        # form.instance.year = metadata['year']
        # form.instance.month = metadata['month']
        # form.instance.journal = metadata['journal']
        # form.instance.volume = metadata['volume']
        # form.instance.issue = metadata['issue']
        # form.instance.publisher = metadata['publisher']
        # form.instance.url = metadata['url']
        # form.instance.doi = metadata['doi']
        # form.instance.authors = f"{metadata['author'][0]['family']} {metadata['author'][0]['given']}"
        # self.object = form.save()

        # print(f"result in form valid: {result}")
        return super(PublicationUpload, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('publication-update', kwargs={'pk': self.object.pk})
    # def model_form_upload(request, self):
    #     if request.method == 'GET':
    #         print("GET METHOD IS USED")
    #         form = PublicationUploadForm(request.POST, request.FILES)
    #         # form.instance.user = self.request.user
    #         if form.is_valid():
    #             form.save()

    #     if request.method == 'POST':
    #         print("POST METHOD IS USED")
    #         form = PublicationUploadForm(request.POST, request.FILES)
    #         # form.instance.user = self.request.user
    #         if form.is_valid():
    #             form.save()
    #             return redirect('publications')
    #     else:
    #         form = PublicationForm()
    #     return render(request, 'publication/publication_update.html', {
    #         'form': form
    #     })

    
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.date_posted = timezone.now()

    #     # pub_id=self.kwargs['pk']
    #     send_file_path = self.kwargs['file_path']
    #     print(f"send file path = {send_file_path}")
    #     # print(f"pk = {pub_id}")

    #     form.instance.title = "CREATED AUTOMATICALLY"
    #     form.instance.year = 1999
    #     form.instance.type = "article"
    #     form.instance.authors = "Аноним"
    #     return super(PublicationUpload, self).form_valid(form)
    
    # def form_invalid(self, form):
    #     print("INVALID")



    # def model_form_upload(request):
    #     if request.method == 'POST':
    #         print("POST METHOD IS USED")
    #         form = PublicationForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('publications')
    #     else:
    #         form = PublicationForm()
    #     return render(request, 'publication/publication_update.html', {
    #         'form': form
    #     })

    # def get_success_url(self):
    #     pub_id=self.kwargs['pk']
    #     send_file_path = self.kwargs['file_path']
    #     print(f"send file path = {send_file_path}")
    #     create_bibtex(send_file_path)
    #     # return reverse_lazy('publication-update', kwargs={'pk': pub_id})
    #     return reverse_lazy('publication-update')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.date_posted = timezone.now()
    #     return super(PublicationCreate, self).form_valid(form)
    
    # def model_form_upload(request):
    #     if request.method == 'POST':
    #         form = PublicationForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('publications')
    #     else:
    #         form = PublicationForm()
    #     return render(request, 'publication/publication_create.html', {
    #         'form': form
    #     })


class PublicationUpdate(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm
    context_object_name = 'publication'
    template_name = 'publication/publication_create.html'
    success_url = reverse_lazy('publications') # url name

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)

        data = form.cleaned_data.copy()
        new_data = dict()
        new_data['author'] = str(data['author'])
        for contributor_type in ['coauthor', 'editor', 'collectioneditor', 'reviewedauthor', 'translator']:
            if data[contributor_type]:
                new_data[contributor_type] = [str(contributor) for contributor in data[contributor_type]]
        

        if data['journal']:
            new_data['journal'] = data['journal'].name
            new_data['ISSN'] = data['journal'].ISSN

        if data['publisher']:
            new_data['publisher'] = data['publisher'].name
            new_data['address'] = data['publisher'].address

        if data['book']:
            new_data['book'] = data['book'].title
        
        if data['event']:
            new_data['event'] = data['event'].title

        
        for value in [
            'publication_type',
            'citation_key', 

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
            'note',

            'URL',
            'ISBN', 
            'DOI',
            'note']:
            if data[value]:
                new_data[value] = data[value]
        csl_data = make_csl(new_data)
        bibtex_result = make_bibtex(csl_data)
        self.object.bibtex = bibtex_result['bibtex']
        result_cite = make_cite(csl_data)
        print(f"RESULT CITE:\n{result_cite}")
        self.object.gost2018 = result_cite

        # tmp = make_bibtex(new_data)
        # self.object.bibtex = tmp['bibtex']
        # self.object.citation_key = tmp['id']
        self.object.save()

        form.save_m2m()

        return super(PublicationUpdate, self).form_valid(form)
    
    def view_form(request):
        form = PublicationForm(request.POST)
        if form.is_valid():
            new_publication = form.save(commit=False)
            new_publication.save()
            form.save_m2m()


class PublicationDelete(LoginRequiredMixin, DeleteView):
    model = Publication
    context_object_name = 'publication'
    success_url = reverse_lazy('publications') # url name


class ContributorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Contributor.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def create(self, text):
        return Contributor.objects.create(name=text)


class PublisherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Publisher.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
    def create_object(self, text):
        name, address = text.split('|')
        return Publisher.objects.create(name=name.strip(), address=address.strip())

class JournalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Journal.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
    def create_object(self, text):
        name, issn = text.split('|')
        return Journal.objects.create(name=name.strip(), ISSN=issn.strip())


class PublicationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Publication.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class EventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Event.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def create(self, text):
        return Event.objects.create(name=text)
