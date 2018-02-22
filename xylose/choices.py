# encoding: utf-8

CREATIVE_COMMONS_TEXTS = {
    "BY": "Attribution",
    "BY-ND": "Attribution-NoDerivatives",
    "BY-SA": "Attribution-ShareAlike",
    "BY-NC": "Attribution-NonCommercial",
    "BY-NC-ND": "Attribution-NonCommercial-NoDerivatives",
    "BY-NC-SA": "Attribution-NonCommercial-ShareAlike"
    ""
}

ISO639_1_to_2 = {
    'gv': 'glv', 'gu': 'guj', 'gd': 'gla', 'ga': 'gle', 'gn': 'grn',
    'gl': 'glg', 'lg': 'lug', 'lb': 'ltz', 'la': 'lat', 'ln': 'lin',
    'lo': 'lao', 'tt': 'tat', 'tr': 'tur', 'ts': 'tso', 'li': 'lim',
    'lv': 'lav', 'to': 'ton', 'lt': 'lit', 'lu': 'lub', 'tk': 'tuk',
    'th': 'tha', 'ti': 'tir', 'tg': 'tgk', 'te': 'tel', 'ta': 'tam',
    'yi': 'yid', 'yo': 'yor', 'de': 'ger', 'da': 'dan', 'dz': 'dzo',
    'st': 'sot', 'dv': 'div', 'qu': 'que', 'el': 'ell', 'eo': 'epo',
    'en': 'eng', 'zh': 'chi', 'ee': 'ewe', 'za': 'zha', 'mh': 'mah',
    'uk': 'ukr', 'eu': 'eus', 'et': 'est', 'es': 'spa', 'ru': 'rus',
    'rw': 'kin', 'rm': 'roh', 'rn': 'run', 'ro': 'ron', 'bn': 'ben',
    'be': 'bel', 'bg': 'bul', 'ba': 'bak', 'wa': 'wln', 'wo': 'wol',
    'bm': 'bam', 'jv': 'jav', 'bo': 'bod', 'bh': 'bih', 'bi': 'bis',
    'br': 'bre', 'bs': 'bos', 'ja': 'jpn', 'om': 'orm', 'oj': 'oji',
    'ty': 'tah', 'oc': 'oci', 'tw': 'twi', 'os': 'oss', 'or': 'ori',
    'xh': 'xho', 'ch': 'cha', 'co': 'cos', 'ca': 'cat', 'ce': 'che',
    'cy': 'cym', 'cs': 'ces', 'cr': 'cre', 'cv': 'chv', 'cu': 'chu',
    've': 'ven', 'ps': 'pus', 'pt': 'por', 'tl': 'tgl', 'pa': 'pan',
    'vi': 'vie', 'pi': 'pli', 'is': 'isl', 'pl': 'pol', 'hz': 'her',
    'hy': 'hye', 'hr': 'hrv', 'iu': 'iku', 'ht': 'hat', 'hu': 'hun',
    'hi': 'hin', 'ho': 'hmo', 'ha': 'hau', 'he': 'heb', 'mg': 'mlg',
    'uz': 'uzb', 'ml': 'mal', 'mn': 'mon', 'mi': 'mri', 'ik': 'ipk',
    'mk': 'mkd', 'ur': 'urd', 'mt': 'mlt', 'ms': 'msa', 'mr': 'mar',
    'ug': 'uig', 'my': 'mya', 'ki': 'kik', 'aa': 'aar', 'ab': 'abk',
    'ae': 'ave', 'ss': 'ssw', 'af': 'afr', 'tn': 'tsn', 'sw': 'swa',
    'ak': 'aka', 'am': 'amh', 'it': 'ita', 'an': 'arg', 'ii': 'iii',
    'ia': 'ina', 'as': 'asm', 'ar': 'ara', 'su': 'sun', 'io': 'ido',
    'av': 'ava', 'ay': 'aym', 'az': 'aze', 'id': 'ind', 'ig': 'ibo',
    'sk': 'slk', 'sr': 'srp', 'nl': 'nld', 'nn': 'nno', 'no': 'nor',
    'na': 'nau', 'nb': 'nob', 'nd': 'nde', 'ne': 'nep', 'ng': 'ndo',
    'ny': 'nya', 'vo': 'vol', 'zu': 'zul', 'so': 'som', 'nr': 'nbl',
    'nv': 'nav', 'sn': 'sna', 'fr': 'fra', 'sm': 'smo', 'fy': 'fry',
    'sv': 'swe', 'fa': 'fas', 'ff': 'ful', 'fi': 'fin', 'fj': 'fij',
    'sa': 'san', 'fo': 'fao', 'ka': 'kat', 'kg': 'kon', 'kk': 'kaz',
    'kj': 'kua', 'sq': 'sqi', 'ko': 'kor', 'kn': 'kan', 'km': 'khm',
    'kl': 'kal', 'ks': 'kas', 'kr': 'kau', 'si': 'sin', 'kw': 'cor',
    'kv': 'kom', 'ku': 'kur', 'sl': 'slv', 'sc': 'srd', 'ky': 'kir',
    'sg': 'sag', 'se': 'sme', 'sd': 'snd'
}
ISO639_1 = set([k for k, v in ISO639_1_to_2.items()])

