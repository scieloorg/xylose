from . import choices

def get_language(iso_format, language):
    if iso_format == u'iso 639-1':
        if language in choices.ISO639_1:
            return language
        else:
            return u'#undefined %s#' % language
    elif iso_format == u'iso 639-2':
        return choices.ISO639_1_to_2.get(language, u'#undefined %s#' % language)
    
    return language