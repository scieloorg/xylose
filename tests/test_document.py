# coding: utf-8

import unittest
import json
import os
from xylose.scielodocument import Article, Citation, Journal, Issue, html_decode, UnavailableMetadataException
from xylose import tools


class ToolsTests(unittest.TestCase):

    def test_creative_commons_text_1(self):
        result = tools.creative_commons_text('BY/4.0')

        expected = u'This work is licensed under a Creative Commons Attribution 4.0 International License.'

        self.assertEqual(result, expected)

    def test_creative_commons_html_1(self):
        result = tools.creative_commons_text('BY/4.0', html=True)

        expected = u'This work is licensed under a <a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.'

        self.assertEqual(result, expected)

    def test_creative_commons_text_2(self):
        result = tools.creative_commons_text('BY-ND/4.0')

        expected = u'This work is licensed under a Creative Commons Attribution-NoDerivatives 4.0 International License.'

        self.assertEqual(result, expected)

    def test_creative_commons_html_2(self):
        result = tools.creative_commons_text('BY-ND/4.0', html=True)

        expected = u'This work is licensed under a <a href="http://creativecommons.org/licenses/by-nd/4.0/">Creative Commons Attribution-NoDerivatives 4.0 International License</a>.'

        self.assertEqual(result, expected)

    def test_creative_commons_text_3(self):
        result = tools.creative_commons_text('BY-SA/4.0')

        expected = u'This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.'

        self.assertEqual(result, expected)

    def test_creative_commons_html_3(self):
        result = tools.creative_commons_text('BY-SA/4.0', html=True)

        expected = u'This work is licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.'

        self.assertEqual(result, expected)

    def test_creative_commons_text_4(self):
        result = tools.creative_commons_text('BY-NC/4.0')

        expected = u'This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.'

        self.assertEqual(result, expected)

    def test_creative_commons_html_4(self):
        result = tools.creative_commons_text('BY-NC/4.0', html=True)

        expected = u'This work is licensed under a <a href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.'

        self.assertEqual(result, expected)

    def test_creative_commons_text_5(self):
        result = tools.creative_commons_text('BY-NC-ND/4.0')

        expected = u'This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.'

        self.assertEqual(result, expected)

    def test_creative_commons_html_5(self):
        result = tools.creative_commons_text('BY-NC-ND/4.0', html=True)

        expected = u'This work is licensed under a <a href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.'

        self.assertEqual(result, expected)

    def test_creative_commons_text_6(self):
        result = tools.creative_commons_text('BY-NC-SA/4.0')

        expected = u'This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.'

        self.assertEqual(result, expected)

    def test_creative_commons_html_6(self):
        result = tools.creative_commons_text('BY-NC-SA/4.0', html=True)

        expected = u'This work is licensed under a <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.'

        self.assertEqual(result, expected)

    def test_creative_commons_text_7(self):
        result = tools.creative_commons_text('by/3.0')

        expected = u'This work is licensed under a Creative Commons Attribution 3.0 International License.'

        self.assertEqual(result, expected)

    def test_creative_commons_text_7(self):
        result = tools.creative_commons_text('by')

        expected = None

        self.assertEqual(result, expected)

    def test_creative_commons_text_8(self):
        result = tools.creative_commons_text('')

        expected = None

        self.assertEqual(result, expected)

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

    def test_get_date_year_month_day_31(self):

        date = tools.get_date('20120331')
        self.assertEqual(date, '2012-03-31')

    def test_get_date_year_month_day(self):

        date = tools.get_date('20120102')
        self.assertEqual(date, '2012-01-02')

    def test_get_date_year_month(self):

        date = tools.get_date('20120100')
        self.assertEqual(date, '2012-01')

    def test_get_date_year(self):

        date = tools.get_date('20120000')
        self.assertEqual(date, '2012')

    def test_get_date_year_day(self):

        date = tools.get_date('20120001')
        self.assertEqual(date, '2012')

    def test_get_date_wrong_day(self):

        date = tools.get_date('201201')
        self.assertEqual(date, '2012-01')

    def test_get_date_wrong_day_month(self):

        date = tools.get_date('2012')
        self.assertEqual(date, '2012')

    def test_get_date_wrong_day_not_int(self):

        date = tools.get_date('201201xx')
        self.assertEqual(date, '2012-01')

    def test_get_date_wrong_day_month_not_int(self):

        date = tools.get_date('2012xxxx')
        self.assertEqual(date, '2012')

    def test_get_date_wrong_month_not_int(self):

        date = tools.get_date('2012xx01')
        self.assertEqual(date, '2012')


class IssueTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/sample_issue.json' % path).read())
        self.issue = Issue(self.fulldoc)

    def test_sections(self):
        issue = self.issue

        expected = {
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

        self.assertEqual(issue.sections, expected)

    def test_issue_journal_without_journal_metadata(self):
        issue = self.issue

        del(issue.data['title'])

        with self.assertRaises(UnavailableMetadataException):
            issue.journal

    def test_assets_code_month(self):
        issue = self.issue

        issue.data['issue']['v4'] = [{'_': 'v10n12'}]

        self.assertEqual(issue.assets_code, 'v10n12')

    def test_start_end_month(self):
        issue = self.issue

        issue.data['issue']['v43'] = [
            {'m': 'out./dez'},
            {'m': 'oct./dic'}
        ]

        self.assertEqual(issue.start_month, '10')
        self.assertEqual(issue.end_month, '12')

    def test_start_end_month_1(self):
        issue = self.issue

        issue.data['issue']['v43'] = [
            {'m': 'xxx./xxx'},
            {'m': 'oct./dic'}
        ]

        self.assertEqual(issue.start_month, '10')
        self.assertEqual(issue.end_month, '12')

    def test_start_end_month_2(self):
        issue = self.issue

        issue.data['issue']['v43'] = [
            {'x': 'xxx./xxx'},
            {'m': 'oct./dic'}
        ]

        self.assertEqual(issue.start_month, '10')
        self.assertEqual(issue.end_month, '12')

    def test_start_end_month_3(self):
        issue = self.issue

        issue.data['issue']['v43'] = [
            {'x': 'xxx./xxx'},
            {'x': 'oct./dic'}
        ]

        self.assertEqual(issue.start_month, None)
        self.assertEqual(issue.end_month, None)

    def test_start_end_month_4(self):
        issue = self.issue

        issue.data['issue']['v43'] = [
            {'m': 'jan./feb'},
            {'m': 'jan./fev'}
        ]

        self.assertEqual(issue.start_month, '01')
        self.assertEqual(issue.end_month, '02')

    def test_start_end_month_5(self):
        issue = self.issue

        issue.data['issue']['v43'] = [
            {'m': 'out.dez.'},
            {'m': 'oct.dic.'}
        ]

        self.assertEqual(issue.start_month, '10')
        self.assertEqual(issue.end_month, '12')

    def test_start_end_month_6(self):
        issue = self.issue

        issue.data['issue']['v43'] = [
            {'m': 'out.-dez.'},
            {'m': 'oct.-dic.'}
        ]

        self.assertEqual(issue.start_month, '10')
        self.assertEqual(issue.end_month, '12')

    def test_is_marked_up(self):
        issue = self.issue

        issue.data['issue']['v220'] = [{'_': 1}]

        self.assertTrue(issue.is_marked_up)

    def test_is_marked_up(self):
        issue = self.issue

        issue.data['issue']['v220'] = [{'_': 0}]

        self.assertFalse(issue.is_marked_up)

    def test_creation_date(self):
        issue = self.issue

        issue.data['issue']['v93'] = [{u'_': u'20120419'}]
        self.assertEqual(issue.creation_date, '2012-04-19')

    def test_creation_date_1(self):
        issue = self.issue

        issue.data['created_at'] = '2012-01-10'
        issue.data['issue']['v93'] = [{u'_': u'20120419'}]
        self.assertEqual(issue.creation_date, '2012-01-10')

    def test_creation_date_2(self):
        issue = self.issue

        issue.data['created_at'] = '2012-01-10'
        self.assertEqual(
            issue.creation_date,
            '2012-01-10')

    def test_update_date(self):
        issue = self.issue

        issue.data['updated_at'] = '2012-01-10'
        self.assertEqual(issue.update_date, '2012-01-10')

    def test_update_date_1(self):
        issue = self.issue

        issue.data['updated_at'] = '2012-01-10'
        issue.data['issue']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(issue.update_date, '2012-01-10')

    def test_update_date_2(self):
        issue = self.issue

        issue.data['issue']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(issue.update_date, '2012-04-19')

    def test_update_date_3(self):
        issue = self.issue

        issue.data['issue']['v91'] = [{u'_': u'20120418'}]
        self.assertEqual(issue.update_date, '2012-04-18')

    def test_permission_from_journal(self):
        issue = self.issue

        del(issue.data['issue']['v540'])
        del(issue.data['issue']['v541'])

        self.assertEqual(issue.permissions['id'], 'by/4.0')

    def test_permission_t0(self):
        issue = self.issue

        issue.data['issue']['v541'] = [{'_': 'BY-NC'}]

        self.assertEqual(issue.permissions['id'], 'by-nc/4.0')

    def test_permission_t1(self):
        issue = self.issue

        del(issue.data['issue']['v541'])

        issue.data['issue']['v540'] = [{
            "t": '<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/80x15.png" /></a> Todo el contenido de la revista, excepto dónde está identificado, está bajo una <a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es">Licencia Creative Commons</a>',
            '_': "",
            'l': "en"
        }]

        self.assertEqual(
            issue.permissions['id'],
            'by/3.0'
        )

    def test_permission_t2(self):
        issue = self.issue

        issue.data['license'] = 'by-nc/3.0'

        self.assertEqual(issue.permissions['id'], 'by-nc/3.0')
        self.assertEqual(issue.permissions['url'], 'http://creativecommons.org/licenses/by-nc/3.0/')

    def test_permission_t3(self):
        issue = self.issue

        self.assertEqual(issue.permissions['id'], 'by/4.0')
        self.assertEqual(issue.permissions['url'], 'http://creativecommons.org/licenses/by/4.0/')

    def test_permission_t4(self):
        issue = self.issue

        issue.data['issue']['v540'] = [
            {
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u"en"
            }, {
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u'es'
            }, {
                u't': u'<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>',
                u'_': u'',
                u'l': u'pt'
            }
        ]

        self.assertEqual(issue.permissions['id'], 'by/4.0')
        self.assertEqual(issue.permissions['url'], 'http://creativecommons.org/licenses/by/4.0/')

    def test_permission_id(self):
        issue = self.issue

        self.assertEqual(issue.permissions['id'], 'by/4.0')

    def test_permission_url(self):
        issue = self.issue

        del(issue.data['issue']['v541'])

        self.assertEqual(issue.permissions['url'], 'http://creativecommons.org/licenses/by/3.0/')

    def test_permission_text(self):
        issue = self.issue

        del(issue.data['issue']['v541'])

        self.assertEqual(issue.permissions['text'], u'This work is licensed under a Creative Commons Attribution 3.0 International License.')

    def test_permission_without_v540(self):
        issue = self.issue
        del(issue.data['issue']['v541'])

        del(issue.data['issue']['v540'])

        del(issue.data['title']['v541'])

        del(issue.data['title']['v540'])

        self.assertEqual(issue.permissions, None)

    def test_permission_without_v540_t(self):
        issue = self.issue

        del(issue.data['issue']['v541'])

        del(issue.data['issue']['v540'])

        del(issue.data['title']['v541'])

        del(issue.data['title']['v540'])

        issue.data['issue']['v540'] = [{'_': ''}]

        self.assertEqual(issue.permissions, None)

    def test_without_standard(self):
        issue = self.issue

        del(issue.data['issue']['v117'])

        # retorna standard de journal

        self.assertEqual(issue.editorial_standard, (u'nbr6023', u'nbr 6023/89 - associa\xe7\xe3o nacional'))

    def test_without_standard_also_in_journal(self):
        issue = self.issue

        del(issue.data['issue']['v117'])
        del(issue.journal.data['v117'])

        self.assertEqual(issue.editorial_standard, None)

    def test_standard(self):
        issue = self.issue

        self.assertEqual(issue.editorial_standard, (u'nbr6023', u'nbr 6023/89 - associação nacional'))

    def test_standard_out_of_choices(self):
        issue = self.issue

        issue.data['issue']['v117'][0]['_'] = 'xxx'

        self.assertEqual(issue.editorial_standard, ('xxx', 'xxx'))

    def test_without_ctrl_vocabulary(self):
        issue = self.issue

        del(issue.data['issue']['v85'])

        # retorna ctrl_vocab de journal

        self.assertEqual(issue.controlled_vocabulary, (u'nd', u'No Descriptor'))

    def test_without_ctrl_vocabulary_also_in_journal(self):
        issue = self.issue

        del(issue.data['issue']['v85'])
        del(issue.journal.data['v85'])

        self.assertEqual(issue.controlled_vocabulary, None)

    def test_ctrl_vocabulary(self):
        issue = self.issue

        self.assertEqual(issue.controlled_vocabulary, ('nd', 'No Descriptor'))

    def test_ctrl_vocabulary_out_of_choices(self):
        issue = self.issue

        issue.data['issue']['v85'][0]['_'] = 'xxx'

        self.assertEqual(issue.controlled_vocabulary, ('xxx', 'xxx'))

    def test_total_documents(self):
        issue = self.issue

        self.assertEqual(issue.total_documents, '19')

    def test_total_documents_without_data(self):
        issue = self.issue

        del(issue.data['issue']['v122'])

        self.assertEqual(issue.total_documents, 0)

    def test_title_titles(self):
        issue = self.issue

        issue.data['issue']['v33'] = [
            {'l': 'pt', '_': 'lang pt'},
            {'l': 'es', '_': 'lang es'}
        ]
        self.assertEqual(sorted(issue.titles.keys()), ['es', 'pt'])
        self.assertEqual(sorted(issue.titles.values()), ['lang es', 'lang pt'])

    def test_title_titles_1(self):
        issue = self.issue

        issue.data['issue']['v33'] = [
            {'l': 'pt', '_': 'lang pt'},
            {'l': 'es'}
        ]
        self.assertEqual(sorted(issue.titles.keys()), ['pt'])
        self.assertEqual(sorted(issue.titles.values()), ['lang pt'])

    def test_title_titles(self):
        issue = self.issue

        issue.data['issue']['v33'] = [
            {'l': 'pt', '_': 'lang pt'},
            {'_': 'lang es'}
        ]
        self.assertEqual(sorted(issue.titles.keys()), ['pt'])
        self.assertEqual(sorted(issue.titles.values()), ['lang pt'])

    def test_title_without_titles(self):
        issue = self.issue

        self.assertEqual(issue.titles, None)

    def test_is_press_release_true(self):
        issue = self.issue

        issue.data['issue']['v41'] = [{'_': 'PR'}]

        self.assertTrue(issue.is_press_release)

    def test_is_press_release_false_1(self):
        issue = self.issue

        issue.data['issue']['v41'] = [{'_': 'XX'}]

        self.assertFalse(issue.is_press_release)

    def test_is_press_release_false_2(self):
        issue = self.issue

        # Elemento não existe na fixture deve retornal False.

        self.assertFalse(issue.is_press_release)

    def test_type_pressrelease(self):
        issue = self.issue

        issue.data['issue']['v41'] = [{'_': 'pr'}]

        self.assertEqual(issue.type, 'pressrelease')

    def test_type_regular(self):
        issue = self.issue

        self.assertEqual(issue.type, 'regular')

    def test_type_supplement_1(self):
        issue = self.issue

        issue.data['issue']['v131'] = [{'_': '3'}]

        self.assertEqual(issue.type, 'supplement')

    def test_type_supplement_2(self):
        issue = self.issue

        issue.data['issue']['v132'] = [{'_': '3'}]

        self.assertEqual(issue.type, 'supplement')

    def test_type_supplement_2(self):
        issue = self.issue

        issue.data['issue']['v32'] = [{'_': 'spe 1'}]

        self.assertEqual(issue.type, 'special')

    def test_type_supplement_2(self):
        issue = self.issue

        issue.data['issue']['v32'] = [{'_': 'ahead'}]

        self.assertEqual(issue.type, 'ahead')

    def test_processing_date(self):
        issue = self.issue

        issue.data['issue']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(issue.processing_date, '2012-04-19')

    def test_processing_date_1(self):
        issue = self.issue

        issue.data['processing_date'] = u'2012-04-19'

        issue.data['issue']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(issue.processing_date, '2012-04-19')

    def test_without_processing_date(self):
        issue = self.issue

        del(issue.data['issue']['v91'])

        self.assertEqual(issue.processing_date, None)

    def test_order(self):

        self.assertEqual(self.issue.order, '3')

    def test_issue_label(self):

        self.assertEqual(self.issue.label, u'v19n3')

    def test_volume(self):

        self.assertEqual(self.issue.volume, u'19')

    def test_without_volume(self):

        del(self.issue.data['issue']['v31'])

        self.assertEqual(self.issue.volume, None)

    def test_publication_date(self):

        self.assertEqual(self.issue.publication_date, u'2001-12')

    def test_without_publication_date(self):

        del(self.issue.data['issue']['v65'])

        self.assertEqual(self.issue.publication_date, None)

    def test_issue(self):

        self.assertEqual(self.issue.number, u'3')

    def test_without_issue(self):

        del(self.issue.data['issue']['v32'])

        self.assertEqual(self.issue.number, None)

    def test_supplement_volume(self):

        self.issue.data['issue']['v131'] = [{u'_': u'test_suppl_volume'}]
        self.assertEqual(self.issue.supplement_volume, u'test_suppl_volume')

    def test_without_supplement_volume(self):

        self.assertEqual(self.issue.supplement_volume, None)

    def test_supplement_number(self):

        self.issue.data['issue']['v132'] = [{u'_': u'test_suppl_issue'}]

        self.assertEqual(self.issue.supplement_number, u'test_suppl_issue')

    def test_without_suplement_number(self):

        self.assertEqual(self.issue.supplement_number, None)

    def test_is_ahead(self):

        self.assertFalse(self.issue.is_ahead_of_print)

    def test_is_ahead_1(self):

        self.issue.data['issue']['v32'][0]['_'] = 'AHEAD'

        self.assertTrue(self.issue.is_ahead_of_print)

    def test_issue_url(self):

        self.assertTrue(self.issue.url, '')

    def test_collection_acronym(self):

        self.assertTrue(self.issue.url, '')


class JournalTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/full_document.json' % path).read())
        self.journal = Journal(self.fulldoc['title'])

    def test_editor_email(self):
        journal = self.journal

        self.assertEqual(journal.editor_email, u'actalb@rc.unesp.br')

    def test_editor_email_without_data(self):
        journal = self.journal

        del(journal.data['v64'])

        self.assertIsNone(journal.editor_email)

    def test_editor_address(self):
        journal = self.journal

        self.assertEqual(journal.editor_address, u'Av. 24 A, 1515, 13506-900 Rio Claro-SP/Brasil, Tel.:(55 19)3526 9107')

    def test_editor_address_without_data(self):
        journal = self.journal

        del(journal.data['v63'])

        self.assertIsNone(journal.editor_address)

    def test_is_publishing_model_continuous_false_without_field(self):
        journal = self.journal

        self.assertFalse(journal.is_publishing_model_continuous)

    def test_is_publishing_model_continuous_false_with_field_undefined(self):
        journal = self.journal

        journal.data['v699'] = [{'_': u'undefined'}]

        self.assertFalse(journal.is_publishing_model_continuous)

    def test_is_publishing_model_continuous_false_with_field_regular(self):
        journal = self.journal

        journal.data['v699'] = [{'_': u'regular'}]

        self.assertFalse(journal.is_publishing_model_continuous)

    def test_is_publishing_model_continuous_true(self):
        journal = self.journal

        journal.data['v699'] = [{'_': u'continuous'}]

        self.assertTrue(journal.is_publishing_model_continuous)

    def test_is_publishing_model_continuous(self):
        journal = self.journal

        journal.data['v699'] = [{'_': u'continuous'}]

        self.assertEqual(journal.publishing_model, 'continuous')

    def test_is_publishing_model_regular_1(self):
        journal = self.journal

        journal.data['v699'] = [{'_': u'regular'}]

        self.assertEqual(journal.publishing_model, 'regular')

    def test_is_publishing_model_regular_2(self):
        journal = self.journal

        self.assertEqual(journal.publishing_model, 'regular')

    def test_is_publishing_model_continuous_true(self):
        journal = self.journal

        journal.data['v699'] = [{'_': u'continuous'}]

        self.assertTrue(journal.is_publishing_model_continuous)

    def test_previous_title(self):
        journal = self.journal

        journal.data['v610'] = [{'_': u'Previous Title'}]

        self.assertEqual(journal.previous_title, u'Previous Title')

    def test_previous_title_without_data(self):
        journal = self.journal

        self.assertEqual(journal.previous_title, None)

    def test_in_scie(self):
        journal = self.journal

        journal.data['v851'] = [{'_': 'SCIE'}]

        self.assertTrue(journal.is_indexed_in_scie)

    def test_in_scie(self):
        journal = self.journal

        self.assertFalse(journal.is_indexed_in_scie)

    def test_in_ssci(self):
        journal = self.journal

        journal.data['v852'] = [{'_': 'SSCI'}]

        self.assertTrue(journal.is_indexed_in_ssci)

    def test_in_ssci(self):
        journal = self.journal

        self.assertFalse(journal.is_indexed_in_ssci)

    def test_in_ahci(self):
        journal = self.journal

        journal.data['v853'] = [{'_': 'A&HCI'}]

        self.assertTrue(journal.is_indexed_in_ahci)

    def test_in_ahci(self):
        journal = self.journal

        self.assertFalse(journal.is_indexed_in_ahci)

    def test_without_periodicity_in_months(self):
        journal = self.journal

        del(journal.data['v380'])

        self.assertEqual(journal.periodicity_in_months, None)

    def test_submission_url(self):
        journal = self.journal

        journal.data['v692'] = [{'_': 'http://www.submision.org/'}]

        self.assertEqual(journal.submission_url, 'http://www.submision.org/')

    def test_submission_url(self):
        journal = self.journal

        self.assertEqual(journal.submission_url, None)

    def test_periodicity_in_months(self):
        journal = self.journal

        self.assertEqual(journal.periodicity_in_months, '4')

    def test_periodicity_in_months_out_of_choices(self):
        journal = self.journal

        journal.data['v380'][0]['_'] = 'XXX'

        self.assertEqual(journal.periodicity_in_months, 'XXX')

    def test_without_plevel(self):
        journal = self.journal

        del(journal.data['v330'])

        self.assertEqual(journal.publication_level, None)

    def test_plevel(self):
        journal = self.journal

        self.assertEqual(journal.publication_level, (u'CT', u'Scientific Technical'))

    def test_plevel_out_of_choices(self):
        journal = self.journal

        journal.data['v330'][0]['_'] = 'XXX'

        self.assertEqual(journal.publication_level, ('XXX', 'XXX'))

    def test_without_ctrl_vocabulary(self):
        journal = self.journal

        del(journal.data['v85'])

        self.assertEqual(journal.controlled_vocabulary, None)

    def test_ctrl_vocabulary(self):
        journal = self.journal

        self.assertEqual(journal.controlled_vocabulary, ('nd', 'No Descriptor'))

    def test_ctrl_vocabulary_out_of_choices(self):
        journal = self.journal

        journal.data['v85'][0]['_'] = 'xxx'

        self.assertEqual(journal.controlled_vocabulary, ('xxx', 'xxx'))

    def test_without_institutional_url(self):
        journal = self.journal

        del(journal.data['v69'])
        self.assertEqual(journal.institutional_url, None)

    def test_institutional_url(self):
        journal = self.journal

        self.assertEqual(journal.institutional_url, u'http://www.ablimno.org.br')

    def test_without_secs_code(self):
        journal = self.journal

        self.assertEqual(journal.secs_code, None)

    def test_secs_code(self):
        journal = self.journal

        journal.data['v37'] = [{'_': 'secs_code'}]
        self.assertEqual(journal.secs_code, 'secs_code')

    def test_without_standard(self):
        journal = self.journal

        del(journal.data['v117'])

        self.assertEqual(journal.editorial_standard, None)

    def test_standard(self):
        journal = self.journal

        self.assertEqual(journal.editorial_standard, ('other', 'other standard'))

    def test_standard_out_of_choices(self):
        journal = self.journal

        journal.data['v117'][0]['_'] = 'xxx'

        self.assertEqual(journal.editorial_standard, ('xxx', 'xxx'))

    def test_without_periodicity(self):
        journal = self.journal

        del(journal.data['v380'])

        self.assertEqual(journal.periodicity, None)

    def test_periodicity(self):
        journal = self.journal

        self.assertEqual(journal.periodicity, ('Q', 'Quarterly'))

    def test_periodicity_out_of_choices(self):
        journal = self.journal

        journal.data['v380'][0]['_'] = 'XXX'

        self.assertEqual(journal.periodicity, ('XXX', 'XXX'))

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

    def test_abstract_languages(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(sorted(journal.abstract_languages), [u'en', u'pt'])

    def test_abstract_languages_without_v350(self):
        del(self.fulldoc['title']['v360'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.abstract_languages, None)

    def test_current_without_v51(self):
        del(self.fulldoc['title']['v51'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.current_status, u'current')

    def test_status_without_v51(self):
        del(self.fulldoc['title']['v51'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [(u'2011-03-25', u'current', '')])

    def test_current_status(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.current_status, u'current')

    def test_status(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [(u'2011-04', u'current', '')])

    def test_current_status_some_changes(self):

        v51 = [
            {'a': '19981126', 'c': "20020000", 'b': "C", 'd': "D", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        journal.current_status

        self.assertEqual(journal.current_status, u'deceased', '')

    def test_status_some_changes(self):

        v51 = [
            {'a': '19981126', 'c': "20020000", 'b': "C", 'd': "D", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [('1998-11-26', 'current', ''), ('2002', 'deceased', '')])

    def test_status_lots_of_changes(self):

        v51 = [
            {'a': "20100800", 'b': "C", '_': "" },
            {'a': "19981016", 'c': "20050100", 'b': "C", 'd': "S", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status, [(u'2010-08', u'current', '')])

    def test_status_lots_of_changes(self):

        v51 = [
            {'a': "20100800", 'b': "C", '_': "" },
            {'a': "19981016", 'c': "20050100", 'b': "C", 'd': "S", '_': ""}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [('1998-10-16', 'current', ''), ('2005-01', 'suspended', 'suspended-by-committee'), ('2010-08', 'current', '')])

    def test_status_lots_of_changes_with_reason(self):

        v51 = [
            {'a': "20100800", 'b': "C", '_': "" },
            {'a': "19981016", 'c': "20050100", 'b': "C", 'd': "S", '_': "", 'e': 'suspended-by-editor'}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [('1998-10-16', 'current', ''), ('2005-01', 'suspended', 'suspended-by-editor'), ('2010-08', 'current', '')])

    def test_status_lots_of_changes_study_case_1(self):

        v51 = [
            {u'a': u'20140805', u'c': u'20140805', u'b': u'?', u'd': u'C', u'_': u''}
        ]

        self.fulldoc['title']['v51'] = v51

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.status_history, [(u'2014-08-05', 'current', ''), (u'2014-08-05', 'inprogress', '')])

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

    def test_load_issn_with_v435(self):
        self.fulldoc['title']['v35'] = [{u'_': u'PRINT'}]
        self.fulldoc['title']['v400'] = [{u'_': u'2222-2222'}]
        self.fulldoc['title']['v435'] = [
            {u'_': u'0000-0000', 't': 'ONLIN'},
            {u'_': u'9999-9999', 't': 'PRINT'}
        ]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.print_issn, u'9999-9999')
        self.assertEqual(journal.electronic_issn, u'0000-0000')

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

        self.assertEqual(
            journal.permissions['id'],
            'by/3.0')

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

        self.assertEqual(journal.permissions['text'], u'This work is licensed under a Creative Commons Attribution-NonCommercial 3.0 International License.')

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

    def test_first_year(self):
        journal = self.journal

        self.assertEqual(journal.first_year, '1986')

    def test_first_year_1(self):
        journal = self.journal

        del(journal.data['v301'])

        self.assertEqual(journal.first_year, None)

    def test_first_year_2(self):
        journal = self.journal

        journal.data['v301'] = [{'_': 'maio 1998'}]

        self.assertEqual(journal.first_year, '1998')

    def test_first_year_3(self):
        journal = self.journal

        journal.data['v301'] = [{'_': 'maio 19980100'}]

        self.assertEqual(journal.first_year, '1998')

    def test_first_year_4(self):
        journal = self.journal

        journal.data['v301'] = [{'_': 'maio 01'}]

        self.assertEqual(journal.first_year, '2001')

    def test_first_volume(self):
        journal = self.journal

        self.assertEqual(journal.first_volume, '1')

    def test_first_volume_1(self):
        journal = self.journal

        del(journal.data['v302'])

        self.assertEqual(journal.first_volume, None)

    def test_first_number(self):
        journal = self.journal

        self.assertEqual(journal.first_number, '1')

    def test_first_number_1(self):
        journal = self.journal

        del(journal.data['v303'])

        self.assertEqual(journal.first_number, None)

    def test_last_year(self):
        journal = self.journal

        journal.data['v304'] = [{'_': '2000'}]

        self.assertEqual(journal.last_year, '2000')

    def test_last_year_1(self):
        journal = self.journal

        self.assertEqual(journal.last_year, None)

    def test_last_year_2(self):
        journal = self.journal

        journal.data['v304'] = [{'_': 'maio 1998'}]

        self.assertEqual(journal.last_year, '1998')

    def test_last_year_3(self):
        journal = self.journal

        journal.data['v304'] = [{'_': 'maio 19980100'}]

        self.assertEqual(journal.last_year, '1998')

    def test_last_year_4(self):
        journal = self.journal

        journal.data['v304'] = [{'_': 'maio 98'}]

        self.assertEqual(journal.last_year, '1998')

    def test_last_volume(self):
        journal = self.journal

        journal.data['v305'] = [{'_': '10'}]

        self.assertEqual(journal.last_volume, '10')

    def test_last_volume_1(self):
        journal = self.journal

        self.assertEqual(journal.last_volume, None)

    def test_last_number(self):
        journal = self.journal

        journal.data['v306'] = [{'_': '30'}]

        self.assertEqual(journal.last_number, '30')

    def test_last_number_1(self):
        journal = self.journal

        self.assertEqual(journal.last_number, None)

    def test_without_journal_url(self):
        journal = self.journal

        del(journal.data['v690'])

        self.assertEqual(journal.url(), None)

    def test_cnn_code(self):
        journal = self.journal

        self.assertEqual(journal.cnn_code, '083639-7')

    def test_last_cnn_code_1(self):
        journal = self.journal

        del(journal.data['v20'])

        self.assertEqual(journal.cnn_code, None)

    def test_journal_url(self):
        journal = self.journal

        expected = u"http://www.scielo.br/scielo.php?script=sci_serial&pid=2179-975X&lng=en"

        self.assertEqual(journal.url(), expected)

    def test_subject_index_coverage(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(
            sorted(journal.index_coverage),
            sorted([u'ASFA - Aquatic Sciences and Fisheries Abstracts']))

    def test_without_index_coverage(self):
        del(self.fulldoc['title']['v450'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.index_coverage, None)

    def test_subject_descriptors(self):
        journal = Journal(self.fulldoc['title'])

        self.assertEqual(
            sorted(journal.subject_descriptors),
            sorted([u'ECOLOGIA DE ECOSSISTEMAS', u'ECOLOGIA']))

    def test_without_subject_descriptors(self):
        del(self.fulldoc['title']['v440'])

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.subject_descriptors, None)

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

        self.assertEqual(journal.publisher_name, [u'Associação Brasileira de Limnologia'])

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

    def test_publisher_city(self):
        journal = self.journal

        self.assertEqual(journal.publisher_city, u'Rio Claro')

    def test_without_publisher_city(self):
        journal = self.journal

        del(journal.data['v490'])
        self.assertEqual(journal.publisher_city, None)

    def test_publisher_state(self):
        journal = self.journal

        self.assertEqual(journal.publisher_state, u'SP')

    def test_without_publisher_state(self):
        journal = self.journal

        del(journal.data['v320'])
        self.assertEqual(journal.publisher_state, None)

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

    def test_journal_fulltitle(self):
        self.fulldoc['title']['v100'] = [{u'_': u'Title'}]
        self.fulldoc['title']['v110'] = [{u'_': u'SubTitle'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.fulltitle, u'Title - SubTitle')

    def test_journal_fulltitle_without_title(self):
        del(self.fulldoc['title']['v100'])
        self.fulldoc['title']['v110'] = [{u'_': u'SubTitle'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.fulltitle, u'SubTitle')

    def test_journal_fulltitle_without_subtitle(self):
        self.fulldoc['title']['v100'] = [{u'_': u'Title'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.fulltitle, u'Title')

    def test_journal_subtitle(self):
        self.fulldoc['title']['v110'] = [{u'_': u'SubTitle'}]

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.subtitle, u'SubTitle')

    def test_journal_without_subtitle(self):

        journal = Journal(self.fulldoc['title'])

        self.assertEqual(journal.subtitle, None)

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

    def test_journal_mission(self):
        journal = self.journal

        expected = {
                "es": u"El Acta Limnologica Brasiliensia es la revista oficial de la Asociaci\u00f3n Brasile\u00f1a de Limnolog\u00eda (ABLimno) cuyo obetivo es publicar trabajos originales en Limnolog\u00eda, incluyendo los aspectos f\u00edsicos, qu\u00edmicos y biol\u00f3gicos de la Ciencia Ecolog\u00eda de Aguas Continentales.",
                "pt": u"A Acta Limnologica Brasiliensia \u00e9 uma revista cient\u00edfica publicada pela Associa\u00e7\u00e3o Brasileira de Limnologia (ABLimno) que publica artigos originais que contribuem para o desenvolvimento cient\u00edfico da Limnologia.",
                "en": u"Acta Limnologica Brasiliensia is a journal published by the Associa\u00e7\u00e3o Brasileira de Limnologia (Brazilian Association of Limnology) that publishes original articles in Limnology comprises physical, chemical and biological aspects of fresh water ecosystems."
                }

        self.assertEqual(journal.mission, expected)

    def test_journal_mission_without_mission(self):
        journal = self.journal

        del(journal.data['v901'])

        self.assertIsNone(journal.mission)

    def test_journal_mission_without_language_key(self):
        self.fulldoc['title']['v901'] = [{"l": "es", "_": "any text"},
                                         {"_": "any text"}]

        journal = Journal(self.fulldoc['title'])

        expected = {'es': "any text"}

        self.assertEqual(journal.mission, expected)

    def test_journal_mission_without_mission_text(self):
        self.fulldoc['title']['v901'] = [{"l": "es"},
                                         {"l": "es", "_": "any text"}]

        journal = Journal(self.fulldoc['title'])

        expected = {'es': "any text"}

        self.assertEqual(journal.mission, expected)

    def test_journal_mission_without_mission_text_and_language(self):
        self.fulldoc['title']['v901'] = [{"l": "es"},
                                         {"_": "any text"}]

        journal = Journal(self.fulldoc['title'])

        self.assertIsNone(journal.mission)

    def test_journal_publisher_country(self):
        journal = self.journal

        expected = ('BR', 'Brazil')

        self.assertEqual(journal.publisher_country, expected)

    def test_journal_publisher_country_without_country(self):
        journal = self.journal

        del(journal.data['v310'])

        self.assertIsNone(journal.publisher_country)

    def test_journal_publisher_country_not_findable_code(self):
        self.fulldoc['title']['v310'] = [{"_": "BRX"}]
        journal = Journal(self.fulldoc['title'])

        self.assertIsNone(journal.publisher_country)

    def test_journal_copyrighter(self):
        journal = self.journal

        self.assertEqual(journal.copyrighter,
            u'Associa\u00e7\u00e3o Brasileira de Limnologia')

    def test_journal_copyrighter_without_copyright(self):
        journal = self.journal

        del(journal.data['v62'])

        self.assertIsNone(journal.copyrighter)

    def test_journal_other_titles(self):
        journal = self.journal

        expected = ['Physical Therapy Movement',
                    'Revista de fisioterapia da PUC-PR']

        self.assertEqual(journal.other_titles, expected)

    def test_journal_other_title_without_other_titles(self):
        journal = self.journal

        del(journal.data['v240'])

        self.assertIsNone(journal.other_titles)

    def test_journal_sponsors(self):
        journal = self.journal

        expected = [u"Associa\u00e7\u00e3o Brasileira de Limnologia - ABLimno",
                    u"Conselho Nacional de Desenvolvimento Cient\u00edfico e Tecnol\u00f3gico - CNPq"]
        self.assertEqual(journal.sponsors, expected)

    def test_journal_sponsors_without_sponsors(self):
        journal = self.journal

        del(journal.data['v140'])

        self.assertIsNone(journal.sponsors)

    def test_journal_sponsors_with_empty_items(self):
        self.fulldoc['title']['v140'] = [{"_": u"Associa\u00e7\u00e3o Brasileira de Limnologia - ABLimno"},
                                         {"_": ""},
                                         {"_": ""}]

        journal = Journal(self.fulldoc['title'])

        expected = [u"Associa\u00e7\u00e3o Brasileira de Limnologia - ABLimno"]

        self.assertEqual(journal.sponsors, expected)


class ArticleTests(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.fulldoc = json.loads(open('%s/fixtures/full_document.json' % path).read())
        self.article = Article(self.fulldoc)

    def test_document_without_journal_metadata(self):
        article = self.article

        del(article.data['title'])

        with self.assertRaises(UnavailableMetadataException):
            article.journal

    def test_document_without_issue_metadata(self):
        article = self.article

        del(article.data['issue'])

        with self.assertRaises(UnavailableMetadataException):
            article.issue

    def test_article(self):
        article = self.article
        self.assertTrue(isinstance(article, Article))

    def test_order(self):

        article = self.article

        self.assertEqual(article.order, '02')

    def test_without_order(self):

        article = self.article

        del(article.data['article']['v121'])

        self.assertEqual(article.order, None)

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

    def test_section_without_field_section(self):
        """
        Article without field section trying to load section from issue metadata

        The field section is populated by a processing, if by some reason the
        processing fails to run, the section field will be empty or absent.
        """

        self.fulldoc['article']['v49'] = [{'_': 'RSP10'}]
        self.fulldoc['issue']['issue']['v49'] = [{
                '_': '',
                'l': 'en',
                'c': 'RSP10',
                't': 'Original Articles'
            }, {
                '_': '',
                'l': 'pt',
                'c': 'RSP10',
                't': 'Artigos Originais'
            }, {
                '_': '',
                'l': 'en',
                'c': 'RSP110',
                't': 'Research Articles'
            }, {
                '_': '',
                'l': 'pt',
                'c': 'RSP110',
                't': 'Artigos de Pesquisas'
            }
        ]

        article = Article(self.fulldoc)

        section = article.section

        self.assertEqual(section, {'pt': 'Artigos Originais', 'en': 'Original Articles'})

    def test_section_code_field_v49(self):
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

    def test_data_model_version_html(self):
        del(self.fulldoc['article']['v120'])

        article = Article(self.fulldoc)

        self.assertEqual(article.data_model_version, u'html')

    def test_data_model_version_html_1(self):
        self.fulldoc['article']['v120'] = [{'_': '4.0'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.data_model_version, u'html')

    def test_data_model_version_xml(self):
        self.fulldoc['article']['v120'] = [{'_': 'XML_1.0'}]

        article = Article(self.fulldoc)

        self.assertEqual(article.data_model_version, u'xml')

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

    def test_publication_date_with_article_date(self):
        article = self.article

        self.assertEqual(article.publication_date, '2012-02-16')

    def test_publication_date_without_article_date(self):
        article = self.article

        article.data['article']['v65'] = [{u'_': u'20120102'}]
        del(article.data['article']['v223'])
        self.assertEqual(article.publication_date, '2012-01-02')

    def test_without_publication_date(self):
        article = self.article

        del(article.data['article']['v65'])
        del(article.data['article']['v223'])
        with self.assertRaises(KeyError):
            article.publication_date

    def test_processing_date(self):
        article = self.article

        article.data['article']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(article.processing_date, '2012-04-19')

    def test_processing_date_1(self):
        article = self.article

        article.data['processing_date'] = u'2012-04-19'

        article.data['article']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(article.processing_date, '2012-04-19')

    def test_without_processing_date(self):
        article = self.article

        del(article.data['article']['v91'])

        self.assertEqual(article.processing_date, None)

    def test_creation_date(self):
        article = self.article

        article.data['article']['v93'] = [{u'_': u'20120419'}]
        self.assertEqual(article.creation_date, '2012-04-19')

    def test_creation_date_1(self):
        article = self.article

        article.data['created_at'] = '2012-01-10'
        article.data['article']['v93'] = [{u'_': u'20120419'}]
        self.assertEqual(article.creation_date, '2012-01-10')

    def test_creation_date_2(self):
        article = self.article

        article.data['created_at'] = '2012-01-10'
        self.assertEqual(
            article.creation_date,
            '2012-01-10')

    def test_update_date(self):
        article = self.article

        article.data['updated_at'] = '2012-01-10'
        self.assertEqual(article.update_date, '2012-01-10')

    def test_update_date_1(self):
        article = self.article

        article.data['updated_at'] = '2012-01-10'
        article.data['article']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(article.update_date, '2012-01-10')

    def test_update_date_2(self):
        article = self.article

        article.data['article']['v91'] = [{u'_': u'20120419'}]
        self.assertEqual(article.update_date, '2012-04-19')

    def test_update_date_3(self):
        article = self.article

        article.data['article']['v91'] = [{u'_': u'20120418'}]
        self.assertEqual(article.update_date, '2012-04-18')

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

    def test_start_page(self):
        article = self.article

        self.assertEqual(article.start_page, u'229')

    def test_start_page_sec(self):
        article = self.article

        self.article.data['article']['v14'] = [
            {
                'l': '232',
                'f': '229',
                '_': '',
                's': '1'  # seq
            }
        ]

        self.assertEqual(article.start_page_sequence, u'1')

    def test_start_page_sec_0(self):
        article = self.article

        self.article.data['article']['v14'] = [
            {
                'l': '232',
                'f': '229',
                '_': '',
                's': '0'  # seq
            }
        ]

        self.assertEqual(article.start_page_sequence, None)

    def test_without_start_page(self):
        article = self.article

        del(article.data['article']['v14'][0]['f'])
        self.assertEqual(article.start_page, None)

    def test_e_location(self):
        article = self.article

        article.data['article']['v14'][0] = {'e': 'eloc1'}

        self.assertEqual(article.elocation, 'eloc1')

    def test_without_e_location(self):
        article = self.article

        del(article.data['article']['v14'])

        self.assertEqual(article.elocation, None)

    def test_start_page_sec_loaded_through_xml(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'',
                u'l': u'122'
            },
            {
                u'_': u'',
                u'f': u'110'
            },
            {
                u'_': u'',
                u's': u'1'  # seq
            }
        ]

        self.assertEqual(article.start_page_sequence, u'1')

    def test_start_page_sec_0_loaded_through_xml(self):
        article = self.article

        article.data['article']['v14'] = [
            {
                u'_': u'',
                u'l': u'122'
            },
            {
                u'_': u'',
                u'f': u'110'
            },
            {
                u'_': u'',
                u's': u'0'  # seq
            }
        ]

        self.assertEqual(article.start_page_sequence, None)

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

    def test_publisher_ahead_id(self):
        article = self.article

        self.assertEqual(article.publisher_ahead_id, u'S2179-975X2012005000004')

    def test_publisher_ahead_id_none(self):
        article = self.article

        del(article.data['article']['v881'])
        self.assertEqual(article.publisher_ahead_id, None)

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

    def test_original_title_subfield_t(self):
        article = self.article

        del(article.data['article']['v12'])

        article.data['article']['v12'] = [{u'_': '', u't': u'article title 1', u'l': u'en'}]

        self.assertEqual(article.original_title(iso_format=None), u'article title 1')

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
                u"s": u"São Paulo",
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
                u"s": u"SP",
                u"_": u"UNIVERSIDADE FEDERAL DE SAO CARLOS"
            },
            {
                u"i": u"A03",
                u"p": u"US",
                u"s": u"São Paulo",
                u"_": u"University of Florida Not Normalized"
            },
            {
                u"i": u"A04",
                u"q": u"Mexico",
                u"p": u"MX",
                u"s": u"Yucatán",
                u"_": u"Secretaría de Salud de Yucatán"
            }
        ]

        amc = article.mixed_affiliations

        result_index = u''.join([i['index'] for i in sorted(amc,  key=lambda k: k['index'])])
        result_country = u''.join([i['country'] for i in sorted(amc,  key=lambda k: k['index'])])
        result_country_iso = u''.join([i['country_iso_3166'] for i in sorted(amc,  key=lambda k: k['index']) if 'country_iso_3166' in i])
        result_status = u''.join([str(i['normalized']) for i in sorted(amc,  key=lambda k: k['index'])])
        result_state = u''.join([i['state'] for i in sorted(amc,  key=lambda k: k['index'])])

        self.assertEqual(result_index, u'A01A02A03A04')
        self.assertEqual(result_country, u'BrazilBrazilUSMexico')
        self.assertEqual(result_country_iso, u'BRBRUSMX')
        self.assertEqual(result_status, u'TrueTrueFalseFalse')
        self.assertEqual(result_state, u'São PauloSão PauloYucatán')

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

        article.normalized_affiliations
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
                'country_iso_3166': 'BR',
                'email': u'caioisola@yahoo.com.br',
                'state': u'SP',
                'orgdiv1': u'Departamento de Ci\xeancias Biol\xf3gicas',
                'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'
            }, {
                'index': u'A02',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'country_iso_3166': 'BR',
                'email': u'alex_peressin@yahoo.com.br',
                'state': u'SP',
                'orgdiv1': u'Programa de P\xf3s-Gradua\xe7\xe3o em Diversidade Biol\xf3gica e Conserva\xe7\xe3o',
                'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'
            }, {
                'index': u'A03',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'country_iso_3166': 'BR',
                'email': u'mcetra@ufscar.br',
                'state': u'SP',
                'orgdiv1': u'Departamento de Ci\xeancias Ambientais',
                'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'
            }, {
                'index': u'A04',
                'city': u'Sorocaba',
                'country': u'BRAZIL',
                'country_iso_3166': 'BR',
                'email': u'vbarrella@pucsp.br',
                'state': u'SP',
                'orgdiv1': u'Laborat\xf3rio de Ecossistemas Aqu\xe1ticos',
                'institution': u'PONTIFICIA UNIVERSIDADE CATOLICA DE SAO PAULO'
            }
        ]
        self.maxDiff = None
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
                'country_iso_3166': 'BR',
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

        expected = [{u'index': u'', u'institution': u'UNIVERSIDADE FEDERAL DE SAO CARLOS'}]

        self.assertEqual(article.affiliations, expected)

    def test_affiliation_with_country_iso_3166(self):

        article = self.article

        del(article.data['article']['v70'])

        article.data['article']['v70'] = [
            {
                u"1": u"Escuela Nacional de Enfermería y Obstetricia",
                u"2": u"División de Estudios de Posgrado e Investigación",
                u"q": u"Mexico",
                u"c": u"México",
                u"i": u"A01",
                u"l": u"a",
                u"p": u"MX",
                u"s": u"D.F.",
                u"_": u"Universidad Nacional Autónoma de México"
           }
        ]

        expected = [
            {
                'index': u'A01',
                'city': u'México',
                'state': u'D.F.',
                'country': u'Mexico',
                'country_iso_3166': u'MX',
                'orgdiv1': u'Escuela Nacional de Enfermería y Obstetricia',
                'orgdiv2': u'División de Estudios de Posgrado e Investigación',
                'institution': u'Universidad Nacional Autónoma de México'
            }
        ]

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

    def test_abstracts(self):
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

        expected = {u'pt': u'Resumo do Artigo', u'en': u'Article Abstract'}

        self.assertEqual(article.abstracts(iso_format=None), expected)

    def test_abstracts_without_v83(self):
        article = self.article

        del(article.data['article']['v83'])

        self.assertEqual(article.abstracts(iso_format=None), None)

    def test_abstracts_iso639_2(self):
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

        expected = {u'por': u'Resumo do Artigo', u'eng': u'Article Abstract'}

        self.assertEqual(article.abstracts(iso_format='iso 639-2'), expected)

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

    def test_publication_type_book_chapter(self):
        json_citation = {}

        json_citation['v18'] = [{u'_': u'It is the book title'}]
        json_citation['v12'] = [{u'_': u'It is the book chapter'}]

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

        self.assertEqual(citation.authors, [])

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

    def test_elocation_14(self):
        json_citation = {}

        json_citation['v14'] = [{u'e': u'eloc1'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.elocation, u'eloc1')

    def test_elocation_514(self):
        json_citation = {}

        json_citation['v514'] = [{u'e': u'eloc2'}]

        citation = Citation(json_citation)

        self.assertEqual(citation.elocation, u'eloc2')

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

    def test_mixed_citation_without_data(self):
        citation = self.citation

        self.assertEqual(citation.mixed_citation, None)

    def test_mixed_citation_1(self):
        citation = self.citation

        citation.data['mixed'] = u'<p><font face=\"verdana\" size=\"2\">ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.     '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_2(self):
        citation = self.citation

        citation.data['mixed'] = u'<p><font face=\"verdana\" size=\"2\">ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</FONT></P>    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_3(self):
        citation = self.citation

        citation.data['mixed'] = u'< p >< font face=\"verdana\" size=\"2\">ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.< / FONT>< / P >    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_4(self):
        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_5(self):
        ## removing p tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., The basis of some <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_6(self):
        ## fixing i

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., The basis of some <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <i >Journal of Industrial Economics< / I>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_7(self):
        ## change b to strong

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\"><b>ALCHIAN, A .A.< /b>, The basis of some <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'<strong>ALCHIAN, A .A.</strong>, The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_8(self):
        ## fixing u

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">< B>ALCHIAN, A .A.< /b>, The < u >basis</U > of some <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <I>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'<strong>ALCHIAN, A .A.</strong>, The <u>basis</u> of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_9(self):
        ## change em to strong

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\"><em>ALCHIAN, A .A.< /em>, The < u >basis</U > of some <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <I>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'<strong>ALCHIAN, A .A.</strong>, The <u>basis</u> of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_10(self):
        ## fixing small

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\"><em>ALCHIAN, A .A.< /em>, The < u >basis</U > of < small>some</ SMALL> <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <I>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'<strong>ALCHIAN, A .A.</strong>, The <u>basis</u> of <small>some</small> recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_11(self):
        ## removing tt

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\"><em>ALCHIAN, A .A.< /em>, The < u >basis</U > of < small>some</ SMALL> <p>recent<p> <tt>advances< / tt> <font face>in</font> the theory of   management of the firm, <I>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'<strong>ALCHIAN, A .A.</strong>, The <u>basis</u> of <small>some</small> recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_12(self):
        ## removing span tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., <span>The< / span > basis of some <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_13(self):
        ## removing cite tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., <span>The< / span > < cite>basis< / CITE> of some <p>recent<p> advances <font face>in</font> the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_14(self):
        ## removing country-region tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., <span>The< / span > < cite>basis< / CITE> of some <p>recent<p> advances <font face>in</font> the theory of   management <country-region >of< /COUNTRY-region > the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P>    '

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_15(self):
        ## removing <font face="Verdana,"/> tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., <span>The< / span > < cite>basis< / CITE> of some <p>recent<p> advances <font face>in</font> the theory of   management <country-region >of< /COUNTRY-region > the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P><font face="Verdana,"/>'

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_16(self):
        ## removing place tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., <place>The< / place > < cite>basis< / CITE> of some <p>recent<p> advances <font face>in</font> the theory of   management <country-region >of< /COUNTRY-region > the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P><font face="Verdana,"/>'

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_17(self):
        ## removing state tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., < state >The< /State> < cite>basis< / CITE> of some <p>recent<p> advances <font face>in</font> the theory of   management <country-region >of< /COUNTRY-region > the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P><font face="Verdana,"/>'

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_18(self):
        ## removing city tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., <city >The< /city> < cite>basis< / CITE> of some <p>recent<p> advances <font face>in</font> the theory of   management <country-region >of< /COUNTRY-region > the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P><font face="Verdana,"/>'

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')

    def test_mixed_citation_19(self):
        ## removing region tags in the middle

        citation = self.citation

        citation.data['mixed'] = u'<    p><  font face=\"verdana\" size=\"2\">ALCHIAN, A .A., <region >The< /region> < cite>basis< / CITE> of some <p>recent<p> advances <font face>in</font> the theory of   management <country-region >of< /COUNTRY-region > the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.</   FONT><  /P><font face="Verdana,"/>'

        self.assertEqual(citation.mixed_citation, u'ALCHIAN, A .A., The basis of some recent advances in the theory of   management of the firm, <i>Journal of Industrial Economics</i>, v. 14, n. 4, p. 30-44, 1965.')
