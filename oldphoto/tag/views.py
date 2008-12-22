# -*- coding: UTF-8 -*-
from django.views.generic.list_detail import object_list
from oldphoto.tag.models import Tag
from oldphoto.photos.models import Photo
from oldphoto.utils.CommonUtils import get_base_context_map


def index(request, tag_id=None):
    """
    显示指定tag的照片
    """
    tag=None
    context_map=get_base_context_map(request)
    if not tag_id:
        photos=Photo.objects.all().order_by("-modification_date")
    else:
        try:
            tag=Tag.objects.get(pk=tag_id)
        except:
            pass#TODO 转到出错页面
        photos=tag.photo_set.all().filter(show_type='s').\
            order_by("-modification_date")
    photos=photos
    context_map['tag']=tag
    context_map['side_tags']=list_tags()
    return object_list(request,
                       photos,
                       paginate_by=20,
                       template_name='tags/index.html',
                       extra_context=context_map,
                       allow_empty=True)


def list_tags(num=30):
    """
    列出num个Tags，每个tag都带有一个em属性
    来指定显示的大小。
    包含内容越多的tag大小越大。
    1.6  ---1
    1.5  ---1
    1.4  ---2
    1.3  ---2
    1.2  ---2
    1.1  ---2
    1-----14
    0.9----4
    0.8----2
    """
    tags = Tag.objects.all().order_by("-obj_count")[:num]
    if num>len(tags):
        num=len(tags)
    if not num:
        return

    def set_tag_em(i, em):
        if i<0:
            i=0;
        if i>=num:
            i=num-1
        tags[i].em=em
    for i in [0,1*num/30-1]:
        set_tag_em(i, "1.6")
    for i in [2*num/30-1,2*num/30-1]:
        set_tag_em(i, "1.5")
    for i in [3*num/30-1,4*num/30-1]:
        set_tag_em(i, "1.4")
    for i in [5*num/30-1,6*num/30-1]:
        set_tag_em(i, "1.3")
    for i in [7*num/30-1,8*num/30-1]:
        set_tag_em(i, "1.2")
    for i in [9*num/30-1,10*num/30-1]:
        set_tag_em(i, "1.1")
    for i in [11*num/30-1,24*num/30-1]:
        set_tag_em(i, "1")
    for i in [25*num/30-1,28*num/30-1]:
        set_tag_em(i, "0.9")
    for i in [29*num/30-1,30*num/30-1]:
        set_tag_em(i, "0.8")
    tags[0].em="1.6"
    """
    new_tags=[]
    for t in tags:
        new_tags.append(t)
    import random
    random.shuffle(new_tags)
    return new_tags"""
    return tags
