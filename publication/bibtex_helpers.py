import pdf2bib
from django.conf import settings
import pdf2doi
import os
import io

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