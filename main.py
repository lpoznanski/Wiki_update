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

        type_is_multi = {'*': 'type'}
        content = "".join(content)
        soup = bs(content, "xml", multi_valued_attributes=type_is_multi)

        document_qid = soup.publicationStmt.idno.string

        # tags_of_interest = ['persName', 'placeName', 'orgName', 'affiliation', 'date', 'education', 'note']

        def format_multiline(str):
            return '"' + str + '"'

        def format_string(str):
            return '"' + str + '"'

        p_list = {
            'beneficjent_laski': 'P25',
            'posiadane_beneficjum': 'P53',
            'posiadana_ekspektatywa_na_beneficjum': 'P54',
            'education': 'P42',
            'przedmiot_nadania': 'P52',
            'osoba_w_sporze': ['P29', 'Q471'],
            'zmarly_w_kurii': ['P29', 'Q472'],
            'rezygnacja_z_beneficjum': ['P29', 'Q473'],
            'maz': 'P56',
            'ojciec': 'P57',
            'zona': 'P33',
            'dziecko': 'P58',
            'nepos': 'P59',
            'familiaris': 'P60',
            'wystawca': 'P22',
            'odbiorca': 'P23',
            'egzekutor': ['P29', 'Q416'],
            'taksa_dokumentu': 'P30',
            'pracownik_kurii': 'P31',
            'nota_marginalna': 'P34',
            'miejsce_wystawienia_dokumentu': 'P13',
            'data_dokumentu': 'P12',
            'tytulatura': 'P38',
            'diecezja': 'P2'
        }

        reverse_p_list = {
            'mąz': 'P33',
            'ojciec': 'P58',
            'zona': 'P56',
            'dziecko': 'P57',
            'posiadane_beneficjum': 'P35',
            'posiadana_ekspektatywa_na_beneficjum': 'P28'
        }

        volumeny = {
            'RL_6': 'Q382',
            'RL_34': 'Q401'
        }

        formy_zachowania = {
            'cop.': 'Q388'
        }

        typy_dokumentow = {
            'bulla': 'Q402',
            'suplika': ''
        }

        rodzaje_lask = {
            'ekspektatywa': 'Q392',
            'odpuszczenie': 'Q406'
        }

        formularze = {
            'dignum': 'Q434',
            'dignum_pro_nobili': 'Q387',
            'provenit': 'Q403'
        }

        typy_edycji = {
            'edycja': 'Q385',
            'regest': 'Q386'
        }



        # with open(f'results/{document_qid}.csv', 'w', newline='') as file:
        #     writer = csv.writer(file)

        #metadane
        typ = soup.find(scheme="forma_dokumentu")['target']
        writer.writerow([document_qid, 'P1', typy_dokumentow[typ], 'S51', document_qid, '', '', '', '', '', '', '', '', '', '', '', ''])

        rodzaj_laski = soup.find(scheme="rodzaj_sprawy")['target']
        writer.writerow([document_qid, 'P24', rodzaje_lask[rodzaj_laski], 'S51', document_qid])

        formularz = soup.find(scheme="formularz")['target']
        writer.writerow([document_qid, 'P19', formularze[formularz], 'S51', document_qid])

        regest = soup.teiHeader.profileDesc.abstract.p.string
        regest = ' '.join(regest.split())
        writer.writerow([document_qid, 'P11', format_string(regest), 'S51', document_qid])

        zrodlo = soup.sourceDesc.listWit.witness
        folia = []
        for element in [item.string.split('f. ')[-1] for item in zrodlo.find_all('locus')]:
            folia.append('P16')
            folia.append(format_string(element))
        volumen = ['P14', volumeny[zrodlo['source']]]
        forma_zachowania = ['P20', formy_zachowania[zrodlo['ana']]]
        # byty_w_sygnaturze
        writer.writerow([document_qid, 'P8', format_string(zrodlo.contents[0])] + forma_zachowania + volumen + folia + ['S51', document_qid])

        data_dokumentu = soup.teiHeader.profileDesc.creation.date['when']
        formatted_date = '+' + data_dokumentu + 'T00:00:00Z/11'
        writer.writerow([document_qid, 'P12', formatted_date, 'S51', document_qid])

        miejsce_wystawienia = soup.teiHeader.profileDesc.creation.placeName['ref']
        writer.writerow([document_qid, 'P13', miejsce_wystawienia, 'S51', document_qid])

        wydania = soup.find_all('bibl')
        for item in wydania:
            writer.writerow([document_qid, 'P17', format_string(item.string), 'P18', typy_edycji[item['type'][0]], 'S51', document_qid])


        #tekst

        # complete_tags = soup.body.p.descendants
        # for child in complete_tags:
        #     if type(child) == bs4.element.Tag and child['type']:
        #         print('-')
        #         print(child)
        #         print(child['type'])

        wystawcy = soup.find_all(type='wystawca')
        for item in wystawcy:
            writer.writerow([document_qid, p_list['wystawca'], (item['ref'].split('-'))[-1], 'S51', document_qid])

        odbiorcy = soup.find_all(type='odbiorca')
        for item in odbiorcy:
            writer.writerow([document_qid, p_list['odbiorca'], (item['ref'].split('-'))[-1], 'S51', document_qid])

        beneficjenci_laski = soup.find_all(type='beneficjent_laski')
        for item in beneficjenci_laski:
            writer.writerow([document_qid, p_list['beneficjent_laski'], (item['ref'].split('-'))[-1],'S51', document_qid])

        przedmioty_nadania = soup.find_all(type='przedmiot_nadania')
        for item in przedmioty_nadania:
            writer.writerow([document_qid, p_list['przedmiot_nadania'], (item['ref'].split('-'))[-1], 'S51', document_qid])

        tytulatury = soup.find_all(type='tytulatura')
        for item in tytulatury:
            writer.writerow([(item['ref'].split('-'))[-1], p_list['tytulatura'], format_string(' '.join(''.join([element for element in item.descendants if type(element)==bs4.element.NavigableString]).split())), 'S51', document_qid])

        education_info = soup.find_all(type='education')
        for item in education_info:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['education'], (item['ref'].split('-'))[-1], 'S51', document_qid])

        # pracownik_kurii = soup.find(type='pracownik_kurii')
        # writer.writerow([document_qid, p_list['pracownik_kurii'], (pracownik_kurii['ref'].split('-'))[-1]])
        #
        # taksa_dokumentu = soup.find(type='magister_registrów').measure['quantity']
        # writer.writerow([document_qid, p_list['taksa_dokumentu'], taksa_dokumentu])

        noty_marginalne = soup.find_all('note')
        for nota in noty_marginalne:
            if nota['place'] in ['left_margin', 'right_margin', 'upper-margin', 'lower-margin']:
                writer.writerow([document_qid, p_list['nota_marginalna'], format_string(nota.string), 'S51', document_qid])

        document_fee = soup.find(type='document_fee')
        pracownik_kurii = soup.find(type='pracownik_kurii')
        taksa_dokumentu = soup.find(type='pracownik_kurii').measure['quantity']
        writer.writerow([document_qid, p_list['nota_marginalna'], format_string(' '.join(''.join([element for element in document_fee.descendants if type(element)==bs4.element.NavigableString]).split())), p_list['pracownik_kurii'], (pracownik_kurii['ref'].split('-'))[-1], p_list['taksa_dokumentu'], taksa_dokumentu, 'S51', document_qid])

        for relacja_rodzinna in ['maz', 'ojciec', 'zona', 'dziecko']:
            znalezione_relacje = soup.find_all(type=relacja_rodzinna)
            for item in znalezione_relacje:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[relacja_rodzinna], (item['ref'].split('-'))[-1], 'S51', document_qid, 'S51', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[relacja_rodzinna], (item.parent['ref'].split('-'))[-1], 'S51', document_qid, 'S51', document_qid])

        for dalsza_relacja in ['nepos', 'familiaris']:
            znalezione_dalsze_relacje = soup.find_all(type=dalsza_relacja)
            for item in znalezione_dalsze_relacje:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[dalsza_relacja], (item['ref'].split('-'))[-1]], 'S51', document_qid)

        for status_beneficjow in ['posiadane_beneficjum', 'posiadana_ekspektatywa_na_beneficjum']:
            znalezione = soup.find_all(type=relacja_rodzinna)
            for item in znalezione:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[status_beneficjow], (item['ref'].split('-'))[-1], 'S51', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[status_beneficjow], (item.parent['ref'].split('-'))[-1], 'S51', document_qid])

        for rola in ['osoba_w_sporze', 'zmarly_w_kurii', 'rezygnacja_z_beneficjum', 'egzekutor']:
            znalezione_role = soup.find_all(type=rola)
            for item in znalezione_role:
                writer.writerow([(item['ref'].split('-'))[-1], p_list[rola][0], p_list[rola][1], 'S51', document_qid])

        diecezje = soup.find_all(type='diecezja')
        for item in diecezje:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['diecezja'], (item['ref'].split('-'))[-1], 'S51', document_qid])

        #byty w dokumencie
        for tag in ['persName', 'affiliation', 'settlement']:
            refs = []
            result = soup.find_all(tag)
            for i in result:
                if (i['ref'].split('-'))[-1] not in refs:
                    refs.append((i['ref'].split('-'))[-1])
                    writer.writerow([document_qid, 'P27', (i['ref'].split('-'))[-1], 'S51', document_qid])


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