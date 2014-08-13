# -*- coding: utf-8 -*-
# Copyright (c) 2014, Brian Jimenez <brian@samurai.cat>

"""
Module to deal with feeds
"""


import gevent
from gevent import monkey

monkey.patch_all()

import feedparser

from urllib2 import urlopen

feed_sources = {u'EL PAÍS': 'http://ep00.epimg.net/rss/elpais/portada.xml',
                u'eldiario.es': 'http://eldiario.es.feedsportal.com/rss',
                u'La Razón': 'http://www.larazon.es/RSS-portlet/feed/la-razon/portada',
                u'Público.es': 'http://feeds.publico.es/atom/principal.xml'}


def get_data_from_feed(feed_source):
    """Gets the feed"""
    feed_data = feedparser.parse(feed_source)
    return feed_data['entries']


def get_feed(feed_url):
    print('Starting %s' % feed_url)
    feed_data = urlopen(url).read()
    print('%s: %s bytes' % (feed_url, len(feed_data)))
    return feed_url, feed_data


if __name__ == "__main__":
    jobs = [gevent.spawn(get_feed, url) for url in feed_sources.itervalues()]

    gevent.wait(jobs)

    for job in jobs:
        url, raw_data = job.value
        print url
        data = feedparser.parse(raw_data)
        print len(data['entries'])