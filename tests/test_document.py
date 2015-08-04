# coding: utf-8

import unittest
import json
import os
from xylose.scielodocument import Article, Citation, Journal, html_decode
from xylose import tools


class ToolsTests(unittest.TestCase):

    def test_get_language_without_iso_format(self):

        language = tools.get_language(u'xx', None)

        self.assertEqual(language, u'xx')

    def test_get_language_iso639_1_defined(self):

        language = tools.get_language(u'pt', u'iso 639-1')

        self.assertEqual(language, u'pt')

    def test_get_language_iso639_1_undefined(self):

        language = tools.get_language(u'xx', u'iso 639-1')

        self.assertEqual(language, u'#undefined xx#')

    def test_get_language_iso639_2_defined(self):

        language = tools.get_language(u'pt', u'iso 639-2')

        self.assertEqual(language, u'por')

    def test_get_language_iso639_2_undefined(self):

        language = tools.get_language(u'xx', u'iso 639-2')

        self.assertEqual(language, u'#undefined xx#')

    def test_get_publication_date_year_month_day(self):

        date = tools.get_publication_date('20120102')
        self.assertEqual(date, '2012-01-02')

    def test_get_publication_date_year_month(self):

        date = tools.get_publication_date('20120100')
        self.assertEqual(date, '2012-01')

    def test_get_publication_date_year(self):

        date = tools.get_publication_date('20120000')
        self.assertEqual(date, '2012')

    def test_get_publication_date_year_day(self):

        date = tools.get_publication_date('20120001')
        self.assertEqual(date, '2012')

    def test_get_publication_date_wrong_day(self):

        date = tools.get_publication_date('201201')
        self.assertEqual(date, '2012-01')

    def test_get_publication_date_wrong_day_month(self):

        date = tools.get_publication_date('2012')
        self.assertEqual(date, '2012')

    def test_get_publication_date_wrong_day_not_int(self):

        date = tools.get_publication_date('201201xx')
        self.assertEqual(date, '2012-01')

    def test_get_publication_date_wrong_day_month_not_int(self):

        date = tools.get_publication_date('2012xxxx')
        self.assertEqual(date, '2012')

    def test_get_publication_date_wrong_month_not_int(self):

        date = tools.get_publication_date('2012xx01')
        self.assertEqual(date, '2012')


class JournalTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/full_document.json' % path).read())
        self.journal = Journal(self.fulldoc['title'])

    def test_journal(self):
        journal = self.journal
        self.assertTrue(isinstance(journal, Journal))

    def test_scielo_issn(self):
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.scielo_issn, '2222-2222')

    def test_languages(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(sorted(journal.languages), [u'en', u'pt'])


    def test_languages_without_v350(self):
        del(self.fulldoc['title']['v350'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.languages, None)

    def test_current_without_v51(self):
        del(self.fulldoc['title']['v51'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.current_status, u'current')

    def test_status_without_v51(self):
        del(self.fulldoc['title']['v51'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [(u'2011-03-25', u'current')])

    def test_current_status(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.current_status, u'current')

    def test_status(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [(u'2011-04', u'current')])

    def test_current_status_some_changes(self):

        v51 = [
            {'a': '19981126', 'c': "20020000", 'b': "C", 'd': "D", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        journal.current_status

        self.assertEqual(journal.current_status, u'deceased')

    def test_status_some_changes(self):

        v51 = [
            {'a': '19981126', 'c': "20020000", 'b': "C", 'd': "D", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [('1998-11-26', 'current'), ('2002', 'deceased')])

    def test_status_lots_of_changes(self):

        v51 = [
            {'a': "20100800", 'b': "C", '_': "" },
            {'a': "19981016", 'c': "20050100", 'b': "C", 'd': "S", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status, [(u'2010-08', u'current')])

    def test_status_lots_of_changes(self):

        v51 = [
            {'a': "20100800", 'b': "C", '_': "" },
            {'a': "19981016", 'c': "20050100", 'b': "C", 'd': "S", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [('1998-10-16', 'current'), ('2005-01', 'suspended'), ('2010-08', 'current')])

    def test_status_lots_of_changes_study_case_1(self):

        v51 = [
            {u'a': u'20140805', u'c': u'20140805', u'b': u'?', u'd': u'C', u'_': u''}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [(u'2014-08-05', 'current'), (u'2014-08-05', 'inprogress')])


    def test_current_status_lots_of_changes_study_case_1(self):

        v51 = [
            {u'a': u'20140805', u'c': u'20140805', u'b': u'?', u'd': u'C', u'_': u''}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.current_status, u'current')

    def test_creation_date(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.creation_date, '2011-03-25')

    def test_update_date(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.update_date, '2012-08-24')

    def test_load_issn_with_v935_without_v35(self):
        del(self.fulldoc['title']['v35'])
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, None)
        self.assertEqual(journal.electronic_issn, None)

    def test_load_issn_without_v935_without_v35(self):
        del(self.fulldoc['title']['v35'])
        del(self.fulldoc['title']['v935'])
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, None)

    def test_load_issn_without_v935_and_v35_PRINT(self):
        self.fulldoc['title']['v35'] = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        del(self.fulldoc['title']['v935'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, u'2222-2222')
        self.assertEqual(journal.electronic_issn, None)

    def test_load_issn_without_v935_and_v35_ONLINE(self):
        self.fulldoc['title']['v35'] = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        del(self.fulldoc['title']['v935'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, None)
        self.assertEqual(journal.electronic_issn, u'2222-2222')

    def test_load_issn_with_v935_and_v35_PRINT(self):
        self.fulldoc['title']['v35'] = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, u'3333-3333')
        self.assertEqual(journal.electronic_issn, u'2222-2222')

    def test_load_issn_with_v935_and_v35_ONLINE(self):
        self.fulldoc['title']['v35'] = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, u'2222-2222')
        self.assertEqual(journal.electronic_issn, u'3333-3333')

    def test_load_issn_with_v935_equal_v400_and_v35_PRINT(self):
        self.fulldoc['title']['v35'] = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, u'3333-3333')
        self.assertEqual(journal.electronic_issn, None)

    def test_load_issn_with_v935_equal_v400_and_v35_ONLINE(self):
        self.fulldoc['title']['v35'] = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, None)
        self.assertEqual(journal.electronic_issn, u'3333-3333')

    def test_any_issn_priority_electronic(self):
        self.fulldoc['title']['v35'] = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.any_issn(priority='electronic'), u'3333-3333')

    def test_any_issn_priority_electronic_without_electronic(self):
        self.fulldoc['title']['v35'] = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.any_issn(priority='electronic'), u'3333-3333')

    def test_any_issn_priority_print(self):
        self.fulldoc['title']['v35'] = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.any_issn(priority='print'), u'2222-2222')

    def test_any_issn_priority_print_without_print(self):
        self.fulldoc['title']['v35'] = [{u'_': u'ONLINE'}]
        self.fulldoc['title']['v400'] = [{u'_': u'3333-3333'}]
        self.fulldoc['title']['v935'] = [{u'_': u'3333-3333'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.any_issn(priority='print'), u'3333-3333')

    def test_permission_t0(self):
        self.fulldoc['title']['v541'] = [{'_': 'BY-NC'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions['id'], 'by-nc/4.0')

    def test_permission_t1(self):
        del(self.fulldoc['title']['v541'])

        self.fulldoc['title']['v540'][0] = {
            "t": '<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/80x15.png" /></a> Todo el contenido de la revista, excepto dónde está identificado, está bajo una <a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es">Licencia Creative Commons</a>',
            '_': "",
            'l': "en"
        }

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions['id'], 'by/3.0')

    def test_permission_t2(self):
        del(self.fulldoc['title']['v541'])
        
        self.fulldoc['license'] = 'by-nc/3.0'

        article = Article(self.fulldoc)

        self.assertEqual(article.permissions['id'], 'by-nc/3.0')
        self.assertEqual(article.permissions['url'], 'http://creativecommons.org/licenses/by-nc/3.0/')

    def test_permission_t3(self):

        self.fulldoc['article']['v540'] = [
            {
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u"en"
            },{
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u'es'
            },{
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u'pt'
            }
        ]

        article = Article(self.fulldoc)

        self.assertEqual(article.permissions['id'], 'by-nc/4.0')
        self.assertEqual(article.permissions['url'], 'http://creativecommons.org/licenses/by-nc/4.0/')

    def test_permission_t4(self):

        self.fulldoc['title']['v540'] = [
            {
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u"en"
            },{
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u'es'
            },{
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u'pt'
            }
        ]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions['id'], 'by-nc/4.0')
        self.assertEqual(journal.permissions['url'], 'http://creativecommons.org/licenses/by-nc/4.0/')

    def test_permission_id(self):
        del(self.fulldoc['title']['v541'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions['id'], 'by-nc/3.0')


    def test_permission_url(self):
        del(self.fulldoc['title']['v541'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions['url'], 'http://creativecommons.org/licenses/by-nc/3.0/')

    def test_permission_text(self):
        del(self.fulldoc['title']['v541'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions['text'], u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc/3.0/80x15.png" /></a> All the contents of this journal, except where otherwise noted, is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/">Creative Commons Attribution License</a>')

    def test_permission_without_v540(self):
        del(self.fulldoc['title']['v541'])

        del(self.fulldoc['title']['v540'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions, None)

    def test_permission_without_v540_t(self):
        del(self.fulldoc['title']['v541'])

        del(self.fulldoc['title']['v540'])

        self.fulldoc['title']['v540'] = [{'_': ''}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.permissions, None)

    def test_without_scielo_domain(self):
        journal = self.journal

        del(journal.data['v690'])

        self.assertEqual(journal.scielo_domain, None)

    def test_without_scielo_domain_title_v690(self):
        journal = self.journal

        self.assertEqual(journal.scielo_domain, u'www.scielo.br')

    def test_collection_acronym(self):

        self.fulldoc['title']['v992'] = [{'_': 'scl'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.collection_acronym, u'scl')

    def test_without_journal_url(self):
        journal = self.journal

        del(journal.data['v690'])

        self.assertEqual(journal.url(), None)

    def test_journal_url(self):
        journal = self.journal

        expected = u"http://www.scielo.br/scielo.php?script=sci_serial&pid=2179-975X&lng=en"

        self.assertEqual(journal.url(), expected)

    def test_wos_subject_areas(self):
        self.fulldoc['title']['v854'] = [{u'_': u'MARINE & FRESHWATER BIOLOGY'}, {u'_': u'OCEANOGRAPHY'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.wos_subject_areas, [u'MARINE & FRESHWATER BIOLOGY', u'OCEANOGRAPHY'])

    def test_without_wos_subject_areas(self):
        del(self.fulldoc['title']['v854'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.wos_subject_areas, None)

    def test_journal_abbreviated_title(self):
        self.fulldoc['title']['v150'] = [{u'_': u'It is the journal title'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.abbreviated_title, u'It is the journal title')

    def test_without_journal_abbreviated_title(self):
        del(self.fulldoc['title']['v150'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.abbreviated_title, None)

    def test_subject_areas(self):
        self.fulldoc['title']['v441'] = [{u'_': u'HEALTH SCIENCES'}, {u'_': u'BIOLOGICAL SCIENCES'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.subject_areas, [u'HEALTH SCIENCES', u'BIOLOGICAL SCIENCES'])

    def test_without_subject_areas(self):
        del(self.fulldoc['title']['v441'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.subject_areas, None)

    def test_wos_citation_indexes(self):
        self.fulldoc['title']['v851'] = [{u'_': u'SCIE'}]
        self.fulldoc['title']['v852'] = [{u'_': u'SSCI'}]
        self.fulldoc['title']['v853'] = [{u'_': u'AHCI'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.wos_citation_indexes, [u'SCIE', u'SSCI', u'AHCI'])

    def test_without_wos_citation_indexes(self):

        journal = Journal(self.fulldoc)

        self.assertEqual(journal.wos_citation_indexes, None)

    def test_publisher_name(self):
        journal = self.journal

        self.assertEqual(journal.publisher_name, u'Associação Brasileira de Limnologia')

    def test_without_publisher_name(self):
        journal = self.journal

        del(journal.data['v480'])
        self.assertEqual(journal.publisher_name, None)

    def test_publisher_loc(self):
        journal = self.journal

        self.assertEqual(journal.publisher_loc, u'Rio Claro')

    def test_without_publisher_loc(self):
        journal = self.journal

        del(journal.data['v490'])
        self.assertEqual(journal.publisher_loc, None)

    def test_journal_title(self):
        journal = self.journal

        self.assertEqual(journal.title, u'Acta Limnologica Brasiliensia')

    def test_without_journal_title(self):
        journal = self.journal

        del(journal.data['v100'])
        self.assertEqual(journal.title, None)

    def test_journal_title_nlm(self):
        self.fulldoc['title']['v421'] = [{u'_': u'Acta Limnologica Brasiliensia NLM'}]
        
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.title_nlm, u'Acta Limnologica Brasiliensia NLM')

    def test_without_journal_title_nlm(self):
        journal = self.journal

        del(journal.data['v100'])
        self.assertEqual(journal.title_nlm, None)

    def test_journal_acronym(self):
        journal = self.journal

        self.assertEqual(journal.acronym, u'alb')

    def test_without_journal_acronym(self):
        journal = self.journal

        del(journal.data['v68'])
        self.assertEqual(journal.acronym, None)


class ArticleTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/full_document.json' % path).read())
        self.article = Article(self.fulldoc)

    def test_article(self):
        article = self.article
        self.assertTrue(isinstance(article, Article))

    def test_original_section_field_v49(self):
        self.fulldoc['section'] = {u'en': u'label en', u'pt': u'label pt', u'es': 'label es'}

        article = Article(self.fulldoc)

        self.assertEqual(article.original_section(), u'label en')

    def test_translated_section_field_v49(self):
        self.fulldoc['section'] = {u'en': u'label en', u'pt': u'label pt', u'es': 'label es'}

        article = Article(self.fulldoc)

        self.assertEqual(sorted([k+v for k, v in article.translated_section().items()]), [u'eslabel es', 'ptlabel pt'])

    def test_section_field_v49(self):
        self.fulldoc['section'] = {u'en': u'label en', u'pt': u'label pt'}

        article = Article(self.fulldoc)

        self.assertEqual(sorted(article.section.keys()), [u'en', u'pt'])

    def test_section_nd_field_v49(self):

        article = Article(self.fulldoc)

        self.assertEqual(article.section, None)

    def test_section_without_field_v49(self):

        del(self.fulldoc['article']['v49'])

        article = Article(self.fulldoc)

        self.assertEqual(article.section, None)

    def test_secion_code_field_v49(self):
        self.fulldoc['article']['v49'] = [{'_': 'RSP10'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.section_code, 'RSP10')

    def test_section_code_nd_field_v49(self):

        article = Article(self.fulldoc)

        self.assertEqual(article.section_code, None)

    def test_section_code_without_field_v49(self):

        del(self.fulldoc['article']['v49'])

        article = Article(self.fulldoc)

        self.assertEqual(article.section_code, None)

    def test_languages_field_v40(self):

        article = Article(self.fulldoc)

        self.assertEqual(sorted(article.languages()), [u'en'])

    def test_original_html_field_body(self):

        article = Article(self.fulldoc)

        self.assertEqual(article.original_html(), u'Body EN')

    def test_translated_htmls_field_body(self):

        article = Article(self.fulldoc)

        self.assertEqual(sorted([k+v for k, v in article.translated_htmls().items()]), [u'esBody ES', u'ptBody PT'])

    def test_issue_label_field_v4(self):

        article = Article(self.fulldoc)

        self.assertEqual(article.issue_label, u'v23n3')


    def test_issue_label_without_field_v4(self):

        del(self.fulldoc['article']['v4'])

        article = Article(self.fulldoc)

        self.assertEqual(article.issue_label, None)

    def test_fulltexts_field_fulltexts(self):

        self.fulldoc['fulltexts'] = {
            u'pdf': {
                'pt': 'url_pdf_pt',
                'es': 'url_pdf_es'
            },
            u'html': {
                'pt': 'url_html_pt',
                'es': 'url_html_es',
            }

        }

        article = Article(self.fulldoc)

        ft = article.fulltexts()

        self.assertEqual(sorted(ft.keys()), [u'html', u'pdf'])
        self.assertEqual(sorted(ft['pdf'].keys()), [u'es', u'pt'])
        self.assertEqual(sorted(ft['html'].keys()), [u'es', u'pt'])

    def test_fulltexts_without_field_fulltexts(self):

        article = Article(self.fulldoc)

        ft = article.fulltexts()

        self.assertEqual(sorted(ft.keys()), [u'html', u'pdf'])
        self.assertEqual(sorted(ft['html'].keys()), [u'en'])
        self.assertEqual(ft['html']['en'], u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S2179-975X2011000300002&lng=en&tlng=en')
        self.assertEqual(sorted(ft['pdf'].keys()), [u'en'])
        self.assertEqual(ft['pdf']['en'], u'http://www.scielo.br/pdf/alb/v23n3/alb_aop_230302.pdf')

    def test_languages_field_fulltexts(self):

        self.fulldoc['fulltexts'] = {
            u'pdf': {
                'pt': 'url_pdf_pt',
                'es': 'url_pdf_es'
            },
            u'html': {
                'pt': 'url_html_pt',
                'es': 'url_html_es',
            }

        }

        article = Article(self.fulldoc)

        self.assertEqual(sorted(article.languages()), [u'en', u'es', u'pt'])

    def test_collection_name_brazil(self):
        self.fulldoc['collection'] = u'scl'

        article = Article(self.fulldoc)

        self.assertEqual(article.collection_name, u'Brazil')

    def test_collection_name_undefined(self):
        self.fulldoc['collection'] = u'xxx'

        article = Article(self.fulldoc)

        self.assertEqual(article.collection_name, u'Undefined: xxx')

    def test_collection_acronym(self):

        article = Article(self.fulldoc)

        self.assertEqual(article.collection_acronym, u'scl')

    def test_collection_acronym_priorizing_collection(self):
        self.fulldoc['collection'] = u'yyy'
        self.fulldoc['article']['v992'] = [{u'_': u'xxx'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.collection_acronym, u'yyy')

    def test_collection_acronym_retrieving_v992(self):
        del(self.fulldoc['collection'])
        self.fulldoc['article']['v992'] = [{u'_': u'xxx'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.collection_acronym, u'xxx')

    def test_without_collection_acronym(self):
        del(self.fulldoc['collection'])

        article = Article(self.fulldoc)

        self.assertEqual(article.collection_acronym, None)

    def test_subject_areas(self):
        self.fulldoc['title']['v441'] = [{u'_': u'HEALTH SCIENCES'}, {u'_': u'BIOLOGICAL SCIENCES'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.journal.subject_areas, [u'HEALTH SCIENCES', u'BIOLOGICAL SCIENCES'])

    def test_without_subject_areas(self):
        del(self.fulldoc['title']['v441'])

        article = Article(self.fulldoc)

        self.assertEqual(article.journal.subject_areas, None)

    def test_wos_citation_indexes(self):
        self.fulldoc['title']['v851'] = [{u'_': u'SCIE'}]
        self.fulldoc['title']['v852'] = [{u'_': u'SSCI'}]
        self.fulldoc['title']['v853'] = [{u'_': u'AHCI'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.journal.wos_citation_indexes, [u'SCIE', u'SSCI', u'AHCI'])

    def test_without_wos_citation_indexes(self):

        article = Article(self.fulldoc)

        self.assertEqual(article.journal.wos_citation_indexes, None)

    def test_file_code(self):
        article = Article(self.fulldoc)

        self.assertEqual(article.file_code(), 'alb_aop_230302')

    def test_file_code_crazy_slashs_1(self):
        self.fulldoc['article']['v702'] = [{u'_': u'file://r\\\\x//y//z\\\\file.html'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.file_code(), 'file')

    def test_file_code_crazy_slashs_2(self):
        self.fulldoc['article']['v702'] = [{"_": "rsp/v47n4/0034-8910-rsp-47-04-0675.xml"}]

        article = Article(self.fulldoc)

        self.assertEqual(article.file_code(), '0034-8910-rsp-47-04-0675')

    def test_wos_subject_areas(self):
        self.fulldoc['title']['v854'] = [{u'_': u'MARINE & FRESHWATER BIOLOGY'}, {u'_': u'OCEANOGRAPHY'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.journal.wos_subject_areas, [u'MARINE & FRESHWATER BIOLOGY', u'OCEANOGRAPHY'])

    def test_without_wos_subject_areas(self):
        del(self.fulldoc['title']['v854'])

        article = Article(self.fulldoc)

        self.assertEqual(article.journal.wos_subject_areas, None)

    def test_journal_abbreviated_title(self):
        self.fulldoc['title']['v150'] = [{u'_': u'It is the journal title'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.journal.abbreviated_title, u'It is the journal title')

    def test_without_journal_abbreviated_title(self):
        del(self.fulldoc['title']['v150'])
        self.assertEqual(self.article.journal.abbreviated_title, None)

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

        self.assertEqual(article.journal.publisher_name, u'Associação Brasileira de Limnologia')

    def test_without_publisher_name(self):
        article = self.article

        del(article.data['title']['v480'])
        self.assertEqual(article.journal.publisher_name, None)

    def test_publisher_loc(self):
        article = self.article

        self.assertEqual(article.journal.publisher_loc, u'Rio Claro')

    def test_without_publisher_loc(self):
        article = self.article

        del(article.data['title']['v490'])
        self.assertEqual(article.journal.publisher_loc, None)

    def test_journal_title(self):
        article = self.article

        self.assertEqual(article.journal.title, u'Acta Limnologica Brasiliensia')

    def test_without_journal_title(self):
        article = self.article

        del(article.data['title']['v100'])
        self.assertEqual(article.journal.title, None)

    def test_journal_acronym(self):
        article = self.article

        self.assertEqual(article.journal.acronym, u'alb')

    def test_without_journal_acronym(self):
        article = self.article

        del(article.data['title']['v68'])
        self.assertEqual(article.journal.acronym, None)

    def test_publication_date(self):
        article = self.article

        article.data['article']['v65'] = [{u'_': u'20120102'}]
        self.assertEqual(article.publication_date, '2012-01-02')

    def test_without_publication_date(self):
        article = self.article

        del(article.data['article']['v65'])
        with self.assertRaises(KeyError):
            article.publication_date

    def test_processing_date(self):
        article = self.article

        article.data['article']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(article.processing_date, '2012-04-19')

    def test_without_processing_date(self):
        article = self.article

        del(article.data['article']['v91'])
        with self.assertRaises(KeyError):
            article.processing_date

    def test_receive_date(self):
        article = self.article

        article.data['article']['v112'] = [{u'_': u'20110706'}]
        self.assertEqual(article.receive_date, '2011-07-06')

    def test_whitwout_receive_date(self):
        article = self.article

        del(article.data['article']['v112'])
        self.assertEqual(article.receive_date, None)

    def test_acceptance_date(self):
        article = self.article

        article.data['article']['v114'] = [{u'_': u'20111214'}]
        self.assertEqual(article.acceptance_date, '2011-12-14')

    def test_whitwout_acceptance_date(self):
        article = self.article

        del(article.data['article']['v114'])
        self.assertEqual(article.acceptance_date, None)

    def test_review_date(self):
        article = self.article

        article.data['article']['v116'] = [{u'_': u'20111215'}]
        self.assertEqual(article.review_date, '2011-12-15')

    def test_whitwout_review_date(self):
        article = self.article

        self.assertEqual(article.review_date, None)

    def test_ahead_publication_date(self):
        article = self.article

        article.data['article']['v223'] = [{u'_': u'20131125'}]
        self.assertEqual(article.ahead_publication_date, '2013-11-25')

    def test_whitwout_ahead_publication_date(self):
        article = self.article

        del(article.data['article']['v223'])
        self.assertEqual(article.ahead_publication_date, None)

    def test_publication_contract(self):
        self.fulldoc['article']['v60'] = [{u'_': u'2009/53056-8'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.contract, u'2009/53056-8')

    def test_without_publication_contract(self):
        del(self.fulldoc['article']['v60'])
        self.assertEqual(self.article.contract, None)

    def test_project_name(self):
        self.fulldoc['article']['v59'] = [{u'_': u'Projeto ABCD'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.project_name, u'Projeto ABCD')

    def test_without_project_name(self):
        self.assertEqual(self.article.project_name, None)

    def test_project_sponsors(self):
        self.fulldoc['article']['v58'] = [{u'_': u'Sponsor name', u'd': u'divisão 1'},
                                          {u'_': u'Sponsor name'},
                                          {u'd': u'divisão 1'}]

        article = Article(self.fulldoc)

        expected = [{u'orgname': u'Sponsor name', u'orgdiv': u'divisão 1'},
                    {u'orgname': u'Sponsor name'},
                    {u'orgdiv': u'divisão 1'}]

        self.assertEqual(article.project_sponsor, expected)

    def test_without_project_sponsor(self):
        del(self.fulldoc['article']['v58'])
        self.assertEqual(self.article.project_sponsor, None)

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

    def test_start_page_loaded_through_xml(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'',
                u'l': u'122'
            },
            {
                u'_': u'',
                u'f': u'110'
            }
        ]

        self.assertEqual(article.start_page, u'110')

    def test_start_page_loaded_crazy_legacy_way_1(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'110-122',
            }
        ]

        self.assertEqual(article.start_page, u'110')

    def test_start_page_loaded_crazy_legacy_way_2(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'122-110',
            }
        ]

        self.assertEqual(article.start_page, u'110')

    def test_last_page(self):
        article = self.article

        self.assertEqual(article.end_page, u'232')

    def test_without_last_page(self):
        article = self.article

        del(article.data['article']['v14'][0]['l'])
        self.assertEqual(article.end_page, None)

    def test_end_page_loaded_through_xml(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'',
                u'f': u'110'
            },
            {
                u'_': u'',
                u'l': u'122'
            }
        ]

        self.assertEqual(article.end_page, u'122')

    def test_end_page_loaded_crazy_legacy_way_1(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'110-122',
            }
        ]

        self.assertEqual(article.end_page, u'122')

    def test_end_page_loaded_crazy_legacy_way_2(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'122-110',
            }
        ]

        self.assertEqual(article.end_page, u'122')

    def test_without_pages(self):
        article = self.article

        del(article.data['article']['v14'])
        self.assertEqual(article.end_page, None)

    def test_doi(self):
        article = self.article

        article.data['doi'] = u'10.1590/S2179-975X2012005000004'

        self.assertEqual(article.doi, u'10.1590/S2179-975X2012005000004')

    def test_doi_v237(self):
        article = self.article

        article.data['article']['v237'] = [{'_': u'10.1590/S2179-975X2012005000004'}]

        self.assertEqual(article.doi, u'10.1590/S2179-975X2012005000004')


    def test_doi_clean_1(self):
        article = self.article

        article.data['doi'] = u'http://www.crossref.org/10.1590/S2179-975X2012005000004'

        self.assertEqual(article.doi, u'10.1590/S2179-975X2012005000004')


    def test_doi_clean_2(self):
        article = self.article

        article.data['doi'] = u'doi: 10.4322/actalb.02203010'

        self.assertEqual(article.doi, u'10.4322/actalb.02203010')

    def test_without_doi(self):
        article = self.article

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


    def test_without_corporative_authors(self):
        article = self.article

        self.assertEqual(article.corporative_authors, None)

    def test_corporative_authors(self):
        article = self.article

        article.data['article']['v11'] = [{u'_': u'Orgname 1', u'd': u'divisão 1'},
                                          {u'_': u'Orgname 2'},
                                          {u'd': u'divisão 1'}]

        expected = [{u'orgname': u'Orgname 1',
                     u'orgdiv': u'divisão 1'},
                    {u'orgname': u'Orgname 2'},
                    {u'orgdiv': u'divisão 1'}]

        self.assertEqual(article.corporative_authors, expected)

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

    def test_first_author_without_author(self):
        article = self.article

        del(article.data['article']['v10'])
        self.assertEqual(article.first_author, None)

    def test_first_author(self):
        article = self.article

        expected_author = {u'role': u'ND',
                           u'xref': [u'A01'],
                           u'surname': u'Gomes',
                           u'given_names': u'Caio Isola Dallevo do Amaral'}

        self.assertEqual(article.first_author, expected_author)

    def test_mixed_affiliations_1(self):
        article = self.article

        article.data['article']['v240'] = [
            {
                u"i": u"A01",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A02",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            }
        ]

        article.data['article']['v70'] = [
            {
                u"i": u"A01",
                u"p": u"BRAZIL",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A02",
                u"p": u"BRAZIL",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A03",
                u"p": u"US",
                u"_": u"University of Florida Not Normalized"
            }
        ]

        amc = article.mixed_affiliations

        result_index = ''.join([i['index'] for i in sorted(amc,  key=lambda k: k['index'])])
        result_country = ''.join([i['country'] for i in sorted(amc,  key=lambda k: k['index'])])
        result_status = ''.join([str(i['normalized']) for i in sorted(amc,  key=lambda k: k['index'])])

        self.assertEqual(result_index, 'A01A02A03')
        self.assertEqual(result_country, 'BrazilBrazilUS')
        self.assertEqual(result_status, 'TrueTrueFalse')

    def test_without_normalized_affiliations(self):
        article = self.article

        self.assertEqual(article.normalized_affiliations, None)

    def test_normalized_affiliations_without_p(self):
        article = self.article

        article.data['article']['v240'] = [
            {
                u"i": u"A01",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A02",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A03",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A04",
                u"p": u"BR",
                u"_": u"PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO"
            }
        ]

        affiliations = [
            {u'index': u'A01',
             u'country_iso_3166': u'BR',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
             u'country': u'Brazil'},
            {u'index': u'A02',
             u'country_iso_3166': u'BR',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
             u'country': u'Brazil'},
            {u'index': u'A03',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'},
            {u'index': u'A04',
             u'country_iso_3166': u'BR',
             u'institution': u'PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO',
             u'country': u'Brazil'}
        ]

        self.assertEqual(article.normalized_affiliations, affiliations)

    def test_normalized_affiliations_undefined_ISO_3166_CODE(self):
        article = self.article

        article.data['article']['v240'] = [
            {
                u"i": u"A01",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A02",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A03",
                u"p": u"XX",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A04",
                u"p": u"BR",
                u"_": u"PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO"
            }
        ]

        affiliations = [
            {u'index': u'A01',
             u'country_iso_3166': u'BR',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
             u'country': u'Brazil'},
            {u'index': u'A02',
             u'country_iso_3166': u'BR',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
             u'country': u'Brazil'},
            {u'index': u'A03',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'},
            {u'index': u'A04',
             u'country_iso_3166': u'BR',
             u'institution': u'PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO',
             u'country': u'Brazil'}
        ]

        self.assertEqual(article.normalized_affiliations, affiliations)

    def test_normalized_affiliations(self):
        article = self.article

        article.data['article']['v240'] = [
            {
                u"i": u"A01",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A02",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A03",
                u"p": u"BR",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A04",
                u"p": u"BR",
                u"_": u"PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO"
            }
        ]

        affiliations = [
            {u'index': u'A01',
             u'country_iso_3166': u'BR',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
             u'country': u'Brazil'},
            {u'index': u'A02',
             u'country_iso_3166': u'BR',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
             u'country': u'Brazil'},
            {u'index': u'A03',
             u'country_iso_3166': u'BR',
             u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS',
             u'country': u'Brazil'},
            {u'index': u'A04',
             u'country_iso_3166': u'BR',
             u'institution': u'PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO',
             u'country': u'Brazil'}
        ]

        self.assertEqual(article.normalized_affiliations, affiliations)

    def test_without_affiliations(self):
        article = self.article

        del(article.data['article']['v70'])
        self.assertEqual(article.affiliations, None)

    def test_affiliations(self):
        article = self.article
        expected = [
            {
                'index': u'A01',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'email': u'caioisola@yahoo.com.br',
                'state': u'SP',
                'orgdiv1': u'Departamento de Ci\xeancias Biol\xf3gicas',
                'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'
            }, {
                'index': u'A02',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'email': u'alex_peressin@yahoo.com.br',
                'state': u'SP',
                'orgdiv1': u'Programa de P\xf3s-Gradua\xe7\xe3o em Diversidade Biol\xf3gica e Conserva\xe7\xe3o',
                'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'
            }, {
                'index': u'A03',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'email': u'mcetra@ufscar.br',
                'state': u'SP',
                'orgdiv1': u'Departamento de Ci\xeancias Ambientais',
                'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'
            }, {
                'index': u'A04',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'email': u'vbarrella@pucsp.br',
                'state': u'SP',
                'orgdiv1': u'Laborat\xf3rio de Ecossistemas Aqu\xe1ticos',
                'institution': u'PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO'
            }
        ]

        self.assertEqual(article.affiliations, expected)

    def test_affiliation_without_affiliation_name(self):
        article = self.article

        del(article.data['article']['v70'])

        article.data['article']['v70'] = [{u"c": u"Sorocaba",
                                           u"e": u"mcetra@ufscar.br",
                                           u"i": u"A03",
                                           u"1": u"Departamento de Ci\u00eancias Ambientais 1",
                                           u"2": u"Departamento de Ci\u00eancias Ambientais 2",
                                           u"p": u"BRAZIL",
                                           u"s": u"SP",
                                           u"z": u"18052-780"}]

        expected = [
            {
                'index': u'A03',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'orgdiv2': u'Departamento de Ci\xeancias Ambientais 2',
                'email': u'mcetra@ufscar.br', 'state': u'SP',
                'orgdiv1': u'Departamento de Ci\xeancias Ambientais 1',
                'institution': ''
            }
        ]

        self.assertEqual(article.affiliations, expected)

    def test_affiliation_just_with_affiliation_name(self):
        article = self.article

        del(article.data['article']['v70'])

        article.data['article']['v70'] = [{u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"}]

        expected = [{u'index': u'nd', u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'}]

        self.assertEqual(article.affiliations, expected)

    def test_without_scielo_domain(self):
        article = self.article

        del(article.data['title']['v690'])
        del(article.data['collection'])

        self.assertEqual(article.scielo_domain, None)

    def test_without_scielo_domain_title_v690(self):
        article = self.article

        self.assertEqual(article.scielo_domain, u'www.scielo.br')

    def test_without_scielo_domain_article_v69(self):
        article = self.article

        del(article.data['title']['v690'])

        article.data['article']['v69'] = [{u'_': u'http://www.scielo.br'}]
        self.assertEqual(article.scielo_domain, u'www.scielo.br')

    def test_without_scielo_domain_article_v69_and_with_title_v690(self):
        article = self.article

        del(article.data['collection'])

        article.data['title']['v690'] = [{u'_': u'http://www.scielo1.br'}]
        article.data['article']['v69'] = [{u'_': u'http://www.scielo2.br'}]

        self.assertEqual(article.scielo_domain, u'www.scielo1.br')

    def test_without_pdf_url(self):
        article = self.article

        del(article.data['title']['v690'])
        del(article.data['collection'])

        self.assertEqual(article.pdf_url(), None)

    def test_pdf_url(self):
        article = self.article

        article.data['article']['v880'] = [{u'_': u'S2179-975X2011000300002'}]

        expected = u"http://www.scielo.br/scielo.php?script=sci_pdf&pid=S2179-975X2011000300002&lng=en&tlng=en"

        self.assertEqual(article.pdf_url(), expected)

    def test_without_html_url(self):
        article = self.article

        del(article.data['title']['v690'])
        del(article.data['collection'])

        self.assertEqual(article.html_url(), None)

    def test_html_url(self):
        article = self.article

        article.data['article']['v880'] = [{u'_': u'S2179-975X2011000300002'}]

        expected = u"http://www.scielo.br/scielo.php?script=sci_arttext&pid=S2179-975X2011000300002&lng=en&tlng=en"

        self.assertEqual(article.html_url(), expected)

    def test_without_issue_url(self):
        article = self.article

        del(article.data['title']['v690'])
        del(article.data['collection'])

        self.assertEqual(article.issue_url(), None)

    def test_issue_url(self):
        article = self.article

        article.data['article']['v880'] = [{u'_': u'S2179-975X2011000300002'}]

        expected = u"http://www.scielo.br/scielo.php?script=sci_issuetoc&pid=S2179-975X20110003&lng=en"

        self.assertEqual(article.issue_url(), expected)

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

    def test_thesis_degree(self):
        self.fulldoc['article']['v51']  = [{u'_': u'Degree 1'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.thesis_degree, u'Degree 1')

    def test_without_thesis_degree(self):
        article = Article(self.fulldoc)

        self.assertEqual(article.thesis_degree, None)

    def test_thesis_organization(self):
        self.fulldoc['article']['v52']  = [{u'_': u'It is the thesis organization'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.thesis_organization, [{u'name': u'It is the thesis organization'}])

    def test_thesis_organization_and_division(self):
        self.fulldoc['article']['v52']  = [{u'_': u'It is the thesis organization', u'd': u'divisão 1'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.thesis_organization, [{u'name': u'It is the thesis organization',
                                                        u'division': u'divisão 1'}])

    def test_thesis_organization_without_name(self):
        self.fulldoc['article']['v52']  = [{u'd': u'divisão 1'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.thesis_organization, [{u'division': u'divisão 1'}])

    def test_without_thesis_organization(self):
        article = Article(self.fulldoc)

        self.assertEqual(article.thesis_organization, None)

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

        del(citation.data['v701'])

        self.assertEqual(citation.index_number, None)

    def test_publication_type_article(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publication_type, u'article')


    def test_publication_type_book(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publication_type, u'book')

    def test_publication_type_conference(self):
        json_citation = {}

        json_citation['v53'] = [{u'_': u'It is the conference title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publication_type, u'conference')

    def test_publication_type_thesis(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the thesis title'}]
        json_citation['v51'] = [{u'_': u'Grau da these'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publication_type, u'thesis')

    def test_publication_type_link(self):
        json_citation = {}

        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]
        json_citation['v12'] = [{u'_': u'It is the link title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publication_type, u'link')

    def test_publication_type_undefined(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.publication_type, u'undefined')

    def test_source_journal(self):
        json_citation = {}
        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.source, u'It is the journal title')

    def test_source_journal_without_journal_title(self):
        json_citation = {}
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.source, None)

    def test_source_book_title(self):
        json_citation = {}
        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v12'] = [{u'_': u'It is the book chapter'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.source, u'It is the book title')

    def test_article_title(self):
        json_citation = {}
        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article chapter'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.article_title, u'It is the article chapter')

    def test_article_without_title(self):
        json_citation = {}
        json_citation['v30'] = [{u'_': u'It is the journal title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.article_title, None)

    def test_book_chapter_title(self):
        json_citation = {}
        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v12'] = [{u'_': u'It is the book chapter'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.chapter_title, u'It is the book chapter')

    def test_book_without_chapter_title(self):
        json_citation = {}
        json_citation['v18'] = [{u'_': u'It is the book title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.chapter_title, None)

    def test_thesis_title(self):
        json_citation = {}
        json_citation['v18'] = [{u'_': u'It is the thesis title'}]
        json_citation['v51'] = [{u'_': u'Grau de Thesis'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.thesis_title, u'It is the thesis title')

    def test_thesis_without_title(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.thesis_title, None)

    def test_conference_name(self):
        json_citation = {}
        json_citation['v53'] = [{u'_': u'It is the conference title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.conference_name, u'It is the conference title')

    def test_conference_without_name(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.conference_title, None)

    def test_link_title(self):
        json_citation = {}
        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]
        json_citation['v12'] = [{u'_': u'It is the link title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.link_title, u'It is the link title')

    def test_link_without_title(self):
        json_citation = {}
        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.link_title, None)

    def test_conference_sponsor(self):
        json_citation = {}
        json_citation['v53'] = [{u'_': u'It is the conference title'}]
        json_citation['v52'] = [{u'_': u'It is the conference sponsor'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.conference_sponsor, u'It is the conference sponsor')

    def test_conference_without_sponsor(self):
        json_citation = {}
        json_citation['v52'] = [{u'_': u'It is the conference sponsor'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.conference_sponsor, None)

    def test_link(self):
        json_citation = {}
        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.link, u'http://www.scielo.br')

    def test_without_link(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.link, None)

    def test_date(self):
        json_citation = {}
        json_citation['v65'] = [{u'_': u'2012'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.date, u'2012')

    def test_a_link_access_date(self):
        json_citation = {}
        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]
        json_citation['v110'] = [{u'_': u'201300'}]
        json_citation['v65'] = [{u'_': u'2012'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.date, u'2013')

    def test_without_date(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.date, None)

    def test_book_edition(self):
        json_citation = {}
        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v63'] = [{u'_': u'ed. 1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.edition, u'ed. 1')

    def test_conference_edition(self):
        json_citation = {}
        json_citation['v53'] = [{u'_': u'It is the conference title'}]
        json_citation['v63'] = [{u'_': u'ed. 1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.edition, u'ed. 1')

    def test_invalid_edition(self):
        json_citation = {}
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v63'] = [{u'_': u'ed. 1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.edition, None)

    def test_without_edition(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.edition, None)

    def test_issn(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v35'] = [{u'_': u'1234-1234'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issn, u'1234-1234')

    def test_issn_but_not_an_article(self):
        json_citation = {}

        json_citation['v35'] = [{u'_': u'1234-1234'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issn, None)

    def test_isbn(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v12'] = [{u'_': u'It is the chapter title'}]
        json_citation['v69'] = [{u'_': u'12341234'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.isbn, u'12341234')

    def test_isbn_but_not_a_book(self):
        json_citation = {}

        json_citation['v69'] = [{u'_': u'12341234'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.isbn, None)

    def test_book_volume(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v31'] = [{u'_': u'1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.volume, u'1')

    def test_journal_volume(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v12'] = [{u'_': u'It is the chapter title'}]
        json_citation['v31'] = [{u'_': u'1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.volume, u'1')

    def test_without_volume(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.volume, None)

    def test_with_volume_but_not_a_journal_article_neither_a_book(self):
        json_citation = {}

        json_citation['v31'] = [{u'_': u'1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.volume, None)

    def test_journal_issue(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v32'] = [{u'_': u'1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issue, u'1')

    def test_without_issue(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issue, None)

    def test_issue_title(self):
        json_citation = {}

        json_citation['v33'] = [{u'_': u'It is the issue title'}]
        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issue_title, u'It is the issue title')

    def test_without_issue_title(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issue_title, None)

    def test_issue_part(self):
        json_citation = {}

        json_citation['v34'] = [{u'_': u'It is the issue part'}]
        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issue_part, u'It is the issue part')

    def test_without_issue_part(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.issue_title, None)

    def test_doi(self):
        json_citation = {}

        json_citation['v237'] = [{u'_': u'DOI_NUMBER'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.doi, u'DOI_NUMBER')

    def test_without_doi(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.doi, None)

    def test_institutions_all_fields(self):
        json_citation = {}

        json_citation['v11'] = [{u'_': u'Institution 11'}]
        json_citation['v17'] = [{u'_': u'Institution 17'}]
        json_citation['v29'] = [{u'_': u'Institution 29'}]
        json_citation['v50'] = [{u'_': u'Institution 50'}]
        json_citation['v58'] = [{u'_': u'Institution 58'}]

        expected = [u'Institution 11',
                    u'Institution 17',
                    u'Institution 29',
                    u'Institution 50',
                    u'Institution 58']

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, expected)

    def test_institutions_v11(self):
        json_citation = {}

        json_citation['v11'] = [{u'_': u'Institution 11'}]

        expected = [u'Institution 11']

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, expected)

    def test_institutions_v17(self):
        json_citation = {}

        json_citation['v17'] = [{u'_': u'Institution 17'}]

        expected = [u'Institution 17']

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, expected)

    def test_institutions_v29(self):
        json_citation = {}

        json_citation['v29'] = [{u'_': u'Institution 29'}]

        expected = [u'Institution 29']

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, expected)

    def test_institutions_v50(self):
        json_citation = {}

        json_citation['v50'] = [{u'_': u'Institution 50'}]

        expected = [u'Institution 50']

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, expected)

    def test_institutions_v58(self):
        json_citation = {}

        json_citation['v58'] = [{u'_': u'Institution 58'}]

        expected = [u'Institution 58']

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, expected)

    def test_without_institutions(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, None)

    def test_analytic_institution_for_a_article_citation(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v11'] = [{u'_': u'Article Institution'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.analytic_institution, [u'Article Institution'])

    def test_analytic_institution_for_a_book_citation(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v11'] = [{u'_': u'Book Institution'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.analytic_institution, [u'Book Institution'])

    def test_thesis_institution(self):
        json_citation = {}

        json_citation['v50'] = [{u'_': u'Thesis Institution'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.thesis_institution, [u'Thesis Institution'])

    def test_without_thesis_institution(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.thesis_institution, None)

    def test_editor(self):
        json_citation = {}

        json_citation['v29'] = [{u'_': u'Editor Institution'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.editor, [u'Editor Institution'])

    def test_without_editor(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.editor, None)

    def test_sponsor(self):
        json_citation = {}

        json_citation['v58'] = [{u'_': u'Sponsor Institution'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.sponsor, [u'Sponsor Institution'])

    def test_without_sponsor(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.sponsor, None)

    def test_without_analytic_institution(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.institutions, None)

    def test_authors_article(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v10'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = [{u'given_names': u'Mike', 'surname': 'Sullivan'},
                    {u'given_names': u'Rubin', 'surname': 'Hurricane Carter'},
                    {u'given_names': u'Adilson', 'surname': 'Maguila Rodrigues'},
                    {u'given_names': u'Acelino Popó Freitas'},
                    {u'surname': u'Zé Marreta'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.authors, expected)

    def test_authors_thesis(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the thesis title'}]
        json_citation['v45'] = [{u'_': u'20120000'}]
        json_citation['v10'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = [{u'given_names': u'Mike', 'surname': 'Sullivan'},
                    {u'given_names': u'Rubin', 'surname': 'Hurricane Carter'},
                    {u'given_names': u'Adilson', 'surname': 'Maguila Rodrigues'},
                    {u'given_names': u'Acelino Popó Freitas'},
                    {u'surname': u'Zé Marreta'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.authors, expected)

    def test_authors_book(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v10'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = [{u'given_names': u'Mike', 'surname': 'Sullivan'},
                    {u'given_names': u'Rubin', 'surname': 'Hurricane Carter'},
                    {u'given_names': u'Adilson', 'surname': 'Maguila Rodrigues'},
                    {u'given_names': u'Acelino Popó Freitas'},
                    {u'surname': u'Zé Marreta'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.authors, expected)

    def test_authors_link(self):
        json_citation = {}

        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]
        json_citation['v10'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = [{u'given_names': u'Mike', 'surname': 'Sullivan'},
                    {u'given_names': u'Rubin', 'surname': 'Hurricane Carter'},
                    {u'given_names': u'Adilson', 'surname': 'Maguila Rodrigues'},
                    {u'given_names': u'Acelino Popó Freitas'},
                    {u'surname': u'Zé Marreta'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.authors, expected)

    def test_without_authors(self):
        json_citation = {}

        json_citation['v10'] = []

        citation = Citation(json_citation)

        self.assertEqual(citation.authors, None)

    def test_monographic_authors(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v16'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = [{u'given_names': u'Mike', u'surname': u'Sullivan'},
                    {u'given_names': u'Rubin', u'surname': u'Hurricane Carter'},
                    {u'given_names': u'Adilson', u'surname': u'Maguila Rodrigues'},
                    {u'given_names': u'Acelino Popó Freitas'},
                    {u'surname': u'Zé Marreta'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.monographic_authors, expected)

    def test_without_monographic_authors(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v16'] = []

        citation = Citation(json_citation)

        self.assertEqual(citation.monographic_authors, None)

    def test_without_monographic_authors_but_not_a_book_citation(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v16'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.monographic_authors, None)

    def test_first_author_article(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v10'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = {u'given_names': u'Mike', 'surname': 'Sullivan'}

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, expected)

    def test_first_author_thesis(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the thesis title'}]
        json_citation['v45'] = [{u'_': u'20120000'}]
        json_citation['v10'] = [{u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Sullivan', u'n': u'Mike'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = {u'given_names': u'Adilson', 'surname': 'Maguila Rodrigues'}

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, expected)

    def test_first_author_book(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v10'] = [{u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = {u'given_names': u'Rubin', 'surname': 'Hurricane Carter'}

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, expected)

    def test_first_author_link(self):
        json_citation = {}

        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]
        json_citation['v10'] = [{u's': u'Acelino Popó Freitas'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u's': u'Zé Marreta'}]

        expected = {u'surname': u'Acelino Popó Freitas'}

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, expected)

    def test_without_first_author(self):
        json_citation = {}

        json_citation['v10'] = []

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, None)

    def test_monographic_first_author(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v16'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        expected = {u'given_names': u'Mike', u'surname': u'Sullivan'}

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, expected)

    def test_first_author_without_monographic_authors(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v16'] = []

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, None)

    def test_first_author_without_monographic_authors_but_not_a_book_citation(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v16'] = [{u's': u'Sullivan', u'n': u'Mike'},
                                {u's': u'Hurricane Carter', u'n': u'Rubin'},
                                {u's': u'Maguila Rodrigues', u'n': u'Adilson'},
                                {u'n': u'Acelino Popó Freitas'},
                                {u's': u'Zé Marreta'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.first_author, None)


    def test_series_journal(self):
        json_citation = {}

        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is the article title'}]
        json_citation['v25'] = [{u'_': u'It is the serie title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.serie, u'It is the serie title')

    def test_series_book(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v25'] = [{u'_': u'It is the serie title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.serie, u'It is the serie title')

    def test_series_conference(self):
        json_citation = {}

        json_citation['v53'] = [{u'_': u'It is the conference title'}]
        json_citation['v25'] = [{u'_': u'It is the serie title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.serie, u'It is the serie title')

    def test_series_but_neither_journal_book_or_conference_citation(self):
        json_citation = {}

        json_citation['v25'] = [{u'_': u'It is the serie title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.serie, None)

    def test_without_series(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.serie, None)

    def test_publisher(self):
        json_citation = {}

        json_citation['v62'] = [{u'_': u'It is the publisher name'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publisher, u'It is the publisher name')

    def test_without_publisher(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.publisher, None)

    def test_publisher_address(self):
        json_citation = {}

        json_citation['v67'] = [{u'_': u'São Paulo, Brazil'}]
        json_citation['v66'] = [{u'_': u'Rua Barão de Limeira, 821', u'e': u'teste@email.com'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publisher_address, u'Rua Barão de Limeira, 821; teste@email.com; São Paulo, Brazil')

    def test_publisher_address_without_e(self):
        json_citation = {}

        json_citation['v66'] = [{u'_': u'São Paulo, Brazil'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.publisher_address, u'São Paulo, Brazil')

    def test_without_publisher_address(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.publisher_address, None)

    def test_start_page_14(self):
        json_citation = {}

        json_citation['v14'] = [{u'_': u'220-230'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.start_page, u'220')

    def test_end_page_14(self):
        json_citation = {}

        json_citation['v14'] = [{u'_': u'220-230'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.end_page, u'230')

    def test_end_page_withdout_data(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.end_page, None)

    def test_start_page_514(self):
        json_citation = {}

        json_citation['v514'] = [{u'f': u'220', u'l': '230'}]
        json_citation['v14'] = [{u'_': u'220-230'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.start_page, u'220')

    def test_start_page_withdout_data(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.start_page, None)

    def test_end_page_514(self):
        json_citation = {}

        json_citation['v514'] = [{u'f': u'220', u'l': '230'}]
        json_citation['v14'] = [{u'_': u'220-230'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.end_page, u'230')

    def test_pages_14(self):
        json_citation = {}

        json_citation['v14'] = [{u'_': u'220-230'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.pages, u'220-230')

    def test_pages_514(self):
        json_citation = {}

        json_citation['v514'] = [{u'f': u'220', u'l': '230'}]
        json_citation['v14'] = [{u'_': u'220-230'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.pages, u'220-230')

    def test_pages_withdout_data(self):
        json_citation = {}

        citation = Citation(json_citation)

        self.assertEqual(citation.pages, None)

    def test_title_when_article_citation(self):
        json_citation = {}

        #when it is a article citation
        json_citation['v30'] = [{u'_': u'It is the journal title'}]
        json_citation['v12'] = [{u'_': u'It is a article title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.title(), u'It is a article title')

    def test_title_when_thesis_citation(self):
        json_citation = {}

        #when it is a thesis citation
        json_citation['v18'] = [{u'_': u'It is the thesis title'}]
        json_citation['v51'] = [{u'_': u'Grau de Thesis'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.title(), u'It is the thesis title')

    def test_title_when_conference_citation(self):
        json_citation = {}

        #when it is a conference citation
        json_citation['v53'] = [{u'_': u'It is the conference name'}]
        json_citation['v12'] = [{u'_': u'It is the conference title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.title(), u'It is the conference title')

    def test_title_when_link_citation(self):
        json_citation = {}

        #when it is a link citation
        json_citation['v37'] = [{u'_': u'http://www.scielo.br'}]
        json_citation['v12'] = [{u'_': u'It is the link title'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.title(), u'It is the link title')

    def test_citation_sample_link(self):

        json_citation = {u'v999': [{u'_': u'../bases-work/ciedu/ciedu'}], u'v37': [{u'_': u'<http://files.eric.ed.gov/fulltext/ED405219.pdf >'}], u'v12': [{u'l': u'en', u'_': u"Development of a questionnaire for assessing teachers' beliefs about science and science teaching in Taiwan and Australia"}], u'v10': [{u's': u'CHUNG-CHIH CHEN', u'r': u'ND', u'_': u'', u'n': u'C. C.'}, {u's': u'TAYLOR', u'r': u'ND', u'_': u'', u'n': u'P. C.'}, {u's': u'ALDRIDGE', u'r': u'ND', u'_': u'', u'n': u'J. M.'}], u'v11': [{u'_': u'ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING'}], u'v71': [{u'_': u'web'}], u'v992': [{u'_': u'scl'}], u'v882': [{u'n': u'3', u'_': u'', u'v': u'20'}], u'v880': [{u'_': u'S1516-7313201400030053500020'}], u'v865': [{u'_': u'20140900'}], u'v66': [{u'_': u'Oak Brook'}], u'v65': [{u'_': u'19970000'}], u'v61': [{u'_': u'Disponible en: <ext-link ext-link-type="uri" ns0:href="&lt;http://files.eric.ed.gov/fulltext/ED405219.pdf &gt;">&lt;http://files.eric.ed.gov/fulltext/ED405219.pdf &gt;</ext-link>'}], u'v17': [{u'_': u'ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING'}], u'v708': [{u'_': u'52'}], u'v2': [{u'_': u'S1516-7313(14)02000300535'}], u'v3': [{u'_': u'1516-7313-ciedu-20-03-0535.xml'}], u'v4': [{u'_': u'v20n3'}], u'v701': [{u'_': u'20'}], u'v700': [{u'_': u'24'}], u'v702': [{u'_': u'ciedu/v20n3/1516-7313-ciedu-20-03-0535.xml'}], u'v705': [{u'_': u'S'}], u'v704': [{u'_': u"<mixed-citation>CHUNG-CHIH CHEN, C. C.; TAYLOR, P. C.; ALDRIDGE, J. M. Development of a questionnaire for assessing teachers' beliefs about science and science teaching in Taiwan and Australia. In: ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING, Oak Brook, 1997. Disponible en: &lt;http://files.eric.ed.gov/fulltext/ED405219.pdf &gt;. Visitado el: 18 Jul. 2014.</mixed-citation>"}], u'v706': [{u'_': u'c'}], u'v109': [{u'_': u'Visitado el: 18 Jul. 2014'}], u'v1': [{u'_': u'br1.1'}], u'v936': [{u'i': u'1516-7313', u'y': u'2014', u'o': u'3', u'_': u''}]}

        citation = Citation(json_citation)

        self.assertEqual(citation.link_title, u'Development of a questionnaire for assessing teachers\' beliefs about science and science teaching in Taiwan and Australia')
        self.assertEqual(citation.link, u'<http://files.eric.ed.gov/fulltext/ED405219.pdf >')
        self.assertEqual(citation.comment, u'Disponible en: <ext-link ext-link-type="uri" ns0:href="&lt;http://files.eric.ed.gov/fulltext/ED405219.pdf &gt;">&lt;http://files.eric.ed.gov/fulltext/ED405219.pdf &gt;</ext-link>')
        self.assertEqual(citation.link_access_date, u'Visitado el: 18 Jul. 2014')
        self.assertEqual(citation.mixed_citation, u"CHUNG-CHIH CHEN, C. C.; TAYLOR, P. C.; ALDRIDGE, J. M. Development of a questionnaire for assessing teachers' beliefs about science and science teaching in Taiwan and Australia. In: ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING, Oak Brook, 1997. Disponible en: <http://files.eric.ed.gov/fulltext/ED405219.pdf >. Visitado el: 18 Jul. 2014.")


    def test_citation_sample_link_without_comment(self):

        json_citation = {u'v999': [{u'_': u'../bases-work/ciedu/ciedu'}], u'v37': [{u'_': u'<http://files.eric.ed.gov/fulltext/ED405219.pdf >'}], u'v12': [{u'l': u'en', u'_': u"Development of a questionnaire for assessing teachers' beliefs about science and science teaching in Taiwan and Australia"}], u'v10': [{u's': u'CHUNG-CHIH CHEN', u'r': u'ND', u'_': u'', u'n': u'C. C.'}, {u's': u'TAYLOR', u'r': u'ND', u'_': u'', u'n': u'P. C.'}, {u's': u'ALDRIDGE', u'r': u'ND', u'_': u'', u'n': u'J. M.'}], u'v11': [{u'_': u'ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING'}], u'v71': [{u'_': u'web'}], u'v992': [{u'_': u'scl'}], u'v882': [{u'n': u'3', u'_': u'', u'v': u'20'}], u'v880': [{u'_': u'S1516-7313201400030053500020'}], u'v865': [{u'_': u'20140900'}], u'v66': [{u'_': u'Oak Brook'}], u'v65': [{u'_': u'19970000'}], u'v17': [{u'_': u'ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING'}], u'v708': [{u'_': u'52'}], u'v2': [{u'_': u'S1516-7313(14)02000300535'}], u'v3': [{u'_': u'1516-7313-ciedu-20-03-0535.xml'}], u'v4': [{u'_': u'v20n3'}], u'v701': [{u'_': u'20'}], u'v700': [{u'_': u'24'}], u'v702': [{u'_': u'ciedu/v20n3/1516-7313-ciedu-20-03-0535.xml'}], u'v705': [{u'_': u'S'}], u'v704': [{u'_': u"<mixed-citation>CHUNG-CHIH CHEN, C. C.; TAYLOR, P. C.; ALDRIDGE, J. M. Development of a questionnaire for assessing teachers' beliefs about science and science teaching in Taiwan and Australia. In: ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING, Oak Brook, 1997. Disponible en: &lt;http://files.eric.ed.gov/fulltext/ED405219.pdf &gt;. Visitado el: 18 Jul. 2014.</mixed-citation>"}], u'v706': [{u'_': u'c'}], u'v109': [{u'_': u'Visitado el: 18 Jul. 2014'}], u'v1': [{u'_': u'br1.1'}], u'v936': [{u'i': u'1516-7313', u'y': u'2014', u'o': u'3', u'_': u''}]}

        citation = Citation(json_citation)

        self.assertEqual(citation.link_title, u'Development of a questionnaire for assessing teachers\' beliefs about science and science teaching in Taiwan and Australia')
        self.assertEqual(citation.link, u'<http://files.eric.ed.gov/fulltext/ED405219.pdf >')
        self.assertEqual(citation.comment, u'Available at: <ext-link ext-link-type="uri" ns0:href="<http://files.eric.ed.gov/fulltext/ED405219.pdf >"><http://files.eric.ed.gov/fulltext/ED405219.pdf ></ext-link>')
        self.assertEqual(citation.link_access_date, u'Visitado el: 18 Jul. 2014')
        self.assertEqual(citation.mixed_citation, u"CHUNG-CHIH CHEN, C. C.; TAYLOR, P. C.; ALDRIDGE, J. M. Development of a questionnaire for assessing teachers' beliefs about science and science teaching in Taiwan and Australia. In: ANNUAL MEETING OF THE NATIONAL ASSOCIATION FOR RESEARCH IN SCIENCE TEACHING, Oak Brook, 1997. Disponible en: <http://files.eric.ed.gov/fulltext/ED405219.pdf >. Visitado el: 18 Jul. 2014.")

    def test_citation_sample_congress(self):

        json_citation= {u'v999': [{u'_': u'../bases-work/ciedu/ciedu'}], u'v12': [{u'l': u'es', u'_': u'Escuelas con poblaciones en riesgo social: proyecto de intervenci\xf3n e investigaci\xf3n en el \xe1rea de ciencias naturales'}], u'v10': [{u's': u'G\xd3MEZ', u'r': u'ND', u'_': u'', u'n': u'S.'}], u'v71': [{u'_': u'conf-proc'}], u'v992': [{u'_': u'scl'}], u'v882': [{u'n': u'3', u'_': u'', u'v': u'20'}], u'v880': [{u'_': u'S1516-7313201400030053500029'}], u'v865': [{u'_': u'20140900'}], u'v66': [{u'_': u'Buenos Aires'}], u'v65': [{u'_': u'20040000'}], u'v62': [{u'_': u'Asociaci\xf3n de Docentes de Ciencias Biol\xf3gicas de la Argentina'}], u'v708': [{u'_': u'52'}], u'v2': [{u'_': u'S1516-7313(14)02000300535'}], u'v3': [{u'_': u'1516-7313-ciedu-20-03-0535.xml'}], u'v4': [{u'_': u'v20n3'}], u'v701': [{u'_': u'29'}], u'v700': [{u'_': u'33'}], u'v702': [{u'_': u'ciedu/v20n3/1516-7313-ciedu-20-03-0535.xml'}], u'v705': [{u'_': u'S'}], u'v704': [{u'_': u'<mixed-citation>G&#211;MEZ, S. et al. Escuelas con poblaciones en riesgo social: proyecto de intervenci&#243;n e investigaci&#243;n en el &#225;rea de ciencias naturales. In: JORNADAS NACIONALES, 6. Y CONGRESO INTERNACIONAL DE ENSE&#209;ANZA DE LA BIOLOG&#205;A, 1., 2004, Buenos Aires. Buenos Aires: Asociaci&#243;n de Docentes de Ciencias Biol&#243;gicas de la Argentina, 2004.</mixed-citation>'}], u'v706': [{u'_': u'c'}], u'v1': [{u'_': u'br1.1'}], u'v56': [{u'_': u'Buenos Aires'}], u'v54': [{u'_': u'2004'}], u'v53': [{u'_': u'JORNADAS NACIONALES, 6'}, {u'_': u'Y CONGRESO INTERNACIONAL DE ENSE\xd1ANZA DE LA BIOLOG\xcdA, 1'}], u'v936': [{u'i': u'1516-7313', u'y': u'2014', u'o': u'3', u'_': u''}]}

        citation = Citation(json_citation)

        self.assertEqual(citation.conference_title, u'Escuelas con poblaciones en riesgo social: proyecto de intervenci\xf3n e investigaci\xf3n en el \xe1rea de ciencias naturales')
        self.assertEqual(citation.conference_name, u'JORNADAS NACIONALES, 6; Y CONGRESO INTERNACIONAL DE ENSEÑANZA DE LA BIOLOGÍA, 1')
        self.assertEqual(citation.date, u'2004')
        self.assertEqual(citation.conference_location, u'Buenos Aires')
