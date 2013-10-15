from . import choices

def get_language(language, iso_format):
    if iso_format == u'iso 639-1':
        if language in choices.ISO639_1:
            return language
        else:
            return u'#undefined %s#' % language
    elif iso_format == u'iso 639-2':
        return choices.ISO639_1_to_2.get(language, u'#undefined %s#' % language)
    
    return language


def get_publication_date(date):
    pub_date = [date[0:4]]

    months = range(1,13)
    days = range(1,31)

    try:
        month = int(date[4:6])
    except ValueError:
        month = None

    try:
        day = int(date[6:8])
    except ValueError:
        day = None

    if month in months:
        pub_date.append("%02d" % month)

        if day in days:
            pub_date.append("%02d" % day)


    return "-".join(pub_date)