# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from apps.photos.models import Photo, PhotoComment, UserTag
from apps.userpanel.models import CollectionPhoto,Friend
from apps.utils.CommonUtils import get_base_context_map,is_superuser


def init_context(request, user_id=0, context_map={}):
    context_map=get_base_context_map(request)
    user = request.user
    context_map['user'] = user
    view_user = user
    context_map['r_c'] = PhotoComment.objects.extra(
        params=[user.id],
        tables=['photos_photo'],
        where=['photo_id=photos_photo.id and photos_photo.user_id=%s'])[:5]
    if user_id:
        view_user = User.objects.get(pk=user_id)
    context_map['view_user'] = view_user
    if user.id==view_user.id:
        context_map['is_self']=True
    else:
        try:
            friend=Friend.objects.get(user=user,friend=view_user)
            context_map['friend']=friend
        except:
            pass
    return context_map, user, view_user


def index(request, user_id=0):
    context_map,user,view_user=\
        init_context(request, user_id=user_id, context_map={})
    self_photos = view_user.photo_set.all().\
        filter(show_type='s').order_by("-modification_date")[:8]
    context_map['self_photos'] = self_photos
    collection_photos = CollectionPhoto.objects.all().\
        filter(user=view_user).\
        extra(
            params=['s'],
            tables=['photos_photo'],
            where=['photo_id=photos_photo.id and photos_photo.show_type=%s']).\
        order_by("-create_date")[:8]
    context_map['collection_photos'] = collection_photos
    return render_to_response('space/index.html', context_map)


def collections(request, user_id=0):
    context_map,user,view_user=\
        init_context(request, user_id=user_id, context_map={})
    #TODO 增加collection类，用于管理用户的收藏
    collection_photos = CollectionPhoto.objects.all().\
        filter(user=view_user).\
        extra(
            params=['s'],
            tables=['photos_photo'],
            where=['photo_id=photos_photo.id and photos_photo.show_type=%s']).\
        order_by("-create_date")
    #context_map['collection_photos'] = collection_photos
    return object_list(request,
                       collection_photos,
                       paginate_by=20,
                       template_name='space/collections.html',
                       extra_context=context_map,
                       allow_empty=True)


def allcomments(request, user_id=0):
    """
    列出该用户的所有评论（翻页）
    """
    context_map,user,view_user=\
        init_context(request, user_id=user_id, context_map={})
    comments = view_user.photocomment_set.all().filter(show_type='s').\
        order_by("-create_date")[:15]
    #context_map['comments']=comments
    return object_list(request,
                       comments,
                       paginate_by=20,
                       template_name='space/allcomments.html',
                       extra_context=context_map,
                       allow_empty=True)


def photos(request, user_id=0):
    context_map,user,view_user=\
        init_context(request, user_id=user_id, context_map={})
    self_photos = view_user.photo_set.all()
    if not is_superuser(user):
        self_photos = self_photos.filter(show_type='s')
    self_photos = self_photos.order_by("-create_date")
    #context_map['self_photos']=self_photos
    return object_list(request,
                       self_photos,
                       paginate_by=20,
                       template_name='space/photos.html',
                       extra_context=context_map,
                       allow_empty=True)


def tags(request, user_id=0, tag_id=0):
    context_map,user,view_user=\
        init_context(request, user_id=user_id, context_map={})
    usertags=view_user.usertag_set.all()[:100]
    context_map['usertags']=usertags
    if tag_id:
        usertag=UserTag.objects.get(pk=tag_id)
        context_map['tag']=usertag
        photos=usertag.photos.all()
    else:
        photos = view_user.photo_set.all()
        if not is_superuser(user):
            photos = photos.filter(show_type='s')
        photos = photos.order_by("-create_date")        
    #context_map['self_photos']=self_photos
    return object_list(request,
                       photos,
                       paginate_by=20,
                       template_name='space/tags.html',
                       extra_context=context_map,
                       allow_empty=True)


def friends(request, user_id=0):
    context_map,user,view_user=\
        init_context(request, user_id=user_id, context_map={})
    users = view_user.users.all()#.filter(user=view_user)
    #context_map['users']=users
    return object_list(request,
                       users,
                       paginate_by=100,
                       template_name='space/friends.html',
                       extra_context=context_map,
                       allow_empty=True)


def followers(request, user_id=0):
    context_map,user,view_user=\
        init_context(request, user_id=user_id, context_map={})
    users = view_user.friends.all()#.filter(friend=view_user)
    #context_map['users']=users
    return object_list(request,
                       users,
                       paginate_by=100,
                       template_name='space/followers.html',
                       extra_context=context_map,
                       allow_empty=True)


@login_required
def add_friend(request, user_id):
    #不能重复建立关系
    user = request.user
    friend_user=User.objects.get(pk=user_id)
    try:
        friend=Friend.objects.get(user=user,friend=friend_user)
        return HttpResponseRedirect('/space/friends/')
    except Friend.DoesNotExist:
        pass
    friend = Friend(user=user, friend=friend_user)
    friend.save()
    return HttpResponseRedirect('/space/friends/')


@login_required
def drop_friend(request, id):
    user = request.user
    friend=Friend.objects.get(pk=id)
    friend.delete()
    return HttpResponseRedirect('/space/friends/')