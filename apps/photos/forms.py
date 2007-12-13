# -*- coding: UTF-8 -*-
import settings_apache as settings
import random
import os
from django import newforms as forms
from apps.photos.models import Photo, PhotoComment
from apps.utils.CommonUtils import txt2set
from django.utils.translation import gettext as _
from apps.utils.ImageUtils import checkImage,make_thumb


def upload_photo(photo, ext):
    """
    上传图片，返回图片名称
    图片分布在100个文件夹内，
    防止单个文件夹内文件数量过多
    ext=filename.split('.')[-1]
    """
    sub_folder_name=str(random.randint(0,100))
    path=settings.PHOTO_ROOT + sub_folder_name + '/'
    #如果文件夹不存在，创建文件夹
    if not os.path.exists(path):
        os.mkdir(path)
    import time
    filename=str(time.time())+str(random.randrange(0,99999,1))+'.'+ext
    ret_filename=sub_folder_name + '/' + filename
    filename=path+filename
    thumb_big_filename=filename.replace('.','_thumb_big.')
    thumb_small_filename=filename.replace('.','_thumb_small.')
    #直接保存
    imgfile = open(filename, 'wb')
    imgfile.write(photo)
    imgfile.close()
    #缩略图
    make_thumb(img=filename, filename=thumb_big_filename,\
        size=135, square=False, quality=75)
    make_thumb(img=filename, filename=thumb_small_filename,\
        size=48, square=False, quality=75)
    return ret_filename

class PhotoForm(forms.Form):
    title = forms.CharField(max_length=40,\
        widget=forms.widgets.TextInput(attrs={'style':'width: 20em;'}),\
            label='标题')
    descn = forms.CharField(\
        widget=forms.widgets.Textarea(attrs={'rows': 5, 'cols': 60}),\
            label='描述', required=False)
    txt_tags = forms.CharField(\
        widget=forms.widgets.Textarea(attrs={'rows': 2, 'cols': 60}),\
        label='Tags')
    photo = forms.CharField(\
        widget=forms.widgets.FileInput(attrs={'size':42}),\
            label='图片', required=False)

    def __init__(self, data=None, files=None, user=None,\
        instance=None, *args, **kwargs):
        super(PhotoForm, self).__init__(data, *args, **kwargs)
        self.user=user
        self.files=files
        self.instance=instance

    def clean_photo(self):
        #TODO 校验
        if self.instance:
            return None
        try:
            value=self.files['photo']
        except:
            raise forms.ValidationError(_('上传图片不能为空'))
        checkImage(value, settings.MAX_PHOTO_SIZE)
        return value

    def clean_txt_tags(self):
        self.d_txt_tags_set=txt2set(self.cleaned_data['txt_tags'])
        if len(self.d_txt_tags_set)==0:
            raise forms.ValidationError(_('tags不能为空'))
        return ' '.join(self.d_txt_tags_set)

    def save(self):
        if self.instance:#update
            photo=self.instance
            old_txt_tags_set=txt2set(photo.get_txt_tags())
            to_remove_tags_set=old_txt_tags_set-self.d_txt_tags_set
            to_add_tags_set=self.d_txt_tags_set-old_txt_tags_set
            photo.add_txt_tags(to_add_tags_set)
            photo.remove_txt_tags(to_remove_tags_set)
            from datetime import datetime
            photo.modification_date=datetime.now()
        else:
            photo = Photo()
            #上传图片
            photo.user=self.user
            filename=upload_photo(self.cleaned_data['photo']['content'],
                self.cleaned_data['photo']['filename'].split('.')[-1])
            photo.photo_url=filename
        photo.title=self.cleaned_data['title']
        from apps.utils.textconvert import plaintext2html
        photo.descn=plaintext2html(self.cleaned_data['descn'])
        #处理tags，删除删除的tag，添加新增加的tags
        photo.txt_tags=self.cleaned_data['txt_tags']
        photo.save()
        if not self.instance:#update
            photo.add_txt_tags(self.d_txt_tags_set)
            photo.save()
        return photo


class PhotoCommentForm(forms.Form):
    comment = forms.CharField(\
        widget=forms.widgets.Textarea(\
            attrs={'rows': 6, 'cols': 65}), label='评论内容')

    def __init__(self, data=None, photo=None, author=None, *args, **kwargs):
        super(PhotoCommentForm, self).__init__(data, *args, **kwargs)
        self.author=author
        self.photo=photo

    def save(self):
        from apps.utils.textconvert import plaintext2html
        comment=plaintext2html(self.cleaned_data['comment'])
        photo_comment = PhotoComment(author=self.author,\
            photo=self.photo,comment=comment)
        self.photo.rep_count=self.photo.rep_count+1
        self.photo.save()
        photo_comment.save()
