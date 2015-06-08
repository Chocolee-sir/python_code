#!/usr/bin/env python
import readline,sys
result = None
list_info = []
info = raw_input('input:').replace(' ', '')
if info.isalpha() or info == "":
    print 'Sorry input error...'
    sys.exit()

def rep(info):
    global list_info 
    if '+' in info:
        info = info.replace('+',' + ')
    if '-' in info:
        info = info.replace('-',' - ')
    if '*' in info:
        info = info.replace('*',' * ')
    if '/' in info:
        info = info.replace('/',' / ')
    if '(' in info:
        info = info.replace('(',' ( ')
    if ')' in info:
        info = info.replace(')',' ) ')
    list_info =info.split()

def jisuan(list_info):            
    global result
    while '/' in list_info:
        a = float(list_info[list_info.index('/')-1]) / float(list_info[list_info.index('/')+1])
        list_info.insert(list_info.index('/')-1,a)
        list_info.pop(list_info.index('/')-1)
        list_info.pop(list_info.index('/')+1)
        list_info.pop(list_info.index('/'))
    while '*' in list_info:
        a = float(list_info[list_info.index('*')-1]) * float(list_info[list_info.index('*')+1])    
        list_info.insert(list_info.index('*')-1,a) 
        list_info.pop(list_info.index('*')-1)
        list_info.pop(list_info.index('*')+1)
        list_info.pop(list_info.index('*'))
    while '-' in list_info:
        a = float(list_info[list_info.index('-')-1]) - float(list_info[list_info.index('-')+1])
        list_info.insert(list_info.index('-')-1,a)
        list_info.pop(list_info.index('-')-1)
        list_info.pop(list_info.index('-')+1)
        list_info.pop(list_info.index('-')) 
    while '+' in list_info:
        a = float(list_info[list_info.index('+')-1]) + float(list_info[list_info.index('+')+1])
        list_info.insert(list_info.index('+')-1,a)
        list_info.pop(list_info.index('+')-1)
        list_info.pop(list_info.index('+')+1)
        list_info.pop(list_info.index('+'))
    result=float(list_info[0])

def run(list_info):
    list_end = []
    if '(' in list_info:
        list_info.reverse()
        last_k = len(list_info) - list_info.index('(') -1
        list_info.reverse()
        first_k = list_info[last_k:].index(')')
        list1 = list_info[last_k+1:last_k+first_k]
        if list1[0] == '-':
            i = '%s%s' %(list1[0],list1[1])
            fushu = float(i)
            list_end.append(fushu)
        else:
            jisuan(list1)
            list_end.append(result)
        new_list = list_info[:last_k] + list_end + list_info[last_k+first_k+1:]
        if '(' in new_list:
            run(new_list)
        else:
            jisuan(new_list)
            print result
    elif ')' not in list_info:
        jisuan(list_info)
        print result
    else:
        print "Sorry,invalid syntax!"

try:
    rep(info)
    run(list_info)
except:
    print "Sorry,invalid syntax!"
