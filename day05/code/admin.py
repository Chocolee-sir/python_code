#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'

from UserClassMain import *

#管理员解锁
if __name__ == '__main__':
    a = UserClass('admin','admin')
    a.super_user()