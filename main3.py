import os
import csv

import pandas as pd

import bs4.element
from bs4 import BeautifulSoup as bs

content = []

with open(f'results/result.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    docs = os.listdir('documents/')
    for doc in docs:
        with open('documents/' + doc, "r", encoding='utf-8') as file:
            content = file.readlines()

        ana_is_multi = {'*': 'ana'}
        source_is_multi = {'*': 'source'}
        content = "".join(content)
        soup = bs(content, "xml", multi_valued_attributes=ana_is_multi)
        soup_meta = bs(content, "xml", multi_valued_attributes=source_is_multi)
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
            # 'osoba_w_sporze': '',
            'stopien_swiecen': 'P35',
            # 'zmarly_w_kurii': 'Q',
            # 'rezygnacja_z_beneficjum': 'Q',
            'wspolmalzonek': 'P4',
            'ojciec': 'P27',
            'dziecko': 'P28',
            'nepos': 'P29',
            'familiaris': 'P30',
            'wystawca': 'P18',
            'odbiorca': 'P19',
            'egzekutor': 'Q424',
            'taksa_dokumentu': 'P23',
            'urzednik_kurialny': 'P22',
            'nota_marginalna': 'P21',
            'miejsce_wystawienia_dokumentu': 'P15',
            'data_dokumentu': 'P14',
            'tytulatura': 'P25',
            'diecezja': 'P2',
            'pochodzenie_spoleczne': 'P37',
            'rola_spoleczna': 'P36',
            'lokalizacja_noty': 'P58'
            # 'protektor': '',
            # 'osoba_wystepujaca_w_dokumencie': ''
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
            'regest': 'Q425',
            'wzmianka': 'Q2122'
        }

        lokalizacje_not = {
            'in_line': 'Q2101',
            'end': 'Q2102',
            'in_marg': 'Q1638'
        }


        # with open(f'results/{document_qid}.csv', 'w', newline='') as file:
        #     writer = csv.writer(file)

        writer.writerow(['', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        #typ = soup.find(scheme="forma_dokumentu")['target']
        #writer.writerow([document_qid, 'P55', typ.split("-")[-1], '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        rodzaj_laski = soup.find(scheme="rodzaj_sprawy")['target']
        writer.writerow([document_qid, 'P7', rodzaj_laski.split("-")[-1], '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        formularz = soup.find(scheme="formularz")['target']
        writer.writerow([document_qid, 'P8', formularz.split("-")[-1]])

        sprawa = soup.find(scheme="sprawa")['target']
        writer.writerow([document_qid, 'P57', sprawa.split("-")[-1]])
        writer.writerow([sprawa.split("-")[-1], 'P57', document_qid])

        regest = soup.teiHeader.profileDesc.abstract.p.string
        regest = ' '.join(regest.split())
        writer.writerow([document_qid, 'P9', format_string(regest)])

        zrodla = soup_meta.find_all('witness')
        for zrodlo in zrodla:
            for wit in zrodlo['source']:
                writer.writerow([document_qid, 'P54', wit.split("-")[-1]])
                writer.writerow([wit.split("-")[-1], 'P53', document_qid])

        data_dokumentu = soup.teiHeader.profileDesc.creation.date['when']
        formatted_date = '+' + data_dokumentu + 'T00:00:00Z/11/J'
        writer.writerow([document_qid, 'P14', formatted_date])

        miejsce_wystawienia = soup.teiHeader.profileDesc.creation.placeName['ref']
        writer.writerow([document_qid, 'P15', miejsce_wystawienia.split('-')[-1]])

        wydania = soup.find_all('bibl')
        for item in wydania:
            if item.string:
                writer.writerow([document_qid, 'P16', format_string(item.string), 'P17', typy_edycji[item['type']]])
            else:
                pass

        #tekst

        # complete_tags = soup.body.p.descendants
        # for child in complete_tags:
        #     if type(child) == bs4.element.Tag and child['type']:
        #         print('-')
        #         print(child)
        #         print(child['type'])

        #sprawdzenie charakteru wystąpienia
        wyst = []

        wystawcy = soup.find_all(ana='wystawca')
        for item in wystawcy:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q536', 'S3', document_qid])
            wyst.append(item['ref'])

        odbiorcy = soup.find_all(ana='odbiorca')
        for item in odbiorcy:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q537', 'S3', document_qid])
            wyst.append(item['ref'])

        beneficjenci_laski = soup.find_all(ana='beneficjent_laski')
        for item in beneficjenci_laski:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q538', 'S3', document_qid])
            wyst.append(item['ref'])

        protektorzy = soup.find_all(ana='protektor')
        for item in protektorzy:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2077', 'S3', document_qid])
            wyst.append(item['ref'])

        osoby_w_dokumencie = soup.find_all(ana='osoba_wystepujaca_w_dokumencie')
        for item in osoby_w_dokumencie:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2078', 'S3', document_qid])
            wyst.append(item['ref'])

        przedmioty_nadania = soup.find_all(ana='przedmiot_nadania')
        for item in przedmioty_nadania:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q656', 'S3', document_qid])
            wyst.append(item['ref'])

        # rezygnacja? zmarły?
        for rola in ['osoba_w_sporze', 'zmarly_w_kurii', 'rezygnacja_z_beneficjum', 'egzekutor']:
            znalezione_role = soup.find_all(ana=rola)
            for item in znalezione_role:
                writer.writerow([(item['ref'].split('-'))[-1], 'P39', p_list[rola], 'S3', document_qid])

        tytulatury = soup.find_all(ana='tytulatura')
        for item in tytulatury:
            writer.writerow([(item['ref'].split('-'))[-1], p_list['tytulatura'], format_string(' '.join(''.join([element for element in item.descendants if type(element)==bs4.element.NavigableString]).split())), 'S3', document_qid])

        education_info = soup.find_all(ana='education')
        for item in education_info:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['education'], (item['ref'].split('-'))[-1], 'S3', document_qid])

        # pracownik_kurii = soup.find(type='pracownik_kurii')
        # writer.writerow([document_qid, p_list['pracownik_kurii'], (pracownik_kurii['ref'].split('-'))[-1]])
        #
        # taksa_dokumentu = soup.find(type='magister_registrów').measure['quantity']
        # writer.writerow([document_qid, p_list['taksa_dokumentu'], taksa_dokumentu])

        #???
        # noty_marginalne = soup.find_all('note')
        # for nota in noty_marginalne:
        #     if nota['place'] in ['left_margin', 'right_margin', 'upper-margin', 'lower-margin']:
        #         writer.writerow([document_qid, p_list['nota_marginalna'], format_string(nota.string), 'S3', document_qid])

        # try:
        #     document_fee = soup.find(type='document_fee')
        #     pracownik_kurii = soup.find(ana='urzednik_kurialny')
        #     taksa_dokumentu = soup.find(ana='taksa_dokumentu')['quantity']
        #     zrodlo = soup_meta.sourceDesc.listWit.witness
        #     for wit in zrodlo['source']:
        #         writer.writerow([wit.split("-")[-1], p_list['nota_marginalna'], format_string(' '.join(''.join([element for element in document_fee.descendants if type(element)==bs4.element.NavigableString]).split())), p_list['urzednik_kurialny'], (pracownik_kurii['ref'].split('-'))[-1], p_list['taksa_dokumentu'], taksa_dokumentu])
        # except TypeError:
        #     pass

        #UWAGA! Skrypt dodaje noty do wszystkich przekazów z listWit - do weryfikacji w przyszłości!
        zrodlo = soup_meta.sourceDesc.listWit.witness
        for wit in zrodlo['source']:
            noty_kancelaryjne = soup.find_all(type='nota_kancelaryjna')
            for nota in noty_kancelaryjne:
                for elem in nota.descendants:
                    if elem.name == 'persName' and not elem.find('measure'):
                        writer.writerow([wit.split("-")[-1], p_list['nota_marginalna'], format_string(' '.join(''.join([element for element in elem.descendants if type(element)==bs4.element.NavigableString]).split())), p_list['urzednik_kurialny'], (elem['ref'].split('-'))[-1], p_list['lokalizacja_noty'], lokalizacje_not[nota['place']]])
                    if elem.name == 'persName' and elem.measure:
                        writer.writerow([wit.split("-")[-1], p_list['nota_marginalna'], format_string(' '.join(''.join(
                            [element for element in elem.descendants if
                             type(element) == bs4.element.NavigableString]).split())), p_list['urzednik_kurialny'],
                                         (elem['ref'].split('-'))[-1], p_list['taksa_dokumentu'],
                                         elem.measure['quantity'], p_list['lokalizacja_noty'], lokalizacje_not[nota['place']]])
                    if elem.name == 'measure' and elem.parent.name != 'persName':
                        writer.writerow([wit.split("-")[-1], p_list['nota_marginalna'], format_string(' '.join(''.join(
                            [element for element in elem.descendants if
                             type(element) == bs4.element.NavigableString]).split())), p_list['taksa_dokumentu'],
                                         elem['quantity'], p_list['lokalizacja_noty'], lokalizacje_not[nota['place']]])


        #wszystkie tagi
        #lokalizacje end, inline, marg
        #sprawdzić_ile_note_ma_dzieci








        malzonkowie = soup.find_all(ana='wspolmalzonek')
        for item in malzonkowie:
            try:
                if item['type']:
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['wspolmalzonek'], (item['ref'].split('-'))[-1], 'P38', format_string(item['type']), 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['wspolmalzonek'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])
                    #laicus
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['stopien_swiecen'], 'Q251', 'P38', 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], p_list['stopien_swiecen'], 'Q251', 'S3', document_qid])
                    #charakter wystąpienia - zmarły współmałżonek
                    if item['ref'] not in wyst:
                        writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q630', 'S3', document_qid])
                else:
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['wspolmalzonek'], (item['ref'].split('-'))[-1], 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['wspolmalzonek'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])
                    # laicus
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['stopien_swiecen'], 'Q251', 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], p_list['stopien_swiecen'], 'Q251', 'S3', document_qid])
                    #charakter wystąpienia - współmałżonek
                    if item['ref'] not in wyst:
                        writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2074', 'S3', document_qid])
            except KeyError:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['wspolmalzonek'], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['wspolmalzonek'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])#charakter wystąpienia - współmałżonek
                # laicus
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['stopien_swiecen'], 'Q251', 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], p_list['stopien_swiecen'], 'Q251', 'S3', document_qid])
                # charakter wystąpienia - współmałżonek (powinien się orientować, jeśli Q wystąpiło już wcześniej z charakterem wystąpienia)
                if item['ref'] not in wyst:
                    writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2074', 'S3', document_qid])

        for relacja_rodzinna in ['ojciec', 'dziecko']:
            znalezione_relacje = soup.find_all(ana=relacja_rodzinna)
            for item in znalezione_relacje:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[relacja_rodzinna], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[relacja_rodzinna], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])
                #charakter wystąpienia - zmarły ojciec
                writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2075', 'S3', document_qid])

        for dalsza_relacja in ['nepos', 'familiaris']:
            znalezione_dalsze_relacje = soup.find_all(ana=dalsza_relacja)
            for item in znalezione_dalsze_relacje:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[dalsza_relacja], (item['ref'].split('-'))[-1], 'S3', document_qid])

        for status_beneficjow in ['zajmowane_stanowisko', 'informacje_o_posiadaniu_stanowiska']:
            znalezione = soup.find_all(ana=status_beneficjow)
            for item in znalezione:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[status_beneficjow], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[status_beneficjow], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])



        for status in ['pochodzenie_spoleczne', 'stopien_swiecen', 'rola_spoleczna']:
            statusy = soup.find_all(ana=status)
            for item in statusy:
                writer.writerow([(item.find_parent('persName')['ref'].split('-'))[-1], p_list[status], (item['ref'].split('-'))[-1], 'S3', document_qid])

        diecezje = soup.find_all(ana='diecezja')
        for item in diecezje:
            writer.writerow([(item.find_parent('persName')['ref'].split('-'))[-1], p_list['diecezja'], (item['ref'].split('-'))[-1], 'S3', document_qid])

        #byty w dokumencie - nie dawać dzieci!! na razie bez dzieci, a potem zobaczymy
        for tag in ['persName', 'affiliation', 'settlement']:
            refs = []
            result = soup.body.p.children
            for i in result:
                if i.name == tag:
                    if (i['ref'].split('-'))[-1] not in refs:
                        refs.append((i['ref'].split('-'))[-1])
                        # writer.writerow([document_qid, 'P24', (i['ref'].split('-'))[-1], 'S3', document_qid])
                        writer.writerow([document_qid, 'P24', (i['ref'].split('-'))[-1]])
                        # writer.writerow([(i['ref'].split('-'))[-1], 'P26', document_qid,'S3', document_qid])
                        writer.writerow([(i['ref'].split('-'))[-1], 'P26', document_qid])

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