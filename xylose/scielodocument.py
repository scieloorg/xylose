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
        """
        This method creates an object level attributes (print_issn and/or electronic issn),
        according to the given metadata.
        This method deal with the legacy datamodel fields (935, 400, 35) where:
        """
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
        This method deals with the legacy fields (40).
        """

        fmt = self._iso_format if not iso_format else iso_format

        return tools.get_language(self.data['article']['v40'][0]['_'], fmt)

    @property
    def publisher_name(self):
        """
        This method retrieves the publisher name of the given article, if it exists.
        This method deals with the legacy fields (480).
        """
        if 'v480' in self.data['title']:
            return self.data['title']['v480'][0]['_']

    @property
    def journal_title(self):
        """
        This method retrieves the journal_title of the given article, if it exists.
        This method deals with the legacy fields (100).
        """
        if 'v100' in self.data['title']:
            return self.data['title']['v100'][0]['_']

    @property
    def publication_date(self):
        """
        This method retrieves the publication date of the given article, if it exists.
        This method deals with the legacy fields (65).
        """
        
        return tools.get_publication_date(self.data['article']['v65'][0]['_'])

    @property
    def contract(self):
        """
        This method retrieves the contract of the given article, if it exists.
        This method deals with the legacy fields (60).
        """
        if 'v60' in self.data['article']:
            return self.data['article']['v60'][0]['_']

    @property
    def project_name(self):
        """
        This method retrieves the project name of the given article, if it exists.
        This method deals with the legacy fields (59).
        """
        if 'v59' in self.data['article']:
            return self.data['article']['v59'][0]['_']

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
                    authordict['orgname'] = sponsor['_']
                if 'd' in sponsor:
                    authordict['orgdiv'] = sponsor['d']

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
            if 'f' in self.data['article']['v14'][0]:
                return self.data['article']['v14'][0]['f']

    @property
    def end_page(self):
        """
        This method retrieves the end page of the given article, if it exists.
        This method deals with the legacy fields (14).
        """
        if 'v14' in self.data['article']:
            if 'l' in self.data['article']['v14'][0]:
                return self.data['article']['v14'][0]['l']

    @property
    def doi(self):
        """
        This method retrieves the DOI of the given article, if it exists.
        """
        if 'doi' in self.data['article']:
            return self.data['article']['doi']

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
        if 'v30' in self.data['article']:
            return self.data['article']['v30'][0]['_']

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
                        return title['_']

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
                        trans_titles.setdefault(language, title['_'])

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
                        return abstract['a']

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
                        trans_abstracts.setdefault(language, abstract['a'])

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
                    authordict['orgname'] = author['_']
                if 'd' in author:
                    authordict['orgdiv'] = author['d']

                authors.append(authordict)

        if len(authors) == 0:
            return None

        return authors

    @property
    def affiliations(self):
        """
        This method retrieves the authors affiliations of the given article, if it exists.
        This method deals with the legacy fields (70).
        """
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
        """
        This method retrieves the collection domains of the given article, if it exists.
        This method deals with the legacy fields (69, 690).
        """
        if 'v690' in self.data['title']:
            return self.data['title']['v690'][0]['_'].replace('http://', '')
        elif 'v69' in self.data['article']:
            return self.data['article']['v69'][0]['_'].replace('http://', '')

    @property
    def pdf_url(self):
        """
        This method retrieves the pdf url of the given article.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_pdf&pid={1}".format(self.scielo_domain,
                                                                         self.publisher_id)

    @property
    def html_url(self):
        """
        This method retrieves the html url of the given article.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_arttext&pid={1}".format(self.scielo_domain,
                                                                             self.publisher_id)

    @property
    def issue_url(self):
        """
        This method retrieves the issue url of the given article.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_issuetoc&pid={1}".format(self.scielo_domain,
                                                                              self.publisher_id[0:18])

    @property
    def journal_url(self):
        """
        This method retrieves the journal url of the given article.
        """
        if self.scielo_domain:
            return "http://{0}/scielo.php?script=sci_serial&pid={1}".format(self.scielo_domain,
                                                                            self.publisher_id[1:10])

    def keywords(self, iso_format='iso 639-2'):
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
                    group = keywords.setdefault(language, [])
                    group.append(keyword['k'])

        if len(keywords) == 0:
            return None

        return keywords

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

        if 'v18' in self.data:
            if 'v45' in self.data:
                return u'thesis'
            else:
                return u'book'
        elif 'v12' in self.data and 'v30' in self.data:
            return u'article'
        elif 'v53' in self.data:
            return u'conference'
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

        if self.publication_type == u'thesis' and 'v18' in self.data:
            return self.data['v18'][0]['_']

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
        This method retrieves a link, if it is exists.
        """

        if 'v37' in self.data:
            return self.data['v37'][0]['_']

    @property
    def date(self):
        """
        This method retrieves the citation date, if it is exists.
        """

        if 'v65' in self.data:
            return self.data['v65'][0]['_']

    @property
    def edition(self):
        """
        This method retrieves the edition, if it is exists. The citation must be
        a conference or book citation.
        """

        if self.publication_type in [u'conference', u'book']:
            if 'v63' in self.data:
                return self.data['v63'][0]['_']

    @property
    def first_page(self):
        pass

    @property
    def last_page(self):
        pass

    @property
    def institutions(self):
        """
        This method retrieves the institutions in the given citation without care about
        the citation type (article, book, thesis, conference, etc).
        """ 

        institutions = []
        if 'v11' in self.data:
            institutions.append(self.data['v11'][0]['_'])
        if 'v17' in self.data:
            institutions.append(self.data['v17'][0]['_'])
        if 'v29' in self.data:
            institutions.append(self.data['v29'][0]['_'])
        if 'v50' in self.data:
            institutions.append(self.data['v50'][0]['_'])
        if 'v58' in self.data:
            institutions.append(self.data['v58'][0]['_'])

        if len(institutions) > 0:
            return institutions

    @property
    def analytic_institution(self):
        """
        This method retrieves the institutions in the given citation. The citation must be 
        an article or book citation, if it exists.
        """ 
        institutions = []
        if self.publication_type in [u'article', u'book'] and 'v11' in self.data:
            if 'v11' in self.data:
                for institution in self.data['v11']:
                    institutions.append(self.data['v11'][0]['_'])

        if len(institutions) > 0:
            return institutions

    @property
    def monographic_institution(self):        
        """
        This method retrieves the institutions in the given citation. The citation must be 
        a book citation, if it exists.
        """ 
        institutions = []
        if self.publication_type == u'book' and 'v17' in self.data:
            if 'v17' in self.data:
                for institution in self.data['v17']:
                    institutions.append(self.data['v17'][0]['_'])

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
                sponsors.append(self.data['v58'][0]['_'])

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
                editors.append(self.data['v29'][0]['_'])

        if len(editors) > 0:
            return editors

    @property
    def thesis_institution(self):
        """
        This method retrieves the thesis institutions in the given citation, if it exists.
        """

        institutions = []
        if 'v50' in self.data:
            for institution in self.data['v50']:
                institutions.append(self.data['v50'][0]['_'])

        if len(institutions) > 0:
            return institutions

    @property
    def issn(self):
        """
        This method retrieves the journal issn, if it is exists. The citation must be
        an article citation.
        """

        if self.publication_type == u'article' and 'v35' in self.data:
            return self.data['v35'][0]['_']

    @property
    def isbn(self):
        """
        This method retrieves the book isbn, if it is exists. The citation must be
        a book citation.
        """

        if self.publication_type == u'book' and 'v69' in self.data:
            return self.data['v69'][0]['_']

    @property
    def volume(self):
        """
        This method retrieves the book our journal volume number, if it exists. The citation must be
        a book our an article citation.
        """

        if self.publication_type in [u'article', u'book']:
            if 'v31' in self.data:
                return self.data['v31'][0]['_']

    @property
    def issue(self):
        """
        This method retrieves the journal issue number, if it exists. The citation must be
        an article citation.
        """

        if self.publication_type in u'article' and 'v32' in self.data:
            return self.data['v32'][0]['_']

    @property
    def issue_title(self):
        """
        This method retrieves the issue title, if it exists. The citation must be
        an article citation.
        """

        if self.publication_type in u'article' and 'v33' in self.data:
            return self.data['v33'][0]['_']

    @property
    def issue_part(self):
        """
        This method retrieves the issue part, if it exists. The citation must be
        an article citation.
        """

        if self.publication_type in u'article' and 'v34' in self.data:
            return self.data['v34'][0]['_']

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
        This method retrieves the authors of the given citation. These authors may
        correspond to an article, book analytic, link or thesis.
        """
        docs = [u'article', u'book', u'link', u'thesis']
        authors = []
        if self.publication_type in docs and 'v10' in self.data:
            for author in self.data['v10']:
                authordict = {}
                if 's' in author:
                    authordict['surname'] = author['s']
                if 'n' in author:
                    authordict['given-names'] = author['n']
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
        if self.publication_type == u'book' and 'v16' in self.data:
            for author in self.data['v16']:
                authordict = {}
                if 's' in author:
                    authordict['surname'] = author['s']
                if 'n' in author:
                    authordict['given-names'] = author['n']
                if 's' in author or 'n' in author:
                    authors.append(authordict)
        
        if len(authors) > 0:
            return authors

    @property
    def serie(self):
        """
        This method retrieves the series title. The serie title must be in a book, article or
        conference citation.
        """
        docs = [u'conference', u'book', u'article']
        if self.publication_type in docs and 'v25' in self.data:
            return self.data['v25'][0]['_']

    @property
    def publisher(self):
        """
        This method retrieves the publisher name, if it exists.
        """
        if 'v62' in self.data:
            return self.data['v62'][0]['_']

    @property
    def publisher_address(self):
        """
        This method retrieves the publisher address, if it exists.
        """
        address = []
        if 'v66' in self.data:
            address.append(self.data['v66'][0]['_'])
            if 'e' in self.data['v66'][0]:
                address.append(self.data['v66'][0]['e'])

        if 'v67' in self.data:
            address.append(self.data['v67'][0]['_'])

        if len(address) > 0:
            return"; ".join(address)
