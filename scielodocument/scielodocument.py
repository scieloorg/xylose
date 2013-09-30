# encoding: utf-8

import choices


class Article(object):

    def __init__(self, data):
        self.data = data
        self.print_issn = None
        self.electronic_issn = None
        self._load_issn()

    def _load_issn(self):

        # ISSN and Other Complex Stuffs from the old version
        if not 'v935' in self.data['title']:  # Old fashion ISSN persistance style
            if self.data['title']['v35'][0] == "PRINT":
                self.print_issn = self.data['title']['v400'][0]['_']
            else:
                self.electronic_issn = self.data['title']['v400'][0]['_']

        else:  # New ISSN persistance style

            if 'v35' in self.data['title']:
                if self.data['title']['v35'][0] == "PRINT":
                    self.print_issn = self.data['title']['v935'][0]['_']
                    if self.data['title']['v935'][0] != self.data['title']['v400'][0]:
                        self.electronic_issn = self.data['title']['v400'][0]['_']
                else:
                    self.electronic_issn = self.data['title']['v935'][0]['_']
                    if self.data['title']['v935'][0] != self.data['title']['v400'][0]:
                        self.print_issn = self.data['title']['v400'][0]['_']

    def original_language(self, format='iso 639-b'):
        """
        Retrive the article original original language
        """

        if format == 'iso 639-b':
            if self.data['article']['v40'][0]['_'] in choices.ISO639_2:
                return choices.ISO639_2[self.data['article']['v40'][0]['_']]
        else:
            return self.data['article']['v40'][0]['_']

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

        pub_date = [self.data['article']['v65'][0]['_'][0:4]]

        months = [i+1 for i in range(12)]
        days = [i+1 for i in range(31)]

        month = int(self.data['article']['v65'][0]['_'][4:6])
        day = int(self.data['article']['v65'][0]['_'][6:8])

        if month in months:
            pub_date.append(self.data['article']['v65'][0]['_'][4:6])

        if day in days:
            pub_date.append(self.data['article']['v65'][0]['_'][6:8])


        return "-".join(pub_date)

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

    @property
    def original_title(self):

        if 'v12' in self.data['article']:
            for title in self.data['article']['v12']:
                if 'l' in title:
                    if title['l'] in choices.ISO639_2: 
                        if choices.ISO639_2[title['l']] == self.original_language():
                            return title['_']

    @property
    def translated_titles(self):

        trans_titles = {}
        if 'v12' in self.data['article']:
            for title in self.data['article']['v12']:
                if 'l' in title:
                    if title['l'] in choices.ISO639_2:
                        l = choices.ISO639_2[title['l']]
                    else:
                        l = 'undefined'
                    if l != self.original_language:
                        trans_titles.setdefault(l, title['_'])

        if len(trans_titles) == 0:
            return None

        return trans_titles

    @property
    def original_abstract(self):

        if 'v83' in self.data['article']:
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    if abstract['l'] in choices.ISO639_2:
                        if choices.ISO639_2[abstract['l']] == self.original_language():
                            return abstract['a']

    @property
    def translated_abstracts(self):

        trans_abstracts = {}
        if 'v83' in self.data['article']:
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    if abstract['l'] in choices.ISO639_2:
                        l = choices.ISO639_2[abstract['l']]
                    else:
                        l = 'undefined'
                    if l != self.original_language:
                        trans_abstracts.setdefault(l, abstract['a'])

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
    def original_title_language(self):

        return self.original_language

    @property
    def original_abstract_language(self):

        return self.original_language

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

    @property
    def keywords(self):

        keywords = {}
        if 'v85' in self.data['article']:
            for keyword in self.data['article']['v85']:
                if 'k' in keyword and 'l' in keyword:
                    if keyword['l'] in choices.ISO639_2:
                        l = choices.ISO639_2[keyword['l']]
                    else:
                        l = 'undefined'
                    group = keywords.setdefault(l, [])
                    group.append(keyword['k'])

        if len(keywords) == 0:
            return None

        return keywords

    def issn(self, priority='electronic'):

        if priority == 'electronic':
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

        if 'citations' in self.data:
            return Citations(self.data['citations'])

        return None


class Citations(object):

    def __init__(self, data):
        pass


class Document(object):

    def __init__(self, data):
        self._article = Article(data)
        self._citations = None
        self._title = None

    @property
    def article(self):
        return self._article
