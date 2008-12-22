# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    """
    发信箱/草稿箱
    """
    rec_user = models.ForeignKey(User, related_name="rec_msgs")
    send_user = models.ForeignKey(User, related_name="send_msgs")
    type = models.CharField('类型',\
        choices=(('d', '草稿'), ('s', '已发送'), ('r', '收信箱')),
        max_length=1, default='d')
    read = models.CharField('是否已读',\
        choices=(('u', '未读'), ('r', '已读')),
        max_length=1, default='u')
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add = True)
    modification_date = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.title

    def has_read(self):
        if self.read=='r':
            return True
        return False
    
    class Admin:
        pass
