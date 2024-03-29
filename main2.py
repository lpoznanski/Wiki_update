import os
import csv

import pandas as pd

import bs4.element
from bs4 import BeautifulSoup as bs

content = []

with open(f'results/result.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    docs = os.listdir('documents/')
    for doc in docs:
        with open('documents/' + doc, "r") as file:
            content = file.readlines()

        ana_is_multi = {'*': 'ana'}
        content = "".join(content)
        soup = bs(content, "xml", multi_valued_attributes=ana_is_multi)

        document_qid = soup.TEI['xml:id']

        # tags_of_interest = ['persName', 'placeName', 'orgName', 'affiliation', 'date', 'education', 'note']

        # def format_multiline(str):
        #     return '"' + str + '"'

        def format_string(str):
            return '"' + str + '"'

        p_list = {
            'beneficjent_laski': 'P20',
            # 'posiadane_beneficjum': 'P53',
            # 'posiadana_ekspektatywa_na_beneficjum': 'P54',
            'zajmowane_stanowisko': 'P32',
            'informacje_o_posiadaniu_stanowiska': 'P33',
            'education': 'P31',
            'przedmiot_nadania': 'P34',
            # 'osoba_w_sporze': ['P29', 'Q471'],
            # 'zmarly_w_kurii': ['P29', 'Q472'],
            # 'rezygnacja_z_beneficjum': ['P29', 'Q473'],
            'stopien_swiecen': 'P35',
            'wspolmalzonek': 'P4',
            'ojciec': 'P27',
            'dziecko': 'P28',
            'nepos': 'P29',
            'familiaris': 'P30',
            'wystawca': 'P18',
            'odbiorca': 'P19',
            'egzekutor': ['P39', 'Q424'],
            'taksa_dokumentu': 'P23',
            'urzednik_kurialny': 'P22',
            'nota_marginalna': 'P21',
            'miejsce_wystawienia_dokumentu': 'P15',
            'data_dokumentu': 'P14',
            'tytulatura': 'P25',
            'diecezja': 'P2',
            'pochodzenie_spoleczne': 'P37'
        }

        reverse_p_list = {
            'wspolmalzonek': 'P4',
            'ojciec': 'P28',
            'dziecko': 'P27',
            'zajmowane_stanowisko': 'P40',
            'informacje_o_posiadaniu_stanowiska': 'P40',
            'posiadana_ekspektatywa_na_beneficjum': 'P28'
        }

        volumeny = {
            'RL_6': '',
            'RL_34': 'Q116'
        }

        formy_zachowania = {
            'cop.': 'Q427'
        }

        typy_edycji = {
            'edycja': 'Q426',
            'regest': 'Q425'
        }



        # with open(f'results/{document_qid}.csv', 'w', newline='') as file:
        #     writer = csv.writer(file)

        #metadane
        #P55
        typ = soup.find(scheme="forma_dokumentu")['target']
        writer.writerow([document_qid, 'P1', typ, 'S3', document_qid, '', '', '', '', '', '', '', '', '', '', '', ''])

        #bez zmian
        rodzaj_laski = soup.find(scheme="rodzaj_sprawy")['target']
        writer.writerow([document_qid, 'P7', rodzaj_laski, 'S3', document_qid])

        #bez zmian
        formularz = soup.find(scheme="formularz")['target']
        writer.writerow([document_qid, 'P8', formularz, 'S3', document_qid])

        #bez zmian
        regest = soup.teiHeader.profileDesc.abstract.p.string
        regest = ' '.join(regest.split())
        writer.writerow([document_qid, 'P9', format_string(regest), 'S3', document_qid])

        #całkowicie inaczej w witness będzie Q manifestacji + nowe P54 i odwrotne P53
        zrodlo = soup.sourceDesc.listWit.children
        for item in zrodlo:
            print(item)
        folia = []
        for element in [item.string.split('f. ')[-1] for item in zrodlo.find_all('locus')]:
            folia.append('P13')
            folia.append(format_string(element))
        volumen = ['P12', volumeny[zrodlo['source']]]
        forma_zachowania = ['P11', formy_zachowania[zrodlo['ana'][0]]]

        #tego nie będzie!
        # byty_w_sygnaturze
        writer.writerow([document_qid, 'P10', format_string(zrodlo.contents[0])] + forma_zachowania + volumen + folia + ['S3', document_qid])

        #tak samo
        data_dokumentu = soup.teiHeader.profileDesc.creation.date['when']
        formatted_date = '+' + data_dokumentu + 'T00:00:00Z/11/J'
        writer.writerow([document_qid, 'P14', formatted_date, 'S3', document_qid])

        #tak samo
        miejsce_wystawienia = soup.teiHeader.profileDesc.creation.placeName['ref']
        writer.writerow([document_qid, 'P15', miejsce_wystawienia.split('-')[-1], 'S3', document_qid])

        #tak samo
        wydania = soup.find_all('bibl')
        for item in wydania:
            writer.writerow([document_qid, 'P16', format_string(item.string), 'P17', typy_edycji[item['type']], 'S3', document_qid])


        #tekst

        # complete_tags = soup.body.p.descendants
        # for child in complete_tags:
        #     if type(child) == bs4.element.Tag and child['type']:
        #         print('-')
        #         print(child)
        #         print(child['type'])

        #idzie do osoby w inny sposób wystawca Q536
        wystawcy = soup.find_all(ana='wystawca')
        for item in wystawcy:
            writer.writerow([document_qid, p_list['wystawca'], (item['ref'].split('-'))[-1], 'S3', document_qid])

        #P39 Q537
        odbiorcy = soup.find_all(ana='odbiorca')
        for item in odbiorcy:
            writer.writerow([document_qid, p_list['odbiorca'], (item['ref'].split('-'))[-1], 'S3', document_qid])

        #P39 Q538
        beneficjenci_laski = soup.find_all(ana='beneficjent_laski')
        for item in beneficjenci_laski:
            writer.writerow([document_qid, p_list['beneficjent_laski'], (item['ref'].split('-'))[-1],'S3', document_qid])

        #P656 tak samo jak z wystawcą, odbiorcą etc.
        przedmioty_nadania = soup.find_all(ana='przedmiot_nadania')
        for item in przedmioty_nadania:
            writer.writerow([document_qid, p_list['przedmiot_nadania'], (item['ref'].split('-'))[-1], 'S3', document_qid])

        #bez zmian
        tytulatury = soup.find_all(ana='tytulatura')
        for item in tytulatury:
            writer.writerow([(item['ref'].split('-'))[-1], p_list['tytulatura'], format_string(' '.join(''.join([element for element in item.descendants if type(element)==bs4.element.NavigableString]).split())), 'S3', document_qid])

        #bez zmian
        education_info = soup.find_all(ana='education')
        for item in education_info:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['education'], (item['ref'].split('-'))[-1], 'S3', document_qid])

        # pracownik_kurii = soup.find(type='pracownik_kurii')
        # writer.writerow([document_qid, p_list['pracownik_kurii'], (pracownik_kurii['ref'].split('-'))[-1]])
        #
        # taksa_dokumentu = soup.find(type='magister_registrów').measure['quantity']
        # writer.writerow([document_qid, p_list['taksa_dokumentu'], taksa_dokumentu])

        #idzie do manifestacji - witness! w przyszłości może się zdarzyć, że jest kilka maifestacji...
        noty_marginalne = soup.find_all('note')
        for nota in noty_marginalne:
            if nota['place'] in ['left_margin', 'right_margin', 'upper-margin', 'lower-margin']:
                writer.writerow([document_qid, p_list['nota_marginalna'], format_string(nota.string), 'S3', document_qid])


        document_fee = soup.find(type='document_fee')
        pracownik_kurii = soup.find(ana='urzednik_kurialny')
        taksa_dokumentu = soup.find(ana='urzednik_kurialny').measure['quantity']
        writer.writerow([document_qid, p_list['nota_marginalna'], format_string(' '.join(''.join([element for element in document_fee.descendants if type(element)==bs4.element.NavigableString]).split())), p_list['urzednik_kurialny'], (pracownik_kurii['ref'].split('-'))[-1], p_list['taksa_dokumentu'], taksa_dokumentu, 'S3', document_qid])

        #bez zmian
        malzonkowie = soup.find_all(ana='wspolmalzonek')
        for item in malzonkowie:
            try:
                if item['type']:
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['wspolmalzonek'], (item['ref'].split('-'))[-1], 'P38', format_string(item['type']), 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['wspolmalzonek'], (item.parent['ref'].split('-'))[-1], 'P38', format_string(item['type']), 'S3', document_qid])
                else:
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['wspolmalzonek'], (item['ref'].split('-'))[-1], 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['wspolmalzonek'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])
            except KeyError:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['wspolmalzonek'], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['wspolmalzonek'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])

        #bez zmian
        for relacja_rodzinna in ['ojciec', 'dziecko']:
            znalezione_relacje = soup.find_all(ana=relacja_rodzinna)
            for item in znalezione_relacje:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[relacja_rodzinna], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[relacja_rodzinna], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])

        #bez zmian
        for dalsza_relacja in ['nepos', 'familiaris']:
            znalezione_dalsze_relacje = soup.find_all(ana=dalsza_relacja)
            for item in znalezione_dalsze_relacje:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[dalsza_relacja], (item['ref'].split('-'))[-1]], 'S3', document_qid)

        #bez zmian
        for status_beneficjow in ['zajmowane_stanowisko', 'informacje_o_posiadaniu_stanowiska']:
            znalezione = soup.find_all(ana=status_beneficjow)
            for item in znalezione:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[status_beneficjow], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[status_beneficjow], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])

        #charakter wystąpienia!! Q657 (osoba w sporze), Q424 (egzekutor)
        for rola in ['osoba_w_sporze', 'zmarly_w_kurii', 'rezygnacja_z_beneficjum', 'egzekutor']:
            znalezione_role = soup.find_all(ana=rola)
            for item in znalezione_role:
                writer.writerow([(item['ref'].split('-'))[-1], p_list[rola][0], p_list[rola][1], 'S3', document_qid])

        #bez zmian
        for status in ['pochodzenie_spoleczne', 'stopien_swiecen', 'rola_spoleczna']:
            statusy = soup.find_all(ana=status)
            for item in statusy:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[status], (item['ref'].split('-'))[-1], 'S3', document_qid])

        #bez zmian
        diecezje = soup.find_all(ana='diecezja')
        for item in diecezje:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['diecezja'], (item['ref'].split('-'))[-1], 'S3', document_qid])

        #byty w dokumencie - nie dawać dzieci!! na razie bez dzieci, a potem zobaczymy
        for tag in ['persName', 'affiliation', 'settlement']:
            refs = []
            result = soup.find_all(tag)
            for i in result:
                if (i['ref'].split('-'))[-1] not in refs:
                    refs.append((i['ref'].split('-'))[-1])
                    writer.writerow([document_qid, 'P24', (i['ref'].split('-'))[-1], 'S3', document_qid])
                    writer.writerow([(i['ref'].split('-'))[-1], 'P26', document_qid,'S3', document_qid])

        #Kto jest czyim familiarisem/neposem?
        #Jak będzie tagowana tytulatura i education?
        #Jak z beneficjami?
        #trzeba ogarnąć catRef, żeby attr były spójne"
        #byty w sygnaturze - skąd wziąć?
        #role? Muszą być powiązane z osobą
        #czy będziemy używać collection w końcu?

#zapisywanie do xls
cvsDataframe = pd.read_csv('results/result.csv')
resultExcelFile = pd.ExcelWriter('result.xlsx')
cvsDataframe.to_excel(resultExcelFile, index=False, header=False)
resultExcelFile._save()