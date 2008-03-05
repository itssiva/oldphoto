# -*- coding: UTF-8 -*-
import settings
from StringIO import StringIO
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from apps.userpanel.forms import LoginForm, SignupForm, EditForm, AvatarForm,\
    UpdatePswdForm
from django.contrib.auth import SESSION_KEY, REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from apps.userpanel.models import UserProfile
from apps.utils import ImageUtils
from apps.utils.CommonUtils import get_base_context_map


def signup(request, next_page=None):
    context_map=get_base_context_map(request)
    form = SignupForm()
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            from django.contrib import auth
            auth.login(request, user_obj)
            return HttpResponseRedirect(next_page or '/')
    context_map['form']=form
    return render_to_response('userpanel/signup.html',context_map)


def login(request):
    context_map=get_base_context_map(request)
    errorMsg=""
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '/')
    form = LoginForm()
    if request.POST:
        errorMsg="登录失败"
        form = LoginForm(request.POST)
        if form.is_valid():
            #做基本验证外的其他验证
            data=form.cleaned_data
            from django.contrib import auth
            user = auth.authenticate(username=data['username'],\
                password=data['password'])
            if user is not None:
                errorMsg=""
                auth.login(request, user)
                #request.session.delete_test_cookie()
                return HttpResponseRedirect(redirect_to)
            else:
                errorMsg="您输入的用户名或密码不正确，请重试。"
    #request.session.set_test_cookie()
    context_map['form']=form
    context_map['errorMsg']=errorMsg
    return render_to_response('userpanel/login.html',context_map)


def logout(request, next_page=None):
    next_page = '/';
    from django.contrib import auth
    auth.logout(request)
    return HttpResponseRedirect(next_page or request.path)


@login_required
def updatepswd(request, next_page=None):
    """
    修改密码
    """
    context_map=get_base_context_map(request)
    next_page = '/'
    u = request.user
    form = UpdatePswdForm()
    if request.POST:
        form = UpdatePswdForm(request.POST, u)
        if form.is_valid():
            u.set_password(form.cleaned_data['new_pswd'])
            u.save()
            return HttpResponseRedirect('/space/')
    context_map['form']=form
    return render_to_response('userpanel/updatepswd.html',context_map)


@login_required
def edit(request):
    context_map=get_base_context_map(request)
    user = request.user
    form = EditForm(user.get_profile().__dict__)
    if request.POST:
        form = EditForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user.get_profile().gender=data['gender']
            user.get_profile().blog=data['blog']
            user.get_profile().intro=data['intro']
            user.get_profile().save()
            return HttpResponseRedirect('/space/')
    context_map['form']=form
    return render_to_response('userpanel/edit.html',context_map)


def upload_avatar(img, userid):
    """
    上传头像
    img 图像stream或文件名
    ext 文件的后缀
    """
    filename=settings.AVATAR_ROOT + str(userid) + '.jpg'
    ImageUtils.make_thumb(img=img, filename=filename, size=48, square=True)


@login_required
def avatar(request):
    context_map=get_base_context_map(request)
    user = request.user
    form = AvatarForm()#user.get_profile().__dict__
    if request.method == 'POST':#if request.POST:
        form = AvatarForm(request.POST, files=request.FILES)
        if form.is_valid():
            clean_data=form.cleaned_data
            if clean_data['avatar']:
                avatar = clean_data['avatar']
                upload_avatar(StringIO(avatar['content']),user.id)
                user.get_profile().avatar=str(user.id)+'.jpg'
            else:
                user.get_profile().avatar=''
            user.get_profile().save()
            return HttpResponseRedirect('/space/')
    context_map['form']=form
    return render_to_response('userpanel/avatar.html',context_map)