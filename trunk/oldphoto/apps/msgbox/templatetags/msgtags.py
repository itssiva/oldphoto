from django import template
from apps.utils.CommonUtils import get_count

register = template.Library()

class NewMsgCountNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        c=get_count("""
            select count(*) from msgbox_message
            where rec_user_id=%s and msgbox_message.read='u'
            and type='r'  """,            
            (context['user'].id,))
        return c

def do_new_msg_count(parser, token):
    return NewMsgCountNode()

register.tag('new_msg_count', do_new_msg_count)