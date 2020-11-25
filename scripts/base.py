#coding:utf-8


import django
import os,sys

def DjangoSetUp():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","SaaS_System.settings")
    django.setup()
