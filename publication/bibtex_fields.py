article_fields = [
    'author',
    'title',
    'journal',
    'year',
    'volume',
    'pages',
    'note'
]


book_fields = [
    'author',
    'editor',
    'title',
    'publisher',
    'year',
    'volume',
    'series',
    'address',
    'edition',
    'month',
    'note'
]

inbook = [
    'author',
    'editor',
    'title',
    'chapter',
    'pages',
    'publisher',
    'year',
    'volume',
    'number',
    'series',
    'type',
    'address',
    'edition',
    'month',
    'note'
]
thesis = [
    'author',
    'title',
    'school',
    'year',
    'type',
    'address',
    'month',
    'note'
]
inproceedings = [
    'author',
    'title',
    'booktitle',
    'year',
    'editor',
    'volume',
    'series',
    'pages',
    'address',
    'month',
    'organization',
    'publisher',
    'note'
]
# Добавить к author еще и coauthor
# Добавить к collectionededitor еще и editor

#container-title -> [journal, booktitle]

dict_type_csl_bib = {
    "article-journal" : "article",
    "book": "book",
    "chapter": "inbook",
    "thesis" : "thesis",
    "paper-conference": "inproceedings"
}

dict_csl_bib = {

    "event": "booktitle",
    "abstract": "annote",
    "archive": "archiveprefix",
    "collection_title": "series",
    # "container_title": "booktitle" (для @inproceedings) / "journal" (для @article),
    "edition": "edition",
    "issue": "number",
    "number_of_pages": "pages",
    "number_of_volumes": "volumes",
    "number_of_pages": "page",
    "page": "pages", 
    "title": "title",
    "volume": "volume",
    "note": "note",
    "ISBN": "isbn",
    "URL": "url",
    "DOI": "doi",
}
# dict_csl_bib = {
#     "publication_type": "publication_type",
#     "citation_key": "citation_key",

#     "author": "author",
#     "editor": "editor",


#     "journal": "journal",
#     "publisher": "",
#     "event": "",

#     "abstract": "",
#     "archive": "",
#     "archive_location": "",
#     "call_number": "",
#     "collection_number": "",
#     "collection_title": "",
#     "container_title": "",
#     "edition": "",
#     "genre": "",
#     "issue": "",

#     "day": "",
#     "year": "",
#     "month": "",

#     "language": "",
#     "medium": "",
#     "number_of_pages": "",
#     "number_of_volumes": "",
#     "page": "",
#     "section": "",
#     "source": "",
#     "title": "",
#     "title_short": "",
#     "version": "",
#     "volume": "",

#     "note": "",
#     "ISBN": "",
#     "URL": "",
#     "DOI": "",
# }