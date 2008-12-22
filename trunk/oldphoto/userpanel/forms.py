# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User
from oldphoto.userpanel.models import UserProfile
from django.utils.translation import gettext as _
from oldphoto.utils.ImageUtils import checkImage

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.widgets.TextInput(\
        attrs={'style':'width: 10em;'}), label='登录名')
    password = forms.CharField(max_length=40, widget=forms.widgets.PasswordInput(\
        attrs={'style':'width: 10em;'}), label='密码')


class UpdatePswdForm(forms.Form):
    old_pswd = forms.CharField(max_length=40,\
        widget=forms.widgets.PasswordInput(\
        attrs={'style':'width: 10em;'}), label='原始密码')
    new_pswd = forms.CharField(max_length=40,\
        widget=forms.widgets.PasswordInput(\
        attrs={'style':'width: 10em;'}), label='新密码')
    r_pswd = forms.CharField(max_length=40,\
        widget=forms.widgets.PasswordInput(\
        attrs={'style':'width: 10em;'}), label='新密码')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UpdatePswdForm, self).__init__(data, *args, **kwargs)
        self.user=user

    def clean_old_pswd(self):
        old_pswd = self.cleaned_data['old_pswd']
        from django.contrib import auth
        self.user = auth.authenticate(username=self.user.username,\
            password=old_pswd)
        if self.user is not None:
            return old_pswd
        raise forms.ValidationError(_('原始密码错误'))

    def clean_r_pswd(self):
        p = self.cleaned_data['new_pswd']
        rp = self.cleaned_data['r_pswd']
        if p==rp:
            return p
        raise forms.ValidationError(_('两次输入的密码不一致'))

class SignupForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.widgets.TextInput(\
        attrs={'style':'width: 10em;'}), label='登录名')
    password = forms.CharField(max_length=40,\
        widget=forms.widgets.PasswordInput(attrs={'style':'width: 10em;'}),\
        label='密码')
    rpassword = forms.CharField(max_length=40,\
        widget=forms.widgets.PasswordInput(attrs={'style':'width: 10em;'}),\
        label='确认密码')

    def clean_username(self):
        n = self.cleaned_data['username']
        try:
            User.objects.get(username=n)
        except User.DoesNotExist:
            return n
        raise forms.ValidationError(_('用户名 "%s" 已存在') % n)

    def clean_rpassword(self):
        p = self.cleaned_data['password']
        rp = self.cleaned_data['rpassword']
        if p==rp:
            return p
        raise forms.ValidationError(_('两次输入的密码不一致'))

    def save(self):
        user_obj = User.objects.create_user(\
            username=self.cleaned_data['username'], email='',\
            password=self.cleaned_data['password'])
        user_obj.is_staff = True
        user_obj.is_superuser = False
        user_obj.save()
        prof_obj = UserProfile(user=user_obj)
        prof_obj.save()
        from django.contrib.auth import authenticate
        return authenticate(username=self.cleaned_data['username'],\
                            password=self.cleaned_data['password']) 

class EditForm(forms.Form):
    gender = forms.CharField(max_length=200, widget=forms.widgets.Select(\
        choices=(('', '保密'), ('M', '男'), ('F', '女')),\
        ), label='性别', required=False)
    blog = forms.URLField(max_length=200,\
        widget=forms.widgets.TextInput(attrs={'style':'width: 21em;'}),\
        label='Blog', required=False)
    intro = forms.CharField(\
        widget=forms.widgets.Textarea(attrs={'rows': 10, 'cols': 50}),\
        label='内容', required=False)

class AvatarForm(forms.Form):
    avatar = forms.CharField(\
        widget=forms.widgets.FileInput(attrs={'size':38}),\
        label='头像', required=False)

    def __init__(self, data=None, files=None, *args, **kwargs):
        super(AvatarForm, self).__init__(data, *args, **kwargs)
        self.files=files

    def clean_avatar(self):
        try:
            value=self.files['avatar']
        except:
            raise forms.ValidationError(_('上传图片不能为空'))
        checkImage(value)
        return value
