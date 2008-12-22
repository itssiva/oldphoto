# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.list_detail import object_list
from apps.photos.models import Photo, PhotoComment
from apps.portal.models import RecommendPhoto
from apps.utils.CommonUtils import get_count, get_base_context_map,\
    is_superuser
    
def index(request):
    context_map=get_base_context_map(request)
    hot_photos=Photo.objects.all().filter(show_type='s').\
        order_by("-view_count")[:8]
    context_map['hot_photos']=hot_photos
    new_photos=Photo.objects.all().filter(show_type='s').\
        order_by("-create_date")[:8]
    context_map['new_photos']=new_photos
    recommend_photos=RecommendPhoto.objects.all().\
        order_by("-create_date")[:4]
    context_map['recommend_photos']=recommend_photos
    from apps.tag.views import list_tags
    context_map['side_tags']=list_tags()
    return render_to_response('index.html',
            context_map)


def base(request):
    return render_to_response('base.html',
        context_instance=RequestContext(request))


def base_3col(request):
    return render_to_response('base_3col.html',
        context_instance=RequestContext(request))


def base_2col(request):
    return render_to_response('base_2col.html',
        context_instance=RequestContext(request))


def sec(request):
    return render_to_response('sec.html',
        context_instance=RequestContext(request))


def test(request):
    return render_to_response('test.html',
        context_instance=RequestContext(request))


def tags(request):
    return render_to_response('tags.html',
        context_instance=RequestContext(request))


def allcomments(request):
    context_map=get_base_context_map(request)
    comments = PhotoComment.objects.all().filter(show_type='s').\
        order_by("-create_date")
    #context_map['comments']=comments
    return object_list(request,
                       comments,
                       paginate_by=25,
                       template_name='allcomments.html',
                       extra_context=context_map,
                       allow_empty=True)


def allrecommends(request):
    context_map=get_base_context_map(request)
    recommend_photos=RecommendPhoto.objects.all().\
        order_by("-create_date")
    #context_map['recommend_photos']=recommend_photos
    return object_list(request,
                       recommend_photos,
                       paginate_by=25,
                       template_name='allrecommend.html',
                       extra_context=context_map,
                       allow_empty=True)


def allhotphotos(request):
    context_map=get_base_context_map(request)
    hot_photos=Photo.objects.all().filter(show_type='s').\
        order_by("-view_count")
    #context_map['hot_photos']=hot_photos
    return object_list(request,
                       hot_photos,
                       paginate_by=25,
                       template_name='allhotphotos.html',
                       extra_context=context_map,
                       allow_empty=True)


def allnewphotos(request):
    context_map=get_base_context_map(request)
    new_photos=Photo.objects.all().filter(show_type='s').\
        order_by("-create_date")
    #context_map['new_photos']=new_photos
    return object_list(request,
                       new_photos,
                       paginate_by=25,
                       template_name='allnewphotos.html',
                       extra_context=context_map,
                       allow_empty=True)


def search(request):
    return render_to_response('search.html',
        context_instance=RequestContext(request))