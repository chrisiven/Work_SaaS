#coding:utf-8


from django.urls import path

from users.views import account

app_name = "users"
urlpatterns = [
    path('register/', account.RegisterView.as_view(), name="register"), #注册
    path('send_code/', account.sendcode, name="sendcode"),#获取验证码
    path('emaillogin/',account.EmailLoginView.as_view(),name="emaillogin"), #邮箱登录
    path('pswdlogin/',account.PswdLoginView.as_view(),name="pswdlogin"), #密码登录
    path("verify_img/",account.verify_picture,name="verify_picture"),
    path("logout/",account.logout,name="logout")
]
