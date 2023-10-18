import os
from bs4 import BeautifulSoup as bs

content = []

docs = os.listdir('documents/')
for doc in docs:
    with open('documents/' + doc, "r") as file:
        content = file.readlines()

    type_is_multi = {'*': 'type'}
    content = "".join(content)
    soup = bs(content, "xml", multi_valued_attributes=type_is_multi)

    document_qid = soup.publicationStmt.idno.string

    volumeny = {
        'RL_6': 'Q382',
        'RL_34': 'Q401'
    }

    formy_zachowania = {
        'cop.': 'Q388'
    }


    zrodlo = soup.sourceDesc.listWit.witness
    folia = []
    for element in  [item.string.split('f. ')[-1] for item in zrodlo.find_all('locus')]:
        folia.append('S16')
        folia.append(element)
    volumen = ['S14', volumeny[zrodlo['source']]]
    forma_zachowania = ['S20', formy_zachowania[zrodlo['ana']]]
    # byty_w_sygnaturze
    print([document_qid, 'P8', zrodlo.contents[0]] + folia + volumen + forma_zachowania)