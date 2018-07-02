# encoding: utf-8
import sys
from functools import wraps
import warnings
import re
import unicodedata
import datetime

try:  # Keep compatibility with python 2.7
    from html import unescape
except ImportError:
    from HTMLParser import HTMLParser

from . import choices
from . import tools
from . import iso3166

from legendarium import formatter

allowed_formats = ['iso 639-2', 'iso 639-1', None]

# --------------
# Py2 compat
# --------------
PY2 = sys.version_info[0] == 2

if PY2:
    html_parser = HTMLParser().unescape
else:
    html_parser = unescape
# --------------

LICENSE_REGEX = re.compile(r'a.+?href="(.+?)"')
LICENSE_CREATIVE_COMMONS = re.compile(r'licenses/(.*?/\d\.\d)') # Extracts the creative commons id from the url.
DOI_REGEX = re.compile(r'\d{2}\.\d+/.*$')
SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')
CLEANUP_MIXED_CITATION = re.compile(r'< *?p.*?>|< *?f.*?>|< *?tt.*?>|< *?span.*?>|< *?cite.*?>|< *?country-region.*?>|< *?region.*?>|< *?place.*?>|< *?state.*?>|< *?city.*?>|< *?dir.*?>|< *?li.*?>|< *?ol.*?>|< *?dt.*?>|< *?dd.*?>|< *?hr.*?>|< *?/ *?p.*?>|< *?/ *?f.*?>|< *?/ *?tt.*?>|< *?/ *?span.*?>|< *?/ *?cite.*?>|< *?/ *?country-region.*?>|< *?/ *?region.*?>|< *?/ *?place.*?>|< *?/ *?state.*?>|< *?/ *?city.*?>|< *?/ *?dir.*?>|< *?/ *?li.*?>|< *?/ *?ol.*?>|< *?/ *?dt.*?>|< *?/ *?dd.*?>', re.IGNORECASE)
REPLACE_TAGS_MIXED_CITATION = (
    (re.compile(r'< *?i.*?>', re.IGNORECASE), '<i>',),
    (re.compile(r'< *?/ *?i.*?>', re.IGNORECASE), '</i>',),
    (re.compile(r'< *?u.*?>', re.IGNORECASE), '<u>',),
    (re.compile(r'< *?/ *?u.*?>', re.IGNORECASE), '</u>',),
    (re.compile(r'< *?b.*?>', re.IGNORECASE), '<strong>',),
    (re.compile(r'< *?/ *?b.*?>', re.IGNORECASE), '</strong>',),
    (re.compile(r'< *?em.*?>', re.IGNORECASE), '<strong>',),
    (re.compile(r'< *?/ *?em.*?>', re.IGNORECASE), '</strong>',),
    (re.compile(r'< *?small.*?>', re.IGNORECASE), '<small>',),
    (re.compile(r'< *?/ *?small.*?>', re.IGNORECASE), '</small>',),
)


class XyloseException(Exception):
    pass


class UnavailableMetadataException(XyloseException):
    pass


def cleanup_number(text):
    """
    Lefting just valid numbers
    """

    return ''.join([i for i in text if i.isdigit()])


def cleanup_string(text):
    """
    Remove any special character like -,./ lefting just numbers and alphabet
    characters
    """

    try:
        nfd_form = unicodedata.normalize('NFD', text.strip().lower())
    except TypeError:
        nfd_form = unicodedata.normalize('NFD', unicode(text.strip().lower()))

    cleaned_str = u''.join(x for x in nfd_form if unicodedata.category(x)[0] == 'L' or x == ' ')

    return cleaned_str


def remove_control_characters(data):
    return "".join(ch for ch in data if unicodedata.category(ch)[0] != "C")


def html_decode(string):

    try:
        string = html_parser(string)
    except:
        return string

    try:
        return remove_control_characters(string)
    except:
        return string


