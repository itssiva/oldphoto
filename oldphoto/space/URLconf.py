from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('oldphoto.space',
                       (r'^$', 'views.index'),
                       (r'^collections/$', 'views.collections'),
                       (r'^collections/(?P<user_id>\d+)/$', 'views.collections'),
                       (r'^photos/$', 'views.photos'),
                       (r'^photos/(?P<user_id>\d+)/$', 'views.photos'),
                       (r'^tags/(?P<user_id>\d+)/$', 'views.tags'),
                       (r'^tags/(?P<user_id>\d+)/(?P<tag_id>\d+)/$', 'views.tags'),
                       (r'^allcomments/$', 'views.allcomments'),
                       (r'^allcomments/(?P<user_id>\d+)/$', 'views.allcomments'),
                       (r'^(?P<user_id>\d+)/$', 'views.index'),
                       (r'^friends/$', 'views.friends'),
                       (r'^friends/(?P<user_id>\d+)/$', 'views.friends'),
                       (r'^followers/$', 'views.followers'),
                       (r'^followers/(?P<user_id>\d+)/$', 'views.followers'),
                       (r'^add_friend/$', 'views.add_friend'),
                       (r'^add_friend/(?P<user_id>\d+)/$', 'views.add_friend'),
                       (r'^drop_friend/$', 'views.drop_friend'),
                       (r'^drop_friend/(?P<id>\d+)/$', 'views.drop_friend'),
)
