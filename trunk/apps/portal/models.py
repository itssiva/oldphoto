# -*- coding: UTF-8 -*-
from django.db import models
from apps.photos.models import Photo

class RecommendPhoto(models.Model):
    """
    推荐照片
    """
    photo = models.ForeignKey(Photo)
    title = models.CharField(maxlength=100, blank=True)#标题
    descn = models.TextField(blank=True)#描述
    modification_date = models.DateTimeField(auto_now_add = True)
    create_date = models.DateTimeField(auto_now_add = True)

    def get_title(self):
        if not self.title:
            return self.photo.title
        return self.title

    def get_descn(self):
        if not self.descn:
            return self.photo.descn
        return self.descn

    def __str__(self):
        return self.get_title()
    
    def __unicode__(self):
        return self.get_title()

    class Admin:
        pass