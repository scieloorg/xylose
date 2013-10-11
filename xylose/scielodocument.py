# encoding: utf-8
from . import choices
from . import tools

allowed_formats = ['iso 639-2', 'iso 639-1', None]

class Article(object):

    def __init__(self, data, iso_format=None):
        """
        Create an Aricle object given a isis2json type 3 SciELO document.

        Keyword arguments:
        iso_format -- the language iso format for methods that retrieve content identified by language.
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
        # ISSN and Other Complex Stuffs from the old version
        if not 'v935' in self.data['title']:  # Old fashion ISSN persistance style
            if 'v35' in self.data['title']:
                if self.data['title']['v35'][0]['_'] == "PRINT":
                    self.print_issn = self.data['title']['v400'][0]['_']
                else:
                    self.electronic_issn = self.data['title']['v400'][0]['_']
        else:  # New ISSN persistance style
            if 'v35' in self.data['title']:
                if self.data['title']['v35'][0]['_'] == "PRINT":
                    self.print_issn = self.data['title']['v935'][0]['_']
                    if self.data['title']['v935'][0]['_'] != self.data['title']['v400'][0]['_']:
                        self.electronic_issn = self.data['title']['v400'][0]['_']
                else:
                    self.electronic_issn = self.data['title']['v935'][0]['_']
                    if self.data['title']['v935'][0]['_'] != self.data['title']['v400'][0]['_']:
                        self.print_issn = self.data['title']['v400'][0]['_']

    def original_language(self, iso_format=None):
        """
        This method retrieves the original language of the given article.
        """

        fmt = self._iso_format if not iso_format else iso_format

        return tools.get_language(self.data['article']['v40'][0]['_'], fmt)

    @property
    def publisher_name(self):

        if 'v480' in self.data['title']:
            return self.data['title']['v480'][0]['_']

    @property
    def journal_title(self):

        if 'v100' in self.data['title']:
            return self.data['title']['v100'][0]['_']

    @property
    def publication_date(self):
        
        return tools.get_publication_date(self.data['article']['v65'][0]['_'])

    @property
    def volume(self):

        if 'v31' in self.data['article']:
            return self.data['article']['v31'][0]['_']

    @property
    def issue(self):

        if 'v32' in self.data['article']:
            return self.data['article']['v32'][0]['_']

    @property
    def supplement_volume(self):

        if 'v131' in self.data['article']:
            return self.data['article']['v131'][0]['_']

    @property
    def supplement_issue(self):

        if 'v132' in self.data['article']:
            return self.data['article']['v132'][0]['_']

    @property
    def start_page(self):

        if 'v14' in self.data['article']:
            if 'f' in self.data['article']['v14'][0]:
                return self.data['article']['v14'][0]['f']

    @property
    def end_page(self):

        if 'v14' in self.data['article']:
            if 'l' in self.data['article']['v14'][0]:
                return self.data['article']['v14'][0]['l']

    @property
    def doi(self):

        if 'doi' in self.data['article']:
            return self.data['article']['doi']

    @property
    def publisher_id(self):
        return self.data['article']['v880'][0]['_']

    @property
    def document_type(self):

        if 'v71' in self.data['article']:
            article_type_code = self.data['article']['v71'][0]['_']
            if article_type_code in choices.article_types:
                return choices.article_types[article_type_code]
            else:
                return choices.article_types['nd']

        return choices.article_types['nd']

    def original_title(self, iso_format=None):

        fmt = iso_format or self._iso_format

        if 'v12' in self.data['article']:
            for title in self.data['article']['v12']:
                if 'l' in title:
                    language = tools.get_language(title['l'], fmt)
                    if language == self.original_language(iso_format=fmt):
                        return title['_']

    def translated_titles(self, iso_format=None):

        fmt = iso_format or self._iso_format

        trans_titles = {}
        if 'v12' in self.data['article']:
            for title in self.data['article']['v12']:
                if 'l' in title:
                    language = tools.get_language(title['l'], fmt)
                    if language != self.original_language(iso_format=fmt):
                        trans_titles.setdefault(language, title['_'])

        if len(trans_titles) == 0:
            return None

        return trans_titles


    def original_abstract(self, iso_format=None):

        fmt = iso_format or self._iso_format

        if 'v83' in self.data['article']:
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    language = tools.get_language(abstract['l'], fmt)
                    if language == self.original_language(iso_format=fmt):
                        return abstract['a']

    def translated_abstracts(self, iso_format=None):

        fmt = iso_format or self._iso_format

        trans_abstracts = {}
        if 'v83' in self.data['article']:
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    language = tools.get_language(abstract['l'], fmt)
                    if language != self.original_language(iso_format=fmt):
                        trans_abstracts.setdefault(language, abstract['a'])

        if len(trans_abstracts) == 0:
            return None

        return trans_abstracts

    @ property
    def authors(self):
        authors = []
        if 'v10' in self.data['article']:
            for author in self.data['article']['v10']:
                authordict = {}
                if 's' in author:
                    authordict['surname'] = author['s']
                else:
                    authordict['surname'] = ''
                if 'n' in author:
                    authordict['given_names'] = author['n']
                else:
                    authordict['given_names'] = ''
                if 'r' in author:
                    authordict['role'] = author['r']
                if '1' in author:
                    authordict['xref'] = author['1'].split(' ')

                authors.append(authordict)

        if len(authors) == 0:
            return None

        return authors

    @property
    def affiliations(self):
        affiliations = []
        if 'v70' in self.data['article']:
            for aff in self.data['article']['v70']:
                affdict = {}
                if '_' in aff:
                    if len(aff['_'].strip()) > 0:
                        affdict['institution'] = aff['_']
                        if 'i' in aff:
                            affdict['index'] = aff['i']
                        else:
                            affdict['index'] = 'nd'
                        if 'c' in aff:
                            affdict['addr_line'] = aff['c']
                        if 'p' in aff:
                            affdict['country'] = aff['p']
                        if 'e' in aff:
                            affdict['email'] = aff['e']

                        affiliations.append(affdict)

        if len(affiliations) == 0:
            return None

        return affiliations

    @property
    def scielo_domain(self):

        if 'v690' in self.data['title']:
            return self.data['title']['v690'][0]['_'].replace('http://', '')
        elif 'v69' in self.data['article']:
            return self.data['article']['v69'][0]['_'].replace('http://', '')

    @property
    def pdf_url(self):

        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_pdf&pid={1}".format(self.scielo_domain,
                                                                         self.publisher_id)

    @property
    def html_url(self):

        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_arttext&pid={1}".format(self.scielo_domain,
                                                                             self.publisher_id)

    @property
    def issue_url(self):

        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_issuetoc&pid={1}".format(self.scielo_domain,
                                                                              self.publisher_id[0:18])

    @property
    def journal_url(self):

        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_serial&pid={1}".format(self.scielo_domain,
                                                                            self.publisher_id[1:10])

    def keywords(self, iso_format='iso 639-2'):

        fmt = iso_format or self._iso_format

        keywords = {}
        if 'v85' in self.data['article']:
            for keyword in self.data['article']['v85']:
                if 'k' in keyword and 'l' in keyword:
                    language = tools.get_language(keyword['l'], fmt)
                    group = keywords.setdefault(language, [])
                    group.append(keyword['k'])

        if len(keywords) == 0:
            return None

        return keywords

    def any_issn(self, priority=u'electronic'):

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
    def citations(self):

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

        if 'v18' in self.data:
            return u'book'
        elif 'v12' in self.data and 'v30' in self.data:
            return u'article'
        elif 'v53' in self.data:
            return u'conference'
        elif 'v45' in self.data:
            return u'thesis'
        elif 'v37' in self.data:
            return u'link'
        else:
            return u'undefined'

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
            return self.data['v30'][0]['_']

        if self.publication_type == u'book' and 'v18' in self.data:
            return self.data['v18'][0]['_']

    @property
    def chapter_title(self):
        """
        If it is a book citation, this method retrieves a chapter title, if it exists.
        """
        if self.publication_type == u'book' and 'v12' in self.data:
            return self.data['v12'][0]['_']

    @property
    def article_title(self):
        """
        If it is an article citation, this method retrieves the article title, if it exists.
        """
        if self.publication_type == u'article' and 'v12' in self.data:
            return self.data['v12'][0]['_']

    @property
    def thesis_title(self):
        """
        If it is a thesis citation, this method retrieves the thesis title, if it exists.
        """

        if self.publication_type == u'thesis' and 'v45' in self.data:
            return self.data['v45'][0]['_']

    @property
    def conference_title(self):
        """
        If it is a conference citation, this method retrieves the conference title, if it exists.
        """

        if self.publication_type == u'conference' and 'v53' in self.data:
            return self.data['v53'][0]['_']

    @property
    def link_title(self):
        """
        If it is a link citation, this method retrieves the link title, if it exists.
        """

        if self.publication_type == u'link' and 'v12' in self.data:
            return self.data['v12'][0]['_']

    @property
    def conference_date(self):
        """
        If it is a conference citation, this method retrieves the conference date, if it exists.
        The conference date is presented like it is in the citation.
        """

        if self.publication_type == u'conference' and 'v54' in self.data:
            return self.data['v54'][0]['_']

    @property
    def conference_sponsor(self):
        """
        If it is a conference citation, this method retrieves the conference sponsor, if it exists.
        The conference sponsor is presented like it is in the citation.
        """

        if self.publication_type == u'conference' and 'v52' in self.data:
            return self.data['v52'][0]['_']

    @property
    def link(self):
        """
        This metod retrieves a link, if it is exists.
        """

        if 'v37' in self.data:
            return self.data['v37'][0]['_']




