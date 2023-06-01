import json
from django.conf import settings
import os

from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON


def make_csl(input_data):
    data = dict()
    data["id"] = input_data["citation_key"]
    data["type"] = input_data["publication_type"]
    data["title"] = input_data["title"]
    data["author"] = list()
    data["author"].append({
        "family": input_data["author"].split(' ')[0],
        "given": input_data["author"].split( )[1]
        })
    

    for field in input_data.keys():
        if field == "coauthor":
            for coauthor in input_data[field]:
                data["author"].append({
                    "family": coauthor.split(' ')[0],
                    "given": coauthor.split(' ')[1]
                })
        if field == "editor":
            data["editor"] = [{
                "family": editor.split(' ')[0],
                "given": editor.split(' ')[1]} for editor in input_data["editor"]]
        if field == "collectioneditor":
            data["collection-editor"] = [{
                "family": collectioneditor.split(' ')[0],
                "given": collectioneditor.split(' ')[1]} for collectioneditor in input_data["collectioneditor"]]
        # if field == "reviewedauthor":
        #     data["reviewed-author"] = [{
        #         "family": reviewedauthor.split(' ')[0],
        #         "given": reviewedauthor.split(' ')[1]} for reviewedauthor in input_data["reviewedauthor"]]
        if field == "translator":
            data["translator"] = [{
                "family": translator.split(' ')[0],
                "given": translator.split(' ')[1]} for translator in input_data["translator"]]
        
        if field == "publisher":
            data["publisher"] = input_data["publisher"]
            data["publisher-place"] = input_data["address"]
        
        if field in ['abstract', 'archive', 'archive_location', 
                     'edition', 'genre', 'issue', 'language', 'medium',
                     'page', 'section', 'source', 'title', 'version', 'volume', 'note', 'URL',
                     'ISBN', 'DOI', 'ISSN']:
            data[field] = input_data[field]
        if field in ['collection_title', 'container_title', 'number_of_pages', 'number_of_volumes', 'title_short']:
            data[field.replace('_', '-')] = input_data[field]
        
        if field == "book":
            data["container-title"] = input_data["book"]
        
        if field == "journal":
            data["container-title"] = input_data["journal"]
            data["ISSN"] = input_data["ISSN"]

        if field == "year":
            issue_list = list()
            issue_list_1 = list()
            issue_list_1.append(input_data["year"])
            for i in ["month", "day"]:
                if i in input_data.keys():
                    issue_list_1.append(input_data[i])
            issue_list.append(issue_list_1)
            data["issued"] = {
                "date-parts": issue_list
            }
    print(f"DATA: {data}")

    # data_list.append(data)
    return data
    # dict_to_json = json.dumps(data_list, indent=4, ensure_ascii=False)
    # return make_cite(data["id"], dict_to_json)

# def make_cite(id, json_input):
def make_cite(data):
    data_list = list()
    data_list.append(data)
    json_input = json.dumps(data_list, indent=4, ensure_ascii=False)
    id = data["id"]
    json_data = json.loads(json_input)
    bib_source = CiteProcJSON(json_data)

    csl_dir = os.path.join(settings.BASE_DIR, 'csl')
    csl_path = os.path.join(csl_dir, 'gost2018.csl')
    bib_style = CitationStylesStyle(csl_path, locale='ru', validate=False)

    bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.html)

    citation1 = Citation([CitationItem(id)])

    bibliography.register(citation1)


    def warn(citation_item):
        print("WARNING: Reference with key '{}' not found in the bibliography."
            .format(citation_item.key))

    print('Citations')
    print('---------')

    print(bibliography.cite(citation1, warn))
    print('')
    print('Bibliography')
    print('------------')

    result = ""

    for item in bibliography.bibliography():
        result = str(item)
    result = result[2:]
    result.replace('  ', ' ')
    return result.replace('..', '.')



def create_cite():

    json_input = """
    [   
        {
            "id": "BOOK",
            "type": "book",
            "title": "Название книги",
            "author": [
                {
                    "family": "Колодезников",
                    "given": "Владимир"
                },
                {
                    "family": "Колодезников",
                    "given": "Ефим"
                }
            ],
            "editor": [
                {
                    "family": "Ардеев",
                    "given": "Дамир"
                },
                {
                    "family": "Данилова",
                    "given": "Агата"
                }
            ],
            "abstract": "Аннотация: супер интересная книга",
            "collection-title": "офиц.текст",
            "collection-number": "10",
            "volume": "5",
            "number-of-volumes": "10",
            "edition": "2",
            "publisher-place": "Санкт-Петербург",
            "publisher": "СПбГУТ им. Бонч-Бруевича",
            "issued": {
                "date-parts": [[2006]]
            },
            "number-of-pages": "200",
            "ISBN": "978-5-699-12014-7"
        }
    ]
    """

    json_data = json.loads(json_input)

    bib_source = CiteProcJSON(json_data)
    bib_style = CitationStylesStyle('gost2018.csl', locale='ru', validate=False)

    bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.html)

    citation1 = Citation([CitationItem('BOOK')])

    bibliography.register(citation1)


    def warn(citation_item):
        print("WARNING: Reference with key '{}' not found in the bibliography."
            .format(citation_item.key))

    print('Citations')
    print('---------')

    print(bibliography.cite(citation1, warn))



    print('')
    print('Bibliography')
    print('------------')

    for item in bibliography.bibliography():
        print(str(item))