import csv
from bs4 import BeautifulSoup as bs

content = []

with open("test.xml", "r") as file:
    content = file.readlines()

content = "".join(content)
soup = bs(content, "lxml-xml")


document_qid = 'QXXX'
# document_qid = soup.publicationStmt.idno

tags_of_interest = ['persName', 'placeName', 'orgName', 'affiliation', 'date', 'education', 'note']

p_list = {
    'beneficjent_łaski': 'P25',
    'posiadane_beneficjum': 'P53',
    'posiadana_ekspektatywa_na_beneficjum': 'P54',
    'education': 'P42',
    'przedmiot_nadania': 'P52',
    'osoba_w_sporze': '',
    'zmarły_w_kurii': '',
    'rezygnacja_z_beneficjum': '',
    'mąż': 'P56',
    'ojciec': 'P57',
    'żona': 'P33',
    'dziecko': 'P58',
    'nepos': 'P59',
    'familiaris': 'P60',
    'wystawca': 'P17',
    'odbiorca': 'P23',
    'egzekutor': '',
    'taksa_dokumentu': 'P30',
    'magister_registrów': 'P31',
    'nota_marginalna': 'P34',
    'miejsce_wystawienia_dokumentu': 'P13',
    'data_dokumentu': 'P12',
    'tytulatura': 'P38'
}

typy_dokumentow = {
    '#bulla': 'Q402'
}

rodzaje_lask = {
    '#ekspektatywa': 'Q392'
}

formularze = {
    '#dignum': 'Q434'
}

typy_edycji = {
    'edycja': 'Q385',
    'regest': 'Q386'
}



with open(f'{document_qid}.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    #metadane
    typ = soup.find(scheme="#typDokumentu")['target']
    writer.writerow([document_qid, 'P1', typy_dokumentow[typ]])

    rodzaj_laski = soup.find(scheme="#rodzajLaski")['target']
    writer.writerow([document_qid, 'P24', rodzaje_lask[rodzaj_laski]])

    formularz = soup.find(scheme="#formularz")['target']
    writer.writerow([document_qid, 'P19', formularze[formularz]])

    regest = soup.teiHeader.profileDesc.abstract.p.string
    writer.writerow([document_qid, 'P11', regest])

    zrodlo = soup.witness
    writer.writerow([document_qid, 'P8', 'xxx'])

    data_dokumentu = soup.teiHeader.profileDesc.creation.date['when']
    formatted_date = '+' + data_dokumentu + 'T00:00:00Z/11'
    writer.writerow([document_qid, 'P12', formatted_date])

    miejsce_wystawienia = soup.teiHeader.profileDesc.creation.placeName['ref']
    writer.writerow([document_qid, 'P13', miejsce_wystawienia])

    wydania = soup.find_all('bibl')
    for item in wydania:
        writer.writerow([document_qid, 'P17', item.string, 'P18', typy_edycji[item['type']]])



    #tekst

    for p in p_list:
            

    # wystawca = soup.find(type='wystawca')
    # print(wystawca['ref'])
    #
    # maz = soup.find(type='mąż')
    # print(maz['ref'])
    # print(maz.parent['ref'])



    # body = soup.body.p
    # for child in body:
    #     if child.name in tags_of_interest and child['type']:
    #         writer.writerow([document_qid, 'P1', child['ref']])



    #1. usunąć 'va-' z refów
    #2. metadane - refy?
    #3. podejście do iteracji...