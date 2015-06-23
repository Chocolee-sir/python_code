#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from UserClass import UserInfo

U = UserInfo('admin')
a = U.admin_info()

tmp_list = []
for i in a.items():
    tmp_list.append(i[1])

print(tmp_list)