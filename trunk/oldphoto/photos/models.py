# -*- coding: UTF-8 -*-
from django.db import models
from oldphoto.tag.models import Tag
from django.contrib.auth.models import User
from django.conf import settings
from oldphoto.utils.CommonUtils import txt2set


class Photo(models.Model):
    """
    图片
    """
    title = models.CharField(max_length=100)
    descn = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    txt_tags = models.TextField(blank=True)
    photo_url = models.CharField(max_length=255, blank=True)

    user = models.ForeignKey(User)

    modification_date = models.DateTimeField(auto_now_add = True)
    create_date = models.DateTimeField(auto_now_add = True)

    view_count = models.IntegerField(default=0)
    rep_count = models.IntegerField(default=0)

    show_type = models.CharField('显示',\
        choices=(('s', '显示'), ('h', '隐藏')),
        max_length=1, default='s')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def is_show(self):
        if self.show_type=='s':
            return True
        return False

    def get_txt_tags(self):
        ts=[t.name for t in self.get_sorted_tags()]
        return ' '.join(ts)

    def get_sorted_tags(self):
        #根据tag的记录数从大到小排序
        def tag_cmp(t1, t2):
            return -cmp(t1.obj_count, t2.obj_count)
        tags=self.tags.all()
        n_tags=[]
        n_tags.extend(tags)
        n_tags.sort(tag_cmp)
        return n_tags

    def get_photo_url(self):
        if not self.photo_url:
            return ''
        return settings.PHOTO_URL_PREFIX + \
            self.photo_url

    def thumb_big_photo_url(self):
        s=self.get_photo_url()
        pos = s.rfind('.')
        return s[:pos]+'_thumb_big'+s[pos:]
        #return self.get_photo_url().replace('.','_thumb_big.')

    def thumb_small_photo_url(self):
        s=self.get_photo_url()
        pos = s.rfind('.')
        return s[:pos]+'_thumb_small'+s[pos:]
        #return self.get_photo_url().replace('.','_thumb_small.')

    def photo_name(self):
        if not self.photo_url:
            return ''
        return self.photo_url

    def thumb_big_photo_name(self):
        return self.photo_name().replace('.','_thumb_big.')

    def thumb_small_photo_name(self):
        return self.photo_name().replace('.','_thumb_small.')

    def txt_tag_set(self):
        return txt2set(self.txt_tags)

    def add_txt_tags(self,txt_tag_set):
        """
        添加tags
        txt_tag_set tag列表，为tag的name
        """
        for txt_tag in txt_tag_set:
            try:
                tag=Tag(name=txt_tag)
                try:
                    tag=Tag.objects.get(name=txt_tag)
                except:
                    pass
                #修改Tag的对象个数
                if self.show_type=='s':
                    tag.obj_count=tag.obj_count+1
                tag.save()
                self.tags.add(tag)
            except:
                pass
        self.user_add_txt_tags(txt_tag_set)

    def user_add_txt_tags(self,txt_tag_set):
        """
        添加tags
        txt_tag_set tag列表，为tag的name
        """
        for txt_tag in txt_tag_set:
            try:
                tag=UserTag(name=txt_tag,user=self.user)
                try:
                    tag=UserTag.objects.get(name=txt_tag,user=self.user)
                except:
                    tag.save()
                #修改Tag的对象个数
                if self.show_type=='s':
                    tag.obj_count=tag.obj_count+1
                tag.photos.add(self)
                tag.save()
            except:
                pass
        pass

    def remove_txt_tags(self,txt_tag_set):
        """
        删除tags
        txt_tag_set tag列表，为tag的name
        """
        for txt_tag in txt_tag_set:
            try:
                tag=Tag.objects.get(name=txt_tag);
                self.tags.remove(tag)
                if self.show_type=='s':
                    tag.obj_count=tag.obj_count-1
                if len(tag.photo_set.all()):
                    tag.save()
                else:
                    tag.delete()
            except:
                pass
        self.user_remove_txt_tags(txt_tag_set)

    def user_remove_txt_tags(self,txt_tag_set):
        """
        删除tags
        txt_tag_set tag列表，为tag的name
        """
        for txt_tag in txt_tag_set:
            try:
                tag=UserTag.objects.get(name=txt_tag,user=self.user)
                tag.photos.remove(self)
                if self.show_type=='s':
                    tag.obj_count=tag.obj_count-1
                if len(tag.photos.all()):
                    tag.save()
                else:
                    tag.delete()
            except:
                pass
        pass

    class Admin:
        pass


class PhotoComment(models.Model):
    """
    图片评论
    """
    author = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    comment = models.TextField()
    create_date = models.DateTimeField(auto_now_add = True)
    modification_date = models.DateTimeField(auto_now_add = True)

    show_type = models.CharField('显示',\
        choices=(('s', '显示'), ('h', '隐藏')),
        max_length=1, default='s')

    def is_show(self):
        if self.show_type=='s':
            return True
        return False

    def get_short_comment(self):
        from oldphoto.utils.html2text import html2text
        comment=html2text(self.comment)
        if len(comment)>40:
            return comment[0:38]+'...'
        return comment

    def __str__(self):
        return self.photo.title

    def __unicode__(self):
        return self.photo.title

    class Admin:
        pass


class UserTag(models.Model):
    """
    用户自定义Tag
    受交叉引用的影响，无法放在tag的models下
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    descn = models.TextField(blank=True)
    photos = models.ManyToManyField(Photo)
    obj_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username + '__' + self.name

    class Admin:
        pass
