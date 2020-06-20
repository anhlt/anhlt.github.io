#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Carol'
SITENAME = 'Deep Learning'
SITEURL = 'https://deepmlml.com'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'vi'

# Plugin
PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican-bootstrapify', 'liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.youtube',
           'liquid_tags.include_code', 'render_math', 'ipynb.liquid', 'pelican-toc']

BOOTSTRAPIFY = {
    'table': ['table', 'table-striped', 'table-hover'],
    'img': ['img-fluid'],
    'blockquote': ['blockquote'],
}

DIRECT_TEMPLATES = ['index', 'tags', 'categories',
                    'authors', 'archives', 'sitemap']
SITEMAP_SAVE_AS = 'sitemap.xml'

# Theme
THEME = 'themes/alchemy/alchemy'
SITESUBTITLE = '\u2728 Hành trình học deep learning'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Machine Learning Cơ Bản', 'http://machinelearningcoban.com/'),
         ('Python.org', 'http://python.org/'),
         ('Pytorch', 'http://pytorch.org/'),)

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
STATIC_PATHS = ['images', 'code', 'downloads', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}}


TOC = {
    'TOC_HEADERS': '^h[1-3]',  # What headers should be included in
    # the generated toc
    # Expected format is a regular expression

    'TOC_RUN': 'true',    # Default value for toc generation,
    # if it does not evaluate
    # to 'true' no toc will be generated

    'TOC_INCLUDE_TITLE': 'false',     # If 'true' include title in toc
}
