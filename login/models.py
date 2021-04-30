# login/models.py

from django.db import models
from django.db.models import F


class User(models.Model):
    '''用户表'''

    gender = (
        ('secret', '保密'),
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='secret')
    rating = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            F('rating').desc(nulls_last=True),
            F('c_time').desc(nulls_last=True)
        ]
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Question(models.Model):
    '''问题表'''
    id = models.IntegerField(unique=True, primary_key=True)
    content = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = [F('c_time').desc(nulls_last=True)]
        verbose_name = '问题'
        verbose_name_plural = '问题'


class Answer(models.Model):
    # 回答表

    id = models.IntegerField(unique=True, primary_key=True)
    content = models.TextField(max_length=1024)
    query = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = [F('c_time').desc(nulls_last=True)]
        verbose_name = '回答'
        verbose_name_plural = '回答'
