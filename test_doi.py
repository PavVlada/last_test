import pdf2bib
from django.conf import settings
import pdf2doi
import os
import io


import json

# Import the citeproc-py classes we'll use below.
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON

def create_bibtex(path):
    pdf2bib.config.set('verbose',False)
    # print(f"NEW PATH: {new_path}")
    result = pdf2bib.pdf2bib(path)

    # output_path = os.path.join(settings.MEDIA_ROOT, 'output/1')
    # with io.open(output_path,'w',encoding='utf8') as f:
    #     f.write(result['validation_info'])
    print(result)
    return result

def get_doi(path):
    result = pdf2doi.pdf2doi(path)
    return result['validation_info']

json_input = get_doi("63-70.pdf")
json_data = json.loads(json_input)
json_data["id"] = 'ITEM'
json_data_list = [json_data]
json_again = json.dumps(json_data, indent=4)
print(json_again)
# bib_source = CiteProcJSON(json_data_list)

# bib_style = CitationStylesStyle('gost-r-7-0-5-2008-numeric.csl', locale='locales-ru-RU', validate=False)
# bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.html)
# citation = Citation([CitationItem('ITEM')])
# bibliography.register(citation)
# print(str(bibliography[0].bibliography()))

