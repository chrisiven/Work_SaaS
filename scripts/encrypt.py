#coding:utf-8
import hashlib
import uuid
from django.conf import settings

def md5(string):
    hash_obj = hashlib.md5(settings.TENCENT_SECRET_KEY.encode("utf-8"))
    hash_obj.update(string.encode("utf-8"))
    return hash_obj.hexdigest()


def uid(string):
    data = "{}-{}".format(uuid.uuid4(),string)
    return md5(data)
if __name__ == '__main__':
    print(uid(2))