# coding: utf-8

import unittest
import json
import os
from xylose.scielodocument import Article, Citation
from xylose import tools

class ToolsTests(unittest.TestCase):

    def test_get_language_without_iso_format(self):

        language = tools.get_language(u'xx', None)

        self.assertEqual(language, u'xx')

    def test_get_language_iso639_1_defined(self):

        language = tools.get_language( u'pt', u'iso 639-1')

        self.assertEqual(language, u'pt')

    def test_get_language_iso639_1_undefined(self):

        language = tools.get_language( u'xx', u'iso 639-1')

        self.assertEqual(language, u'#undefined xx#')

    def test_get_language_iso639_2_defined(self):

        language = tools.get_language( u'pt', u'iso 639-2')

        self.assertEqual(language, u'por')

    def test_get_language_iso639_2_undefined(self):

        language = tools.get_language( u'xx', u'iso 639-2')

        self.assertEqual(language, u'#undefined xx#')

class ArticleTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/full_document.json' % path).read())
        self.article = Article(self.fulldoc)

    def test_article(self):
        article = self.article
        self.assertTrue(isinstance(article, Article))

    def test_load_issn_with_v935_without_v35(self):
        del(self.fulldoc['title']['v35'])
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, None)
        self.assertEqual(article.electronic_issn, None)

    def test_load_issn_without_v935_without_v35(self):
        del(self.fulldoc['title']['v35'])
        del(self.fulldoc['title']['v935'])
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, None)

    def test_load_issn_without_v935_and_v35_PRINT(self):
        self.fulldoc['title']['v35']  = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        del(self.fulldoc['title']['v935'])

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, u'2222-2222')
        self.assertEqual(article.electronic_issn, None)

    def test_load_issn_without_v935_and_v35_ONLINE(self):
        self.fulldoc['title']['v35']  = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        del(self.fulldoc['title']['v935'])

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, None)
        self.assertEqual(article.electronic_issn, u'2222-2222')

    def test_load_issn_with_v935_and_v35_PRINT(self):
        self.fulldoc['title']['v35']  = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, u'3333-3333')
        self.assertEqual(article.electronic_issn, u'2222-2222')

    def test_load_issn_with_v935_and_v35_ONLINE(self):
        self.fulldoc['title']['v35']  = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, u'2222-2222')
        self.assertEqual(article.electronic_issn, u'3333-3333')

    def test_load_issn_with_v935_equal_v400_and_v35_PRINT(self):
        self.fulldoc['title']['v35']  = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, u'3333-3333')
        self.assertEqual(article.electronic_issn, None)

    def test_load_issn_with_v935_equal_v400_and_v35_ONLINE(self):
        self.fulldoc['title']['v35']  = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.print_issn, None)
        self.assertEqual(article.electronic_issn, u'3333-3333')

    def test_any_issn_priority_electronic(self):
        self.fulldoc['title']['v35']  = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.any_issn(priority='electronic'), u'3333-3333')

    def test_any_issn_priority_electronic_without_electronic(self):
        self.fulldoc['title']['v35']  = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.any_issn(priority='electronic'), u'3333-3333')

    def test_any_issn_priority_print(self):
        self.fulldoc['title']['v35']  = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.any_issn(priority='print'), u'2222-2222')

    def test_any_issn_priority_print_without_print(self):
        self.fulldoc['title']['v35']  = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.any_issn(priority='print'), u'3333-3333')

    def test_original_language_iso639_2(self):
        article = self.article
        
        self.assertEqual(article.original_language(iso_format='iso 639-2'), u'eng')

    def test_original_language_invalid_iso639_2(self):
        article = self.article
        
        article.data['article']['v40'][0]['_'] = u'XXX'

        self.assertEqual(article.original_language(iso_format='iso 639-2'), u'#undefined XXX#')

    def test_original_language_original(self):
        article = self.article
        
        self.assertEqual(article.original_language(iso_format=None), u'en')

    def test_publisher_name(self):
        article = self.article

        self.assertEqual(article.publisher_name, u'Associação Brasileira de Limnologia')

    def test_without_publisher_name(self):
        article = self.article

        del(article.data['title']['v480'])
        self.assertEqual(article.publisher_name, None)

    def test_journal_title(self):
        article = self.article

        self.assertEqual(article.journal_title, u'Acta Limnologica Brasiliensia')

    def test_without_journal_title(self):
        article = self.article

        del(article.data['title']['v100'])
        self.assertEqual(article.journal_title, None)

    def test_publication_date_just_year(self):
        article = self.article
        
        article.data['article']['v65'] = [{u'_': u'20120102'}]
        self.assertEqual(article.publication_date, '2012-01-02')

        article.data['article']['v65'] = [{u'_': u'20120100'}]
        self.assertEqual(article.publication_date, '2012-01')

        article.data['article']['v65'] = [{u'_': u'20120000'}]
        self.assertEqual(article.publication_date, '2012')

    def test_without_publication_date(self):
        article = self.article

        del(article.data['article']['v65'])
        with self.assertRaises(KeyError):
            article.publication_date

    def test_volume(self):
        article = self.article

        self.assertEqual(article.volume, u'23')

    def test_without_volume(self):
        article = self.article

        del(article.data['article']['v31'])
        self.assertEqual(article.volume, None)

    def test_issue(self):
        article = self.article

        self.assertEqual(article.issue, u'3')

    def test_without_issue(self):
        article = self.article

        del(article.data['article']['v32'])
        self.assertEqual(article.issue, None)

    def test_supplement_volume(self):
        article = self.article

        article.data['article']['v131'] = [{u'_': u'test_suppl_volume'}]
        self.assertEqual(article.supplement_volume, u'test_suppl_volume')

    def test_without_supplement_volume(self):
        article = self.article

        self.assertEqual(article.supplement_volume, None)

    def test_supplement_issue(self):
        article = self.article

        article.data['article']['v132'] = [{u'_': u'test_suppl_issue'}]
        
        self.assertEqual(article.supplement_issue, u'test_suppl_issue')

    def test_without_suplement_issue(self):
        article = self.article

        self.assertEqual(article.supplement_issue, None)

    def test_start_page(self):
        article = self.article

        self.assertEqual(article.start_page, u'229')

    def test_without_start_page(self):
        article = self.article

        del(article.data['article']['v14'][0]['f'])
        self.assertEqual(article.start_page, None)

    def test_last_page(self):
        article = self.article

        self.assertEqual(article.end_page, u'232')

    def test_without_last_page(self):
        article = self.article

        del(article.data['article']['v14'][0]['l'])
        self.assertEqual(article.end_page, None)

    def test_without_pages(self):
        article = self.article

        del(article.data['article']['v14'])
        self.assertEqual(article.end_page, None)

    def test_doi(self):
        article = self.article

        self.assertEqual(article.doi, u'10.1590/S2179-975X2012005000004')

    def test_without_doi(self):
        article = self.article

        del(article.data['article']['doi'])
        self.assertEqual(article.doi, None)

    def test_publisher_id(self):
        article = self.article

        self.assertEqual(article.publisher_id, u'S2179-975X2011000300002')

    def test_without_publisher_id(self):
        article = self.article

        del(article.data['article']['v880'])
        with self.assertRaises(KeyError):
            article.publisher_id

    def test_document_type(self):
        article = self.article

        self.assertEqual(article.document_type, u'research-article')

    def test_without_document_type(self):
        article = self.article

        del(article.data['article']['v71'])
        self.assertEqual(article.document_type, u'undefined')

    def test_invalid_document_type(self):
        article = self.article

        article.data['article']['v71'] = [{u'_': u'invalid'}]
        self.assertEqual(article.document_type, u'undefined')

    def test_without_original_title(self):
        article = self.article

        del(article.data['article']['v12'])
        self.assertEqual(article.original_title(iso_format=None), None)

    def test_original_title_without_language_defined(self):
        article = self.article

        del(article.data['article']['v12'])

        article.data['article']['v12'] = [{u'_': u'article title 1'}, {u'_': u'article title 2'}]
        self.assertEqual(article.original_title(iso_format=None), None)

    def test_original_title_with_just_one_language_defined(self):
        article = self.article

        del(article.data['article']['v12'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v12'] = [{u'_': u'article title 1', u'l': u'en'}, 
                                          {u'_': u'article title 2'}]

        self.assertEqual(article.original_title(iso_format=None), u'article title 1')

    def test_original_title_with_language_defined(self):
        article = self.article

        del(article.data['article']['v12'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v12'] = [{u'_': u'article title 1', u'l': u'pt'}, 
                                          {u'_': u'article title 2', u'l': u'en'}]

        self.assertEqual(article.original_title(iso_format=None), u'article title 2')

    def test_original_title_with_language_defined_but_different_of_the_article_original_language(self):
        article = self.article

        del(article.data['article']['v12'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v12'] = [{u'_': u'article title 1', u'l': u'pt'}, 
                                          {u'_': u'article title 2', u'l': u'fr'}]

        self.assertEqual(article.original_title(iso_format=None), None)

    def test_without_original_abstract(self):
        article = self.article

        del(article.data['article']['v83'])
        self.assertEqual(article.original_abstract(iso_format=None), None)

    def test_original_abstract_without_language_defined(self):
        article = self.article

        del(article.data['article']['v83'])

        article.data['article']['v83'] = [{u'a': u'article abstract 1'}, {u'a': u'abstract title 2'}]
        self.assertEqual(article.original_abstract(iso_format=None), None)

    def test_original_abstract_with_just_one_language_defined(self):
        article = self.article

        del(article.data['article']['v83'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v83'] = [{u'a': u'article abstract 1', u'l': u'en'}, 
                                          {u'a': u'article abstract 2'}]

        self.assertEqual(article.original_abstract(iso_format=None), u'article abstract 1')

    def test_original_abstract_with_language_defined(self):
        article = self.article

        del(article.data['article']['v83'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v83'] = [{u'a': u'article abstract 1', u'l': u'pt'}, 
                                          {u'a': u'article abstract 2', u'l': u'en'}]

        self.assertEqual(article.original_abstract(iso_format=None), u'article abstract 2')

    def test_original_abstract_with_language_defined_but_different_of_the_article_original_language(self):
        article = self.article

        del(article.data['article']['v83'])

        article.data['article']['v40'][0]['_'] = u'en'
        article.data['article']['v83'] = [{u'a': u'article abstract 1', u'l': u'pt'}, 
                                          {u'a': u'article abstract 2', u'l': u'fr'}]

        self.assertEqual(article.original_abstract(iso_format=None), None)


    def test_without_authors(self):
        article = self.article

        del(article.data['article']['v10'])
        self.assertEqual(article.authors, None)

    def test_authors(self):
        article = self.article

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
        self.assertEqual(article.authors, authors)

    def test_author_with_two_affiliations(self):
        article = self.article
        
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
        
        self.assertEqual(article.authors, expected)

    def test_author_without_affiliations(self):
        article = self.article
        
        del(article.data['article']['v10'])
        article.data['article']['v10'] = [{u"s": "Gomes",
                                           u"r": "ND",
                                           u"_": "",
                                           u"n": "Caio Isola Dallevo do Amaral"}]
        expected = [{u'role': u'ND',
                     u'surname': u'Gomes',
                     u'given_names': u'Caio Isola Dallevo do Amaral'}]
        
        self.assertEqual(article.authors, expected)

    def test_author_without_surname_and_given_names(self):
        article = self.article
        
        del(article.data['article']['v10'])
        article.data['article']['v10'] = [{u"1": u"A01 A02",
                                           u"r": u"ND",
                                           u"_": u""}]
        expected = [{u'role': u'ND',
                     u'xref': [u'A01', u'A02'],
                     u'surname': u'',
                     u'given_names': u''}]
        
        self.assertEqual(article.authors, expected)

    def test_author_with_two_role(self):
        article = self.article
        
        del(article.data['article']['v10'])
        article.data['article']['v10'] = [{u"1": u"A01 A02",
                                           u"s": u"Gomes",
                                           u"_": u"",
                                           u"n": u"Caio Isola Dallevo do Amaral"}]
        expected = [{u'xref': [u'A01', u'A02'],
                     u'surname': u'Gomes',
                     u'given_names': u'Caio Isola Dallevo do Amaral'}]

        self.assertEqual(article.authors, expected)

    def test_without_affiliations(self):
        article = self.article

        del(article.data['article']['v70'])
        self.assertEqual(article.affiliations, None)

    def test_affiliations(self):
        article = self.article

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

        self.assertEqual(article.affiliations, affiliations)

    def test_affiliation_without_affiliation_name(self):
        article = self.article

        del(article.data['article']['v70'])

        article.data['article']['v70'] = [{u"c": u"Sorocaba",
                                           u"e": u"mcetra@ufscar.br",
                                           u"i": u"A03",
                                           u"1": u"Departamento de Ci\u00eancias Ambientais",
                                           u"p": u"BRAZIL",
                                           u"s": u"SP",
                                           u"z": u"18052-780"}]
        
        self.assertEqual(article.affiliations, None)

    def test_affiliation_just_with_affiliation_name(self):
        article = self.article

        del(article.data['article']['v70'])

        article.data['article']['v70'] = [{u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"}]

        expected = [{u'index': u'nd', u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'}]
        
        self.assertEqual(article.affiliations, expected)

    def test_without_scielo_domain(self):
        article = self.article

        del(article.data['title']['v690'])
        
        self.assertEqual(article.scielo_domain, None)

    def test_without_scielo_domain_title_v690(self):
        article = self.article
        
        self.assertEqual(article.scielo_domain, u'www.scielo.br')

    def test_without_scielo_domain_article_v69(self):
        article = self.article
        
        del(article.data['title']['v690'])

        article.data['article']['v69'] = [{u'_': u'http://www.scielo.br'}]
        self.assertEqual(article.scielo_domain, u'www.scielo.br')

    def test_without_scielo_domain_article_v69_and_title_v690(self):
        article = self.article
        
        article.data['title']['v690'] = [{u'_': u'http://www.scielo1.br'}]
        article.data['article']['v69'] = [{u'_': u'http://www.scielo2.br'}]

        self.assertEqual(article.scielo_domain, u'www.scielo1.br')

    def test_without_pdf_url(self):
        article = self.article

        del(article.data['title']['v690'])

        self.assertEqual(article.pdf_url, None)

    def test_pdf_url(self):
        article = self.article

        article.data['article']['v880'] = [{u'_': u'S2179-975X2011000300002'}]
        article.data['title']['v690'] = [{u'_': u'http://www.scielo.br'}]

        expected = u"http://www.scielo.br/scielo.php?script=sci_pdf&pid=S2179-975X2011000300002"

        self.assertEqual(article.pdf_url, expected)

    def test_without_html_url(self):
        article = self.article

        del(article.data['title']['v690'])

        self.assertEqual(article.html_url, None)

    def test_html_url(self):
        article = self.article

        article.data['article']['v880'] = [{u'_': u'S2179-975X2011000300002'}]
        article.data['title']['v690'] = [{u'_': u'http://www.scielo.br'}]

        expected = u"http://www.scielo.br/scielo.php?script=sci_arttext&pid=S2179-975X2011000300002"

        self.assertEqual(article.html_url, expected)

    def test_without_issue_url(self):
        article = self.article

        del(article.data['title']['v690'])

        self.assertEqual(article.issue_url, None)

    def test_issue_url(self):
        article = self.article

        article.data['article']['v880'] = [{u'_': u'S2179-975X2011000300002'}]
        article.data['title']['v690'] = [{u'_': u'http://www.scielo.br'}]

        expected = u"http://www.scielo.br/scielo.php?script=sci_issuetoc&pid=S2179-975X20110003"

        self.assertEqual(article.issue_url, expected)

    def test_without_journal_url(self):
        article = self.article

        del(article.data['title']['v690'])

        self.assertEqual(article.journal_url, None)

    def test_journal_url(self):
        article = self.article

        article.data['article']['v880'] = [{u'_': u'S2179-975X2011000300002'}]
        article.data['title']['v690'] = [{u'_': u'http://www.scielo.br'}]

        expected = u"http://www.scielo.br/scielo.php?script=sci_serial&pid=2179-975X"

        self.assertEqual(article.journal_url, expected)

    def test_without_keywords(self):
        article = self.article

        del(article.data['article']['v85'])

        self.assertEqual(article.keywords(iso_format='iso 639-2'), None)

    def test_keywords_without_subfield_k(self):
        article = self.article

        article.data['article']['v85'] = [{
                                            u"i": u"1",
                                            u"d": u"nd",
                                            u"_": u"",
                                            u"l": u"en"
                                          }]

        self.assertEqual(article.keywords(iso_format='iso 639-2'), None)

    def test_keywords_without_subfield_l(self):
        article = self.article

        article.data['article']['v85'] = [{
                                            u"i": u"1",
                                            u"d": u"nd",
                                            u"_": u"",
                                            u"k": u"keyword"
                                          }]

        self.assertEqual(article.keywords(iso_format='iso 639-2'), None)

    def test_keywords_with_undefined_language(self):
        article = self.article

        article.data['article']['v85'] = [{
                                            u"i": u"1",
                                            u"d": u"nd",
                                            u"_": u"",
                                            u"k": u"keyword",
                                            u"l": u"xx"
                                          }]

        expected  = {u'#undefined xx#': [u'keyword']}
        self.assertEqual(article.keywords(iso_format='iso 639-2'), expected)

    def test_keywords(self):
        article = self.article

        expected  = {'por': [u'Dojo',
                             u'esp\xe9cies ex\xf3ticas',
                             u'maturidade sexual',
                             u'sobreposi\xe7\xe3o de dieta',
                             u'Estado de S\xe3o Paulo'],
                     'eng': [u'Oriental weatherfish',
                             u'exotic species',
                             u'sexual maturity',
                             u'diet overlap',
                             u'S\xe3o Paulo State']
                        }

        self.assertEqual(article.keywords(iso_format='iso 639-2'), expected)

    def test_keywords_iso639_2(self):
        article = self.article

        article.data['article']['v85'] = [
                                            {
                                                "i": "1",
                                                "k": "keyword",
                                                "t": "m",
                                                "_": "",
                                                "l": "en"
                                            },
                                            {
                                                "i": "1",
                                                "k": "palavra-chave",
                                                "t": "m",
                                                "_": "",
                                                "l": "pt"
                                            },
                                         ]

        expected = {u'pt': [u'palavra-chave'], u'en': [u'keyword']}

        self.assertEqual(article.keywords(iso_format=None), expected)

    def test_without_citations(self):
        article = self.article

        del(article.data['citations'])

        self.assertEqual(article.citations, None)

    def test_translated_titles_without_v12(self):
        article = self.article        

        del(article.data['article']['v12'])

        self.assertEqual(article.translated_titles(), None)

    def test_translated_titles_iso639_2(self):
        article = self.article

        article.data['article']['v12'] = [
                                            {
                                                u"l": u"en",
                                                u"_": u"Article Title"
                                            },
                                            {
                                                u"l": u"pt",
                                                u"_": u"Título do Artigo"
                                            }
                                         ]

        expected = {u'por': u'Título do Artigo'}

        self.assertEqual(article.translated_titles(iso_format='iso 639-2'), expected)

    def test_translated_titles(self):
        article = self.article

        article.data['article']['v12'] = [
                                            {
                                                u"l": u"en",
                                                u"_": u"Article Title"
                                            },
                                            {
                                                u"l": u"pt",
                                                u"_": u"Título do Artigo"
                                            }
                                         ]

        expected = {u'pt': u'Título do Artigo'}

        self.assertEqual(article.translated_titles(iso_format=None), expected)


    def test_translated_abstracts_without_v83(self):
        article = self.article        

        del(article.data['article']['v83'])

        self.assertEqual(article.translated_abstracts(iso_format=None), None)

    def test_translated_abtracts_iso639_2(self):
        article = self.article

        article.data['article']['v83'] = [
                                            {
                                                u"l": u"en",
                                                u"a": u"Article Abstract"
                                            },
                                            {
                                                u"l": u"pt",
                                                u"a": u"Resumo do Artigo"
                                            }
                                         ]

        expected = {u'por': u'Resumo do Artigo'}

        self.assertEqual(article.translated_abstracts(iso_format='iso 639-2'), expected)

    def test_translated_abstracts(self):
        article = self.article

        article.data['article']['v83'] = [
                                            {
                                                u"l": u"en",
                                                u"a": u"Article Abstract"
                                            },
                                            {
                                                u"l": u"pt",
                                                u"a": u"Resumo do Artigo"
                                            }
                                         ]

        expected = {u'pt': u'Resumo do Artigo'}

        self.assertEqual(article.translated_abstracts(iso_format=None), expected)

    @unittest.skip
    def test_citations(self):
        article = self.article

        article.data['citations']

        #self.assertTrue(article.citations, Citations)


class CitationTest(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.json_citation = json.loads(open('%s/fixtures/sample_citation.json' % path).read())
        self.citation = Citation(self.json_citation)

    def test_index_number(self):
        citation = self.citation

        self.assertEqual(citation.index_number, 1)

    def test_without_index_number(self):
        citation = self.citation

        self.assertEqual(citation.index_number, None)

    def test_publication_type_article(self):
        citation = self.citation

        del(citation['v18'])
        citation['v12'][0]['_'] = u'it is an article title'

        self.assertEqual(citation.publication_type, u'article')


    def test_publication_type_book(self):
        citation = self.citation

        citation['v18'][0]['_'] = u'it is a book title'

        self.assertEqual(citation.publication_type, u'book')

    def test_publication_type_conference(self):
        citation = self.citation

        del(citation['v18'])
        citation['v53'][0]['_'] = u'it is a conference title'

        self.assertEqual(citation.publication_type, u'conference')

    def test_publication_type_thesis(self):
        citation = self.citation

        del(citation['v18'])
        citation['v45'][0]['_'] = u'it is a thesis title'

        self.assertEqual(citation.publication_type, u'thesis')

    def test_publication_type_undefined(self):
        citation = self.citation

        del(citation['v18'])

        self.assertEqual(citation.publication_type, u'undefined')

    def test_source_title_journal(self):
        citation = self.citation

        del(citation['v18'])

        self.assertEqual(citation.publication_type, u'undefined')







