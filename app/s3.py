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

    def __init__(self, accessKeyID, secretAccessKey):
        self.bucketName = accessKeyID.lower() + '-dump'
        self.connect()
        self.createBucket()

    def connect(self):
        self.conn = boto.connect_s3(self.accessKeyID, self.secretAccessKey)

    def createBucket(self):
        self.bucket = self.conn.create_bucket(self.bucketName, location=boto.s3.connection.Location.DEFAULT)

    def uploadFile(self, fileName):
        print("Uploading {} to Amazon S3 bucket {}".format(fileName, self.bucketName))

        k = Key(self.bucket)
        k.key = 'my test file'
        k.set_contents_from_filename(fileName, cb=percent_cb, num_cb=10)