class Issue(object):

    def __init__(self, data, iso_format=None):
        """
        Create an Issue object given a isis2json type 3 SciELO document.

        Keyword arguments:
        iso_format -- the language iso format for methods that retrieve content
        identified by language.
        ['iso 639-2', 'iso 639-1', None]
        """
        if iso_format not in allowed_formats:
            raise ValueError('Language format not allowed ({0})'.format(iso_format))

        self._iso_format = iso_format
        self._journal = None
        self.data = data

    def bibliographic_legends(self, language='en'):

        legends = {}
        legends['descriptive_short_format'] = formatter.descriptive_short_format(
            self.journal.title,
            self.journal.abbreviated_title,
            self.publication_date,
            self.volume,
            self.number,
            (self.supplement_volume or '') + (self.supplement_number or ''),
            language
            )
        legends['descriptive_html_short_format'] = formatter.descriptive_html_short_format(
            self.journal.title,
            self.journal.abbreviated_title,
            self.publication_date,
            self.volume,
            self.number,
            (self.supplement_volume or '') + (self.supplement_number or ''),
            language
            )
        legends['descriptive_very_short_format'] = formatter.descriptive_very_short_format(
            self.publication_date,
            self.volume,
            self.number,
            (self.supplement_volume or '') + (self.supplement_number or ''),
            language
            )
        legends['descriptive_html_very_short_format'] = formatter.descriptive_html_very_short_format(
            self.publication_date,
            self.volume,
            self.number,
            (self.supplement_volume or '') + (self.supplement_number or ''),
            language
            )

        return legends

    @property
    def journal(self):

        if 'title' in self.data:
            self._journal = self._journal or Journal(self.data['title'], iso_format=self._iso_format)
        else:
            msg = 'Journal metadata not found for the issue %s' % self.publisher_id
            raise UnavailableMetadataException(msg)

        return self._journal

    @property
    def publisher_id(self):
        """
        This method retrieves the publisher id of the given issue, if it exists.
        This method deals with the legacy fields (880).
        """
        return self.data['issue']['v880'][0]['_']

    @property
    def collection_acronym(self):
        """
        This method retrieves the collection of the given article,
        if it exists.
        The subject areas are based on the journal subject areas.
        This method deals with the legacy fields (v992) and the
        new field (collection), the field collection is priorized.
        """
        if 'collection' in self.data:
            return self.data['collection']

        if 'v992' in self.data['issue']:
            if isinstance(self.data['issue']['v992'], list):
                return self.data['issue']['v992'][0]['_']
            else:
                return self.data['issue']['v992']

        if 'v992' in self.data['title']:
            if isinstance(self.data['title']['v992'], list):
                return self.data['title']['v992'][0]['_']
            else:
                return self.data['title']['v992']

    @property
    def scielo_domain(self):
        """
        This method retrieves the collection domains of the given article, if it exists.
        This method deals with the legacy fields (69, 690).
        """

        if self.collection_acronym:
            return choices.collections.get(
                self.collection_acronym,
                [u'Undefined: %s' % self.collection_acronym, None]
            )[1] or None

        if 'v690' in self.data['title']:
            return self.data['title']['v690'][0]['_'].replace('http://', '')
        elif 'v69' in self.data['title']:
            return self.data['title']['v69'][0]['_'].replace('http://', '')

    @property
    def is_marked_up(self):
        """
        This method retrieves the issue order of the given article.
        This method deals with the fields (v880).
        """

        imu = self.data['issue'].get('v200', [{'_': 0}])[0]['_']

        return True if str(imu) == '1' else False

    @property
    def order(self):
        """
        This method retrieves the issue order of the given article.
        This method deals with the fields (v880).
        """

        order = self.data['issue'].get('v36', [{'_': None}])[0]['_']

        if not order:
            return None

        return str(int(order[4:]))

    @property
    def assets_code(self):
        """
        This method retrieves the issue label available in the field v4. The
        path to the document assets is build with this code.
        ex: /pdf/[journal_acronym]/[assets_code]/[file_code]
        """

        return self.data['issue'].get('v4', [{'_': None}])[0]['_']

    @property
    def type(self):
        """
        This method retrieves the issue type ['ahead', 'regular', 'supplement', 'special', 'pressrelease'].
        """

        label = ''.join([
            self.data['issue'].get('v31', [{'_': ''}])[0]['_'],
            self.data['issue'].get('v32', [{'_': ''}])[0]['_'],
            self.data['issue'].get('v131', [{'_': ''}])[0]['_'],
            self.data['issue'].get('v132', [{'_': ''}])[0]['_'],
            self.data['issue'].get('v41', [{'_': ''}])[0]['_'],
        ]).lower()

        if 'pr' in label:
            return 'pressrelease'

        if 'ahead' in label:
            return 'ahead'

        if 'v131' in self.data['issue'] or 'v132' in self.data['issue']:
            return 'supplement'

        if 'suppl' in label:
            return 'supplement'

        if 'spe' in label:
            return 'special'

        return 'regular'

    @property
    def label(self):
        """
        This method retrieves the issue label. A combined value that describes
        the entire issue label. Ex: v20n2, v20spe1, etc.
        """

        label = ''
        label_issue = self.number or ''
        label_volume = self.volume or ''
        label_suppl_issue = ' suppl %s' % self.supplement_number if self.supplement_number else ''

        if label_suppl_issue:
            label_issue += label_suppl_issue

        label_suppl_volume = ' suppl %s' % self.supplement_volume if self.supplement_volume else ''

        if label_suppl_volume:
            label_issue += label_suppl_volume

        label_issue = SUPPLBEG_REGEX.sub('', label_issue)
        label_issue = SUPPLEND_REGEX.sub('', label_issue)

        label += ''.join(['v'+label_volume, 'n'+label_issue])

        return label

    @property
    def volume(self):
        """
        This method retrieves the issue volume of the given issue, if it exists.
        This method deals with the legacy fields (31).
        """
        if 'v31' in self.data['issue']:
            return self.data['issue']['v31'][0]['_']

    @property
    def number(self):
        """
        This method retrieves the issue number of the given issue, if it exists.
        This method deals with the legacy fields (32).
        """
        if 'v32' in self.data['issue']:
            return self.data['issue']['v32'][0]['_']

    @property
    def _start_end_months(self):
        list_str_with_months = [
            cleanup_string(x.get('m', '')) for x in self.data['issue'].get('v43', [{}]) if 'm' in x
        ]

        if not list_str_with_months:
            return None

        str_with_months = ''.join(list_str_with_months).lower()

        found_months = set()
        for month_str, month_number in choices.month_bad_prediction.items():
            if month_str in str_with_months:
                found_months.add(month_number)

        found_months = sorted(list(found_months))

        return found_months

    @property
    def start_month(self):
        """
        This method retrieves the stating month of the issue.
        This method deals with the field (v43)
        The issue database do not have a feaseble way to collect this data. It
        is a exact match made from a field content that is filled by convention
        eg: feb./mar
            jan/mar
            ene/mar
            out/dez
            oct/dic
            oct.dic
        As it is a convetion it may be filled out of the convetion :-/ :-o in
        this situations the result will be None.
        """

        return '%02d' % (self._start_end_months[0]) if self._start_end_months else None

    @property
    def end_month(self):
        """
        This method retrieves the stating month of the issue.
        This method deals with the field (v43)
        The issue database do not have a feaseble way to collect this data. It
        is a exact match made from a field content that is filled by convention
        eg: feb./mar
            jan/mar
            ene/mar
            out/dez
            oct/dic
        As it is a convetion it may be filled out of the convetion :-/ :-o in
        this situations the result will be None.
        """

        return '%02d' % (self._start_end_months[-1]) if self._start_end_months else None

    @property
    def supplement_volume(self):
        """
        This method retrieves the supplement of volume of the given issue, if it exists.
        This method deals with the legacy fields (131).
        """
        if 'v131' in self.data['issue']:
            return self.data['issue']['v131'][0]['_']

    @property
    def supplement_number(self):
        """
        This method retrieves the supplement number of the given issue, if it exists.
        This method deals with the legacy fields (132).
        """
        if 'v132' in self.data['issue']:
            return self.data['issue']['v132'][0]['_']

    @property
    def is_ahead_of_print(self):

        if self.number and 'ahead' in self.number.lower():
            return True

        return False

    def url(self, language='en'):
        """
        This method retrieves the issue url of the given issue.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_issuetoc&pid={1}&lng={2}".format(
                self.scielo_domain,
                self.publisher_id,
                language
            )

    @property
    def publication_date(self):
        """
        This method retrieves the publication date of the given issue, if it exists.
        This method deals with the legacy fields (65).
        """

        pdate = self.data['issue'].get('v65',[{'_': None}])[0]['_']

        if pdate:
            return (tools.get_date(pdate))

        return None

    @property
    def processing_date(self):
        """
        This method retrieves the processing date of the given issue, if it exists.
        This method deals with the legacy fields (91).
        """

        pdate = self.data.get(
            'processing_date',
            self.data['issue'].get('v91', [{'_': ''}])[0]['_']
        )

        if not pdate:
            return None

        return tools.get_date(pdate.replace('-', '')) if pdate else None

    @property
    def is_press_release(self):

        pr = self.data['issue'].get('v41', [{'_': ''}])[0]['_'].lower()

        return True if 'pr' in pr else False

    @property
    def titles(self):

        titles = {}

        for title in self.data['issue'].get('v33', []):
            if 'l' in title and '_' in title:
                titles[title['l']] = title['_']

        if not titles:
            return None

        return titles

    @property
    def total_documents(self):

        return self.data['issue'].get('v122', [{'_': 0}])[0]['_']

    @property
    def controlled_vocabulary(self):

        cv = self.data['issue'].get('v85', [{'_': None}])[0]['_']

        cv = cv.lower() if cv else None

        if cv is None:
            return self.journal.controlled_vocabulary

        return (cv, choices.journal_ctrl_vocabulary.get(cv, cv))

    @property
    def editorial_standard(self):

        es = self.data['issue'].get('v117', [{'_': None}])[0]['_']

        es = es.lower() if es else None

        if es is None:
            return self.journal.editorial_standard

        return (es, choices.journal_standard.get(es, es))

    @property
    def permissions(self):
        data = None

        if 'license' in self.data:
            data = {}
            data['text'] = tools.creative_commons_text(self.data['license'])
            data['url'] = 'http://creativecommons.org/licenses/%s/' % self.data['license']
            data['id'] = self.data['license']

            return data

        if 'v541' in self.data['issue'] and self.data['issue']['v541'][0]['_'].lower() == 'nd':
            return None

        if 'v541' in self.data['issue']:
            if len(self.data['issue']['v541'][0]['_'].lower().split('/')) == 1:
                license = '%s/4.0' % self.data['issue']['v541'][0]['_'].lower()
            else:
                license = self.data['issue']['v541'][0]['_'].lower()
            data = {}
            data['text'] = tools.creative_commons_text(license)
            data['url'] = 'http://creativecommons.org/licenses/%s/' % license
            data['id'] = license
            return data

        if 'v540' in self.data['issue']:
            for dlicense in self.data['issue']['v540']:
                if not 't' in dlicense:
                    continue

                license_url = LICENSE_REGEX.findall(dlicense['t'])
                if len(license_url) == 0:
                    continue

                license_id = LICENSE_CREATIVE_COMMONS.findall(license_url[0])

                if len(license_id) == 0:
                    continue

                data = {}
                data['text'] = tools.creative_commons_text(license_id[0]) or dlicense['t']
                data['url'] = license_url[0]
                data['id'] = license_id[0]

                if 'l' in dlicense and dlicense['l'] == 'en':
                    break

        return data or self.journal.permissions

    @property
    def processing_date(self):
        """
        This method retrieves the processing date of the given issue, if it exists.
        This method deals with the legacy fields (91).
        """

        pdate = self.data.get(
            'processing_date',
            self.data['issue'].get('v91', [{'_': ''}])[0]['_']
        )

        if not pdate:
            return None

        return tools.get_date(pdate.replace('-', '')) if pdate else None

    @property
    def update_date(self):
        """
        This method retrieves the update date of the given issue, if it exists.
        If not it will retrieve de update date.
        This method deals with the legacy fields (91) and new field updated_at.
        """

        updated_at = self.data.get(
            'updated_at',
            self.processing_date
        )

        if not updated_at:
            update_at = self.creation_date

        return tools.get_date(updated_at.replace('-', '')) if updated_at else None

    @property
    def creation_date(self):
        """
        This method retrieves the creation_date date of the given issue, if it exists.
        This method deals with the legacy fields (93) and new field created_at.
        """

        created_at = self.data.get(
            'created_at',
            self.data['issue'].get('v93', [{'_': ''}])[0]['_']
        )

        return tools.get_date(created_at.replace('-', '')) if created_at else None

    @property
    def sections(self):
        """
        This method retrieves the sections of the given issue, if it exists.
        This method deals with the legacy fields (49) and new field created_at.
        Eg:
        {
            "CODE020": {
                "en": "Other Themes",
                "pt": "Temas Livres"
            },
            "CODE100": {
                "en": "Review",
                "pt": "Resenha"
            },
            "CODE120": {
                "en": "Theme",
                "pt": "Artigos do tema"
            },
            "CODE040": {
                "en": "Editorial",
                "pt": "Editorial"
            }
        }
        """
        sections = {}

        for section in self.data['issue'].get('v49', []):
            if not 'c' in section or not 'l' in section or not 't' in section:
                continue
            sections.setdefault(section['c'], {})
            sections[section['c']][section['l']] = section['t']

        return sections if sections else None


class Journal(object):

    def __init__(self, data, iso_format=None):
        """
        Create an Journal object given a isis2json type 3 SciELO document.

        Keyword arguments:
        iso_format -- the language iso format for methods that retrieve content
        identified by language.
        ['iso 639-2', 'iso 639-1', None]
        """
        if not iso_format in allowed_formats:
            raise ValueError('Language format not allowed ({0})'.format(iso_format))

        self._iso_format = iso_format
        self.data = data
        self.print_issn = None
        self.electronic_issn = None
        self._load_issn()

    def _load_issn(self):
        """
        This method creates an object level attributes (print_issn and/or
        electronic issn), according to the given metadata.
        This method deal with the legacy datamodel fields (935, 400, 35, 435) where:
        """

        if 'v435' in self.data:
            for item in self.data['v435']:
                if 't' in item and item['t'] == 'PRINT':
                    self.print_issn = item['_']
                if 't' in item and item['t'] == 'ONLIN':
                    self.electronic_issn = item['_']
            return None

        if not 'v35' in self.data:
            return None

        # ISSN and Other Complex Stuffs from the old version
        if not 'v935' in self.data:  # Old fashion ISSN persistance style
            if self.data['v35'][0]['_'] == "PRINT":
                self.print_issn = self.data['v400'][0]['_']
            else:
                self.electronic_issn = self.data['v400'][0]['_']
        else:  # New ISSN persistance style
            if self.data['v35'][0]['_'] == "PRINT":
                self.print_issn = self.data['v935'][0]['_']
                if self.data['v935'][0]['_'] != self.data['v400'][0]['_']:
                    self.electronic_issn = self.data['v400'][0]['_']
            else:
                self.electronic_issn = self.data['v935'][0]['_']
                if self.data['v935'][0]['_'] != self.data['v400'][0]['_']:
                    self.print_issn = self.data['v400'][0]['_']

    @property
    def permissions(self):
        data = None

        if 'license' in self.data:
            data = {}
            data['text'] = tools.creative_commons_text(self.data['license'])
            data['url'] = 'http://creativecommons.org/licenses/%s/' % self.data['license']
            data['id'] = self.data['license']

            return data

        if 'v541' in self.data and self.data['v541'][0]['_'].lower() == 'nd':
            return None

        if 'v541' in self.data:
            if len(self.data['v541'][0]['_'].lower().split('/')) == 1:
                license = '%s/4.0' % self.data['v541'][0]['_'].lower()
            else:
                license = self.data['v541'][0]['_'].lower()
            data = {}
            data['text'] = tools.creative_commons_text(license)
            data['url'] = 'http://creativecommons.org/licenses/%s/' % license
            data['id'] = license
            return data

        if 'v540' in self.data:
            for dlicense in self.data['v540']:
                if not 't' in dlicense:
                    continue

                license_url = LICENSE_REGEX.findall(dlicense['t'])
                if len(license_url) == 0:
                    continue

                license_id = LICENSE_CREATIVE_COMMONS.findall(license_url[0])

                if len(license_id) == 0:
                    continue

                data = {}
                data['text'] = tools.creative_commons_text(license_id[0]) or dlicense['t']
                data['url'] = license_url[0]
                data['id'] = license_id[0]

                if 'l' in dlicense and dlicense['l'] == 'en':
                    break

        return data

    @property
    def publishing_model(self):
        """
        This method retrieve the publishing model
        This method deals with the field (v699)
        """

        value = self.data.get('v699', [{'_': ''}])[0]['_']

        if value.lower() == 'continuous':
            return 'continuous'

        return 'regular'

    @property
    def is_publishing_model_continuous(self):
        """
        This method retrieve the publishing model
        This method deals with the field (v699)
        """

        value = self.data.get('v699', [{'_': ''}])[0]['_']

        if self.publishing_model == 'continuous':
            return True

        return False

    @property
    def editor_address(self):
        """
        This method retrieve the editor address
        This method deals with the field (v63)
        """

        if not 'v63' in self.data:
            return None

        return ', '.join([i['_'] for i in self.data.get('v63') if '_' in i and i['_'] != ''])

    @property
    def editor_email(self):
        """
        This method retrieve the editor address
        This method deals with the field (v63)
        """

        return self.data.get('v64', [{'_': None}])[0]['_']

    @property
    def is_indexed_in_scie(self):
        """
        This method indicates if the given journal is indexed at SCIE
        This method deals with the field (v851)
        """

        return True if self.data.get('v851', [{'_': None}])[0]['_'] else False

    @property
    def is_indexed_in_ssci(self):
        """
        This method indicates if the given journal is indexed at SSCI
        This method deals with the field (v852)
        """

        return True if self.data.get('v852', [{'_': None}])[0]['_'] else False

    @property
    def is_indexed_in_ahci(self):
        """
        This method indicates if the given journal is indexed at SCIE
        This method deals with the field (v853)
        """

        return True if self.data.get('v853', [{'_': None}])[0]['_'] else False

    @property
    def publication_level(self):

        pl = self.data.get('v330', [{'_': None}])[0]['_']

        pl = pl.upper() if pl else None

        if pl is None:
            return None

        return (pl, choices.journal_publication_level.get(pl, pl))

    @property
    def controlled_vocabulary(self):

        cv = self.data.get('v85', [{'_': None}])[0]['_']

        cv = cv.lower() if cv else None

        if cv is None:
            return None

        return (cv, choices.journal_ctrl_vocabulary.get(cv, cv))

    @property
    def editorial_standard(self):

        es = self.data.get('v117', [{'_': None}])[0]['_']

        es = es.lower() if es else None

        if es is None:
            return None

        return (es, choices.journal_standard.get(es, es))

    @property
    def submission_url(self):
        """
        This method retrieves the submission system url of the given journal
        This method deals with the legacy field (v692).
        """

        return self.data.get('v692', [{'_': None}])[0]['_']

    @property
    def scimago_code(self):
        """
        This method retrieves the secs_code of the journal
        This method deals with the field (scimago_id).
        """

        return self.data.get('scimago_id', None)

    @property
    def secs_code(self):
        """
        This method retrieves the secs_code of the journal
        This method deals with the legacy field (v37).
        """

        return self.data.get('v37', [{'_': None}])[0]['_']

    @property
    def cnn_code(self):
        """
        This method retrieves the cnn_code of the journal
        This method deals with the legacy field (v20).
        """

        return self.data.get('v20', [{'_': None}])[0]['_']

    @property
    def first_year(self):
        """
        This method retrieves the first year of the journal, not considering only
        the issues published on the collection. It represents the entire collection
        of the journal.
        This method deals with the legacy field (v301).
        """

        data = self.data.get('v301', [{'_': None}])[0]['_']

        if data is None:
            return None

        year = cleanup_number(data)[:4]

        if len(year) == 4:
            return str(datetime.datetime.strptime(year, '%Y').year)

        if len(year) == 2:
            return str(datetime.datetime.strptime(year, '%y').year)

    @property
    def first_volume(self):
        """
        This method retrieves the first volume of the journal, not considering only
        the issues published on the collection. It represents the entire collection
        of the journal.
        This method deals with the legacy field (v302).
        """

        return self.data.get('v302', [{'_': None}])[0]['_']

    @property
    def first_number(self):
        """
        This method retrieves the first number of the journal, not considering
        the issues published on the collection. It represents the entire collection
        of the journal.
        This method deals with the legacy field (v303).
        """

        return self.data.get('v303', [{'_': None}])[0]['_']

    @property
    def last_year(self):
        """
        This method retrieves the last year of the journal, not considering only
        the issues published on the collection. It represents the entire collection
        of the journal.
        This method deals with the legacy field (v304).
        """

        data = self.data.get('v304', [{'_': None}])[0]['_']

        if data is None:
            return None

        year = cleanup_number(data)[:4]

        if len(year) == 4:
            return str(datetime.datetime.strptime(year, '%Y').year)

        if len(year) == 2:
            return str(datetime.datetime.strptime(year, '%y').year)


    @property
    def last_volume(self):
        """
        This method retrieves the last volume of the journal, not considering only
        the issues published on the collection. It represents the entire collection
        of the journal.
        This method deals with the legacy field (v305).
        """

        return self.data.get('v305', [{'_': None}])[0]['_']

    @property
    def last_number(self):
        """
        This method retrieves the last year of the journal, not considering only
        the issues published on the collection. It represents the entire collection
        of the journal.
        This method deals with the legacy field (v306).
        """

        return self.data.get('v306', [{'_': None}])[0]['_']

    @property
    def languages(self):
        """
        This method retrieves a list of possible languages that the journal
        publishes the fulltexts.
        This method deals with the legacy fields (v350).
        """
        if 'v350' in self.data:
            langs = [i['_'] for i in self.data['v350'] if i['_'] in choices.ISO639_1_to_2.keys()]
            if len(langs) > 0:
                return langs

    @property
    def abstract_languages(self):
        """
        This method retrieves a list of possible languages that the journal
        publishes the abstracts.
        This method deals with the legacy fields (v360).
        """
        if 'v360' in self.data:
            langs = [i['_'] for i in self.data['v360'] if i['_'] in choices.ISO639_1_to_2.keys()]
            if len(langs) > 0:
                return langs

    @property
    def collection_acronym(self):
        """
        This method retrieves the collection of the given journal,
        if it exists.
        This method deals with the legacy fields (v992).
        """

        if 'v992' in self.data:
            if isinstance(self.data['v992'], list):
                return self.data['v992'][0]['_']
            else:
                return self.data['v992']

    @property
    def scielo_domain(self):
        """
        This method retrieves the collection domains of the given journal, if it exists.
        This method deals with the legacy fields (690).
        """

        if self.collection_acronym:
            return choices.collections.get(
                self.collection_acronym,
                [u'Undefined: %s' % self.collection_acronym, None]
            )[1] or None

        if 'v690' in self.data:
            return self.data['v690'][0]['_'].replace('http://', '')

    def any_issn(self, priority=u'electronic'):
        """
        This method retrieves the issn of the given article, acoording to the given priority.
        """
        if priority == u'electronic':
            if self.electronic_issn:
                return self.electronic_issn
            else:
                return self.print_issn
        else:
            if self.print_issn:
                return self.print_issn
            else:
                return self.electronic_issn

    @property
    def scielo_issn(self):
        """
        This method retrieves the original language of the given article.
        This method deals with the legacy fields (v400).
        """

        return self.data.get('v400', [{'_': None}])[0]['_']

    @property
    def institutional_url(self):
        """
        This method retrieves the journal institutional url of the given article.
        """

        return self.data.get('v69', [{'_': None}])[0]['_']

    def url(self, language='en'):
        """
        This method retrieves the journal url of the given article.
        """

        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_serial&pid={1}&lng={2}".format(
                self.scielo_domain,
                self.scielo_issn,
                language
            )

    @property
    def subject_descriptors(self):
        """
        This method retrieves the subject descriptors of the given journal,
        if it exists.
        This method deals with the legacy fields (441).
        """

        if 'v440' in self.data:
            return [area['_'] for area in self.data['v440']]

    @property
    def index_coverage(self):
        """
        This method retrieves the index coverage of the given
        journal, if it exists.
        This method deals with the legacy fields (450).
        """

        if 'v450' in self.data:
            return [area['_'] for area in self.data['v450']]

    @property
    def subject_areas(self):
        """
        This method retrieves the subject areas of the given journal,
        if it exists.
        The subject areas are based on the journal subject areas.
        This method deals with the legacy fields (441).
        """

        if 'v441' in self.data:
            return [area['_'] for area in self.data['v441']]

    @property
    def wos_subject_areas(self):
        """
        This method retrieves the Wob of Sciences subject areas of the given
        journal, if it exists.
        This method deals with the legacy fields (854).
        """

        if 'v854' in self.data:
            return [area['_'] for area in self.data['v854']]

    @property
    def wos_citation_indexes(self):
        """
        This method retrieves the Wob of Sciences Citation Indexes of the given
        journal, if it exists.
        This method deals with the legacy fields (851).
        """

        areas = []
        if 'v851' in self.data:
            areas += [area['_'] for area in self.data['v851']]

        if 'v852' in self.data:
            areas += [area['_'] for area in self.data['v852']]

        if 'v853' in self.data:
            areas += [area['_'] for area in self.data['v853']]

        if not len(areas) == 0:
            return areas

    @property
    def publisher_name(self):
        """
        This method retrieves the publisher name of the given article,
        if it exists.
        This method deals with the legacy fields (480).

        This method return a list:

        ["Associa\u00e7\u00e3o Brasileira de Limnologia",
        "Sociedade Botânica do Brasil"]
        """
        if 'v480' not in self.data:
            return None

        return [publisher['_'] for publisher in self.data.get('v480') if '_' in publisher and publisher['_'] != ""]

    @property
    def publisher_loc(self):
        """
        This method retrieves the publisher localization of the given journal,
        if it exists.
        This method deals with the legacy fields (490).
        """

        warnings.warn("deprecated, use journal.publisher_city", DeprecationWarning)

        return self.data.get('v490', [{'_': None}])[0]['_']

    @property
    def publisher_city(self):
        """
        This method retrieves the publisher localization of the given journal,
        if it exists.
        This method deals with the legacy fields (490).
        """

        return self.data.get('v490', [{'_': None}])[0]['_']

    @property
    def publisher_state(self):
        """
        This method retrieves the publisher state of the given journal,
        if it exists.
        This method deals with the legacy fields (320).
        """

        return self.data.get('v320', [{'_': None}])[0]['_']

    @property
    def previous_title(self):
        """
        This method retrieves the previous journal title of the given article,
        if it exists.
        This method deals with the legacy fields (610).
        """

        return self.data.get('v610', [{'_': None}])[0]['_']

    @property
    def title(self):
        """
        This method retrieves the journal_title of the given article,
        if it exists.
        This method deals with the legacy fields (100).
        """

        return self.data.get('v100', [{'_': None}])[0]['_']

    @property
    def publisher_country(self):
        """
        This method retrieves the publisher country of journal.
        This method return a tuple: ('US', u'United States'), otherwise
        return None.
        """
        if 'v310' not in self.data:
            return None

        country_code = self.data.get('v310', [{'_': None}])[0]['_']
        country_name = iso3166.COUNTRY_CODES_ALPHA_2.get(country_code, {'name': None})['name']

        if not country_code or not country_name:
            return None

        return (country_code, country_name)

    @property
    def subtitle(self):
        """
        This method retrieves the journal subtitle.
        This method deals with the legacy fields (v110).
        """

        return self.data.get('v110', [{'_': None}])[0]['_']

    @property
    def fulltitle(self):
        """
        This method retrieves the join of the journal title plus the subtitle.
        This method deals with the legacy fields (v100, v110).
        """

        data = []

        data.append(self.title)
        data.append(self.subtitle)

        return ' - '.join([i for i in data if i])

    @property
    def title_nlm(self):
        """
        This method retrieves the journal title registered in the PubMed Central
        of the given article, if it exists.
        This method deals with the legacy fields (421).
        """

        return self.data.get('v421', [{'_': None}])[0]['_']

    @property
    def abbreviated_title(self):
        """
        This method retrieves the journal abbreviated title of the given article, if it exists.
        This method deals with the legacy fields (150).
        """

        return self.data.get('v150', [{'_': None}])[0]['_']

    @property
    def abbreviated_iso_title(self):
        """
        This method retrieves the journal abbreviated title of the given article, if it exists.
        This method deals with the legacy fields (151).
        """

        return self.data.get('v151', [{'_': None}])[0]['_']

    @property
    def acronym(self):
        """
        This method retrieves the journal_acronym of the given article,
        if it exists.
        This method deals with the legacy fields (68).
        """

        return self.data.get('v68', [{'_': None}])[0]['_']

    @property
    def periodicity(self):
        """
        This method retrieves the journal_acronym of the given article,
        if it exists.
        This method deals with the legacy fields (380).
        """

        per = self.data.get('v380', [{'_': None}])[0]['_']

        per = per.upper() if per else None

        if per is None:
            return None

        return (per, choices.periodicity.get(per, per))

    @property
    def periodicity_in_months(self):
        """
        This method retrieves the journal_acronym of the given article,
        if it exists.
        This method deals with the legacy fields (380).
        """

        per = self.data.get('v380', [{'_': None}])[0]['_']

        per = per.upper() if per else None

        return choices.periodicity_in_months.get(per, per)

    @property
    def status_history(self):
        """
        This method retrieves the journal status of the given journal,
        if it exists.
        This method deals with the legacy fields (51) and retrieve a list of
        statuses sorted ascending according to the date of the status change.
        """
        history = []

        if not 'v51' in self.data:
            return [(self.creation_date, choices.journal_status.get(self.data['v50'][0]['_'].lower(), 'inprogress'), '')]

        for item in self.data['v51']:

            history.append(
                (
                    tools.get_date(item['a']),
                    choices.journal_status.get(item['b'].lower(), 'inprogress'),
                    ''
                )
            )

            if 'c' in item and 'd' in item:
                history.append(
                    (
                        tools.get_date(item['c']),
                        choices.journal_status.get(item['d'].lower(), 'inprogress'),
                        item.get('e', 'suspended-by-committee') if item['d'].lower() == 's' else ''
                    )
                )

        return sorted(history)

    @property
    def current_status(self):
        """
        Fast track to get the current_status.
        """

        last_change = self.status_history[-1][0]

        same_date_statuses = [i[1] for i in self.status_history if i[0] == last_change]

        if len(same_date_statuses) == 1:
            return same_date_statuses[0]

        return choices.journal_status.get(self.data['v50'][0]['_'].lower(), 'inprogress')

    @property
    def creation_date(self):
        """
        This method retrieves the creation date of the given journal, if it exists.
        This method deals with the legacy fields (940).
        """

        return self.data.get("created_at", tools.get_date(self.data['v940'][0]['_']))

    @property
    def update_date(self):
        """
        This method retrieves the update date of the given journal, if it exists.
        This method deals with the legacy fields (941).
        """

        return self.data.get("updated_at", tools.get_date(self.data['v941'][0]['_']))

    @property
    def processing_date(self):
        """
        This method retrieves the update date of the given journal, if it exists.
        This method deals with the legacy fields (941).
        """

        return self.data.get("processing_date", tools.get_date(self.data['v941'][0]['_']))

    @property
    def mission(self):
        """
        This method retrieves the mission of journal.
        This method deals with the legacy fields (901).

        Return a dict like this:
            {
            "es": "La missión es..",
            "pt": "A missão é.. ",
            "en": "The mission is"
            }

        """
        if 'v901' not in self.data:
            return None

        missions = {}
        for mission in self.data.get('v901', []):
            if 'l' in mission and '_' in mission:
                missions[mission['l']] = mission['_']

        if not missions:
            return None

        return missions

    @property
    def copyrighter(self):
        """
        This method retrieves the journal copyrighter of the given journal,
        if it exists.

        This method deals with the legacy fields (v62).
        """
        return self.data.get('v62', [{'_': None}])[0]['_']

    @property
    def other_titles(self):
        """
        This method retrieves the other titles of the given journal,
        if it exists.

        Return a list: ['Physical Therapy Movement',
                        'Revista de fisioterapia da PUC-PR']
        """
        if 'v240' not in self.data:
            return None

        return [title['_'] for title in self.data.get('v240') if '_' in title and title['_'] != ""]

    @property
    def sponsors(self):
        """
        This method retrieves the journal sponsors of the given journal,
        if it exists.

        There method clean empty 140 field.
        """
        if 'v140' not in self.data:
            return None

        sponsors = self.data.get('v140')

        return [sponsor['_'] for sponsor in sponsors if '_' in sponsor and sponsor['_'] != ""]


class Article(object):

    def __init__(self, data, iso_format=None):
        """
        Create an Aricle object given a isis2json type 3 SciELO document.

        Keyword arguments:
        iso_format -- the language iso format for methods that retrieve content
        identified by language.
        ['iso 639-2', 'iso 639-1', None]
        """

        if not iso_format in allowed_formats:
            raise ValueError('Language format not allowed ({0})'.format(iso_format))

        self._iso_format = iso_format
        self.data = data
        self.print_issn = None
        self.electronic_issn = None
        self._journal = None
        self._issue = None
        self._citations = None

    def bibliographic_legends(self, language='en'):

        legends = {}
        legends['descriptive_format'] = formatter.descriptive_format(
            self.journal.title,
            self.journal.abbreviated_title,
            self.publication_date,
            self.issue.volume,
            self.issue.number,
            self.start_page,
            self.end_page,
            self.elocation,
            (self.issue.supplement_volume or '') + (self.issue.supplement_number or ''),
            language
            )
        legends['descriptive_html_format'] = formatter.descriptive_html_format(
            self.journal.title,
            self.journal.abbreviated_title,
            self.publication_date,
            self.issue.volume,
            self.issue.number,
            self.start_page,
            self.end_page,
            self.elocation,
            (self.issue.supplement_volume or '') + (self.issue.supplement_number or ''),
            language
            )

        return legends

    @property
    def issue(self):

        if 'issue' in self.data:
            self._issue = self._issue or Issue(self.data['issue'], iso_format=self._iso_format)
        else:
            msg = 'Issue metadata not found for the document %s' % self.publisher_id
            raise UnavailableMetadataException(msg)

        return self._issue

    @property
    def journal(self):

        if 'title' in self.data:
            self._journal = self._journal or Journal(self.data['title'], iso_format=self._iso_format)
        else:
            msg = 'Journal metadata not found for the document %s' % self.publisher_id
            raise UnavailableMetadataException(msg)

        return self._journal

    @property
    def order(self):

        return self.data['article'].get('v121', [{'_': None}])[0]['_']

    @property
    def permissions(self):
        data = None

        if 'license' in self.data:
            data = {}
            data['text'] = tools.creative_commons_text(self.data['license'])
            data['url'] = 'http://creativecommons.org/licenses/%s/' % self.data['license']
            data['id'] = self.data['license']

            return data

        if 'v540' in self.data['article']:
            for dlicense in self.data['article']['v540']:
                if not 't' in dlicense:
                    continue

                license_url = LICENSE_REGEX.findall(dlicense['t'])
                if len(license_url) == 0:
                    continue

                license_id = LICENSE_CREATIVE_COMMONS.findall(license_url[0])

                if len(license_id) == 0:
                    continue

                data = {}
                data['text'] = tools.creative_commons_text(license_id[0]) or html_decode(dlicense['t'])
                data['url'] = license_url[0]
                data['id'] = license_id[0]

                if 'l' in dlicense and dlicense['l'] == 'en':
                    break
        else:
            data = self.journal.permissions

        return data

    @property
    def is_ahead_of_print(self):

        warnings.warn("deprecated, use issue.is_ahead_of_print", DeprecationWarning)

        return self.issue.is_ahead_of_print

    def original_section(self, iso_format=None):

        if not 'section' in self.data:
            return None

        return self.data['section'].get(self.original_language(iso_format), None)

    def translated_section(self, iso_format=None):

        if not 'section' in self.data:
            return None

        return {k: v for k, v in self.data['section'].items() if k != self.original_language(iso_format)}

    @property
    def section(self):
        """
        This method retrieves the section code for the given article.
        This method deals with the fields (section).
        """

        section = self.data.get('section', None)

        if section:
            return section

        return self.issue.sections.get(self.section_code or '', None) if self.issue.sections else None


    @property
    def section_code(self):
        """
        This method retrieves the section code for the given article.
        This method deals with the fields (v49).
        """

        section = self.data['article'].get('v49', [{'_': None}])[0]['_']

        if section == 'nd':
            return None

        return section

    def xml_languages(self, iso_format=None):
        """
        This method retrieves the languages of the fulltext versions available in XML
        for the given article. This method deals with the fields (v601).
        v601: Field that extracts the fulltext languages from translations in the XML files
        """

        if 'v601' in self.data['article']:
            return [i['_'] for i in self.data['article']['v601']]

    @property
    def issue_label(self):
        """
        This method retrieves the issue label. A combined value that describes
        the entire issue label. Ex: v20n2, v20spe1, etc.
        """

        warnings.warn("deprecated, use issue.label", DeprecationWarning)

        return self.issue.label

    @property
    def assets_code(self):
        """
        This method retrieves the issue label available in the field v4. The
        path to the document assets is build with this code.
        ex: /pdf/[journal_acronym]/[assets_code]/[file_code]
        """

        return self.data['article'].get('v4', [{'_': None}])[0]['_']

    def fulltexts(self, iso_format=None):

        if 'fulltexts' in self.data:
            return self.data['fulltexts']

        original_pdf = 'http://%s/pdf/%s/%s/%s.pdf' % (
            self.scielo_domain,
            self.journal.acronym.lower(),
            self.assets_code,
            self.file_code()
        )

        ol = self.original_language(iso_format=iso_format)
        fulltexts = {
            'html': {
                ol: self.html_url(language=ol)
            },
            'pdf': {
                ol: original_pdf
            }
        }

        return fulltexts

    def original_html(self, iso_format=None):

        fmt = iso_format or self._iso_format

        for language, body in self.data.get('body', {}).items():
            if language == self.original_language(iso_format=fmt):
                return body

    def translated_htmls(self, iso_format=None):

        fmt = iso_format or self._iso_format

        if not 'body' in self.data:
            return None

        translated_bodies = {}
        for language, body in self.data.get('body', {}).items():
            if language != self.original_language(iso_format=fmt):
                translated_bodies[language] = body

        if len(translated_bodies) == 0:
            return None

        return translated_bodies

    def languages(self, show_urls=False, iso_format=None):
        """
        This method retrieves the languages of the fulltext versions available
        for the given article. This method deals with the fields (fulltexts and
        v40).
        """

        languages = set()

        if 'fulltexts' in self.data:

            if 'pdf' in self.data['fulltexts']:
                for lang in self.data['fulltexts']['pdf'].keys():
                    languages.add(lang)

            if 'html' in self.data['fulltexts']:
                for lang in self.data['fulltexts']['html'].keys():
                    languages.add(lang)

        languages.add(self.original_language(iso_format=iso_format))

        if len(languages) > 0:
            return [i for i in languages]

    def original_language(self, iso_format=None):
        """
        This method retrieves the original language of the given article.
        This method deals with the legacy fields (40).
        """

        fmt = self._iso_format if not iso_format else iso_format

        return tools.get_language(self.data['article']['v40'][0]['_'], fmt)

    @property
    def collection_name(self):
        """
        This method retrieves the collection name of the given article,
        if it exists.
        """
        return choices.collections.get(
            self.collection_acronym,
            [u'Undefined: %s' % self.collection_acronym, '']
        )[0]

    @property
    def collection_acronym(self):
        """
        This method retrieves the collection of the given article,
        if it exists.
        The subject areas are based on the journal subject areas.
        This method deals with the legacy fields (v992) and the
        new field (collection), the field collection is priorized.
        """
        if 'collection' in self.data:
            return self.data['collection']

        if 'v992' in self.data['article']:
            if isinstance(self.data['article']['v992'], list):
                return self.data['article']['v992'][0]['_']
            else:
                return self.data['article']['v992']

        if 'v992' in self.data['title']:
            if isinstance(self.data['title']['v992'], list):
                return self.data['title']['v992'][0]['_']
            else:
                return self.data['title']['v992']

    @property
    def data_model_version(self, fullpath=False):
        """
        This method retrieves the document version
        This method deals with the legacy fields (120).
        """
        if 'xml' in self.data['article'].get('v120', [{'_': ''}])[0]['_'].lower():
            return 'xml'

        return 'html'

    def file_code(self, fullpath=False):
        """
        This method retrieves the file code for the pdf and html files stored
        in the file system.
        This method deals with the legacy fields (702).
        """
        if fullpath == True and 'v702' in self.data['article']:
            return self.data['article']['v702'][0]['_']

        if 'v702' in self.data['article']:
            splited = self.data['article']['v702'][0]['_'].replace('/', '\\').split('\\')
            filename = splited[-1].split('.')[0]
            return filename

    @property
    def publication_date(self):
        """
        This method retrieves the publication date of the given article, if it exists.
        This method deals with the legacy fields (65) and (223).
        65 represents the issue date
        223 represents the article publication date
        """

        if 'v223' in self.data['article']:
            return tools.get_date(self.data['article']['v223'][0]['_'])

        return tools.get_date(self.data['article']['v65'][0]['_'])

    @property
    def processing_date(self):
        """
        This method retrieves the processing date of the given article, if it exists.
        This method deals with the legacy fields (91).
        """

        pdate = self.data.get(
            'processing_date',
            self.data['article'].get('v91', [{'_': ''}])[0]['_']
        )

        if not pdate:
            return None

        return tools.get_date(pdate.replace('-', '')) if pdate else None

    @property
    def update_date(self):
        """
        This method retrieves the update date of the given article, if it exists.
        If not it will retrieve de update date.
        This method deals with the legacy fields (91) and new field updated_at.
        """

        updated_at = self.data.get(
            'updated_at',
            self.data['article'].get('v91', [{'_': ''}])[0]['_']
        )

        if not updated_at:
            update_at = self.creation_date

        return tools.get_date(updated_at.replace('-', '')) if updated_at else None

    @property
    def creation_date(self):
        """
        This method retrieves the creation_date date of the given article, if it exists.
        This method deals with the legacy fields (93) and new field created_at.
        """

        created_at = self.data.get(
            'created_at',
            self.data['article'].get('v93', [{'_': ''}])[0]['_']
        )

        return tools.get_date(created_at.replace('-', '')) if created_at else None

    @property
    def receive_date(self):
        """
        This method retrieves the receive date of the given article, if it exist.
        This method deals with the legacy fields (112).
        """
        if 'v112' in self.data['article']:
            return tools.get_date(self.data['article']['v112'][0]['_'])
        return None

    @property
    def acceptance_date(self):
        """
        This method retrieves the acceptance date of the given article, if it exist.
        This method deals with the legacy fields (114).
        """
        if 'v114' in self.data['article']:
            return tools.get_date(self.data['article']['v114'][0]['_'])
        return None

    @property
    def review_date(self):
        """
        This method retrieves the review date of the given article, if it exist.
        This method deals with the legacy fields (116).
        """
        if 'v116' in self.data['article']:
            return tools.get_date(self.data['article']['v116'][0]['_'])
        return None

    @property
    def ahead_publication_date(self):
        """
        This method retrieves the ahead of print date of the given article, if it exist.
        This method deals with the legacy fields (223).
        """
        if 'v223' in self.data['article']:
            return tools.get_date(self.data['article']['v223'][0]['_'])
        return None

    @property
    def contract(self):
        """
        This method retrieves the contract of the given article, if it exists.
        This method deals with the legacy fields (60).
        """
        if 'v60' in self.data['article']:
            return html_decode(self.data['article']['v60'][0]['_'])

    @property
    def project_name(self):
        """
        This method retrieves the project name of the given article, if it exists.
        This method deals with the legacy fields (59).
        """
        if 'v59' in self.data['article']:
            return html_decode(self.data['article']['v59'][0]['_'])

    @property
    def project_sponsor(self):
        """
        This method retrieves the project sponsor of the given article, if it exists.
        This method deals with the legacy fields (58).
        """
        sponsors = []
        if 'v58' in self.data['article']:
            for sponsor in self.data['article']['v58']:
                authordict = {}
                if '_' in sponsor:
                    authordict['orgname'] = html_decode(sponsor['_'])
                if 'd' in sponsor:
                    authordict['orgdiv'] = html_decode(sponsor['d'])

                sponsors.append(authordict)

        if len(sponsors) == 0:
            return None

        return sponsors

    @property
    def start_page_sequence(self):
        """
        This method retrieves the star page sequence of the given article, if it exists.
        This method deals with the legacy fields (14).

        Este metodo atende as seguinte variancias de dados do legado:
        {'v14': [{'f': 10, 'l': 12, 's': 1}]}
        {'v14': [{'f': 10}, {'l': 12}, {'s': 1}]}
        """

        for item in self.data['article'].get('v14', [{}]):
            if 's' in item and item['s'].replace('0', '') != '':
                return item['s']

        data = self.data['article'].get('v14', [{}])[0].get('s', '')

        if data.replace('0', '') != '':
            return data


    @property
    def internal_sequence_id(self):
        """
        This method retrieves the article sequence identification inside a issue.
        This is an internal sequence to uniquely identify the article of an issue.

        This id is not the elocation identification and it do not replaces the
        elocation number in any situation.

        This method deals with the legacy field (121).
        """

        return self.data['article'].get('121', [{'_': 0}])[0]['_']

    @property
    def start_page(self):
        """
        This method retrieves the star page of the given article, if it exists.
        This method deals with the legacy fields (14).

        Este metodo atende as seguinte variancias de dados do legado:
        {'v14': [{'f': 10, 'l': 12}]}
        {'v14': [{'f': 10}, {'l': 12}]}
        """

        for item in self.data['article'].get('v14', [{}]):
            if 'f' in item and item['f'].replace('0', '') != '':
                return item['f']

        data = self.data['article'].get('v14', [{}])[0].get('f', '')

        if data.replace('0', '') != '':
            return html_decode(data)

        # if nothing works until now. we will try once more. It's tested.

        #pages = sorted(self.data['article']['v14'][0]['_'].split('-'))
        pages = sorted(self.data['article'].get('v14', [{}])[0].get('_', '').split('-'))

        return html_decode(pages[0]) if pages[0].replace('0', '') != '' else None

    @property
    def end_page(self):
        """
        This method retrieves the end page of the given article, if it exists.
        This method deals with the legacy fields (14).
        """

        for item in self.data['article'].get('v14', [{}]):
            if 'l' in item and item['l'].replace('0', '') != '':
                return item['l']

        # if nothing works until now. we will try once more. It's tested.

        pages = sorted(self.data['article'].get('v14', [{}])[0].get('_', '').split('-'))

        return html_decode(pages[-1]) if pages[-1].replace('0', '') != '' else None

    @property
    def elocation(self):
        """
        This method retrieves the e-location of the given article.
        This method deals with the legacy fields (14).
        {'v14': [{'f': 10, 'l': 12, 'e': 'eloc'}]}
        {'v14': [{'f': 10}, {'l': 12}, {'e': 'eloc'}]}
        """

        for item in self.data['article'].get('v14', [{}]):
            if 'e' in item and item['e'].replace('0', '') != '':
                return item['e']

    @property
    def doi(self):
        """
        This method retrieves the DOI of the given article, if it exists.
        """
        raw_doi = None

        if 'doi' in self.data:
            raw_doi = self.data['doi']

        if 'v237' in self.data['article']:
            raw_doi = self.data['article']['v237'][0]['_']


        if not raw_doi:
            return None

        doi = DOI_REGEX.findall(raw_doi)

        if len(doi) == 1:
            return doi[0]

    @property
    def publisher_id(self):
        """
        This method retrieves the publisher id of the given article, if it exists.
        This method deals with the legacy fields (880).
        """
        return self.data['article']['v880'][0]['_']

    @property
    def publisher_ahead_id(self):
        """
        This method retrieves the publisher ahead id of the given article, if it exists.
        The ahead id is stored in the field v881 when the Ahead of Print document
        is prometed to an oficial issue, and leave the ahead of print status.
        This method deals with the legacy fields (881).
        """
        return self.data['article'].get('v881', [{'_': None}])[0]['_']

    @property
    def document_type(self):
        """
        This method retrieves the document type of the given article, if it exists.
        This method deals with the legacy fields (71).
        """
        if 'v71' in self.data['article']:
            article_type_code = self.data['article']['v71'][0]['_']
            if article_type_code in choices.article_types:
                return choices.article_types[article_type_code]
            else:
                return choices.article_types['nd']

        return choices.article_types['nd']

    def original_title(self, iso_format=None):
        """
        This method retrieves just the title related with the original language
        of the given article, if it exists.
        This method deals with the legacy fields (12).
        """

        fmt = iso_format or self._iso_format

        if 'v12' in self.data['article']:
            for title in self.data['article']['v12']:
                if 'l' in title:
                    language = tools.get_language(title['l'], fmt)
                    if language == self.original_language(iso_format=fmt):
                        t = title.get('_', '').strip()
                        if not t:
                            t = title.get('t', '').strip()

                        return html_decode(t)

    def translated_titles(self, iso_format=None):
        """
        This method retrieves just the translated titles of the given article, if it exists.
        This method deals with the legacy fields (12).
        """

        fmt = iso_format or self._iso_format

        trans_titles = {}
        if 'v12' in self.data['article']:
            for title in self.data['article']['v12']:
                if 'l' in title:
                    language = tools.get_language(title['l'], fmt)
                    if language != self.original_language(iso_format=fmt):
                        t = title.get('_', '').strip()
                        if not t:
                            t = title.get('t', '').strip()

                        trans_titles.setdefault(
                            html_decode(language),
                            html_decode(t)
                        )

        if len(trans_titles) == 0:
            return None

        return trans_titles

    def original_abstract(self, iso_format=None):
        """
        This method retrieves just the abstract related with the original language
        of the given article, if it exists.
        This method deals with the legacy fields (83).
        """
        fmt = iso_format or self._iso_format

        if 'v83' in self.data['article']:
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    language = tools.get_language(abstract['l'], fmt)
                    if language == self.original_language(iso_format=fmt):
                        return html_decode(abstract['a'])

    def translated_abstracts(self, iso_format=None):
        """
        This method retrieves just the trasnlated abstracts of the given article, if it exists.
        This method deals with the legacy fields (83).
        """
        fmt = iso_format or self._iso_format

        trans_abstracts = {}
        if 'v83' in self.data['article']:
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    language = tools.get_language(abstract['l'], fmt)
                    if language != self.original_language(iso_format=fmt):
                        trans_abstracts.setdefault(
                            html_decode(language),
                            html_decode(abstract['a'])
                        )

        if len(trans_abstracts) == 0:
            return None

        return trans_abstracts

    def abstracts(self, iso_format=None):
        """
        This method retrieves just the trasnlated abstracts of the given article, if it exists.
        This method deals with the legacy fields (83).
        """
        fmt = iso_format or self._iso_format

        trans_abstracts = {}
        if 'v83' in self.data['article']:
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    language = tools.get_language(abstract['l'], fmt)

                    trans_abstracts.setdefault(
                        html_decode(language),
                        html_decode(abstract['a'])
                    )

        if len(trans_abstracts) == 0:
            return None

        return trans_abstracts

    @property
    def authors(self):
        """
        This method retrieves the analytics authors of the given article, if it exists.
        This method deals with the legacy fields (10).
        """
        authors = []
        if 'v10' in self.data['article']:
            for author in self.data['article']['v10']:
                authordict = {}
                if 's' in author:
                    authordict['surname'] = html_decode(author['s'])
                else:
                    authordict['surname'] = ''
                if 'n' in author:
                    authordict['given_names'] = html_decode(author['n'])
                else:
                    authordict['given_names'] = ''
                if 'r' in author:
                    authordict['role'] = html_decode(author['r'])
                if '1' in author:
                    authordict['xref'] = html_decode(author['1'].split(' '))
                if 'k' in author:
                    authordict['orcid'] = html_decode(author['k'])

                authors.append(authordict)

        if len(authors) == 0:
            return None

        return authors

    @property
    def first_author(self):
        """
        This property try do get the first author of the article, otherwise
        returns None.

        :returns: dict with key ``surname``, ``given_names``, ``role`` adn ``xref``.
        """
        if self.authors:
            return self.authors[0]

    @property
    def corporative_authors(self):
        """
        This method retrieves the organizational authors of the given article, if it exists.
        This method deals with the legacy fields (11).
        """
        authors = []
        if 'v11' in self.data['article']:
            for author in self.data['article']['v11']:
                authordict = {}

                if '_' in author:
                    authordict['orgname'] = html_decode(author['_'])
                if 'd' in author:
                    authordict['orgdiv'] = html_decode(author['d'])

                authors.append(authordict)

        if len(authors) == 0:
            return None

        return authors

    @property
    def mixed_affiliations(self):
        """
        This method retrieves the normalized affiliations of the given
        article, if it exists.
        If some document does not have all the affiliations normalized, this
        method will mix the original affiliation data with the normalized data.
        """
        normalized = {}

        if self.affiliations:
            for aff in self.affiliations:
                    normalized[aff['index']] = aff.copy()
                    normalized[aff['index']]['normalized'] = False
                    normalized[aff['index']]['country_iso_3166'] = aff.get('country_iso_3166', '')

        if self.normalized_affiliations:
            for aff in self.normalized_affiliations:
                if not aff['index'] in normalized:
                    continue
                normalized[aff['index']]['normalized'] = True
                normalized[aff['index']]['country'] = aff.get('country', '')
                normalized[aff['index']]['country_iso_3166'] = aff.get('country_iso_3166', '')
                normalized[aff['index']]['institution'] = aff.get('institution', '')
                normalized[aff['index']]['state'] = aff.get('state', '')

        return [v for i, v in normalized.items()]

    @property
    def normalized_affiliations(self):
        """
        This method retrieves the affiliations of the given article, if it exists.
        This method deals with the legacy fields (240).
        """
        affiliations = []
        if 'v240' in self.data['article']:
            for aff in self.data['article']['v240']:
                affdict = {}
                if '_' in aff:
                    if len(aff['_'].strip()) > 0:
                        affdict['institution'] = html_decode(aff['_'])

                        if 'i' in aff:
                            affdict['index'] = aff['i'].upper()
                        else:
                            affdict['index'] = ''

                        if 'p' in aff and html_decode(aff['p']).lower() in iso3166.COUNTRY_CODES_ALPHA_2_FORMS:
                            affdict['country_iso_3166'] = iso3166.COUNTRY_CODES_ALPHA_2_FORMS.get(aff['p'].lower(), '')
                            affdict['country'] = html_decode(iso3166.COUNTRY_CODES_ALPHA_2.get(aff['p'], {'name': html_decode(aff['p'])})['name'])

                        if 's' in aff:
                            affdict['state'] = aff['s']

                        affiliations.append(affdict)

        if len(affiliations) == 0:
            return None

        return affiliations

    @property
    def affiliations(self):
        """
        This method retrieves the affiliations of the given article, if it exists.
        This method deals with the legacy fields (70).
        """
        affiliations = []
        if 'v70' in self.data['article']:
            for aff in self.data['article']['v70']:
                affdict = {}
                affdict['institution'] = html_decode(aff.get('_', ''))
                if 'i' in aff:
                    affdict['index'] = html_decode(aff['i'].upper())
                else:
                    affdict['index'] = ''
                if 'c' in aff:
                    affdict['city'] = html_decode(aff['c'])
                if 's' in aff:
                    affdict['state'] = html_decode(aff['s'])
                if 'p' in aff:
                    affdict['country'] = html_decode(aff['p'])
                    if html_decode(aff['p']).lower() in iso3166.COUNTRY_CODES_ALPHA_2_FORMS:
                        affdict['country_iso_3166'] = iso3166.COUNTRY_CODES_ALPHA_2_FORMS.get(aff['p'].lower(), '')

                if 'p' in aff and 'q' in aff and aff['p'] in iso3166.COUNTRY_CODES_ALPHA_2:
                    affdict['country'] = iso3166.COUNTRY_CODES_ALPHA_2[aff['p']]['name']
                    affdict['country_iso_3166'] = aff['p']

                if 'e' in aff:
                    affdict['email'] = html_decode(aff['e'])
                if 'd' in aff:
                    affdict['division'] = html_decode(aff['d'])
                if '1' in aff:
                    affdict['orgdiv1'] = html_decode(aff['1'])
                if '2' in aff:
                    affdict['orgdiv2'] = html_decode(aff['2'])

                affiliations.append(affdict)

        if len(affiliations) == 0:
            return None

        return affiliations

    @property
    def scielo_domain(self):
        """
        This method retrieves the collection domains of the given article, if it exists.
        This method deals with the legacy fields (69, 690).
        """

        if self.collection_acronym:
            return choices.collections.get(
                self.collection_acronym,
                [u'Undefined: %s' % self.collection_acronym, None]
            )[1] or None

        if 'v690' in self.data['title']:
            return self.data['title']['v690'][0]['_'].replace('http://', '')
        elif 'v69' in self.data['article']:
            return self.data['article']['v69'][0]['_'].replace('http://', '')

    def pdf_url(self, language='en'):
        """
        This method retrieves the pdf url of the given article.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_pdf&pid={1}&lng={2}&tlng={3}".format(
                self.scielo_domain,
                self.publisher_id,
                language,
                language
            )

    def html_url(self, language='en'):
        """
        This method retrieves the html url of the given article.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_arttext&pid={1}&lng={2}&tlng={3}".format(
                self.scielo_domain,
                self.publisher_id,
                language,
                language
            )

    def issue_url(self, language='en'):
        """
        This method retrieves the issue url of the given article.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_issuetoc&pid={1}&lng={2}".format(
                self.scielo_domain,
                self.publisher_id[0:18],
                language
            )

    def keywords(self, iso_format=None):
        """
        This method retrieves the keywords of the given article, if it exists.
        This method deals with the legacy fields (85).
        """
        fmt = iso_format or self._iso_format

        keywords = {}
        if 'v85' in self.data['article']:
            for keyword in self.data['article']['v85']:
                if 'k' in keyword and 'l' in keyword:
                    language = tools.get_language(keyword['l'], fmt)
                    group = keywords.setdefault(html_decode(language), [])
                    group.append(html_decode(keyword['k']))

        if len(keywords) == 0:
            return None

        return keywords

    def any_issn(self, priority=u'electronic'):
        """
        This method retrieves the issn of the given article, acoording to the given priority.
        """
        warnings.warn("deprecated, use journal.any_issn", DeprecationWarning)

        return self.journal.any_issn(priority=priority)

    @property
    def thesis_degree(self):
        """
        This method retrieves the thesis degree of the given document, If it exists.
        This method deals with the legacy fields (51).
        """
        if 'v51' in self.data['article']:
            return html_decode(self.data['article']['v51'][0]['_'])

    @property
    def thesis_organization(self):
        """
        This method retrieves the thesis organization of the given article, if it exists.
        This method deals with the legacy fields (52).
        """

        organizations = []
        if 'v52' in self.data['article']:
            for organization in self.data['article']['v52']:
                org = {}
                if '_' in organization:
                    org = {'name': html_decode(organization['_'])}
                if 'd' in organization:
                    org.update({'division': html_decode(organization['d'])})

                organizations.append(org)

        if len(organizations) > 0:
            return organizations

    @property
    def citations(self):
        """
        This method retrieves a list with all the citation objects of the given article.
        """
        citations = []
        if 'citations' in self.data:
            for citation in self.data['citations']:
                citations.append(Citation(citation))

        if len(citations) > 0:
            return citations


