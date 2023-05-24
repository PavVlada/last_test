from citeproc.source.bibtex import BibTeX

# Import the citeproc-py classes we'll use below.
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc import Citation, CitationItem
import tempfile


# Parse the BibTeX database.

bib_str = """@ARTICLE{serg1999may,
   author = {L[eslie] A. Aamport},
   title = {The Gnats and Gnus Document Preparation System},
   journal = {\mbox{G-Animal's} Journal},
   year = 1986,
   volume = 41,
   number = 7,
   pages = "73+",
   month = jul,
   note = "This is a full ARTICLE entry",
}"""
# tmp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False, suffix=".bib", encoding='utf8', dir='/home/jaabi484/diploma/the_last_diploma')
# bib_source = BibTeX('testbibtex.bib', encoding='utf8')
# tmp_file.write(bib_str)
# temp_file_name = tmp_file.name
# print(temp_file_name)
# tmp = open(temp_file_name)
# str_tmp = tmp.read()
# print(f"STR TMP: {str_tmp}")
# tmp.close()
bib_source = BibTeX('this.bib', encoding='utf8')
# tmp_file.close()

print("BIB SOURCE")
# load a CSL style (from the current directory)

bib_style = CitationStylesStyle('gost-r-7-0-5-2008-numeric.csl', locale='ru-RU', validate=False)


# Create the citeproc-py bibliography, passing it the:
# * CitationStylesStyle,
# * BibliographySource (BibTeX in this case), and
# * a formatter (plain, html, or you can write a custom formatter)

bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.plain)


# Processing citations in a document needs to be done in two passes as for some
# CSL styles, a citation can depend on the order of citations in the
# bibliography and thus on citations following the current one.
# For this reason, we first need to register all citations with the
# CitationStylesBibliography.

# citation1 = Citation([CitationItem('article-full')])
citation1 = Citation([CitationItem('Zakharov_2020')])
# citation2 = Citation([CitationItem('whole-set'), CitationItem('misc-full')])
# citation3 = Citation([CitationItem('techreport-full')])
# citation4 = Citation([CitationItem('mastersthesis-minimal')])
# citation5 = Citation([CitationItem('inproceedings-full'),
#                       CitationItem('unpublished-full')])
bibliography.register(citation1)
# bibliography.register(citation1)
# bibliography.register(citation2)
# bibliography.register(citation3)
# bibliography.register(citation4)
# bibliography.register(citation5)


# In the second pass, CitationStylesBibliography can generate citations.
# CitationStylesBibliography.cite() requires a callback function to be passed
# along to be called in case a CitationItem's key is not present in the
# bibliography.

def warn(citation_item):
    print("WARNING: Reference with key '{}' not found in the bibliography."
        .format(citation_item.key))


print('Citations')
print('---------')


print(bibliography.cite(citation1, warn))
# print(bibliography.cite(citation2, warn))
# print(bibliography.cite(citation3, warn))
# print(bibliography.cite(citation4, warn))
# print(bibliography.cite(citation5, warn))


# And finally, the bibliography can be rendered.

print('')
print('Bibliography')
print('------------')

for item in bibliography.bibliography():
    print(str(item))