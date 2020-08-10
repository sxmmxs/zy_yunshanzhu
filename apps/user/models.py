from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    """自定义用户模型类"""
    username = models.CharField(max_length=11, verbose_name='姓名')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    company = models.CharField(max_length=50, default=None, null=True, verbose_name='公司名称')
    consulting = models.CharField(max_length=5000, default=None, null=True, verbose_name='咨询内容')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'

