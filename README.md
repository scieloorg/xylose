# Xylose

A SciELO library to abstract a JSON data structure that is a product of the ISIS2JSON conversion using the ISIS2JSON type 3 data model.


[![Build Status](https://travis-ci.org/scieloorg/xylose.svg?branch=master)](https://travis-ci.org/scieloorg/xylose)
[![PyPI version](https://badge.fury.io/py/xylose.svg)](https://badge.fury.io/py/xylose)


## Objective

This library intends to delivery a object interface that abstracts the ISIS2JSON documents to facilitate the access to the SciELO documents metadata. This library will be mainly used during the migration process for the new SciELO architecture.

## Install

### Stable
```
$ pip install xylose
```

### Development

```
$ pip install -e git+https://github.com/scieloorg/xylose.git
```

## How to use

### Example

**Reading an Article**

    >>> import json
    >>> import urllib2
    >>> from xylose.scielodocument import Article
    >>> article_json = json.loads(urllib2.urlopen('http://articlemeta.scielo.org/api/v1/article/?code=S2179-975X2011000300002&format=json').read())
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
    >>> journal_json = json.loads(urllib2.urlopen('http://articlemeta.scielo.org/api/v1/journal?collection=scl&issn=0103-0663').read())
    >>> journal = Journal(journal_json[0])
    >>> journal.title
    u'Revista de Odontologia da Universidade de S\xe3o Paulo'
    >>> journal.scielo_issn
    u'0103-0663'

**Reading an Issue**

    >>> import json
    >>> import urllib2
    >>> from xylose.scielodocument import Issue
    >>> issue_json = json.loads(urllib2.urlopen('http://articlemeta.scielo.org/api/v1/issue/?collection=scl&code=0103-066319970002').read())
    >>> issue = Issue(issue_json)
    >>> issue.journal
    u'Rev. Odontol. Univ. S\u00e3o Paulo'
    >>> issue.volume
    u'11'

## Testes Automatizados

No servidor local:
`python setup.py test`


## Report issues, or request changes

To report bugs or request some new functionality, you can [create a ticket](<https://github.com/scieloorg/xlose/issues>) with your requests.


## Development and Maintenance Team

- Desenvolvimento <dev@scielo.org>
- Infraestrutura <infra@scielo.org>
