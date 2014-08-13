# -*- coding: utf-8 -*-
#!/usr/bin/env python

from multiprocessing import Pool
from multiprocessing import freeze_support
import feedparser


feed_sources = {u'EL PAÍS': 'http://ep00.epimg.net/rss/elpais/portada.xml',
                u'eldiario.es': 'http://eldiario.es.feedsportal.com/rss',
                u'La Razón': 'http://www.larazon.es/RSS-portlet/feed/la-razon/portada',
                u'Público.es': 'http://feeds.publico.es/atom/principal.xml'}


def fetch_rss(feed_url):
    try:
        data = feedparser.parse(feed_url)
    except Exception as e:
        return feed_url, None, str(e)
    else:
        e = data.get('bozo_exception')
        return feed_url, data['entries'], str(e) if e else None


if __name__ == "__main__":
    freeze_support()

    urls = feed_sources.itervalues()
    pool = Pool(4)
    for url, items, error in pool.imap_unordered(fetch_rss, urls):
        if error is None:
            print(url, len(items))
        else:
            print(url, error)