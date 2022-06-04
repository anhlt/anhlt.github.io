#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Walking_pup'
SITENAME = 'Random Thoughts'
SITEURL = 'https://anhlt.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'en'

# Plugin
# PLUGIN_PATHS = ['plugins']

PLUGINS = ['pelican.plugins.liquid_tags', 'pelican.plugins.render_math', 'series']


LIQUID_TAGS = ["img", "literal", "video", "youtube",
               "vimeo", "include_code"]

IGNORE_FILES = [".ipynb_checkpoints"]
MARKUP = ('md', )

DIRECT_TEMPLATES = ['index', 'tags', 'categories',
                    'authors', 'archives', 'sitemap']
SITEMAP_SAVE_AS = 'sitemap.xml'

# Theme
THEME = 'themes/basic'
SITESUBTITLE = '\u2728 Suy nghĩ vu vơ'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('Facebook', 'https://www.facebook.com/deepmlml/'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
DISQUS_SITENAME = "deepmlml"
GOOGLE_ANALYTICS = "UA-12027115-4"

# liquid tag
CODE_DIR = 'code'

# copy CNAME
STATIC_PATHS = ['images', 'code']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

MARKDOWN = {
  'extension_configs': {
    'markdown.extensions.toc': {
      'title': 'Table of contents:' 
    },
    'markdown.extensions.codehilite': {'css_class': 'highlight'},
    'markdown.extensions.extra': {},
    'markdown.extensions.meta': {},
  },
  'output_format': 'html5',
}
