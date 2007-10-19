from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('apps.userpanel',
                       (r'^signup/$', 'views.signup'),
                       (r'^login/$', 'views.login'),
                       (r'^logout/$', 'views.logout'),
                       (r'^edit/$', 'views.edit'),
                       (r'^updatepswd/$', 'views.updatepswd'),
                       (r'^avatar/$', 'views.avatar'),
                       (r'^inbox/$', 'views.inbox'),
                       (r'^outbox/$', 'views.outbox'),
                       (r'^draftbox/$', 'views.draftbox'),
                       (r'^compose_message/$', 'views.compose_message'),
                       (r'^compose_message/(?P<to_user_id>\d+)/$', 'views.compose_message'),
)