import json
import re
import logging
import urllib.parse
from unidecode import unidecode

def remove_latex_codes(text):
    #It replaces any latex special code (e.g. {\`{u}}) by the "closest" unicode character (e.g. u). This is useful when
    #certain strings which might contain latex codes need to be used in contexts where only unicode characters are accepted
    
    #This regex looks for any substring that matches the pattern "{\string1{string2}}" where string1 can be anything,
    #and it replaces the whole substring by string2
    text_sanitized = re.sub(r"{\\[^\{]+{([\w]+)}}", r"\1",text)
    return text_sanitized

def make_bibtex(metadata):
    #Based on the metadata contained in the input dictionary metadata, it creates a valid bibtex entry
    #The ID of the bibtex entry has the format [lastname_firstauthor][year][first_word_title] all in lower case
    #If the tag url is present, any possible ascii code (e.g. %2f) is decoded
    #Note: the code below assumes that the field for the authors is either a string in the format "Name1 Lastname1 and Name2 Lastname2 and ... "
    #or a list of dictionaries in the format  [{'given': 'Name1', 'family': 'LastName1'}, {'given': 'Name2', 'family': 'LastName2'}, ... [{'given': 'NameN', 'family': 'LastNameN'}]
    
    data = metadata.copy()

    if 'author' in data.keys():
        authors = data['author']
    else:
        authors = ''

    # if not(type(authors) in (str, list)):
    #     raise TypeError('The value corresponding to the key ''author'' must be either a string or a list of strings')
    
    #Generate the ID by looking for last name of first author, year of publicaton, and first word of title
    try:
        if authors and isinstance(authors,list):
            firstauthor = authors[0]['given']
            lastname_firstauthor = authors[0]['family']
            # firstauthor = authors[0]
            # lastname_firstauthor = (firstauthor['family'].strip()).split(' ')[0]
        elif authors and isinstance(authors,str): 
            # lastname_firstauthor = authors.split(" and ")[0].split(" ")[-1] #We assume that the word before the first occurence of and is the last name of first author
            lastname_firstauthor = authors["family"]
            firstauthor = authors["given"]
        else: 
            lastname_firstauthor = ''
    except:
        lastname_firstauthor =''
    year = data['year'] if 'year' in data.keys() else ''
    try:
        first_word_title =  data['title'].split(' ')[0] if 'title' in data.keys()  else ''
    except:
        first_word_title =''
    id = lastname_firstauthor + str(year) + first_word_title
    id = id.lower()
    id = remove_latex_codes(id)
    id = unidecode(id) #This makes sure that the id of the bibtex entry is only made out of ascii characters (i.e. no accents, tildes, etc.)
    id = id.replace('-','') #Make sure to remove any possible hyphen
    if id == '':
        id = 'NoValidID'

    #Sanitize the URL
    if 'url' in data.keys():
        data['url'] = urllib.parse.unquote(data['url'])

    if not 'ENTRYTYPE' in data.keys():
        data['ENTRYTYPE'] = 'article'

    if  isinstance(authors,list):
        #if authors is defined as a list, it will have the format [{'given': 'Name1', 'family': 'LastName1'}, {'given': 'Name2', 'family': 'LastName2'}, ... [{'given': 'NameN', 'family': 'LastNameN'}]
        #We convert it into a string Name1 Lastname1 and Name2 Lastname2 and ... "
        # authors_string = " and ".join([ a.get('given', '') +  " " + a.get('family', '')  for a in authors if (('family' in a) or ('given' in a))])
        authors_string = " and ".join([ a.get('given', '') +  " " + a.get('family', '')  for a in authors if (('family' in a) or ('given' in a))])
        data['author'] = authors_string
    elif isinstance(authors,str):
        #if instead authors is a string, then it is already in the right format
        data['author'] = authors

    #Create the bibtex entry as a string 
    metadata_not_to_use = ['ENTRYTYPE','ID'] #These are temporary metadata, not useful for bibtex
    text = ["@"+data['ENTRYTYPE']+"{" + id]
    for key, value in data.items():
        if value and not (key in metadata_not_to_use):
            text.append("\t%s = {%s}" % (key, value))
    bibtex_entry = (",\n").join(text) + "\n" + "}"
    return bibtex_entry

bib_dict = dict()
bib_dict["ENTRYTYPE"] = "article"
bib_dict["author"] = list()
author1 = {
    "given": "Владимир",
    "family": "Колодезников"
}
author2 = {
    "given": "Ефим",
    "family": "Колодезников"
}
bib_dict["author"].append(author1)
bib_dict["author"].append(author2)
bib_dict["title"] = "Название публикации"
bib_dict["year"] = 2020
bib_dict["publisher"] = "Санкт-Петербургский государственный университет телекоммуникаций им. проф. Бонч-Бруевича"
bib_file = make_bibtex(bib_dict)
print(bib_file)