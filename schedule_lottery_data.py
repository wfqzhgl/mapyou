#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wufaqing'

import os
import sys
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup, NavigableString, Tag, Comment


def get_data(req_url):
    """

    """
    try:
        request = urllib2.Request(req_url)
        request.add_header('Referer', 'http://datachart.500.com/ssq/history/history.shtml')
        request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        request.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36")
        opener = urllib2.build_opener()
        req_open = opener.open(request, timeout=10)
        soup = BeautifulSoup(req_open.read(), fromEncoding='gb2312')
        sp = soup.findAll("tr", attrs={'class': 't_tr1'})
        for tmp in sp:
            if type(tmp) in [NavigableString, Comment]:
                continue
            tmp_list = []
            for cc in tmp.contents:
                if type(cc) in [NavigableString, Comment]:
                    continue
                tmp_list.append(cc.text.replace(',', ''))
            print '-----------', len(tmp_list), tmp_list
            if len(tmp_list) == 16:
                d = tmp_list[15]
                if DataLotteryShsq.objects.filter(date=d).exists():
                    continue
                dm = DataLotteryShsq(code=tmp_list[0], reds=' '.join(tmp_list[1:7]), blue=tmp_list[7],
                                     award_total=tmp_list[9], count_1=tmp_list[10], award_1=tmp_list[11],
                                     count_2=tmp_list[12], award_2=tmp_list[13], bet_total=tmp_list[14],
                                     date=d)
                dm.save()
    except Exception, e:
        print e


if __name__ == "__main__":
    setting_module = "mapyou.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_module)

    from django.conf import settings
    import logging
    from app.models import *

    url = "http://datachart.500.com/ssq/history/newinc/history.php?limit=10000&sort=0"
    get_data(url)


