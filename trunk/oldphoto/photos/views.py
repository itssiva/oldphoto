# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from oldphoto.photos.forms import PhotoForm, PhotoCommentForm
from oldphoto.photos.models import Photo, PhotoComment
from oldphoto.utils.decorators import superuser_required
from oldphoto.utils.CommonUtils import get_count, get_base_context_map,\
    is_superuser
from oldphoto.portal.models import RecommendPhoto
from oldphoto.userpanel.models import CollectionPhoto
from django.conf import settings

@login_required
def upload(request):
    """
    上传图片
    """
    user = request.user
    form = PhotoForm()
    context_map=get_base_context_map(request)
    if request.POST:
        form = PhotoForm(request.POST, request.FILES, user)
        if form.is_valid():
            photo=form.save()
            if photo==None:
                context_map['form']=form
                return render_to_response('photos/upload.html',
                    context_map)
            return HttpResponseRedirect('/photos/check/%s/' % photo.id)
    context_map['form']=form
    return render_to_response('photos/upload.html',
        context_map)


@login_required
def edit(request, id):
    photo=get_object_or_404(Photo, pk=id)
    user = request.user
    if photo.user!=user:
        return HttpResponseRedirect('/photos/check/%s/' % photo.id)
    context_map=get_base_context_map(request)
    data=photo.__dict__
    from oldphoto.utils.html2text import html2text
    data['descn']=html2text(photo.descn)
    data['txt_tags']=photo.get_txt_tags()
    form = PhotoForm(data=data)
    if request.POST:
        form = PhotoForm(request.POST, request.FILES, user, photo)
        if form.is_valid():
            photo=form.save()
            if photo==None:
                context_map['form']=form
                return render_to_response('photos/edit.html',
                    context_map)
            return HttpResponseRedirect('/photos/check/%s/' % photo.id)
    context_map['form']=form
    context_map['photo']=photo
    return render_to_response('photos/edit.html',
        context_map)


def view_photo(request, id):
    """
    查看图片
    """
    photo=get_object_or_404(Photo, pk=id)
    user = request.user
    if photo.show_type=='h' and not is_superuser(user):
        raise Http404
    context_map=get_base_context_map(request)
    #TODO 评论翻页
    comments=photo.photocomment_set.all()
    if not is_superuser(user):
        comments=comments.filter(show_type='s')
    user_s_other_photo = photo.user.photo_set.all()
    if not is_superuser(user):
        user_s_other_photo = user_s_other_photo.filter(show_type='s')
    user_s_other_photo = user_s_other_photo.order_by("-create_date")[0:8]
    form = PhotoCommentForm()
    if request.method == 'POST':
        """
        添加评论
        """
        #TODO 登录判断
        if user.is_anonymous():
            return HttpResponseRedirect('/photos/%s/#beginComment' % id)
        form = PhotoCommentForm(request.POST,photo=photo,author=user)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/photos/%s/#beginComment' % id)
    else:
        photo.view_count=photo.view_count+1
        photo.save()
    context_map['form']=form
    context_map['photo']=photo
    context_map['user_s_other_photo']=user_s_other_photo
    context_map['comments']=comments
    context_map['user']=user
    #TODO 查看图片是否已经收藏过了
    context_map['has_collection']=get_count("""
    select count(*) from
    userpanel_collectionphoto uc
    where uc.photo_id=%s and uc.user_id=%s
    """, [photo.id, user.id])
    if user==photo.user or is_superuser(user):
        context_map['can_edit']=True
    return render_to_response('photos/view_photo.html', context_map)


def check(request, id):
    """
    确认图片（添加/编辑后）
    """
    photo=get_object_or_404(Photo, pk=id)
    user = request.user
    if photo.show_type=='h' and not is_superuser(user):
        raise Http404
    context_map=get_base_context_map(request)
    context_map['photo']=photo
    return render_to_response('photos/check.html',
        context_map)


@superuser_required
def hidden(request, id):
    photo=get_object_or_404(Photo, pk=id)
    if photo.show_type=='s':
        photo.show_type='h'
        #TODO清理tag的记录数
        for t in photo.tags.all():
            t.obj_count=t.obj_count-1
            t.save()
        for t in photo.usertag_set.all():
            t.obj_count=t.obj_count-1
            t.save()
        photo.save()
    return HttpResponseRedirect('/space/tags/%s/' % photo.user.id)


@superuser_required
def show(request, id):
    photo=get_object_or_404(Photo, pk=id)
    if photo.show_type=='h':
        photo.show_type='s'
        for t in photo.tags.all():
            t.obj_count=t.obj_count+1
            t.save()
        for t in photo.usertag_set.all():
            t.obj_count=t.obj_count+1
            t.save()
        photo.save()
    return HttpResponseRedirect('/photos/%s/' % id)


@login_required
def delete(request, id):
    photo=get_object_or_404(Photo, pk=id)
    u=request.user
    if (photo.user!=u) and (not is_superuser(u)):
        return HttpResponseRedirect('/photos/check/%s/' % photo.id)    
    user_id=photo.user.id
    try:
        if photo.show_type=='s':
            for t in photo.tags.all():
                t.obj_count=t.obj_count-1
                if len(t.photo_set.all())>1:#=1为当前图片
                    t.save()
                else:
                    t.delete()
            for t in photo.usertag_set.all():
                t.obj_count=t.obj_count-1
                if len(t.photos.all())>1:
                    t.save()
                else:
                    t.delete()
        import os
        os.remove(settings.PHOTO_ROOT+photo.photo_name())
        os.remove(settings.PHOTO_ROOT+photo.thumb_big_photo_name())
        os.remove(settings.PHOTO_ROOT+photo.thumb_small_photo_name())
    except  Exception, e:
        pass
    photo.delete()
    return HttpResponseRedirect('/space/tags/%s/' % user_id)


@superuser_required
def recommend(request, id):
    photo=get_object_or_404(Photo, pk=id)
    rc=RecommendPhoto(photo=photo)
    rc.save()
    return HttpResponseRedirect('/allrecommends/')


@login_required
def collection(request, id):
    u = request.user
    photo=get_object_or_404(Photo, pk=id)
    c=CollectionPhoto(photo=photo, user=u)
    c.save()
    return HttpResponseRedirect('/space/collections/')


@login_required
def dis_collection(request, id):
    try:
        u = request.user
        photo=get_object_or_404(Photo, pk=id)
        c=CollectionPhoto.objects.get(photo=photo, user=u)
        c.delete()        
    except:
        pass
    return HttpResponseRedirect('/space/collections/')


@superuser_required
def comment_hidden(request, id):
    c=get_object_or_404(PhotoComment, pk=id)
    if c.show_type=='s':
        c.show_type='h'
        c.save()
        p=c.photo
        p.rep_count=p.rep_count-1
        p.save()        
    return HttpResponseRedirect('/photos/%s/#newComment' % p.id)


@superuser_required
def comment_show(request, id):
    c=get_object_or_404(PhotoComment, pk=id)
    if c.show_type=='h':
        c.show_type='s'
        c.save()
        p=c.photo
        p.rep_count=p.rep_count+1
        p.save()        
    return HttpResponseRedirect('/photos/%s/#newComment' % p.id)


@superuser_required
def comment_delete(request, id):
    c=get_object_or_404(PhotoComment, pk=id)
    p=c.photo
    if c.show_type=='s':
        p.rep_count=p.rep_count-1
    p.save()
    c.delete()
    return HttpResponseRedirect('/photos/%s/#newComment' % p.id)
