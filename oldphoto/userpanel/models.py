# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from oldphoto.photos.models import Photo
from django.contrib import admin

#用户附加信息
#信箱
#收藏
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    avatar = models.CharField(max_length=255, blank=True)
    gender = models.CharField('性别',\
        choices=(('', '保密'), ('M', '男'), ('F', '女')),
        max_length=1, blank=True)
    blog = models.URLField(blank=True)
    intro = models.TextField(blank=True)
    photo_count=models.IntegerField(default=0)
    rep_count=models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add = True)

    class Admin:
        pass

    def __str__(self):
        return self.user.username
    
    def __unicode__(self):
        return self.user.username

    def get_avatar(self):
        a = settings.DEFAULT_AVATAR_IMAGE
        if self.avatar:
            a = str(self.id)+'.jpg';
        return settings.AVATAR_URL_PREFIX + a

admin.site.register(UserProfile)

class CollectionPhoto(models.Model):
    """
    用户收藏
    """
    user=models.ForeignKey(User)
    photo=models.ForeignKey(Photo)
    modification_date = models.DateTimeField(auto_now_add = True)
    create_date = models.DateTimeField(auto_now_add = True)


class Friend(models.Model):
    """
    用户收藏
    """
    user=models.ForeignKey(User, related_name="users")#加为用户的人
    friend=models.ForeignKey(User, related_name="friends")#好友
    create_date = models.DateTimeField(auto_now_add = True)
