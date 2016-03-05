#!/usr/bin/python
# Copyright (c) 2011, Xabier (slok) Larrakoetxea
# Copyright (c) 2011, Iraide (Sharem) Diaz
#
# 3 clause/New BSD license:
#   opensource: http://www.opensource.org/licenses/BSD-3-Clause
#   wikipedia: http://en.wikipedia.org/wiki/BSD_licenses
#
#-----------------------------------------------------------------------
# This script  allows to upload to Fileserve with FTP various files at the same time
#
# Use:
#   python ./ftpFilserveUploader.py ./Downloads/xxx.y ./yyyy.z  /home/xxx/yyyy.zz
#
from ftplib import FTP
import sys
import os
########### MODIFY ########################

USER = 'xxxxxx'
PASS = 'xxxxxxxxx'
DESTINATION_DIR="documents"
########### MODIFY IF YOU WANT ############
UPLOADED_DIR='uploaded'
SERVER = 'ftp.fileserve.com'
PORT = 21
BINARY_STORE = True # if False then line store (not valid for binary files (videos, music, photos...))

###########################################
from ftpparameters import *



def print_line(result):
    print(result)

def connect_ftp():
    #Connect to the server
    ftp = FTP()
    ftp.connect(SERVER, PORT)
    ftp.login(USER, PASS)

    return ftp

def upload_file(ftp_connetion, upload_file_path):

    #Open the file
    try:
        upload_file = open(upload_file_path, 'r')

        #get the name
        path_split = upload_file_path.split('/')
        final_file_name = path_split[len(path_split)-1]

        #transfer the file
        print('Uploading ' + final_file_name + '...')

        if BINARY_STORE:
            ftp_connetion.storbinary('STOR '+ final_file_name, upload_file)
        else:
            #ftp_connetion.storlines('STOR ' + final_file_name, upload_file, print_line)
            ftp_connetion.storlines('STOR '+ final_file_name, upload_file)

        print('Upload finished.')
    except IOError:
        print ("No such file or directory... passing to next file")


def getFileList(mydir):
    filelist = [ os.path.join(mydir,f) for f in os.listdir(mydir) if os.path.isfile(os.path.join(mydir,f))]
    return filelist

def getFilesToUpload():
    if len(sys.argv) < 2:
        print "Enter source local directory as parameter"
    else:
        filestoupload=[]
        sourcedirs=sys.argv[1:]
        for arg in sourcedirs:
            print arg
            filestoupload.extend(getFileList(arg))
    return filestoupload

def cdTree(currentDir,ftp):
    if currentDir != "":
        try:
            ftp.cwd(currentDir)
        except IOError:
            cdTree("/".join(currentDir.split("/")[:-1]))
            ftp.mkd(currentDir)
            ftp.cwd(currentDir)


def uploadfiles():
    filelist=getFilesToUpload()
    try:
        ftp_conn = connect_ftp()
        print "Connected"
        cdTree(DESTINATION_DIR,ftp_conn)
    except:
        print 'Connection error - unable to open connection to ftp server or nonexisting dir'
        sys.exit(1)
    else:
        for item in filelist:
            print "Uploading file: " + str(item)
            try:
                upload_file(ftp_conn, item)
            except:
                print "Error uploading file: "+str(item)
            else:
                print "Uploaded file: "+str(item)


#Take all the files and upload all
#ftp_conn = connect_ftp()
#for arg in sys.argv:
#    upload_file(ftp_conn, arg)
print UPLOADED_DIR
print SERVER
uploadfiles()