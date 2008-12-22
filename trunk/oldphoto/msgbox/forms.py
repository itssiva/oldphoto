# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from oldphoto.msgbox.models import Message
#from oldphoto.utils.html2text import html2text
from oldphoto.utils.textconvert import plaintext2html


class ComposeMessageForm(forms.Form):
    """
    站内消息
    """

    def __init__(self, data=None, friends=None, user=None, *args, **kwargs):
        super(ComposeMessageForm, self).__init__(data, *args, **kwargs)
        self.friends=friends
        self.fields['rec_user'].choices=friends
        self.user=user
    rec_user = forms.ChoiceField(choices=(), widget=forms.Select())
    title = forms.CharField(max_length=200,\
        widget=forms.widgets.TextInput(attrs={'style':'width: 30em;'}),\
        label='Blog', required=True)
    content = forms.CharField(\
        widget=forms.widgets.Textarea(attrs={'rows': 12, 'cols': 70}),\
        label='内容', required=True)

    def clean_rec_user(self):
        id = self.cleaned_data['rec_user']
        try:
            self.rec_user_obj=User.objects.get(pk=id)
        except User.DoesNotExist:
            raise forms.ValidationError(_('收信人不存在'))
        return id

    def save(self, type):
        msg=Message(rec_user=self.rec_user_obj,send_user=self.user,type=type,\
            title=self.cleaned_data['title'], read='u',\
            content=plaintext2html(self.cleaned_data['content']))
        msg.save()

    def save_draft(self):
        self.save('d')

    def send(self):
        self.save('s')
        self.save('r')
