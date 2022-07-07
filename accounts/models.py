from __future__ import unicode_literals
from django.db import models


class Users(models.Model) :
    userid = models.CharField(max_length=30, primary_key=True, verbose_name='사용자ID')
    password = models.CharField(max_length=15, verbose_name='사용자PW')
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜', null=True)
    modifier_id = models.CharField(max_length=30, verbose_name='수정자ID', null=True)
    updated_dt = models.DateTimeField(auto_now_add=True, verbose_name='수정날짜', null=True)
    del_yn = models.CharField(max_length=30, verbose_name='탈퇴유무', default='N')

    def __str__(self):
        return self.userid

    class Meta :
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