article_types = {
    'ab': 'abstract',
    'an': 'news',
    'ax': 'addendum',
    'co': 'article-commentary',
    'cr': 'case-report',
    'ct': 'research-article',
    'ed': 'editorial',
    'er': 'correction',
    'in': 'editorial',
    'le': 'letter',
    'mt': 'research-article',
    'nd': 'undefined',
    'oa': 'research-article',
    'pr': 'press-release',
    'pv': 'editorial',
    'rc': 'book-review',
    'rn': 'brief-report',
    'ra': 'review-article',
    'sc': 'rapid-communication',
    'tr': 'research-article',
    'up': 'undefined'
}

periodicity = {
    u'M': u'Monthly',
    u'B': u'Bimonthly (every two months)',
    u'Q': u'Quarterly',
    u'T': u'Three times a year',
    u'F': u'Semiannual (twice a year)',
    u'A': u'Annual',
    u'K': u'Irregular (know to be so)',
    u'Z': u'Other frequencies'
}

periodicity_in_months = {
    u'M': u'12',
    u'B': u'6',
    u'Q': u'4',
    u'T': u'3',
    u'F': u'2',
    u'A': u'1',
    u'K': u'undefined',
    u'Z': u'undefined'
}

collections = {
    'scl': ['Brazil', 'www.scielo.br'],
    'arg': ['Argentina', 'www.scielo.org.ar'],
    'cub': ['Cuba', 'scielo.sld.cu'],
    'esp': ['Spain', 'scielo.isciii.es'],
    'col': ['Colombia', 'www.scielo.org.co'],
    'sss': ['Social Sciences', 'socialsciences.scielo.org'],
    'spa': ['Public Health', 'www.scielosp.org'],
    'mex': ['Mexico', 'www.scielo.org.mx'],
    'prt': ['Portugal', 'www.scielo.mec.pt'],
    'cri': ['Costa Rica', 'www.scielo.sa.cr'],
    'ven': ['Venezuela', 'www.scielo.org.ve'],
    'ury': ['Uruguay', 'www.scielo.edu.uy'],
    'per': ['Peru', 'www.scielo.org.pe'],
    'chl': ['Chile', 'www.scielo.cl'],
    'sza': ['South Africa', 'www.scielo.org.za'],
    'bol': ['Bolivia', 'www.scielo.org.bo'],
    'pry': ['Paraguay', 'scielo.iics.una.py'],
    'psi': ['PEPSIC', 'pepsic.bvsalud.org'],
    'ppg': ['PPEGEO', 'ppegeo.igc.usp.br'],
    'rve': ['RevOdonto', 'revodonto.bvsalud.org'],
    'edc': ['Educa', 'educa.fcc.org.br'],
    'inv': [u'Inovação', 'inovacao.scielo.br'],
    'cic': [u'Ciência e Cultura', 'cienciaecultura.bvs.br'],
    'cci': [u'ComCiência', 'comciencia.scielo.br'],
    'wid': ['West Indians', 'caribbean.scielo.org'],
    'pro': ['Proceedings', 'www.proceedings.scielo.br'],
    'ecu': ['Ecuador', 'scielo.senescyt.gob.ec'],
}

journal_status = {
    'c': u'current',
    'd': u'deceased',
    '?': u'inprogress',
    'p': u'inprogress',
    's': u'suspended'
}

journal_standard = {
    u'iso690': u'iso 690/87 - international standard',
    u'nbr6023': u'nbr 6023/89 - associação nacional',
    u'other': u'other standard',
    u'vancouv': u'the vancouver group - uniform',
    u'apa': u'American Psychological Association'
}

journal_ctrl_vocabulary = {
    u'decs': u'Health Sciences Descriptors',
    u'nd': u'No Descriptor'
}

journal_publication_level = {
    u'DI': u'Divulgation',
    u'CT': u'Scientific Technical'
}

journal_title_category = {
    u'paralleltitle': u'Parallel Title',
    u'other': u'Other',
    u'abbrev_scopus': u'Scopus (abbreviated)',
    u'abbrev_wos': u'Web of Science (abbreviated)',
    u'abbrev_nlm': u'National Library of Medicine (abbreviated)',
}

month_bad_prediction = {
    u'jan': 1,
    u'ene': 1,
    u'janeiro': 1,
    u'enero': 1,
    u'january': 1,
    u'fev': 2,
    u'feb': 2,
    u'fevereiro': 2,
    u'febrero': 2,
    u'february': 2,
    u'mar': 3,
    u'março': 3,
    u'marzo': 3,
    u'march': 3,
    u'abr': 4,
    u'apr': 4,
    u'abril': 4,
    u'april': 4,
    u'mai': 5,
    u'may': 5,
    u'maio': 5,
    u'mayo': 5,
    u'jun': 6,
    u'junho': 6,
    u'junio': 6,
    u'june': 6,
    u'jul': 7,
    u'julho': 7,
    u'julio': 7,
    u'july': 7,
    u'ago': 8,
    u'aug': 8,
    u'agosto': 8,
    u'august': 8,
    u'set': 9,
    u'sep': 9,
    u'setembro': 9,
    u'septiembre': 9,
    u'september': 9,
    u'out': 10,
    u'oct': 10,
    u'outubro': 10,
    u'octubre': 10,
    u'actober': 10,
    u'nov': 11,
    u'novembro': 11,
    u'noviembre': 11,
    u'november': 11,
    u'dez': 12,
    u'dic': 12,
    u'dezembro': 12,
    u'diciembre': 12,
    u'december': 12
}
