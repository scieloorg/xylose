# encoding: utf-8

ISO639_1_to_2 = {'gv': 'glv', 'gu': 'guj', 'gd': 'gla', 'ga': 'gle', 'gn': 'grn', 'gl': 'glg', 'lg': 'lug', 'lb': 'ltz', 'la': 'lat', 'ln': 'lin', 'lo': 'lao', 'tt': 'tat', 'tr': 'tur', 'ts': 'tso', 'li': 'lim', 'lv': 'lav', 'to': 'ton', 'lt': 'lit', 'lu': 'lub', 'tk': 'tuk', 'th': 'tha', 'ti': 'tir', 'tg': 'tgk', 'te': 'tel', 'ta': 'tam', 'yi': 'yid', 'yo': 'yor', 'de': 'ger* / deu', 'da': 'dan', 'dz': 'dzo', 'st': 'sot', 'dv': 'div', 'qu': 'que', 'el': 'gre* / ell', 'eo': 'epo', 'en': 'eng', 'zh': 'zho / chi*', 'ee': 'ewe', 'za': 'zha', 'mh': 'mah', 'uk': 'ukr', 'eu': 'eus / baq*', 'et': 'est', 'es': 'spa', 'ru': 'rus', 'rw': 'kin', 'rm': 'roh', 'rn': 'run', 'ro': 'rum* / ron', 'bn': 'ben', 'be': 'bel', 'bg': 'bul', 'ba': 'bak', 'wa': 'wln', 'wo': 'wol', 'bm': 'bam', 'jv': 'jav', 'bo': 'tib* / bod', 'bh': 'bih', 'bi': 'bis', 'br': 'bre', 'bs': 'bos', 'ja': 'jpn', 'om': 'orm', 'oj': 'oji', 'ty': 'tah', 'oc': 'oci', 'tw': 'twi', 'os': 'oss', 'or': 'ori', 'xh': 'xho', 'ch': 'cha', 'co': 'cos', 'ca': 'cat', 'ce': 'che', 'cy': 'wel* / cym', 'cs': 'cze* / ces', 'cr': 'cre', 'cv': 'chv', 'cu': 'chu', 've': 'ven', 'ps': 'pus', 'i.e.': 'ile', 'pt': 'por', 'tl': 'tgl', 'pa': 'pan', 'vi': 'vie', 'pi': 'pli', 'is': 'isl / ice*', 'pl': 'pol', 'hz': 'her', 'hy': 'hye / arm*', 'hr': 'hrv', 'iu': 'iku', 'ht': 'hat', 'hu': 'hun', 'hi': 'hin', 'ho': 'hmo', 'ha': 'hau', 'he': 'heb', 'mg': 'mlg', 'uz': 'uzb', 'ml': 'mal', 'mn': 'mon', 'mi': 'mri / mao*', 'ik': 'ipk', 'mk': 'mkd / mac*', 'ur': 'urd', 'mt': 'mlt', 'ms': 'msa / may*', 'mr': 'mar', 'ug': 'uig', 'my': 'mya / bur*', 'ki': 'kik', 'aa': 'aar', 'ab': 'abk', 'ae': 'ave', 'ss': 'ssw', 'af': 'afr', 'tn': 'tsn', 'sw': 'swa', 'ak': 'aka', 'am': 'amh', 'it': 'ita', 'an': 'arg', 'ii': 'iii', 'ia': 'ina', 'as': 'asm', 'ar': 'ara', 'su': 'sun', 'io': 'ido', 'av': 'ava', 'ay': 'aym', 'az': 'aze', 'id': 'ind', 'ig': 'ibo', 'sk': 'slk / slo*', 'sr': 'srp', 'nl': 'nld / dut*', 'nn': 'nno', 'no': 'nor', 'na': 'nau', 'nb': 'nob', 'nd': 'nde', 'ne': 'nep', 'ng': 'ndo', 'ny': 'nya', 'vo': 'vol', 'zu': 'zul', 'so': 'som', 'nr': 'nbl', 'nv': 'nav', 'sn': 'sna', 'fr': 'fre* / fra', 'sm': 'smo', 'fy': 'fry', 'sv': 'swe', 'fa': 'per* / fas', 'ff': 'ful', 'fi': 'fin', 'fj': 'fij', 'sa': 'san', 'fo': 'fao', 'ka': 'kat / geo*', 'kg': 'kon', 'kk': 'kaz', 'kj': 'kua', 'sq': 'sqi / alb*', 'ko': 'kor', 'kn': 'kan', 'km': 'khm', 'kl': 'kal', 'ks': 'kas', 'kr': 'kau', 'si': 'sin', 'kw': 'cor', 'kv': 'kom', 'ku': 'kur', 'sl': 'slv', 'sc': 'srd', 'ky': 'kir', 'sg': 'sag', 'se': 'sme', 'sd': 'snd'}
ISO639_1 = set([k for k,v in ISO639_1_to_2.items()])

article_types = {
    'rc': 'undefined',
    'ab': 'abstract',
    'pv': 'article-commentary',
    'ed': 'editorial',
    'in': 'oration',
    'tr': 'research-article',
    'up': 'review-article',
    'oa': 'research-article',
    'an': 'undefined',
    'ax': 'undefined',
    'mt': 'research-article',
    'le': 'letter',
    'ra': 'review-article',
    'nd': 'undefined',
    'cr': 'case-report',
    'sc': 'rapid-communication',
    'co': 'article-commentary',
    'rn': 'brief-report'
}
