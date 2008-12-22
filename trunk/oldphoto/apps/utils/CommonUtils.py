# -*- coding: UTF-8 -*-
def UTF_8_to_Unicode(t):
    return unicode(t,'UTF-8')


def txt2set(s):
    """
    将用空格分割的字符串转换成set
    """
    return set([e.strip().lower() for e in s.split(" ") if e.strip() != ''])


def get_base_context_map(request, ext_context_map={}):
    user=request.user
    ext_context_map['user']=request.user
    #if user.is_authenticated():
    #    ext_context_map['new_mail_count']=get_count("""
    #        select count(*) from msgbox_message
    #        where rec_user_id=%s and msgbox_message.read='u'
    #        and type='r'  """,
    #        (user.id,))
    return ext_context_map


def get_count(sql, params):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql, params)
    count=0
    for row in cursor.fetchall():
        count=row[0]
    return count


def is_superuser(u):
    return u.is_authenticated() and u.is_superuser