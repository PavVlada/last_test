import pdf2bib
from django.conf import settings
import pdf2doi
import os
import io
import urllib.parse
from .bibtex_fields import dict_csl_bib, dict_type_csl_bib
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc import Citation, CitationItem

def create_bibtex(path):
    new_path = os.path.join(settings.MEDIA_ROOT, path)
    pdf2bib.config.set('verbose',False)
    # print(f"NEW PATH: {new_path}")
    result = pdf2bib.pdf2bib(new_path)

    # output_path = os.path.join(settings.MEDIA_ROOT, 'output/1')
    # with io.open(output_path,'w',encoding='utf8') as f:
    #     f.write(result['validation_info'])
    print(result)
    return result

def get_doi(path):
    new_path = os.path.join(settings.MEDIA_ROOT, path)
    result = pdf2doi.pdf2doi(new_path)
    print(result)
    return result

def test(data):
    for key, value in data.items():
        print(f"{key}: {value}")
    return "bibtex test"

def make_bibtex(metadata):
    # data = metadata.copy()
    print(f"METADATA: {metadata}")
    data = dict()
    for key, value in dict_csl_bib.items():
        if key in metadata:
            data[value] = metadata[key]
    print(data)
    data['type'] = dict_type_csl_bib.get(metadata['type'])
    print(data)
    if not data['type']:
        return dict()
    if 'pages' in data:
        data['pages'] = data['pages'].replace('-', '--')
    if data['type'] == 'inbook':
        data['booktitle'] = metadata['container-title']
    elif data['type'] == 'article':
        data['journal'] = metadata['container-title']
    if 'issued' in metadata:
        data['year'] = metadata['issued']['date-parts'][0][0]
        if  len(metadata['issued']['date-parts'][0]) == 2:
            data['month'] = metadata['issued']['date-parts'][0][1]
    authors_tmp = metadata['author']
    authors = list()
    for author in authors_tmp:
        authors.append(author["given"] + ' ' + author['family'])

    id = metadata['id']

    #Sanitize the URL
    if 'url' in data.keys():
        data['url'] = urllib.parse.unquote(data['url'])


    if  isinstance(authors,list):
        authors_string = " and ".join([author for author in authors])
        data['author'] = authors_string
    elif isinstance(authors,str):
        data['author'] = authors

    #Create the bibtex entry as a string 
    metadata_not_to_use = ['type'] #These are temporary metadata, not useful for bibtex
    text = ["@"+data['type'].upper()+"{" + id]
    result = dict()
    for key, value in data.items():
        if value and not (key in metadata_not_to_use):
            text.append("\t%s = {%s}" % (key, value))
    result['bibtex'] = (",\n").join(text) + "\n" + "}"
    result['id'] = id
    
    return result

# def make_style(id_item, bib_source, style):
#     print(f'id item: {id_item}')
#     print(f'bib source: {bib_source}')
#     style_dir = os.path.join(settings.BASE_DIR, 'csl')
#     style_path = os.path.join(style_dir, style + '.csl')
#     bib_style = CitationStylesStyle(style_path, locale='ru-RU', validate=False)
#     bibliography = CitationStylesBibliography(bib_style, bib_source)
#     citation1 = Citation([CitationItem(id_item)])
#     bibliography.register(citation1)
#     def warn(citation_item):
#         print("WARNING: Reference with key '{}' not found in the bibliography."
#           .format(citation_item.key))


#     print('Citations')
#     print('---------')

#     print(bibliography.cite(citation1, warn))
#     print('')
#     print('Bibliography')
#     print('------------')
#     result = ''
#     for item in bibliography.bibliography():
#         result = str(item)
#         print(str(item))
#     return result