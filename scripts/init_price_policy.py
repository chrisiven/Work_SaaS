#coding:utf-8

from scripts import base
# please make you table and module
base.DjangoSetUp()

from proj import models
print("django Setuping...")


da = [
    models.PricePolicy(
        category=1,
        title="个人免费版",
        price=0,
        project_num=3,
        project_member=2,
        project_space=2,
        pro_file_size=5
    )
    ,
    models.PricePolicy(
        category=2,
        title="收费版",
        price=0,
        project_num=3,
        project_member=2,
        project_space=2,
        pro_file_size=5
    ),
models.PricePolicy(
        category=3,
        title="其他版",
        price=0,
        project_num=3,
        project_member=2,
        project_space=2,
        pro_file_size=5
    )
]

models.PricePolicy.objects.bulk_create(da)






