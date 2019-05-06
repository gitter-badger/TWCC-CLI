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
from twcc.services.S3 import S3

import click,time

@click.group()
def cli():
    pass

# Bucket functions
@click.command()
@click.option('-n','--name','bucket_name',required=True,type=str,help='Name of the Bucket')
def create_bucket(bucket_name):
    ''' Create new s3 bucket.
    '''
    s3 = S3()
    s3.create_bucket(bucket_name)

@click.command()
@click.option('-lb','list4buckets',is_flag = False,type=bool, help = 'Show all buckets in this project')
def list_buckets(list4buckets):
    ''' List all the exist s3 buckets in the project.
    '''
    s3 = S3()
    if not list4buckets:
        buckets = s3.list_bucket()
        s3.test_table(buckets)

@click.command()
@click.option('-n','--name','bucket_name',required=True, help = 'Name of the Bucket.')
@click.option('-df','df',is_flag = True,help = 'Help delete all the files inside the bucket before delete bucket.')
def del_bucket(bucket_name,df):
    ''' Delete s3 bucket
    '''
    s3 = S3()
    s3.del_bucket(bucket_name,df)

# File functions
@click.command()
@click.option('-n','--name','bucket_name',required=True, help = 'Name of the Bucket.')
def list_files(bucket_name):
    ''' List all the exist files inside the s3 bucket.
    '''
    s3 = S3()
    files = s3.list_object(bucket_name)
    s3.test_table(files)

@click.command()
@click.option('-n','--name','bucket_name',required=True, help = 'Name of the Bucket.')
@click.option('-f','--file_name','file_name',required=True, help = 'Name of the File.')
def del_file(bucket_name,file_name):
    ''' Delete file from s3 bucket
    '''
    s3 = S3()
    s3.del_object(bucket_name,file_name)

@click.command()
@click.option('-s','--source','source', help = 'Name of the File.')
@click.option('-d','--directory','directory', help = 'Name of the Bucket.')
@click.option('-k','--key','key',help ='The name of the key to upload to.') 
@click.option('-r','r',is_flag = True,help = 'Recursively copy entire directories.' )
def upload(source,directory,key,r):
    ''' Upload to s3 bucket
    '''
    s3 = S3()
    # Check for source type
    if os.path.isdir(source):
        if r != True:
            raise Exception("{} is path, need to set recursive to True".format(source))
        s3.upload_bucket(path = source ,bucket_name = directory,r=r)
    else:
        if key == None:
            key = source.split('/')[-1]
        s3.upload_bucket(file_name = source ,bucket_name = directory,key = key)

#download_bucket(self,bucket_name=None,key=None,file_name=None,path=None,r=False)
@click.command()
@click.option('-s','--source','source', help = 'Name of the Bucket.')
@click.option('-d','--directory','directory', help = 'Name of the path.')
@click.option('-k','--key','key',help ='The name of the key to download.') 
@click.option('-r','r',is_flag = True,help = 'Recursively copy entire directories.' )
def download(source,directory,key,r):
    ''' Download from s3 bucket
    '''
    s3 = S3()
    # Check for source type 
    if not s3.check_4_bucket(source):
        raise Exception("No such bucket name {} exists".format(source))

    # Check if the directory exists
    if os.path.isdir(directory) and key == None:
        if r != True:
            raise Exception("{} is path, need to set recursive to True".format(directory))
        s3.download_bucket(bucket_name = source,path=directory,r=r)
    else:
        if directory.endswith('/'):
            directory = directory + key
        s3.download_bucket(file_name = directory,bucket_name = source,key = key)

cli.add_command(create_bucket)
cli.add_command(list_buckets)
cli.add_command(del_bucket)
cli.add_command(list_files)
cli.add_command(del_file)
cli.add_command(upload)
cli.add_command(download)

if __name__ == '__main__':
    cli()
    #s3 = S3()
    # Create a new bucket
    #s3.create_bucket('thisistestbucket')

    # List out all the new bucket
    #buckets = s3.list_bucket()
    #s3.test_table(buckets)
#
#    # Upload single file to bucket
#    s3.upload_bucket(file_name = '/Users/WillyChen/Work/UploadMe.txt',bucket_name = 'thisistestbucket',key = 'DownloadMe.txt')
#    # Download single file from bucket 
#    s3.download_bucket(bucket_name = 'thisistestbucket',key = 'DownloadMe.txt',file_name = '/Users/WillyChen/Work/DownloadMe.txt')
#
#    # List files inside of bucket
#    files = s3.list_object('thisistestbucket')
#    s3.test_table(files)
#
#    # Upload files to bucket
#    s3.upload_bucket(path = '/Users/WillyChen/Work/UploadFromHere',bucket_name = 'thisistestbucket',r = True)
#    # Download files to bucket
#    s3.download_bucket(bucket_name = 'thisistestbucket',path='/Users/WillyChen/Work/DownloadToHere',r = True)
#    files = s3.list_object('thisistestbucket')
#    s3.test_table(files)
#    # Delete bucket
#    s3.del_bucket('thisistestbucket')