class Citation(object):

    def __init__(self, data):
        self.data = data
        self.publication_type = self._publication_type()

    def _publication_type(self):
        """
        This method retrieves the publication type of the citation.
        """

        if 'v30' in self.data:
            return u'article'
        elif 'v53' in self.data:
            return u'conference'
        elif 'v18' in self.data:
            if 'v51' in self.data:
                return u'thesis'
            else:
                return u'book'
        elif 'v150' in self.data:
            return u'patent'
        elif 'v37' in self.data:
            return u'link'
        else:
            return u'undefined'

    @property
    def start_page(self):
        """
        This method retrieves the start page of the citation.
        This method deals with the legacy fields (514 and 14).
        """

        if 'v514' in self.data:
            return html_decode(self.data['v514'][0].get('f', None))

        if not 'v14' in self.data:
            return None

        return html_decode(self.data['v14'][0]['_'].split('-')[0])

    @property
    def end_page(self):
        """
        This method retrieves the end page of the citation.
        This method deals with the legacy fields (514 and 14).
        """

        if 'v514' in self.data:
            return html_decode(self.data['v514'][0].get('l', None))

        if not 'v14' in self.data:
            return None

        splited = self.data['v14'][0]['_'].split('-')

        if not len(splited) == 2:
            return None

        return html_decode(splited[1])

    @property
    def elocation(self):
        """
        This method retrieves the e-location of the citation.
        This method deals with the legacy fields (514 and 14).
        """

        if 'v514' in self.data:
            return self.data['v514'][0].get('e', None)

        if not 'v14' in self.data:
            return None

        return self.data['v14'][0].get('e', None)

    @property
    def pages(self):
        """
        This method retrieves the start and end page of the citation
        separeted by hipen.
        This method deals with the legacy fields (514 and 14).
        """

        if 'v514' in self.data:
            return '-'.join(sorted([v for v in self.data['v514'][0].values()]))

        if not 'v14' in self.data:
            return None

        return self.data['v14'][0]['_']

    @property
    def index_number(self):
        """
        This method retrieves the index number of the citation. The
        index number represents the original number given in the article.
        """
        if 'v701' in self.data:
            return int(self.data['v701'][0]['_'])

    @property
    def source(self):
        """
        This method retrieves the citation source title. Ex:
        Journal: Journal of Microbiology
        Book: Alice's Adventures in Wonderland
        """
        if self.publication_type == u'article' and 'v30' in self.data:
            return html_decode(self.data['v30'][0]['_'])

        if self.publication_type in [u'book', u'conference'] and 'v18' in self.data:
            return html_decode(self.data['v18'][0]['_'])

    @property
    def chapter_title(self):
        """
        If it is a book citation, this method retrieves a chapter title, if it exists.
        """
        if self.publication_type == u'book' and 'v12' in self.data:
            return html_decode(self.data['v12'][0]['_'])

    @property
    def article_title(self):
        """
        If it is an article citation, this method retrieves the article title, if it exists.
        """
        if self.publication_type == u'article' and 'v12' in self.data:
            return html_decode(self.data['v12'][0]['_'])

    @property
    def thesis_title(self):
        """
        If it is a thesis citation, this method retrieves the thesis title, if it exists.
        """

        if self.publication_type == u'thesis' and 'v18' in self.data:
            return html_decode(self.data['v18'][0]['_'])

    @property
    def conference_title(self):
        if self.publication_type == u'conference' and 'v12' in self.data:
            return html_decode(self.data['v12'][0]['_'])

    @property
    def conference_name(self):
        """
        If it is a conference citation, this method retrieves the conference name, if it exists.
        """

        if self.publication_type == u'conference' and 'v53' in self.data:
            titles = []
            for item in self.data['v53']:
                titles.append(html_decode(item['_']))

            return '; '.join(titles)

    @property
    def link_title(self):
        """
        If it is a link citation, this method retrieves the link title, if it exists.
        """

        if self.publication_type == u'link' and 'v12' in self.data:
            return html_decode(self.data['v12'][0]['_'])

    def title(self):
        """
        This method returns the first title independent of citation type
        """
        type_titles = ['article_title', 'thesis_title', 'conference_title', 'link_title']

        titles = []

        for title in type_titles:
            if getattr(self, title):
                titles.append(getattr(self, title))

        return ', '.join(titles)

    @property
    def conference_sponsor(self):
        """
        If it is a conference citation, this method retrieves the conference sponsor, if it exists.
        The conference sponsor is presented like it is in the citation. (v52)
        """

        if self.publication_type == u'conference' and 'v52' in self.data:
            return html_decode(self.data['v52'][0]['_'])

    @property
    def conference_location(self):
        """
        If it is a conference citation, this method retrieves the conference location, if it exists.
        The conference location is presented like it is in the citation. (v56)
        """

        if self.publication_type == u'conference' and 'v56' in self.data:
            return html_decode(self.data['v56'][0]['_'])

    @property
    def link(self):
        """
        This method retrieves a link, if it is exists.
        """

        if 'v37' in self.data:
            return html_decode(self.data['v37'][0]['_'])

    @property
    def date(self):
        """
        This method retrieves the date, if it is exists, according to the
        reference type
        Se é desejável obter a data de publicação, usar: self.publication_date
        """
        if self.access_date:
            return self.access_date

        if self.thesis_date:
            return self.thesis_date

        if self.conference_date:
            return self.conference_date

        if self.publication_date:
            return self.publication_date

    @property
    def publication_date(self):
        """
        This method retrieves the publication date, if it is exists.
        """
        if 'v65' in self.data:
            return tools.get_date(self.data['v65'][0]['_'])

        if self.thesis_date:
            return self.thesis_date

        if self.conference_date:
            return self.conference_date

    @property
    def access_date(self):
        """
        This method retrieves the access date, if it is exists.
        """
        if self.publication_type == u'link' and 'v110' in self.data:
            return tools.get_date(self.data['v110'][0]['_'])

    @property
    def thesis_date(self):
        """
        This method retrieves the thesis date, if it is exists.
        """
        if self.publication_type == u'thesis' and 'v45' in self.data:
            return tools.get_date(self.data['v45'][0]['_'])

    @property
    def conference_date(self):
        """
        This method retrieves the conference date, if it is exists.
        """
        if self.publication_type == u'conference' and 'v55' in self.data:
            return tools.get_date(self.data['v55'][0]['_'])

    @property
    def edition(self):
        """
        This method retrieves the edition, if it is exists. The citation must
        be a conference or book citation.
        """

        if self.publication_type in [u'conference', u'book']:
            if 'v63' in self.data:
                return html_decode(self.data['v63'][0]['_'])

    @property
    def first_page(self):
        return self.start_page

    @property
    def last_page(self):
        return self.end_page

    @property
    def institutions(self):
        """
        This method retrieves the institutions in the given citation without
        care about the citation type (article, book, thesis, conference, etc).
        """

        institutions = []
        if 'v11' in self.data:
            institutions.append(html_decode(self.data['v11'][0]['_']))
        if 'v17' in self.data:
            institutions.append(html_decode(self.data['v17'][0]['_']))
        if 'v29' in self.data:
            institutions.append(html_decode(self.data['v29'][0]['_']))
        if 'v50' in self.data:
            institutions.append(html_decode(self.data['v50'][0]['_']))
        if 'v58' in self.data:
            institutions.append(html_decode(self.data['v58'][0]['_']))

        if len(institutions) > 0:
            return institutions

    @property
    def issn(self):
        """
        This method retrieves the journal ISSN if it is present in the citation.
        This method deals with the legacy field v35.
        """

        if self.publication_type == 'article':
            return self.data.get('v35', None)


    @property
    def analytic_institution(self):
        """
        This method retrieves the institutions in the given citation. The
        citation must be an article or book citation, if it exists.
        """
        institutions = []
        if self.publication_type in [u'article', u'book'] and 'v11' in self.data:
            if 'v11' in self.data:
                for institution in self.data['v11']:
                    institutions.append(html_decode(self.data['v11'][0]['_']))

        if len(institutions) > 0:
            return institutions

    @property
    def monographic_institution(self):
        """
        This method retrieves the institutions in the given citation. The
        citation must be a book citation, if it exists.
        """
        institutions = []
        if self.publication_type == u'book' and 'v17' in self.data:
            if 'v17' in self.data:
                for institution in self.data['v17']:
                    institutions.append(html_decode(self.data['v17'][0]['_']))

        if len(institutions) > 0:
            return institutions

    @property
    def sponsor(self):
        """
        This method retrieves the sponsors in the given citation, if it exists.
        """
        sponsors = []
        if 'v58' in self.data:
            for sponsor in self.data['v58']:
                sponsors.append(html_decode(self.data['v58'][0]['_']))

        if len(sponsors) > 0:
            return sponsors

    @property
    def editor(self):
        """
        This method retrieves the editors in the given citation, if it exists.
        """

        editors = []
        if 'v29' in self.data:
            for editor in self.data['v29']:
                editors.append(html_decode(self.data['v29'][0]['_']))

        if len(editors) > 0:
            return editors

    @property
    def thesis_institution(self):
        """
        This method retrieves the thesis institutions in the given citation, if
        it exists.
        """

        institutions = []
        if 'v50' in self.data:
            for institution in self.data['v50']:
                institutions.append(html_decode(self.data['v50'][0]['_']))

        if len(institutions) > 0:
            return institutions

    @property
    def comment(self):
        """
        This method retrieves the citation comment, mainly used in link citation
        if exists (v61).
        """

        if 'v61' in self.data:
            return self.data['v61'][0]['_']

        if self.publication_type == u'link' and 'v37' in self.data:
            return u'Available at: <ext-link ext-link-type="uri" ns0:href="{0}">{1}</ext-link>'.format(self.link, self.link)

    @property
    def mixed_citation(self):

        if 'mixed' in self.data:
            data = html_decode(self.data['mixed']).strip()
            cleaned = CLEANUP_MIXED_CITATION.sub('', data)
            for pattern, value in REPLACE_TAGS_MIXED_CITATION:
                cleaned = pattern.sub(value, cleaned)
            return cleaned

        if 'v704' in self.data:
            data = html_decode(self.data['v704'][0]['_'].replace('<mixed-citation>', '').replace('</mixed-citation>', ''))
            cleaned = CLEANUP_MIXED_CITATION.sub('', data)
            for pattern, value in REPLACE_TAGS_MIXED_CITATION:
                cleaned = pattern.sub(value, cleaned)
            return cleaned

    @property
    def link_access_date(self):
        """
        This method retrieves the citation access date, mainly used in link citation
        if exists (v109).
        """

        if 'v109' in self.data:
            return self.data['v109'][0]['_']

    @property
    def issn(self):
        """
        This method retrieves the journal issn, if it is exists. The citation
        must be an article citation.
        """

        if self.publication_type == u'article' and 'v35' in self.data:
            return self.data['v35'][0]['_']

    @property
    def isbn(self):
        """
        This method retrieves the book isbn, if it is exists. The citation must
        be a book citation.
        """

        if self.publication_type == u'book' and 'v69' in self.data:
            return self.data['v69'][0]['_']

    @property
    def volume(self):
        """
        This method retrieves the book our journal volume number, if it exists.
        The citation must be a book our an article citation.
        """

        if self.publication_type in [u'article', u'book']:
            if 'v31' in self.data:
                return self.data['v31'][0]['_']

    @property
    def issue(self):
        """
        This method retrieves the journal issue number, if it exists. The
        citation must be an article citation.
        """

        if self.publication_type in u'article' and 'v32' in self.data:
            return self.data['v32'][0]['_']

    @property
    def issue_title(self):
        """
        This method retrieves the issue title, if it exists. The citation must
        be an article citation.
        """

        if self.publication_type in u'article' and 'v33' in self.data:
            return html_decode(html_decode(html_decode(self.data['v33'][0]['_'])))

    @property
    def issue_part(self):
        """
        This method retrieves the issue part, if it exists. The citation must
        be an article citation.
        """

        if self.publication_type in u'article' and 'v34' in self.data:
            return html_decode(html_decode(self.data['v34'][0]['_']))

    @property
    def doi(self):
        """
        This method retrieves the citation DOI number, if it exists.
        """

        if 'v237' in self.data:
            return self.data['v237'][0]['_']

    @property
    def authors(self):

        aa = self.analytic_authors or []
        ma = self.monographic_authors or []
        return aa + ma

    @property
    def analytic_authors(self):
        """
        This method retrieves the authors of the given citation. These authors
        may correspond to an article, book analytic, link or thesis.
        """

        authors = []
        if 'v10' in self.data:
            for author in self.data['v10']:
                authordict = {}
                if 's' in author:
                    authordict['surname'] = html_decode(author['s'])
                if 'n' in author:
                    authordict['given_names'] = html_decode(author['n'])
                if 's' in author or 'n' in author:
                    authors.append(authordict)

        if len(authors) > 0:
            return authors

    @property
    def monographic_authors(self):
        """
        This method retrieves the authors of the given book citation. These authors may
        correspond to a book monography citation.
        """

        authors = []
        if 'v16' in self.data:
            for author in self.data['v16']:
                authordict = {}
                if 's' in author:
                    authordict['surname'] = html_decode(author['s'])
                if 'n' in author:
                    authordict['given_names'] = html_decode(author['n'])
                if 's' in author or 'n' in author:
                    authors.append(authordict)

        if len(authors) > 0:
            return authors

    @property
    def first_author(self):
        """
        This property retrieves the first author of the given citation,
        independent of citation type.

        :returns: dict with keys ``given_names`` and ``surname``
        """

        if self.authors:
            return self.authors[0]
        elif self.monographic_authors:
            return self.monographic_authors[0]

    @property
    def serie(self):
        """
        This method retrieves the series title. The serie title must be in a book, article or
        conference citation.
        """
        docs = [u'conference', u'book', u'article']
        if self.publication_type in docs and 'v25' in self.data:
            return html_decode(self.data['v25'][0]['_'])

    @property
    def publisher(self):
        """
        This method retrieves the publisher name, if it exists.
        """
        if 'v62' in self.data:
            return html_decode(self.data['v62'][0]['_'])

    @property
    def publisher_address(self):
        """
        This method retrieves the publisher address, if it exists.
        """
        address = []
        if 'v66' in self.data:
            address.append(html_decode(self.data['v66'][0]['_']))
            if 'e' in self.data['v66'][0]:
                address.append(html_decode(self.data['v66'][0]['e']))

        if 'v67' in self.data:
            address.append(html_decode(self.data['v67'][0]['_']))

        if len(address) > 0:
            return"; ".join(address)
