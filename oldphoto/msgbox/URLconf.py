from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('oldphoto.msgbox',
                       (r'^inbox/$', 'views.inbox'),
                       (r'^outbox/$', 'views.outbox'),
                       (r'^draftbox/$', 'views.draftbox'),
                       (r'^compose_message/$', 'views.compose_message'),
                       (r'^compose_message/(?P<to_user_id>\d+)/$', 'views.compose_message'),
                       (r'^view_message/(?P<msg_id>\d+)/$', 'views.view_message'),
                       (r'^delete_message/(?P<msg_id>\d+)/$', 'views.delete_message'),
                       (r'^reply_message/(?P<msg_id>\d+)/$', 'views.reply_message'),
)
