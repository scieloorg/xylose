# coding: utf-8

import unittest
import json
import os
from scielodocument.scielodocument import Document, Article, Citations


class DocumentTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/full_document.json' % path).read())

    def test_instancianting_document(self):        
        doc = Document(self.fulldoc)
        self.assertTrue(doc._title is None)
        self.assertTrue(doc._citations is None)
        self.assertTrue(isinstance(doc._article, Article))


class ArticleTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/full_document.json' % path).read())
        self.document = Document(self.fulldoc)

    def test_article(self):
        article = self.document.article
        self.assertTrue(isinstance(article, Article))

    def test_original_language_iso639b(self):
        article = self.document.article
        
        self.assertTrue(article.original_language() == u'eng')

    def test_original_language_invalid_iso639b(self):
        article = self.document.article
        
        article.data['article']['v40'][0]['_'] = u'XXX'

        self.assertTrue(article.original_language() == None)

    def test_original_language_original(self):
        article = self.document.article
        
        self.assertTrue(article.original_language(format='orig') == u'en')

    def test_publisher_name(self):
        article = self.document.article

        self.assertTrue(article.publisher_name == u'Associação Brasileira de Limnologia')

    def test_without_publisher_name(self):
        article = self.document.article

        del(article.data['title']['v480'])
        self.assertTrue(article.publisher_name == None)

    def test_journal_title(self):
        article = self.document.article

        self.assertTrue(article.journal_title == u'Acta Limnologica Brasiliensia')

    def test_without_journal_title(self):
        article = self.document.article

        del(article.data['title']['v100'])
        self.assertTrue(article.journal_title == None)

    def test_publication_date_just_year(self):
        article = self.document.article
        
        article.data['article']['v65'] = [{u'_': u'20120102'}]
        self.assertTrue(article.publication_date == '2012-01-02')

        article.data['article']['v65'] = [{u'_': u'20120100'}]
        self.assertTrue(article.publication_date == '2012-01')

        article.data['article']['v65'] = [{u'_': u'20120000'}]
        self.assertTrue(article.publication_date == '2012')

    def test_without_publication_date(self):
        article = self.document.article

        del(article.data['article']['v65'])
        with self.assertRaises(KeyError):
            article.publication_date

    def test_volume(self):
        article = self.document.article

        self.assertTrue(article.volume == u'23')

    def test_without_volume(self):
        article = self.document.article

        del(article.data['article']['v31'])
        self.assertTrue(article.volume == None)

    def test_issue(self):
        article = self.document.article

        self.assertTrue(article.issue == u'3')

    def test_without_issue(self):
        article = self.document.article

        del(article.data['article']['v32'])
        self.assertTrue(article.issue == None)

    def test_supplement_volume(self):
        article = self.document.article

        article.data['article']['v131'] = [{u'_': u'test_suppl_volume'}]
        self.assertTrue(article.supplement_volume == u'test_suppl_volume')

    def test_without_supplement_volume(self):
        article = self.document.article

        self.assertTrue(article.supplement_volume == None)

    def test_supplement_issue(self):
        article = self.document.article

        article.data['article']['v132'] = [{u'_': u'test_suppl_issue'}]
        self.assertTrue(article.supplement_issue == u'test_suppl_issue')

    def test_without_suplement_issue(self):
        article = self.document.article

        self.assertTrue(article.supplement_issue == None)

    def test_start_page(self):
        article = self.document.article

        self.assertTrue(article.start_page == u'229')

    def test_without_start_page(self):
        article = self.document.article

        del(article.data['article']['v14'][0]['f'])
        self.assertTrue(article.start_page == None)

    def test_last_page(self):
        article = self.document.article

        self.assertTrue(article.end_page == u'232')

    def test_without_last_page(self):
        article = self.document.article

        del(article.data['article']['v14'][0]['l'])
        self.assertTrue(article.end_page == None)

    def test_without_pages(self):
        article = self.document.article

        del(article.data['article']['v14'])
        self.assertTrue(article.end_page == None)

    def test_doi(self):
        article = self.document.article

        self.assertTrue(article.doi == u'10.1590/S2179-975X2012005000004')

    def test_without_doi(self):
        article = self.document.article

        del(article.data['article']['doi'])
        self.assertTrue(article.doi == None)

    def test_publisher_id(self):
        article = self.document.article

        self.assertTrue(article.publisher_id == u'S2179-975X2011000300002')

    def test_without_publisher_id(self):
        article = self.document.article

        del(article.data['article']['v880'])
        with self.assertRaises(KeyError):
            article.publisher_id

    def test_document_type(self):
        article = self.document.article

        self.assertTrue(article.document_type == u'research-article')

    def test_without_document_type(self):
        article = self.document.article

        del(article.data['article']['v71'])
        self.assertTrue(article.document_type == u'undefined')

    def test_invalid_document_type(self):
        article = self.document.article

        article.data['article']['v71'] = [{u'_': u'invalid'}]
        self.assertTrue(article.document_type == u'undefined')

    def test_without_original_title(self):
        article = self.document.article

        del(article.data['article']['v12'])
        self.assertTrue(article.original_title == None)

    def test_original_title_without_language_defined(self):
        article = self.document.article

        del(article.data['article']['v12'])

        article.data['article']['v12'] = [{u'_': u'article title 1'}, {u'_': u'article title 2'}]
        self.assertTrue(article.original_title == None)

    def test_original_title_with_just_one_language_defined(self):
        article = self.document.article

        del(article.data['article']['v12'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v12'] = [{u'_': u'article title 1', u'l': u'en'}, 
                                          {u'_': u'article title 2'}]

        self.assertTrue(article.original_title == u'article title 1')

    def test_original_title_with_language_defined(self):
        article = self.document.article

        del(article.data['article']['v12'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v12'] = [{u'_': u'article title 1', u'l': u'pt'}, 
                                          {u'_': u'article title 2', u'l': u'en'}]

        self.assertTrue(article.original_title == u'article title 2')

    def test_original_title_with_language_defined_but_different_of_the_article_original_language(self):
        article = self.document.article

        del(article.data['article']['v12'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v12'] = [{u'_': u'article title 1', u'l': u'pt'}, 
                                          {u'_': u'article title 2', u'l': u'fr'}]

        self.assertTrue(article.original_title == None)

    @unittest.skip("must be tested")
    def test_translated_titles(self):
        pass

    def test_without_original_abstract(self):
        article = self.document.article

        del(article.data['article']['v83'])
        self.assertTrue(article.original_abstract == None)

    def test_original_abstract_without_language_defined(self):
        article = self.document.article

        del(article.data['article']['v83'])

        article.data['article']['v83'] = [{u'a': u'article abstract 1'}, {u'a': u'abstract title 2'}]
        self.assertTrue(article.original_abstract == None)

    def test_original_abstract_with_just_one_language_defined(self):
        article = self.document.article

        del(article.data['article']['v83'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v83'] = [{u'a': u'article abstract 1', u'l': u'en'}, 
                                          {u'a': u'article abstract 2'}]

        self.assertTrue(article.original_abstract == u'article abstract 1')

    def test_original_abstract_with_language_defined(self):
        article = self.document.article

        del(article.data['article']['v83'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v83'] = [{u'a': u'article abstract 1', u'l': u'pt'}, 
                                          {u'a': u'article abstract 2', u'l': u'en'}]

        self.assertTrue(article.original_abstract == u'article abstract 2')

    def test_original_abstract_with_language_defined_but_different_of_the_article_original_language(self):
        article = self.document.article

        del(article.data['article']['v83'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v83'] = [{u'a': u'article abstract 1', u'l': u'pt'}, 
                                          {u'a': u'article abstract 2', u'l': u'fr'}]

        self.assertTrue(article.original_abstract == None)

    @unittest.skip("must be tested")
    def test_translated_abstracts(self):
        pass

    def test_without_authors(self):
        article = self.document.article

        del(article.data['article']['v10'])
        self.assertTrue(article.authors == None)

    def test_authors(self):
        article = self.document.article

        authors = [{u'role': u'ND', 
                    u'xref': [u'A01'],
                    u'surname': u'Gomes',
                    u'given_names': u'Caio Isola Dallevo do Amaral'},
                   {u'role': u'ND',
                    u'xref': [u'A02'],
                    u'surname': u'Peressin',
                    u'given_names': u'Alexandre'},
                   {u'role': u'ND',
                    u'xref': [u'A03'],
                    u'surname': u'Cetra',
                    u'given_names': u'Mauricio'},
                   {u'role': u'ND',
                    u'xref': [u'A04'],
                    u'surname': u'Barrella',
                    u'given_names': u'Walter'}
                   ]
        self.assertTrue(article.authors == authors)

    def test_author_with_two_affiliations(self):
        article = self.document.article
        
        del(article.data['article']['v10'])
        article.data['article']['v10'] = [{u"1": "A01 A02",
                                           u"s": "Gomes",
                                           u"r": "ND",
                                           u"_": "",
                                           u"n": "Caio Isola Dallevo do Amaral"}]
        expected = [{u'role': u'ND',
                     u'xref': [u'A01', u'A02'],
                     u'surname': u'Gomes',
                     u'given_names': u'Caio Isola Dallevo do Amaral'}]
        
        self.assertTrue(article.authors == expected)

    def test_author_without_affiliations(self):
        article = self.document.article
        
        del(article.data['article']['v10'])
        article.data['article']['v10'] = [{u"s": "Gomes",
                                           u"r": "ND",
                                           u"_": "",
                                           u"n": "Caio Isola Dallevo do Amaral"}]
        expected = [{u'role': u'ND',
                     u'surname': u'Gomes',
                     u'given_names': u'Caio Isola Dallevo do Amaral'}]
        
        self.assertTrue(article.authors == expected)

    def test_author_without_surname_and_given_names(self):
        article = self.document.article
        
        del(article.data['article']['v10'])
        article.data['article']['v10'] = [{u"1": u"A01 A02",
                                           u"r": u"ND",
                                           u"_": u""}]
        expected = [{u'role': u'ND',
                     u'xref': [u'A01', u'A02'],
                     u'surname': u'',
                     u'given_names': u''}]
        
        self.assertTrue(article.authors == expected)

    def test_author_with_two_role(self):
        article = self.document.article
        
        del(article.data['article']['v10'])
        article.data['article']['v10'] = [{u"1": u"A01 A02",
                                           u"s": u"Gomes",
                                           u"_": u"",
                                           u"n": u"Caio Isola Dallevo do Amaral"}]
        expected = [{u'xref': [u'A01', u'A02'],
                     u'surname': u'Gomes',
                     u'given_names': u'Caio Isola Dallevo do Amaral'}]

        self.assertTrue(article.authors == expected)

    def test_without_affiliations(self):
        article = self.document.article

        del(article.data['article']['v70'])
        self.assertTrue(article.affiliations == None)

    def test_affiliations(self):
        article = self.document.article

        affiliations = [
                        {u'index': u'A01',
                         u'addr_line': u'Sorocaba',
                         u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
                         u'email': u'caioisola@yahoo.com.br',
                         u'country': u'BRAZIL'},
                        {u'index': u'A02',
                         u'addr_line': u'Sorocaba',
                         u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
                         u'email': u'alex_peressin@yahoo.com.br',
                         u'country': u'BRAZIL'},
                        {u'index': u'A03',
                         u'addr_line': u'Sorocaba',
                         u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
                         u'email': u'mcetra@ufscar.br',
                         u'country': u'BRAZIL'},
                        {u'index': u'A04',
                         u'addr_line': u'Sorocaba',
                         u'institution': u'PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO',
                         u'email': u'vbarrella@pucsp.br',
                         u'country': u'BRAZIL'}]

        self.assertTrue(article.affiliations == affiliations)

    def test_affiliation_without_affiliation_name(self):
        article = self.document.article

        del(article.data['article']['v70'])

        article.data['article']['v70'] = [{"c": "Sorocaba",
                                           "e": "mcetra@ufscar.br",
                                           "i": "A03",
                                           "1": "Departamento de Ci\u00eancias Ambientais",
                                           "p": "BRAZIL",
                                           "s": "SP",
                                           "z": "18052-780"}]
        
        self.assertTrue(article.affiliations == None)

    def test_affiliation_just_with_affiliation_name(self):
        article = self.document.article

        del(article.data['article']['v70'])

        article.data['article']['v70'] = [{"_": "UNIVERSIDADE FEDERAL DE SAO CARLOS"}]

        expected = [{u'index': u'nd', u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'}]
        
        self.assertTrue(article.affiliations == expected)













