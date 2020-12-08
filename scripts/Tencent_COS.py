#coding:utf-8

from qcloud_cos import CosConfig
from django.conf import settings
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

region = 'ap-nanjing'     # 替换为用户的 Region 区域

config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
client = CosS3Client(config)

def create_bucket(name,region):
    client.create_bucket(Bucket="{}-{}".format(name,settings.TENCENT_SECRET_NUMBER))
    return "{}-{}".format(name,settings.TENCENT_SECRET_NUMBER)

def upload_file(bucketName,file_object,key):

    response = client.upload_file_from_buffer(
        Bucket=bucketName,
        Body=file_object,
        Key=key, #上传之后的名称
    )

    return "https://{}.cos.{}.myqcloud.com/{}".format(bucketName,settings.MY_REGION,key)


class TenCent_COS:


    def __init__(self):

        self.secret_id = settings.TENCENT_SECRET_ID
        self.secret_key =settings.TENCENT_SECRET_KEY
        self.region = "ap-nanjing"
        self.scheme = "https" # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        self.token = None # 使用临时密钥需要传入 Token，默认为空，可不填
        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key)
        self.client = CosS3Client(self.config)



    def create_buc(self,bucketName):
        result = self.client.create_bucket(Bucket="{}-1257752450".format(bucketName))
        print(result)

    def delete_buc(self,bucketName):
        result = self.client.delete_bucket(Bucket="{}-1257752450".format(bucketName))
        print(result)


if __name__ == '__main__':
    print(settings.secret_id)
