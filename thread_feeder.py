# -*- coding: utf-8 -*-
#!/usr/bin/env python

import threading
import Queue
import feedparser


THREAD_LIMIT = 4
jobs = Queue.Queue(0)
rss_to_process = Queue.Queue(THREAD_LIMIT)


feed_sources = {u'EL PAÍS': 'http://ep00.epimg.net/rss/elpais/portada.xml',
                u'eldiario.es': 'http://eldiario.es.feedsportal.com/rss',
                u'La Razón': 'http://www.larazon.es/RSS-portlet/feed/la-razon/portada',
                u'Público.es': 'http://feeds.publico.es/atom/principal.xml'}


def thread():
    while True:
        try:
            id, feed_url = jobs.get(False)
            print feed_url
        except Queue.Empty:
            return

        entries = feedparser.parse(feed_url).entries
        rss_to_process.put((id, entries), True)


if __name__ == "__main__":
    for name, url in feed_sources.iteritems():
        jobs.put([name, url])

    for n in xrange(THREAD_LIMIT):
        t = threading.Thread(target=thread)
        t.start()

    while threading.activeCount() > 1 or not rss_to_process.empty():
        try:
            id_job, entries = rss_to_process.get(False, 1)
        except Queue.Empty:
            continue