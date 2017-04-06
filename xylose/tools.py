from . import choices


def creative_commons_text(license, html=False):

    splited_license = license.split('/')

    if not len(splited_license) == 2:
        return None

    license, version = splited_license

    license_text = choices.CREATIVE_COMMONS_TEXTS.get(license.upper(), None)

    if not license_text:
        return None

    text = u'This work is licensed under a Creative Commons %s %s International License.' % (license_text, version)

    if html:
        text = u'This work is licensed under a <a href="http://creativecommons.org/licenses/%s/%s/">Creative Commons %s %s International License</a>.' % (license.lower(), version, license_text, version)

    return text


def get_language(language, iso_format):
    if iso_format == u'iso 639-1':
        if language in choices.ISO639_1:
            return language
        else:
            return u'#undefined %s#' % language
    elif iso_format == u'iso 639-2':
        return choices.ISO639_1_to_2.get(language, u'#undefined %s#' % language)

    return language


def get_date(date):
    pub_date = [date[0:4]]

    months = range(1, 13)
    days = range(1, 32)

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


def get_country_ISO_3166_code_from_name(something):

    iso_country_ISP_3166 = None

    return iso_country_ISP_3166