import os

import boto3


class AWSFileHandler:
    def __init__(self):
        self.storage_bucket = os.environ.get('BUCKET_NAME')
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    def s3_create_client(self):
        return boto3.client(
            's3', aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_key)

    def s3_create_resource(self):
        return boto3.resource(
            's3', aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_key)

    #   upload a binary file to aws
    def upload_binary_file(self, binary_file_name):
        data = open(binary_file_name, 'rb')
        s3 = self.s3_create_resource()
        s3.Bucket(self.storage_bucket).put_object(Key=binary_file_name, Body=data)

    # Upload the new file to AWS S3
    def replace_binary_file(self, binary_file_name, new_file_name):
        s3 = self.s3_create_resource()
        data = open(new_file_name, 'rb')
        s3.Bucket(self.storage_bucket).put_object(Key=binary_file_name, Body=data)

    # download a binary file to aws cloud
    def download_binary_file(self, binary_file_name):
        s3 = self.s3_create_client()
        s3.download_file(self.storage_bucket, binary_file_name, binary_file_name)

    # Delete an object from aws cloud
    def delete_binary_file(self, binary_file_name):
        s3 = self.s3_create_client()
        s3.delete_object(Bucket=self.storage_bucket, Key=binary_file_name)  # Only **kw accepted

    def get_binary_file_url(self, binary_file_name):
        s3 = self.s3_create_client()
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.storage_bucket, 'Key': binary_file_name},
            ExpiresIn=3600  # URL expiration time in seconds
        )
        return url

    def put_object_from_file_stream_to_static(self, file_name, image_body):
        s3 = self.s3_create_client()
        bucket_name = self.storage_bucket
        s3.put_object(Bucket=bucket_name, Key=f'Static/{file_name}', Body=image_body)

    def put_object_from_file_stream_to_articles(self, file_name, image_body):
        s3 = self.s3_create_client()
        bucket_name = self.storage_bucket
        s3.put_object(Bucket=bucket_name, Key=f'Articles/{file_name}', Body=image_body)




