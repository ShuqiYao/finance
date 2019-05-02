# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/12/12

import datetime
import traceback
import os
def get_vals(vs):
    vals = ''
    for v in range(0,len(vs)):
        if v ==0:
            vals += str(vs[v])
        else:
            vals += '\t'+str(vs[v])
    return vals

def f(file,*info1):
    file.write(get_vals(info1)+'\n')
    file.flush()

def info_f(file,*info1):
    v = info_v(*info1)
    file.write(v+'\n')
    file.flush()

def info(*info1):
    print(info_v(*info1))

def info_v(*info1):
    return str(datetime.datetime.now())[0:19]+'\tINFO\t'+get_vals(info1)

def debug(*debug1):
    print(debug_v(*debug1))

def debug_v(*debug1):
    return str(datetime.datetime.now())[0:19]+'\tDEBUG\t'+get_vals(debug1)

def debug_f(file,*info1):
    v = debug_v(*info1)
    file.write(v+'\n')
    file.flush()

def warn(*warn1):
    print(warn_v(*warn1))

def warn_v(*warn1):
    return str(datetime.datetime.now())[0:19]+'\tWARN\t'+get_vals(warn1)

def warn_f(file,*info1):
    v = warn_v(*info1)
    file.write(v+'\n')
    file.flush()

def error(*error1):
    try:
        #print str(datetime.datetime.now())[0:19]
        # raise Exception(error_v(*error1))
        print(error_v(*error1))
    except Exception as e:
        traceback.print_exc()
        os._exit(1)

def error_v(*error1):
        return str(datetime.datetime.now())[0:19]+'\tERROR\t'+get_vals(error1)

def error_f(file,*info1):
    v = error_v(*info1)
    file.write(v+'\n')
    file.flush()

#print info('asdf','qwerqwer')