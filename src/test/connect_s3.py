from __future__ import print_function
import sys, os
TWCC_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path[1]=TWCC_PATH

from termcolor import colored
def TWCC_LOGO():
    print (
        colored(">"*10+" Welcome to ", 'yellow'),
        colored('TWCC.ai', 'white', attrs=['reverse', 'blink']),
        colored(" "+"<"*10, 'yellow')
    )
TWCC_LOGO() ## here is logo
import re
from twcc.services.s3 import S3

import click,time



if __name__ == '__main__':
    s3 = S3('s3','*','*','twgc-s3.nchc.org.tw')
    #buckets = s3.list_bucket()
    #s3.test_table(buckets)
    #s3.create_bucket('thisistest5')
    buckets = s3.list_bucket()
    s3.test_table(buckets)
    #s3.upload_bucket('this_is_test_file.txt','thisistest4','this_is_test_file.txt')
    #s3.upload_bucket('this_is_test_file2.txt','thisistest4','this_is_test_file2.txt')
    files = s3.list_object('thisistest5')
    s3.test_table(files)
    #s3.upload_bucket(path = '/Users/WillyChen/Learning/try_loc',bucket_name = 'thisistest5',r = True)
    #s3.download_bucket(bucket_name = 'thisistest5',path='/Users/WillyChen/Learning/try_loc2',r = True)
    #files = s3.list_object('thisistest5')
    #s3.test_table(files)
    s3.del_bucket('thisistest5')

