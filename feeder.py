# -*- coding: utf-8 -*-
# Copyright (c) 2014, Brian Jimenez <brian@samurai.cat>

"""
Module to deal with feeds
"""

import feedparser
import gevent
import time


feed_sources = {u'EL PAÍS': 'http://ep00.epimg.net/rss/elpais/portada.xml',
                u'eldiario.es': 'http://eldiario.es.feedsportal.com/rss',
                u'La Razón': 'http://www.larazon.es/RSS-portlet/feed/la-razon/portada',
                u'Público.es': 'http://feeds.publico.es/atom/principal.xml'}


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        return ret, (time2 - time1) * 1000.0
    return wrap

@timing
def get_data_from_feed(feed_source):
    """Gets the feed"""
    return feedparser.parse(feed_source)


if __name__ == "__main__":
    data = {}
    for feed_name, feed_source in feed_sources.iteritems():
        data[feed_name], t = get_data_from_feed(feed_source)
        print t, data[feed_name]['feed']['title']
