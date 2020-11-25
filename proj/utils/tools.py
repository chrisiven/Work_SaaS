#coding:utf-8
import random

def gen_order_id():
    #生成订单id
    base_num = 9
    order_id =  str(base_num) + str(random.randint(10000000,99999999))

    return order_id
print(gen_order_id())
# print(gen_order_id())
# print(gen_order_id())
# import datetime as dt
# print(dt.datetime.now().date())
# # print(dt.datetime.date())