#!/usr/bin/env python
#coding=utf-8
import Image
import os
from django.utils.translation import gettext as _
from django import forms


def checkImage(value, max_size=0):
    """
    检查上传的图片是否合法
    max_size 最大大小，单位K。0表示无限制
    """
    if value.name.split('.')[-1].lower() not in ['jpeg', 'gif', 'png', 'jpg']:
        raise forms.ValidationError(_('只支持JPEG, PNG, GIF'))
    try:
        img = Image.open(value)
        x, y = img.size
    except:
        raise forms.ValidationError(_('无效的图形文件。'))
    if max_size!=0 and value.size>max_size*1024:
        raise forms.ValidationError(_('图片大小不得大于%sK') % max_size)


def make_thumb(img, filename, size=48, square=True, quality=100):
    """
    缩略图生成程序 by Neil Chen
    sizes 参数传递要生成的尺寸，可以生成多种尺寸
    """
    try:
        im = Image.open(img)
    except IOError:
        return
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    """
    if width == height:
        region = im
    """
    if square:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)
        region = im.crop(box)
    else:
        region = im
        if width>=height and width>size:
            new_width=size
            new_height=height*size/width
        elif height>width and height>size:
            new_width=width*size/height
            new_height=size
        else:
            new_width=width
            new_height=height
            """
            if width > height:
                new_width=size
                new_height=height*size/width
            else:
                new_width=width*size/height
                new_height=size
            """
    #for size in sizes:
    if square:
        thumb = region.resize((size,size), Image.ANTIALIAS)
    else:
        thumb = region.resize((new_width,new_height), Image.ANTIALIAS)
    thumb.save(filename, quality=quality) # 默认 JPEG 保存质量是 75, 不太清楚。可选值(0~100)


def make_thumb_x(path, size=75, square=True):
    """
    缩略图生成程序 by Neil Chen
    sizes 参数传递要生成的尺寸，可以生成多种尺寸
    """
    base, ext = os.path.splitext(path)
    try:
        im = Image.open(path)
    except IOError:
        return
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    if width == height:
        region = im
    elif square:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)
        region = im.crop(box)
    else:
        region = im
        if width > height:
            new_width=size
            new_height=height*size/width
        else:
            new_width=width*size/height
            new_height=size
    #for size in sizes:
    if square:
        filename = base + "_" + "%sx%s" % (str(size), str(size)) + ".jpg"
        thumb = region.resize((size,size), Image.ANTIALIAS)
    else:
        filename = base + "_" + "%sx%s" % (str(new_width), str(new_height)) + ".jpg"
        thumb = region.resize((new_width,new_height), Image.ANTIALIAS)
    thumb.save(filename, quality=100) # 默认 JPEG 保存质量是 75, 不太清楚。可选值(0~100)

if __name__ == '__main__':
    make_thumb(r"C:/f5b1a8ff-7f4f-4746-a07f-480703819751.jpg", square=False)
    make_thumb(r"C:/f5b1a8ff-7f4f-4746-a07f-480703819751.jpg", square=True)
