# coding: utf-8

import os
import csv

COUNTRY_CODES = []
try:
    pointer = open(os.path.dirname(os.path.realpath(__file__)) + '/assets/country_codes.csv', 'r', encoding='utf-8')
    with pointer as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            COUNTRY_CODES.append([i for i in row])
except TypeError:
    pointer = open(os.path.dirname(os.path.realpath(__file__)) + '/assets/country_codes.csv', 'r')
    with pointer as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            COUNTRY_CODES.append([i.decode('utf-8') for i in row])


def load_alpha_2():

    data = {}
    for alpha_2, alpha_3, en, pt, es in COUNTRY_CODES:
        data[alpha_2] = {
            'alpha_2': alpha_2,
            'alpha_3': alpha_3,
            'name': en,
            'pt': pt,
            'es': es,
            'en': en
        }

    return data


def load_alpha_3():

    data = {}
    for alpha_2, alpha_3, en, pt, es in COUNTRY_CODES:
        data[alpha_3] = {
            'alpha_2': alpha_2,
            'alpha_3': alpha_3,
            'name': en,
            'pt': pt,
            'es': es,
            'en': en
        }

    return data

COUNTRY_CODES_ALPHA_2 = load_alpha_2()
COUNTRY_CODES_ALPHA_3 = load_alpha_3()


def load_alpha_2_forms():

    data = {}

    for code, forms in COUNTRY_CODES_ALPHA_2.items():
        for form in forms.values():
            if form == '':
                continue
            data[form.lower()] = code

    return data


def load_alpha_3_forms():

    data = {}

    for code, forms in COUNTRY_CODES_ALPHA_3.items():
        for form in forms.values():
            if form == '':
                continue
            data[form.lower()] = code

    return data

COUNTRY_CODES_ALPHA_2_FORMS = load_alpha_2_forms()
COUNTRY_CODES_ALPHA_3_FORMS = load_alpha_3_forms()
