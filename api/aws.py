import os

import boto3


class AWSFileHandler:
    def __init__(self, storage_bucket='almd-site'):
        self.storage_bucket = storage_bucket

    #
    # #   upload a binary file to aws
    # def upload_binary_file(self, binary_file_name):
    #     data = open(binary_file_name, 'rb')
    #     s3 = boto3.resource('s3')
    #     s3.Bucket(self.storage_bucket).put_object(Key=binary_file_name, Body=data)
    #
    # # upload a binary file to aws cloud
    # def download_binary_file(self, binary_file_name):
    #     s3 = boto3.client('s3')
    #     s3.download_file(self.storage_bucket, binary_file_name, binary_file_name)
    #
    # def replace_binary_file(self, binary_file_name, new_file_name):
    #     s3 = boto3.resource('s3')
    #     # Upload the new file to AWS S3
    #     data = open(new_file_name, 'rb')
    #     s3.Bucket(self.storage_bucket).put_object(Key=binary_file_name, Body=data)
    #
    # # Delete and object from aws cloud
    # def delete_binary_file(self, binary_file_name):
    #     s3 = boto3.client('s3')
    #     s3.delete_object(Bucket=self.storage_bucket, Key=binary_file_name)  # Only **kw accepted

    # def get_binary_file_url(self, binary_file_name):
    #     s3 = boto3.client('s3')
    #     url = s3.generate_presigned_url(
    #         ClientMethod='get_object',
    #         Params={'Bucket': self.storage_bucket, 'Key': binary_file_name},
    #         ExpiresIn=3600  # URL expiration time in seconds
    #     )
    #     return url

    def put_object_from_file_stream(self, file_name, image_body):
        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ.get('AWS_ACCSES_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

        bucket_name = self.storage_bucket
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=image_body)
