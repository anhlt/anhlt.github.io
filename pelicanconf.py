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
           'liquid_tags.youtube', 'liquid_tags.vimeo',
           'liquid_tags.include_code', 'render_math']

BOOTSTRAPIFY = {
    'table': ['table', 'table-striped', 'table-hover'],
    'img': ['img-fluid'],
    'blockquote': ['blockquote'],
}

DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'sitemap']
SITEMAP_SAVE_AS = 'sitemap.xml'

# Theme
THEME = 'themes/alchemy/alchemy'
SITESUBTITLE = 'Hành trình đi lấy vợ \u2728 à nhầm, hành trình học deep learning'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Machine Learning Cơ Bản', 'http://machinelearningcoban.com/'),
         ('Python.org', 'http://python.org/'),
         ('Pytorch', 'http://pytorch.org/'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/tuananh_bk'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
DISQUS_SITENAME = "deepmlml"
GOOGLE_ANALYTICS = "UA-12027115-4"

# liquid tag
CODE_DIR = 'code'

# copy CNAME
STATIC_PATHS = ['images', 'code', 'downloads', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}}
