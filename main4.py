import os
import csv

import pandas as pd

import bs4.element
from bs4 import BeautifulSoup as bs

content = []

with open(f'results/result.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # docs = os.listdir('documents/')
    docs = os.listdir('final/')
    for doc in docs:
        # with open('documents/' + doc, "r", encoding='utf-8') as file:
        with open('final/' + doc, "r", encoding='utf-8') as file:
            content = file.readlines()

        ana_is_multi = {'*': 'ana'}
        source_is_multi = {'*': 'source'}
        content = "".join(content)
        soup = bs(content, "xml", multi_valued_attributes=ana_is_multi)
        soup_meta = bs(content, "xml", multi_valued_attributes=source_is_multi)
        document_qid = soup.TEI['xml:id']


        def format_string(str):
            return '"' + str + '"'

        p_list = {
            'beneficiary': 'P20',
            'position_held': 'P32',
            'informacje_o_posiadaniu_stanowiska': 'P33',
            'education': 'P31',
            'object_of_grant': 'P34',
            'ordination': 'P35',
            'spouse': 'P4',
            'parent': 'P27', #ma dziecko
            'child': 'P28', #posiada rodzica
            'nepos': 'P29',
            'familiaris': 'P30',
            'has_a_familiaris': 'P77',
            'issuer': 'P18',
            'recipient': 'P19',
            'executor': 'Q424',
            'document_fee': 'P23',
            'curial_official': 'P22',
            'nota_marginalna': 'P21',
            'place_of_issue': 'P15',
            'data_dokumentu': 'P14',
            'title': 'P25',
            'diocese': 'P2',
            'social_origin': 'P37',
            'social_role': 'P36',
            'lokalizacja_noty': 'P58',
            'described_as': 'P63',
            'expectative': 'P64',
            'protector': 'P65',
            'protege': 'P66',
            'sibling': 'P56',
            'conservator': '',
            'provision': 'P69'
        }

        p39_q_list = {
            'beneficiary': 'Q538',
            'conservator': 'Q2763',
            'executor': 'Q424',
            'indulgence_holder': 'Q4664',
            'injured_party': 'Q4665',
            'judge': 'Q4666',
            'procurator': 'Q1513',
            'public_notary': 'Q1521',
            'suplicant': 'Q2752',
            'witness': 'Q4667',
            'has_a_conservator': 'Q4668',
            'releasing_office': 'Q4669',
            'issuer_of_inserted_document': 'Q4670',
            'object_of_incorporation': 'Q2775',
            'sentenced': 'Q4879',
            'acknowledger': 'Q5107',
            'payer': 'Q5108',
            'intermediary': 'Q5109',
            'tithe_title': 'Q5110'
        }

        reverse_p_list = {
            'spouse': 'P4',
            'parent': 'P28', #ma dziecko
            'child': 'P27', #posiada rodzica
            'position_held': 'P40',
            'informacje_o_posiadaniu_stanowiska': 'P40',
            'posiadana_ekspektatywa_na_beneficjum': 'P28',
            'protector': 'P66',
            'protege': 'P65',
            'expectative': 'P72',
            'familiaris': 'P77',
            'has_a_familiaris': 'P30'
        }

        volumeny = {
            'RL_6': '',
            'RL_34': 'Q116'
        }

        formy_zachowania = {
            'cop.': 'Q427'
        }

        typy_edycji = {
            'edition': 'Q426',
            'regest': 'Q425',
            'mentio': 'Q2122',
            'editorial_note': 'editorial_note jako typ edycji... do usunięcia'
        }

        lokalizacje_not = {
            'in_line': 'Q2101',
            'end': 'Q2102',
            'in_marg': 'Q1638',
            'recto super plicam ad d.': 'do sprawdzenia: recto super plicam ad d.',
            'recto super plicam ad s.': 'do sprawdzenia: recto super plicam ad s.',
            'recto sub plica ad s.': 'do sprawdzenia: recto sub plica ad s.',
            'a tergo in angulo inf. s.': 'do sprawdzenia: a tergo in angulo inf. s.',
            'recto in angulo sup. s.': 'do sprawdzenia: recto in angulo sup. s.',
            'recto in angulo sup. d.': 'do sprawdzenia: recto in angulo sup. d.',
            'a tergo in medio megine sup.': 'do sprawdzenia: a tergo in medio megine sup.'
        }

        rodzaje_swiadkow = {
            'or.': 'Q605',
            'copy_reg': 'Q427',
            'copy': 'Q2347'
        }

        #pusta linia na początku
        writer.writerow(['', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        #metadane
        case = soup.find(scheme="case")['target']
        writer.writerow([document_qid, 'P57', case.split("-")[-1]])
        writer.writerow([case.split("-")[-1], 'P57', document_qid])
        writer.writerow([case.split("-")[-1], 'P1', 'Q867'])


        rodzaj_laski_1 = soup.find(scheme="case_type")
        if rodzaj_laski_1 and rodzaj_laski_1.has_attr("target"):
            rodzaj_laski = rodzaj_laski_1["target"]
            writer.writerow([case.split("-")[-1], 'P7', rodzaj_laski.split("-")[-1], '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        else:
            pass

        form_el = soup.find(scheme="form")
        if form_el and form_el.has_attr("target"):
            form = form_el["target"]
            writer.writerow([document_qid, "P8", form.split("-")[-1]])
        else:
            pass


        pontyfikat = soup.find(scheme="pontificate")['target']
        writer.writerow([document_qid, 'P31', pontyfikat.split("-")[-1]])


        regest = soup.teiHeader.profileDesc.abstract.p.string
        if regest:
            regest = ' '.join(regest.split())
            writer.writerow([document_qid, 'P9', format_string(regest)])


        rodzaj_dokumentu = soup.find(scheme="source_type")['target']
        writer.writerow([document_qid, 'P1', rodzaj_dokumentu.split("-")[-1]])


        zrodla = soup_meta.find_all('witness')
        for zrodlo in zrodla:
            for wit in zrodlo['source']:
                writer.writerow([document_qid, 'P54', wit.split("-")[-1]])
                writer.writerow([wit.split("-")[-1], 'P53', document_qid])
                writer.writerow([wit.split("-")[-1], 'P1', rodzaje_swiadkow[zrodlo['ana']]])


        date_tag = soup.teiHeader.profileDesc.creation.date
        if date_tag and date_tag.has_attr('when'):
            data_dokumentu = date_tag['when']
            formatted_date = f'+{data_dokumentu}T00:00:00Z/11/J'
            writer.writerow([document_qid, 'P14', formatted_date])


        place_tag = soup.teiHeader.profileDesc.creation.placeName
        if place_tag and place_tag.has_attr('ref'):
            miejsce_wystawienia = place_tag['ref']
            writer.writerow([document_qid, 'P15', miejsce_wystawienia.split('-')[-1]])


        wydania = soup.find_all('bibl')
        for item in wydania:
            if item.string:
                writer.writerow([document_qid, 'P16', format_string(item.string), 'P17', typy_edycji[item['type']]])
            else:
                pass


        # zrodlo = soup_meta.sourceDesc.listWit.witness
        # for wit in zrodlo['source']:
        #     noty_kancelaryjne = soup.find_all(type='chancery_note')
        #     for nota in noty_kancelaryjne:
        #         for elem in nota.descendants:
        #             if isinstance(elem, bs4.NavigableString):
        #                 # tekst bezpośrednio w nocie
        #                 text = format_string(str(elem).strip())
        #                 if text:
        #                     writer.writerow([
        #                         wit.split("-")[-1],
        #                         p_list['nota_marginalna'],
        #                         text,
        #                         p_list['lokalizacja_noty'],
        #                         lokalizacje_not[nota['place']]
        #                     ])
        #             elif elem.name == 'rs':
        #                 measure = elem.find('measure')  # bezpieczne sprawdzenie
        #                 text = format_string(' '.join(''.join(
        #                     [element for element in elem.descendants
        #                      if isinstance(element, bs4.element.NavigableString)]
        #                 ).split()))
        #
        #                 if measure is None:
        #                     # przypadek bez <measure>
        #                     writer.writerow([
        #                         wit.split("-")[-1],
        #                         p_list['nota_marginalna'],
        #                         text,
        #                         p_list['curial_official'],
        #                         (elem['ref'].split('-'))[-1],
        #                         p_list['lokalizacja_noty'],
        #                         lokalizacje_not[nota['place']]
        #                     ])
        #                 else:
        #                     # przypadek z <measure>
        #                     writer.writerow([
        #                         wit.split("-")[-1],
        #                         p_list['nota_marginalna'],
        #                         text,
        #                         p_list['curial_official'],
        #                         (elem['ref'].split('-'))[-1],
        #                         p_list['document_fee'],
        #                         measure['quantity'],
        #                         p_list['lokalizacja_noty'],
        #                         lokalizacje_not[nota['place']]
        #                     ])
        #
        #             elif elem.name == 'measure' and elem.parent.name != 'rs':
        #                 # przypadek niezależnego <measure>
        #                 text = format_string(' '.join(''.join(
        #                     [element for element in elem.descendants
        #                      if isinstance(element, bs4.element.NavigableString)]
        #                 ).split()))
        #                 writer.writerow([
        #                     wit.split("-")[-1],
        #                     p_list['nota_marginalna'],
        #                     text,
        #                     p_list['document_fee'],
        #                     elem['quantity'],
        #                     p_list['lokalizacja_noty'],
        #                     lokalizacje_not[nota['place']]
        #                 ])


        #dane z treści
        wystawcy = soup.find_all(ana='issuer')
        for item in wystawcy:
            writer.writerow([document_qid, p_list['issuer'], (item['ref'].split('-'))[-1]])
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q536', 'S3', document_qid])
            # wyst.append(item['ref'])


        odbiorcy = soup.find_all(ana='recipient')
        for item in odbiorcy:
            writer.writerow([document_qid, p_list['recipient'], (item['ref'].split('-'))[-1]])
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q537', 'S3', document_qid])
            # wyst.append(item['ref'])


        for prop in [
                        'conservator',
                        'executor',
                        'indulgence_holder',
                        'injured_party',
                        'judge',
                        'procurator',
                        'public_notary',
                        'suplicant',
                        'witness',
                        'has_a_conservator',
                        'releasing_office',
                        'issuer_of_inserted_document',
                        'object_of_incorporation',
                        'sentenced',
                        'acknowledger',
                        'payer',
                        'intermediary',
                        'tithe_title'
                    ]:
            properties = soup.find_all(ana=prop)
            for item in properties:
                writer.writerow([(item['ref'].split('-'))[-1], 'P39', p39_q_list[prop],'S3', document_qid])


        beneficiary = soup.find_all(ana='beneficiary')
        for item in beneficiary:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', p39_q_list['beneficiary'],'S3', document_qid])
            writer.writerow([case.split("-")[-1], 'P20', (item['ref'].split('-'))[-1], 'S3', document_qid])


        protektorzy = soup.find_all(ana='protector')
        for item in protektorzy:
            writer.writerow(
                [(item['ref'].split('-'))[-1], 'P39', 'Q2077', 'S3',
                 document_qid])


        protegowani = soup.find_all(ana='protege')
        for item in protegowani:
            writer.writerow(
                [(item.parent['ref'].split('-'))[-1], p_list['protege'], (item['ref'].split('-'))[-1], 'S3',
                 document_qid])
            writer.writerow(
                [(item['ref'].split('-'))[-1], reverse_p_list['protege'], (item.parent['ref'].split('-'))[-1], 'S3',
                 document_qid])


        prowizje = soup.find_all(ana='provision')
        for item in prowizje:
            writer.writerow(
                [(item.parent['ref'].split('-'))[-1], p_list['provision'], (item['ref'].split('-'))[-1], 'S3',
                 document_qid])


        przedmioty_nadania = soup.find_all(ana='object_of_grant')
        for item in przedmioty_nadania:
            writer.writerow(
                [(item['ref'].split('-'))[-1], 'P39', 'Q656', 'S3',
                 document_qid])
            writer.writerow([case.split("-")[-1], p_list['object_of_grant'], (item['ref'].split('-'))[-1], 'S3', document_qid])


        strony_sporu = soup.find_all(ana='disputing_party')
        for item in strony_sporu:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q4663', 'S3', document_qid])
            writer.writerow([case.split("-")[-1], 'P71', (item['ref'].split('-'))[-1], 'S3', document_qid])


        indulgence_day = soup.find_all(ana='indulgence_day')
        # for item in indulgence_day:
        #     writer.writerow([(item.parent['ref'].split('-'))[-1], 'P73', (item['ref'].split('-'))[-1], 'S3', document_qid])
        for item in indulgence_day:
            rs = item.find_parent('rs')
            if rs and rs.has_attr('ref'):
                writer.writerow([
                    rs['ref'].split('-')[-1],
                    'P73',
                    item['ref'].split('-')[-1],
                    'S3',
                    document_qid
                ])

        przedmioty_sporu = soup.find_all(ana='object_of_dispute')
        for item in przedmioty_sporu:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2753', 'S3', document_qid])
            writer.writerow([case.split("-")[-1], 'P74', (item['ref'].split('-'))[-1], 'S3', document_qid])


        represented = soup.find_all(ana='represented')
        for item in represented:
            writer.writerow([(item.parent['ref'].split('-'))[-1], 'P75', (item['ref'].split('-'))[-1], 'S3', document_qid])
            writer.writerow([(item['ref'].split('-'))[-1], 'P76', (item.parent['ref'].split('-'))[-1], 'S3', document_qid])

        tytulatury = soup.find_all(ana='title')
        for item in tytulatury:
            writer.writerow([(item['ref'].split('-'))[-1], p_list['title'], format_string(' '.join(''.join([element for element in item.descendants if type(element)==bs4.element.NavigableString]).split())), 'S3', document_qid])


        education_info = soup.find_all(ana='education')
        for item in education_info:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['education'], (item['ref'].split('-'))[-1], 'S3', document_qid])


        ekspektatywy = soup.find_all(ana='expectative')
        for item in ekspektatywy:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['expectative'], (item['ref'].split('-'))[-1], 'S3', document_qid])
            writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['expectative'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])


        malzonkowie = soup.find_all(ana='spouse')
        for item in malzonkowie:
            try:
                if item['type']:
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['spouse'], (item['ref'].split('-'))[-1], 'P38', format_string(item['type']), 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['spouse'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])
                    #laicus
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['ordination'], 'Q251', 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], p_list['ordination'], 'Q251', 'S3', document_qid])
                else:
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['spouse'], (item['ref'].split('-'))[-1], 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['spouse'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])
                    # laicus
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['ordination'], 'Q251', 'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], p_list['ordination'], 'Q251', 'S3', document_qid])


            except KeyError:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['spouse'], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list['spouse'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])#charakter wystąpienia - współmałżonek
                # laicus
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['ordination'], 'Q251', 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], p_list['ordination'], 'Q251', 'S3', document_qid])


        for relacja_rodzinna in ['parent', 'child']:
            znalezione_relacje = soup.find_all(ana=relacja_rodzinna)
            for item in znalezione_relacje:
                if item.get('type'):
                    writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[relacja_rodzinna], (item['ref'].split('-'))[-1], 'P38', item['type'],'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[relacja_rodzinna], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])
                else:
                    writer.writerow(
                        [(item.parent['ref'].split('-'))[-1], p_list[relacja_rodzinna], (item['ref'].split('-'))[-1],
                         'S3', document_qid])
                    writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[relacja_rodzinna],
                                     (item.parent['ref'].split('-'))[-1], 'S3', document_qid])


        for dalsza_relacja in ['has_a_familiaris', 'familiaris']:
            znalezione_dalsze_relacje = soup.find_all(ana=dalsza_relacja)
            for item in znalezione_dalsze_relacje:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[dalsza_relacja], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow(
                    [(item['ref'].split('-'))[-1], reverse_p_list[dalsza_relacja], (item.parent['ref'].split('-'))[-1], 'S3',
                     document_qid])

        nepos = soup.find_all(ana='nepos')
        for item in nepos:
            writer.writerow(
                [(item.parent['ref'].split('-'))[-1], p_list['nepos'], (item['ref'].split('-'))[-1], 'S3', document_qid])


        rodzenstwo = soup.find_all('sibling')
        for item in rodzenstwo:
            writer.writerow([(item.parent['ref'].split('-'))[-1], p_list['sibling'], (item['ref'].split('-'))[-1], 'S3', document_qid])
            writer.writerow([(item['ref'].split('-'))[-1], p_list['sibling'], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])


        for founders in ['founder']:
            found = soup.find_all(ana=founders)
            for i in found:
                writer.writerow(
                    [(item.parent['ref'].split('-'))[-1], 'P79', (item['ref'].split('-'))[-1], 'S3',
                     document_qid])
                writer.writerow(
                    [(item['ref'].split('-'))[-1], 'P70', (item.parent['ref'].split('-'))[-1],
                     'S3',
                     document_qid])



        suplikant = soup.find_all('suplicant')
        for item in suplikant:
            writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2752', 'S3', document_qid])


        for status_beneficjow in ['position_held', 'informacje_o_posiadaniu_stanowiska']:
            znalezione = soup.find_all(ana=status_beneficjow)
            for item in znalezione:
                writer.writerow([(item.parent['ref'].split('-'))[-1], p_list[status_beneficjow], (item['ref'].split('-'))[-1], 'S3', document_qid])
                writer.writerow([(item['ref'].split('-'))[-1], reverse_p_list[status_beneficjow], (item.parent['ref'].split('-'))[-1], 'S3', document_qid])


        diecezje = soup.find_all(ana='diocese')
        for item in diecezje:
            writer.writerow([(item.find_parent('rs')['ref'].split('-'))[-1], p_list['diocese'], (item['ref'].split('-'))[-1], 'S3', document_qid])


        opisany_jako = soup.find_all(ana='described_as')
        for item in opisany_jako:
            if item.get('type'):
                writer.writerow([(item.find_parent('rs')['ref'].split('-'))[-1], p_list['described_as'],
                                 (item['ref'].split('-'))[-1], 'P38', format_string(item['type']), 'S3', document_qid])
            else:
                writer.writerow([(item.find_parent('rs')['ref'].split('-'))[-1], p_list['described_as'], (item['ref'].split('-'))[-1], 'S3', document_qid])


        byt_wspomniany = soup.find_all(ana='mentioned_entity')
        for item in byt_wspomniany:
            if item.get('type'):
                writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2078', 'S3', document_qid])
                # writer.writerow([document_qid, 'P24', (item['ref'].split('-'))[-1], 'P38', format_string(item['type'])])
            else:
                writer.writerow([(item['ref'].split('-'))[-1], 'P39', 'Q2078', 'S3', document_qid])
                # writer.writerow([document_qid, 'P24', (item['ref'].split('-'))[-1]])
        # mentioned_entity - wszystkie elementy bez described_as


        #byty w dokumencie
        # p_tags = soup.find_all('p')
        # for p in p_tags:
        #     for child in p.children:
        #         # sprawdź, czy to jest tag <rs>
        #         if getattr(child, 'name', None) == 'rs':
        #             # dodatkowe zabezpieczenie: upewnij się, że ten <rs> nie jest w innym <rs>
        #             if not child.find_parent('rs'):
        #                 # tutaj robisz, co chcesz, np. zapis do CSV
        #                 writer.writerow([document_qid, 'P24', (child['ref'].split('-'))[-1]])

        rs_tags = soup.select('p rs:not(rs rs)')

        for rs in rs_tags:
            if rs.get('ref'):
                writer.writerow([
                    document_qid,
                    'P24',
                    rs['ref'].split('-')[-1]
                ])
                writer.writerow([rs['ref'].split('-')[-1], 'P26', document_qid])

#zapisywanie do xls
cvsDataframe = pd.read_csv('results/result.csv')
resultExcelFile = pd.ExcelWriter('result.xlsx')
cvsDataframe.to_excel(resultExcelFile, index=False, header=False)
resultExcelFile._save()