# -*- coding: utf-8 -*-
import re
test_string = """
Universitetet i Bergen
Uttak 26.10.2014
2159 papirartikler

Nyhetsklipp:

> VG 14.2.1948 side 9, VG, 14.02.1948

> VG 14.2.1948 side 9, VG, 14.02.1948

> VG 14.2.1948 side 9, VG, 14.02.1948

> Hognestad om New Age: Hummer og kanari, humbug og alvor, Aftenposten Morgen, 20.09.1989

> «Denne bok er et hospital» Le Figaro om «Les Fleurs du Mal», Dagbladet, 05.11.1999


VG 6.5.1946 side 8
------------------------------------------------------------------------------
VG, 06.05.1946
Side 8
Publisert på trykk. 


Fortsatt fra 3. side.) Kanskje er Morne en del tyngre på hånden enn Øverland, og 
han sakner dennes spiritualitet og bitende vidd. Men de følger begge den klaa & 
r under kampen mot hitleriamen.
© VG

Les hele nyheten på http://ret.nu/JrnQMsUG
==============================================================================

Forventningsfulle kristne i Sovjet
------------------------------------------------------------------------------
Aftenposten Morgen, 10.06.1988
WILLERSRUD AASMUND
Side 16
Publisert på trykk. 

AASMUND WILLERSRUD Moskva. - Kristne i SovjetUnionen har forhåpninger om en lettere 
fremtid. Inntil det motsatte er bevist, vil jeg være med og tro på en silk åpning,


også gjennom den offisielle lovgivning, sier biskop Andreas Aarflot. Han representerer 
også gjennom den offisielle lovgivning, sier biskop Andreas Aarflot. Han representerer 
Den norske kirke ved den russiskortodokse kirkes 1000års jubileum i Moskva. 
Konfrontert med pessimistiske uttalelser fra kristne dissidenter, som ikke tror 
i Kreml.

Bildetekst: Biskop Andreas Aarflot foran Hotel Ukraina i Moskva. Han representerer Den norske 
kirke under den russiskortodokse kirkes jubileum. (Foto: NTB)© Aftenposten

==============================================================================

Nobels litteraturpris til egypteren Naguib Mahfouz: Naturbegavet satiriker
------------------------------------------------------------------------------
Aftenposten Morgen, 14.10.1988
GLEICHMANN GABI
Side 7
Pu blisert på trykk. 

GABI GLEICHMANN Når årets Nobelpris i litteratur er tildelt egypteren Naguib Mahfouz, 
er det gledelig i dobbelt forstand; dels har Svenska Akademien valgt et spennende 
og vitalt forfatterskap,

dels innebærer utmerkelsen en oppmerksomhet mot en kultur som er relativt ukjent 
for 


"""
inputfile = 'testcorpus.txt'
str_equalspattern = "="*78
str_dashpattern = "-"*78
regex_index = re.compile('\>.*')
regex_singlearticle = re.compile(ur'(?:\-{78}).+?(?<=\n{3})', re.DOTALL)

atekst_index = []
atekst_meta = []
articles = []
first_headline = ''
first_article = ''


with open(inputfile, 'r') as f:
    file_string = f.read()

for i, string in enumerate(file_string.split(str_equalspattern)): #in this for-loop we deal with the meta info, the index and the first article
    if i == 0: # this is the index and the first article
        index_list = regex_index.findall(string) # finds all index items (beginning with >)
        for line in index_list: # loop through all the lines in the index
            line = line.replace('> ','') # removes the clutter
            atekst_index.append(line) # append to the atekst_index dictionary
        meta_string = string.splitlines() # split and put into a list
        meta_string = meta_string[1:4] # take the three first lines
        atekst_meta.append(meta_string) # put them into their own dictionary.
        string = string.partition(str_dashpattern) # split the line on the first dash-row
        meta_string = string[0].splitlines() # split into lines
        first_headline = meta_string[-1] # take the last element, which will be title for the first article, write it to a list
        string = string[2] # take the article part of the partition
        string = string.splitlines() # split it into lines
        first_article = string[1:-2] # choose the lines that contain the article (and the right line breaks)
        first_article = '\n'.join(first_article) # convert the list into a string

    else: # this is the rest of the articles
        articles.append(string) # take the rest and throw into the article set

articles.insert(0, first_article) #insert the first article into the articles dictionary
articles.insert(0, str_dashpattern) # insert first headline into the articles dictionary
articles.insert(0, first_headline) # insert first headline into the articles dictionary

article = regex_singlearticle.findall(''.join(articles))

for art in article:
    print art.replace(str_dashpattern, '').replace('\n\n','')

# print '-'*100 + 'Meta' + '-'*100
# print atekst_meta
# print '-'*100 + 'Index' + '-'*100
# print '\n'.join(atekst_index)
# print '-'*100 + 'Articles' + '-'*100
# print '\n'.join(articles)