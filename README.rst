.. image:: https://secure.travis-ci.org/scieloorg/xylose.png?branch=master
`See Build details <http://travis-ci.org/#!/scieloorg/xylose>`_

======
Xylose
======

A SciELO library to abstract a JSON data structure that is a product of the ISIS2JSON conversion using the ISIS2JSON type 3 data model.

Objective
=========

This library intends to delivery a object interface that abstracts the ISIS2JSON documents to facilitate the access to the SciELO documents metadata. This library will be mainly used during the migration process for the new SciELO architecture.

Install
=======

How to use
==========

**Reading an Article**

    >>> import json
    >>> import urllib2
    >>> from xylose.scielodocument import Article
    >>> article_json = json.loads(urllib2.urlopen('http://200.136.72.162:7000/api/v1/article?code=S2179-975X2011000300002&format=json').read())
    >>> article = Article(article_json)
    >>> article.original_title()
    u'First adult record of Misgurnus anguillicaudatus, Cantor 1842 from Ribeira de Iguape River Basin, Brazil'
    >>> article.any_issn()
    u'2179-975X'
    >>> article.authors
    [{'role': u'ND', 'xref': [u'A01'], 'surname': u'Gomes', 'given_names': u'Caio Isola Dallevo do Amaral'}, {'role': u'ND', 'xref': [u'A02'], 'surname': u'Peressin', 'given_names': u'Alexandre'}, {'role': u'ND', 'xref': [u'A03'], 'surname': u'Cetra', 'given_names': u'Mauricio'}, {'role': u'ND', 'xref': [u'A04'], 'surname': u'Barrella', 'given_names': u'Walter'}]

**Reading a Journal**

    >>> import json
    >>> import urllib2
    >>> from xylose.scielodocument import Journal
    >>> journal_json = article_json = json.loads(urllib2.urlopen('http://200.136.72.162:7000/api/v1/journal?collection=scl&issn=0103-0663').read())
    >>> journal = Journal(journal_json[0])
    >>> journal.title
    u'Revista de Odontologia da Universidade de S\xe3o Paulo'
    >>> journal.scielo_issn
    u'0103-0663'