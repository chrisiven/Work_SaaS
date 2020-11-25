#coding:utf-8

import django
import os,sys
from proj.utils import tools
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","SaaS_System.settings")
django.setup()
from users import models
from proj.models import Transaction
# models.UserInfo.objects.create(username="iven",email="chrisiven@qq.com",mobile_phone="13838383838",password="123456")
import datetime


Transaction.objects.create(order_id=tools.gen_order_id(),state="已支付",actual_delivery="399",service_start_time=datetime.datetime.now().date(),service_end_time=datetime.datetime.now().date(),
            number=1,price_category_id=2,user_id=1)
Transaction.objects.create(order_id=tools.gen_order_id(),state="已支付",actual_delivery="399",service_start_time=datetime.datetime.now().date(),service_end_time=datetime.datetime.now().date(),
            number=1,price_category_id=3,user_id=2)