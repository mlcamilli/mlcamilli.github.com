#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Matt Camilli'
SITENAME = 'MattCamilli'
SITEURL = ''
PATH = 'content'
TIMEZONE = 'US/Eastern'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

THEME = "themes/camillitheme"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

TEMPLATE_PAGES = {
    'extra/about.html': 'about.html',
    'extra/robots.txt': 'robots.txt',
    'extra/talks.html' : 'talks.html'
}

ARTICLE_EXCLUDES = (('pages','extra','drafts', 'talks'))
STATIC_PATHS = [
        'talks',
]
