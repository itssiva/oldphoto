# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from apps.msgbox.forms import ComposeMessageForm
from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.msgbox.models import Message
from apps.utils.CommonUtils import get_base_context_map


def get_friends(user):
    friends=user.friends.all()
    return [[f.user.id, f.user.username] for f in friends]


@login_required
def compose_message(request, to_user_id=None):
    user = request.user
    context_map=get_base_context_map(request)
    friends=None
    if to_user_id:
        to_user=User.objects.get(pk=to_user_id)
        context_map['to_user']=to_user
        friends=(to_user,)
    context_map['user']=user
    if not friends:
        friends=get_friends(user)
    form=ComposeMessageForm(friends=friends)
    if request.POST:
        form = ComposeMessageForm(request.POST,get_friends(user),user)
        if form.is_valid():
            if request.POST['action']=='save':
                form.save_draft()
                return HttpResponseRedirect('/msgbox/draftbox/')
            if request.POST['action']=='send':
                form.send()
                return HttpResponseRedirect('/msgbox/outbox/')
    context_map['form']=form
    return render_to_response('msgbox/compose_message.html',
        context_map)


def remove_msgs(ids, user):
    for id in ids:
        try:
            msg=Message.objects.get(pk=id)
            if msg.rec_user==user or msg.send_user==user:
                msg.delete()
        except:
            pass
    pass


@login_required
def inbox(request):
    user = request.user
    context_map=get_base_context_map(request)    
    rec_msgs=user.rec_msgs.all().filter(type='r').\
        order_by("-modification_date")
    if request.POST:
        ids=request.POST.getlist('ids')
        remove_msgs(ids, user)    
    return object_list(request,
                       rec_msgs,
                       paginate_by=99999,
                       template_name='msgbox/inbox.html',
                       extra_context=context_map,
                       allow_empty=True)


@login_required
def outbox(request):
    user = request.user
    context_map=get_base_context_map(request)    
    send_msgs=user.send_msgs.all().filter(type='s').\
        order_by("-modification_date")
    if request.POST:
        ids=request.POST.getlist('ids')
        remove_msgs(ids, user)
    return object_list(request,
                       send_msgs,
                       paginate_by=99999,
                       template_name='msgbox/outbox.html',
                       extra_context=context_map,
                       allow_empty=True)


@login_required
def draftbox(request):
    user = request.user
    context_map=get_base_context_map(request)    
    send_msgs=user.send_msgs.all().filter(type='d').\
        order_by("-modification_date")
    return object_list(request,
                       send_msgs,
                       paginate_by=99999,
                       template_name='msgbox/draftbox.html',
                       extra_context=context_map,
                       allow_empty=True)

@login_required
def view_message(request, msg_id):
    """
    查看消息内容，需要判断消息是否为本人所有
    """
    context_map={}
    user = request.user
    context_map['user']=user
    msg=get_object_or_404(Message, pk=msg_id)
    context_map['msg']=msg
    if msg.type=='r':
        context_map['r']=True
    if msg.type=='s':
        context_map['s']=True
    if msg.type=='d':
        context_map['d']=True
    if msg.rec_user!=user and msg.send_user!=user:
        return HttpResponseRedirect('/msgbox/inbox/')
    if msg.rec_user==user:
        msg.read='r'
        msg.save()
    return render_to_response('msgbox/view_message.html',
        context_map)


@login_required
def delete_message(request, msg_id):
    """
    查看消息内容，需要判断消息是否为本人所有
    """
    msg=get_object_or_404(Message, pk=msg_id)
    user = request.user
    if msg.type=='r':
        ret_path='/msgbox/inbox/'
    if msg.type=='s':
        ret_path='/msgbox/outbox/'
    if msg.type=='d':
        ret_path='/msgbox/draftbox/'
    #TODO 根据消息类型决定返回的路径
    if msg.rec_user!=user and msg.send_user!=user:
        return HttpResponseRedirect(ret_path)
    msg.delete()
    return HttpResponseRedirect(ret_path)


def get_reply_message(msg):
    s=u'\r\n\r\n-----------在%s，%s写道：-----------\r\n' %\
        (msg.modification_date, msg.send_user.username)
    return s+msg.content


@login_required
def reply_message(request, msg_id):
    user = request.user
    context_map=get_base_context_map(request)    
    msg=get_object_or_404(Message, pk=msg_id)
    if msg.rec_user!=user and msg.send_user!=user:
        return HttpResponseRedirect('/msgbox/inbox/')    
    context_map['to_user']=msg.send_user
    context_map['title']='RE:'+msg.title
    #friends=get_friends(user)
    form=ComposeMessageForm(\
        {'title':'RE:'+msg.title, 'rec_user': msg.send_user.id,\
        'content':get_reply_message(msg)},\
        friends=(msg.send_user,))
    context_map['form']=form
    return render_to_response('msgbox/compose_message.html',
        context_map)