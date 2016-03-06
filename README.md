# FtpUploadFromDir 

Uploads files from dir to FTP and moves uploaded files to UPLOADED_DIR

Usage:

1. Modify parameters in script or create ftpparameters.py file in same dir as script and put yor own parameters in file.
```
USER = 'xxxxxx'
PASS = 'xxxxxxxxx'
DESTINATION_DIR="documents"
UPLOADED_DIR='uploaded'
SERVER = 'ftp.fileserve.com'
PORT = 21
BINARY_STORE = True # if False then line store (not valid for binary files (videos, music, photos...))
SENDER = "XXX@XXX"
RECEIVERS = ["XXXXX@XX.XXX","YYYYY@YYY.YY"]
MESSAGE = """TEXT FOR EMAIL"""
SUBJECT = "report of uploading files"
```
2. Start script with directory where files you want to upload are as parameter ie.

```./FtpServerUploader.py /PATH/TO/MY/DIR```
