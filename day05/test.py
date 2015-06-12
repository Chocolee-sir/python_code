#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'


import hashlib

file='e:/ftp_data/liyiliang/2007.wmv'
md5file=open(file,'rb')
md5=hashlib.md5(md5file.read()).hexdigest()
md5file.close()
print(md5)