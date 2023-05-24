from ajax_select import register, LookupChannel
from .models import Author, Editor

@register('author')
class AuthorLookup(LookupChannel):

    model = Author

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

    def format_item_display(self, item):
        return u"<span class='author'>%s</span>" % item.name


@register('editor')
class EditorLookup(LookupChannel):

    model = Editor

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

    def format_item_display(self, item):
        return u"<span class='author'>%s</span>" % item.name