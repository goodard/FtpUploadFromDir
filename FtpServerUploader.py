#!/usr/bin/python
# Copyright (c) 2016, Marko Stojanovic
#
# This is modification of Xabier (slok) Larrakoetxea and Iraide (Sharem) Diaz project
# https://gist.github.com/slok/1447559
#
# -----------------------------------------------------------------------
# This script  allows to upload files from multiple dirs to FTP server
#
# Use:
#   python ./ftpFilserveUploader.py SOURCE_DIR
#
from ftplib import FTP
import sys
import os

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.MIMEText import MIMEText

########### MODIFY ########################

USER = 'xxxxxx'
PASS = 'xxxxxxxxx'
DESTINATION_DIR = "documents"
########### MODIFY IF YOU WANT ############
UPLOADED_DIR = 'uploaded'
SERVER = 'ftp.fileserve.com'
PORT = 21
BINARY_STORE = True  # if False then line store (not valid for binary files (videos, music, photos...))
SENDER = "XXX@XXX"
RECEIVERS = ["XXXXX@XX.XXX"]
MESSAGE = """TEXT FOR EMAIL"""
SUBJECT = "report of uploading files"
###########################################
# This will import  parameters defined in file ftpparameters.py  overwriting one ABOVE
from ftpparameters import *


def sendMail(sender=SENDER, receivers=RECEIVERS, message=MESSAGE, subject=SUBJECT):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ",".join(receivers)
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print 'Successfully sent email'
    except smtplib.SMTPException:
        print 'Error: unable to send email'


def print_line(result):
    print(result)


def connect_ftp():
    # Connect to the server
    ftp = FTP()
    ftp.connect(SERVER, PORT)
    ftp.login(USER, PASS)

    return ftp


def upload_file(ftp_connetion, upload_file_path):
    # Open the file
    try:
        upload_file = open(upload_file_path, 'r')

        # get the name
        path_split = upload_file_path.split('/')
        final_file_name = path_split[len(path_split) - 1]

        # transfer the file
        print('Uploading ' + final_file_name + '...')

        if BINARY_STORE:
            ftp_connetion.storbinary('STOR ' + final_file_name, upload_file)
        else:
            # ftp_connetion.storlines('STOR ' + final_file_name, upload_file, print_line)
            ftp_connetion.storlines('STOR ' + final_file_name, upload_file)

        print('Upload finished.')
    except IOError:
        print ("No such file or directory... passing to next file")


def getFileList(mydir):
    filelist = [os.path.join(mydir, f) for f in os.listdir(mydir) if os.path.isfile(os.path.join(mydir, f))]
    return filelist


def getFilesToUpload():
    if len(sys.argv) < 2:
        print "Enter source local directory as parameter"
    else:
        filestoupload = []
        sourcedirs = sys.argv[1:]
        for arg in sourcedirs:
            print arg
            filestoupload.extend(getFileList(arg))
    return filestoupload


def cdTree(currentDir, ftp):
    if currentDir != "":
        try:
            ftp.cwd(currentDir)
        except IOError:
            cdTree("/".join(currentDir.split("/")[:-1]))
            ftp.mkd(currentDir)
            ftp.cwd(currentDir)


def uploadfiles():
    filelist = getFilesToUpload()
    try:
        ftp_conn = connect_ftp()
        print "Connected"
        cdTree(DESTINATION_DIR, ftp_conn)
    except:
        print 'Connection error - unable to open connection to ftp server or nonexisting dir'
        MESSAGE = "Error when connecting to ftp. \n Nothing uploaded "
        SUBJECT = "Erron when connecting %s " %SERVER
        sendMail(message=MESSAGE,subject=SUBJECT)

        sys.exit(1)
    else:
        failed_files = []
        for item in filelist:
            print "Uploading file: " + str(item)
            try:
                upload_file(ftp_conn, item)
            except:
                print "Error uploading file: " + str(item)
                failed_files.append(item)
            else:
                print "Uploaded file: " + str(item)
                PATH = os.path.split(item)
                NEWDIR = os.path.join(PATH[0], UPLOADED_DIR)
                NEWPATH = os.path.join(NEWDIR, PATH[1])
                if os.path.exists(NEWDIR):
                    print NEWPATH
                    os.rename(item, NEWPATH)
                else:
                    print "Make new dir: " + str(NEWDIR)
                    os.mkdir(NEWDIR)
                    print "Move to: " + str(NEWPATH)
                    os.rename(item, NEWPATH)
        if len(failed_files)>0:
            MESSAGE=""
            for failed_item in failed_files:
                MESSAGE += "Failed file %s\n" % failed_item
                SUBJECT = "Failed files"
            sendMail(message=MESSAGE,subject=SUBJECT)
#        sendMail(message="TEST",subject="TEST")


if __name__ == "__main__":
    uploadfiles()
