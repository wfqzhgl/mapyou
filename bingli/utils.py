# -*-coding:utf8-*-

'''
Created on 2015年4月16日

@author: faqingw
'''

import os
import hashlib
import time
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def get_page_obj(request, queryset, perpage=30, tag=None):
    """
            获取分页对象
            输入：request：request；queryset：分页对象数据；perpage：页码，默认为30
            输出：分页后的对象数据
    """
    if perpage == "all" or perpage == 0:
        perpage = len(queryset)
        perpage = perpage if perpage > 0 else 1
    else:
        try:
            perpage = int(perpage)
        except:
            perpage = 30

    p = Paginator(queryset, perpage)
    try:
        page = request.REQUEST.get('page', None)
        if not page:
            kk = ('f_page' + tag) if tag else 'f_page'
            page = request.COOKIES.get(kk, 1)
        page = int(page)
    except ValueError:
        page = 1
    try:
        page_obj = p.page(page)
    except (EmptyPage, InvalidPage):
        page_obj = p.page(p.num_pages)
    return page_obj


def gen_file_name(file):
    """
            获取文件name
    """
    if not file:
        return ''
    path = str(file)
    filename = os.path.splitext(path)[0]
    ext=os.path.splitext(path)[1]
    hash_name=hashlib.md5(filename).hexdigest()
    fn = time.strftime('%Y%m%d%H%M%S')
    return fn+'_'+hash_name+ext


def handle_uploaded_file(path,f):
    """
        upload file to specific path(include file name)
    """
    if not f:
        return
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()