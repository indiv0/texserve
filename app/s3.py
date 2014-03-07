import sys

import boto
import boto.s3
from boto.s3.key import Key


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


class Bucket(object):
    accessKeyID = ''
    secretAccessKey = ''
    bucketName = ''
    bucket = ()

    def __init__(self, bucketName, accessKeyID, secretAccessKey):
        self.bucketName = bucketName
        self.accessKeyID = accessKeyID
        self.secretAccessKey = secretAccessKey
        self.connect()
        self.getBucket()

    def connect(self):
        self.conn = boto.connect_s3(self.accessKeyID, self.secretAccessKey)

    def getBucket(self):
        self.bucket = self.conn.get_bucket(self.bucketName)

    def uploadFile(self, fileName):
        print("Uploading {} to Amazon S3 bucket {}".format(fileName, self.bucketName))

        k = Key(self.bucket)
        k.key = fileName
        k.set_contents_from_filename(fileName, cb=percent_cb, num_cb=10)

    def getFile(self, fileName):
        print("Downloading {} from Amazon S3 bucket {}".format(fileName, self.bucketName))

        k = Key(self.bucket)
        k.key = fileName
        return k.get_contents_as_string()
