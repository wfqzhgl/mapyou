# -*-coding:utf8-*-

'''
Created on 2015年4月16日

@author: faqingw
'''

import os
import hashlib
import time


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