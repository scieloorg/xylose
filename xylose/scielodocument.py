# encoding: utf-8
import sys
from functools import wraps
import warnings
import re

try:  # Keep compatibility with python 2.7
    from html import unescape
except ImportError:
    from HTMLParser import HTMLParser

from . import choices
from . import tools

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
        This method deal with the legacy datamodel fields (935, 400, 35) where:
        """
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

        if 'v541' in self.data and self.data['v541'][0]['_'].lower() == 'nd':
            return None

        if 'v541' in self.data:
            if len(self.data['v541'][0]['_'].lower().split('/')) == 1:
                license = '%s/4.0' % self.data['v541'][0]['_'].lower()
            else:
                license = self.data['v541'][0]['_'].lower()
            data = {}
            data['text'] = None
            data['url'] = 'http://creativecommons.org/licenses/%s/' % license
            data['id'] = license
            return data

        if  'v540' in self.data:
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
                data['text'] = dlicense['t']
                data['url'] = license_url[0]
                data['id'] = license_id[0]

                if 'l' in dlicense and dlicense['l'] == 'en':
                    break

        return data

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
        if not 'v400' in self.data:
            return None

        return self.data['v400'][0]['_']

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
    def subject_areas(self):
        """
        This method retrieves the subject areas of the given article,
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
    def abbreviated_title(self):
        """
        This method retrieves the journal abbreviated title of the given article, if it exists.
        This method deals with the legacy fields (150).
        """
        if 'v150' in self.data:
            return self.data['v150'][0]['_']

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
        """

        if 'v480' in self.data:
            return self.data['v480'][0]['_']

    @property
    def publisher_loc(self):
        """
        This method retrieves the publisher localization of the given article,
        if it exists.
        This method deals with the legacy fields (490).
        """

        if 'v490' in self.data:
            return self.data['v490'][0]['_']

    @property
    def title(self):
        """
        This method retrieves the journal_title of the given article,
        if it exists.
        This method deals with the legacy fields (100).
        """

        if 'v100' in self.data:
            return self.data['v100'][0]['_']

    @property
    def title_nlm(self):
        """
        This method retrieves the journal title registered in the PubMed Central
        of the given article, if it exists.
        This method deals with the legacy fields (421).
        """

        if 'v421' in self.data:
            return self.data['v421'][0]['_']

    @property
    def acronym(self):
        """
        This method retrieves the journal_acronym of the given article,
        if it exists.
        This method deals with the legacy fields (68).
        """

        if 'v68' in self.data:
            return self.data['v68'][0]['_'].lower()

    @property
    def periodicity(self):
        """
        This method retrieves the journal_acronym of the given article,
        if it exists.
        This method deals with the legacy fields (380).
        """

        per = self.data.get('v380', [{'_': None}])[0]['_']

        per = per.upper() if per else None

        return choices.periodicity.get(per, per)

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
            return [(self.creation_date, choices.journal_status.get(self.data['v50'][0]['_'].lower(), 'inprogress'))]

        for item in self.data['v51']:

            history.append(
                (
                    tools.get_date(item['a']),
                    choices.journal_status.get(item['b'].lower(), 'inprogress')
                )
            )

            if 'c' in item and 'd' in item:
                history.append(
                    (
                        tools.get_date(item['c']),
                        choices.journal_status.get(item['d'].lower(), 'inprogress')
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

        return tools.get_date(self.data['v940'][0]['_'])

    @property
    def update_date(self):
        """
        This method retrieves the update date of the given journal, if it exists.
        This method deals with the legacy fields (941).
        """

        return tools.get_date(self.data['v941'][0]['_'])

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
        self._citations = None

    @property
    def journal(self):

        if 'title' in self.data:
            self._journal = self._journal or Journal(self.data['title'], iso_format=self._iso_format)

        return self._journal

    @property
    def order(self):

        return self.data['article'].get('v121', [{'_': None}])[0]['_']

    @property
    def permissions(self):
        data = None

        if 'license' in self.data:
            data = {}
            data['text'] = None
            data['url'] = 'http://creativecommons.org/licenses/%s/' % self.data['license']
            data['id'] = self.data['license']

            return data


        if  'v540' in self.data['article']:
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
                data['text'] = html_decode(dlicense['t'])
                data['url'] = license_url[0]
                data['id'] = license_id[0]

                if 'l' in dlicense and dlicense['l'] == 'en':
                    break
        else:
            data = self.journal.permissions

        return data

    @property
    def is_ahead_of_print(self):

        if self.issue and 'ahead' in self.issue.lower():
            return True

        return False

    def original_section(self, iso_format=None):

        if not 'section' in self.data:
            return None
        
        return self.data['section'].get(self.original_language(iso_format), None)

    def translated_section(self, iso_format=None):
        
        if not 'section' in self.data:
            return None

        return {k:v for k, v in self.data['section'].items() if k != self.original_language(iso_format)}

    @property
    def section(self):
        """
        This method retrieves the section code for the given article.
        This method deals with the fields (section).
        """

        if 'section' in self.data:

            return self.data['section']

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

        if 'v4' in self.data['article']:
            return self.data['article']['v4'][0]['_']


    def fulltexts(self, iso_format=None):

        if 'fulltexts' in self.data:
            return self.data['fulltexts']

        original_pdf = 'http://%s/pdf/%s/%s/%s.pdf' % (
            self.scielo_domain,
            self.journal.acronym.lower(),
            self.issue_label,
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

    @property
    def scielo_issn(self):
        """
        This method retrieves the issn used as id in SciELO.
        This method deals with the legacy fields (v400).
        """
        warnings.warn("deprecated, use journal.scielo_issn", DeprecationWarning)

        return self.journal.scielo_issn

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
    def subject_areas(self):
        """
        This method retrieves the subject areas of the given article,
        if it exists.
        The subject areas are based on the journal subject areas.
        This method deals with the legacy fields (441).
        """
        warnings.warn("deprecated, use journal.subject_areas", DeprecationWarning)

        return html_decode(self.journal.subject_areas)

    @property
    def wos_subject_areas(self):
        """
        This method retrieves the Wob of Sciences subject areas of the given
        journal, if it exists.
        This method deals with the legacy fields (854).
        """
        warnings.warn("deprecated, use journal.wos_subject_areas", DeprecationWarning)

        return html_decode(self.journal.wos_subject_areas)

    @property
    def wos_citation_indexes(self):
        """
        This method retrieves the Wob of Sciences Citation Indexes of the given
        journal, if it exists.
        This method deals with the legacy fields (851).
        """
        warnings.warn("deprecated, use journal.wos_citation_index", DeprecationWarning)

        return html_decode(self.journal.wos_citation_indexes)

    @property
    def publisher_name(self):
        """
        This method retrieves the publisher name of the given article,
        if it exists.
        This method deals with the legacy fields (480).
        """
        warnings.warn("deprecated, use journal.publisher_name", DeprecationWarning)

        return html_decode(self.journal.publisher_name)

    @property
    def publisher_loc(self):
        """
        This method retrieves the publisher localization of the given article,
        if it exists.
        This method deals with the legacy fields (490).
        """
        warnings.warn("deprecated, use journal.publisher_loc", DeprecationWarning)

        return html_decode(self.journal.publisher_loc)

    @property
    def journal_title(self):
        """
        This method retrieves the journal_title of the given article,
        if it exists.
        This method deals with the legacy fields (100).
        """
        warnings.warn("deprecated, use journal.title", DeprecationWarning)

        return html_decode(self.journal.title)

    @property
    def journal_acronym(self):
        """
        This method retrieves the journal_acronym of the given article,
        if it exists.
        This method deals with the legacy fields (68).
        """
        warnings.warn("deprecated, use journal.acronym", DeprecationWarning)

        return self.journal.acronym

    @property
    def data_model_version(self, fullpath=False):
        """
        This method retrieves the document version
        This method deals with the legacy fields (601).
        """
        if 'v601' in self.data['article']:
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
        This method deals with the legacy fields (65).
        """

        return tools.get_date(self.data['article']['v65'][0]['_'])

    @property
    def processing_date(self):
        """
        This method retrieves the processing date of the given article, if it exists.
        This method deals with the legacy fields (91).
        """
        warnings.warn("deprecated, use article.processing_date", DeprecationWarning)

        pdate = self.data.get(
            'processing_date',
            self.data['article'].get('v91', [{'_': ''}])[0]['_']
        ).replace('-','')

        return tools.get_date(pdate) if pdate else None

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
        ).replace('-','')

        if not updated_at:
            return self.creation_date

        return tools.get_date(updated_at) if updated_at else None

    @property
    def creation_date(self):
        """
        This method retrieves the creation_date date of the given article, if it exists.
        This method deals with the legacy fields (93) and new field created_at.
        """

        created_at = self.data.get(
            'created_at', 
            self.data['article'].get('v93', [{'_': ''}])[0]['_']
        ).replace('-','')

        return tools.get_date(created_at) if created_at else None

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
    def volume(self):
        """
        This method retrieves the issue volume of the given article, if it exists.
        This method deals with the legacy fields (31).
        """
        if 'v31' in self.data['article']:
            return self.data['article']['v31'][0]['_']

    @property
    def issue(self):
        """
        This method retrieves the issue number of the given article, if it exists.
        This method deals with the legacy fields (32).
        """
        if 'v32' in self.data['article']:
            return self.data['article']['v32'][0]['_']

    @property
    def supplement_volume(self):
        """
        This method retrieves the supplement of volume of the given article, if it exists.
        This method deals with the legacy fields (131).
        """
        if 'v131' in self.data['article']:
            return self.data['article']['v131'][0]['_']

    @property
    def supplement_issue(self):
        """
        This method retrieves the supplement number of the given article, if it exists.
        This method deals with the legacy fields (132).
        """
        if 'v132' in self.data['article']:
            return self.data['article']['v132'][0]['_']

    @property
    def start_page(self):
        """
        This method retrieves the star page of the given article, if it exists.
        This method deals with the legacy fields (14).
        """
        if 'v14' in self.data['article']:
            for item in self.data['article']['v14']:
                if 'f' in item:
                    return item['f']

            # if nothing works until now. we will try once more. It's tested.

            pages = sorted(self.data['article']['v14'][0]['_'].split('-'))

            return pages[0] or None

    @property
    def end_page(self):
        """
        This method retrieves the end page of the given article, if it exists.
        This method deals with the legacy fields (14).
        """
        if 'v14' in self.data['article']:
            for item in self.data['article']['v14']:
                if 'l' in item:
                    return item['l']

            # if nothing works until now. we will try once more. It's tested.

            pages = sorted(self.data['article']['v14'][0]['_'].split('-'))

            return pages[-1] or None

    @property
    def elocation(self):
        """
        This method retrieves the e-location of the given article.
        This method deals with the legacy fields (14).
        """

        if not 'v14' in self.data['article']:
            return None

        return self.data['article']['v14'][0].get('e', None)


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
    def journal_abbreviated_title(self):
        """
        This method retrieves the journal abbreviated title of the given article, if it exists.
        This method deals with the legacy fields (30).
        """

        warnings.warn("deprecated, use journal.abbreviated_title", DeprecationWarning)

        return self.journal.abbreviated_title

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

        if self.normalized_affiliations:
            for aff in self.normalized_affiliations:
                if not aff['index'] in normalized:
                    continue
                normalized[aff['index']]['normalized'] = True
                normalized[aff['index']]['country'] = aff.get('country', '')
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

                        if 'p' in aff and aff['p'] in choices.ISO_3166:
                            affdict['country'] = choices.ISO_3166[aff['p']]
                            if aff['p'] in choices.ISO_3166:
                                affdict['country_iso_3166'] = aff['p']

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

    def journal_url(self, language='en'):
        """
        This method retrieves the journal url of the given article.
        """
        warnings.warn("deprecated, use journal.url", DeprecationWarning)

        return self.journal.url(language=language)

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
            return self.data['v514'][0].get('f', None)

        if not 'v14' in self.data:
            return None

        return self.data['v14'][0]['_'].split('-')[0]

    @property
    def end_page(self):
        """
        This method retrieves the end page of the citation.
        This method deals with the legacy fields (514 and 14).
        """

        if 'v514' in self.data:
            return self.data['v514'][0].get('l', None)

        if not 'v14' in self.data:
            return None

        splited = self.data['v14'][0]['_'].split('-')

        if not len(splited) == 2:
            return None

        return splited[1]

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
            return self.data['v37'][0]['_']

    @property
    def date(self):
        """
        This method retrieves the citation date, if it is exists.
        """

        if self.publication_type == u'link' and 'v110' in self.data:
            return tools.get_date(self.data['v110'][0]['_'])

        if self.publication_type == u'thesis' and 'v45' in self.data:
            return tools.get_date(self.data['v45'][0]['_'])

        if self.publication_type == u'conference' and 'v55' in self.data:
            return tools.get_date(self.data['v55'][0]['_'])

        if 'v65' in self.data:
            return tools.get_date(self.data['v65'][0]['_'])

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
        if 'v704' in self.data:
            return html_decode(self.data['v704'][0]['_'].replace('<mixed-citation>', '').replace('</mixed-citation>', ''))

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
        """
        This method retrieves the authors of the given citation. These authors
        may correspond to an article, book analytic, link or thesis.
        """
        docs = [u'article', u'book', u'link', u'thesis']
        authors = []
        if self.publication_type in docs and 'v10' in self.data:
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
        docs = [u'book', u'thesis']
        authors = []
        if self.publication_type in docs and 'v16' in self.data:
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
