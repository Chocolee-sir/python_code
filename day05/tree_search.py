#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'

tree_dic = {

    'id':1,
    'name': 'alex',
    'node':{
        'id':2,
        'node':{
            'id':3,
            'name':'alex',
            'node':{
                'id':4,
                'node':{
                    'id':5,
                    'name':'jack',
                    'node':{},
                }
            }
        }
    }
}

count = 0
def find_alex(tree_dic):
    global count
    for k,v in tree_dic.items():
        if v == 'alex':
            count += 1
        elif type(v) is dict:
            find_alex(v)

find_alex(tree_dic)
print count