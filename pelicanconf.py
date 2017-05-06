#!/uterspill-ensr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'guozhongxin'
SITENAME = u"guozhongxin's blog"
SITEURL = 'http://www.guozhongxin.com'
THEME='tuxlite_tbs'

PATH = 'content'

GITHUB_URL = 'https://github.com/guozhongxin'
ARCHIVES_URL = 'archives.html'
ARTICLE_URL = 'pages/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'pages/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

TIMEZONE = 'Asia/Shanghai'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

DEFAULT_LANG = u'zh'

#DISQUS_SITENAME = 'guozhongxin'
GENTIE163_COMMENT = True

GOOGLE_ANALYTICS = 'UA-55010568-1'
GOOGLE_CUSTOM_SEARCH_NAVBAR = '010247264787335947909:uh5tyymk1xe'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
ARTICLE_FEED_RSS='feeds/articles/%s.rss.xml'

PLUGIN_PATHS = ['/Users/macbook/Documents/myblog/plugins']
PLUGINS = ["baidu_sitemap","sitemap"]

## 配置sitemap 插件
BAIDU_SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.9,
        "indexes": 0.5,
        "pages": 0.6,
    },
    "changefreqs": {
        "articles": "daily",
        "indexes": "daily",
        "pages": "daily",
    }
}

## 配置sitemap 插件
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.9,
        "indexes": 0.5,
        "pages": 0.6,
    },
    "changefreqs": {
        "articles": "daily",
        "indexes": "daily",
        "pages": "daily",
    }
}

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python', 'http://python.org/'),
         ('Spark', 'http://spark.apache.org/'),)

# Social widget
SOCIAL = ((' Linkedin', 'http://www.linkedin.com/profile/view?id=317695648'),
          (' Github', 'https://github.com/guozhongxin'),
          (' Weibo', 'http://weibo.com/u/1832109601'),
          (' E-mail', 'mailto:buptmr.guo@gmail.com'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
