#coding:utf-8
import time
from SaaS_System.settings import MAX_VERIFYCODE_COUNT
import datetime as dt
from django_redis import get_redis_connection
conn = get_redis_connection("timemanager")

def oneHourMaxClickNumber(user:str): #一个小时内最大的点击数
    now_hour = dt.datetime.now().hour #系统当前时间

    user_now_time = dt.datetime.now() #用户当前的时间
    start_time = dt.datetime.strptime(str(dt.datetime.now().date()) + '{}:00'.format(now_hour), '%Y-%m-%d%H:%M') #在一个小时内的开头时间
    over_time = dt.datetime.strptime(str(dt.datetime.now().date()) + '{}:59'.format(now_hour), '%Y-%m-%d%H:%M')#在这一段时间内的结尾时间
    if user_now_time > start_time and user_now_time < over_time:
        try:
            result = int(conn.get(user+"time").decode("utf-8"))

            if isinstance(result, int):
                if result >= MAX_VERIFYCODE_COUNT:
                # 如果有请求次数了,并且类型一定是number的,那么直接将其+1
                    return False
                elif result < MAX_VERIFYCODE_COUNT:
                    number = result + 1
                    conn.set(user + "time", number, ex=3600)  # 一个小时内
                    return True
        except Exception as e:
            conn.set(user + "time", 1, ex=3600)  # 没有则创建,初始化为1
            return True


if __name__ == '__main__':

    print(oneHourMaxClickNumber("chrisiven_"))


