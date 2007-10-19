from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('apps.photos',
                       (r'^$', 'views.index'),
                       (r'^upload/$', 'views.upload'),
                       (r'^edit/(?P<id>\d+)/$', 'views.edit'),
                       (r'^hidden/(?P<id>\d+)/$', 'views.hidden'),
                       (r'^show/(?P<id>\d+)/$', 'views.show'),
                       (r'^delete/(?P<id>\d+)/$', 'views.delete'),
                       (r'^recommend/(?P<id>\d+)/$', 'views.recommend'),
                       (r'^collection/(?P<id>\d+)/$', 'views.collection'),
                       (r'^dis_collection/(?P<id>\d+)/$', 'views.dis_collection'),
                       (r'^check/(?P<id>\d+)/$', 'views.check'),
                       (r'^(?P<id>\d+)/$', 'views.view_photo'),
                       (r'^comment/hidden/(?P<id>\d+)/$', 'views.comment_hidden'),
                       (r'^comment/show/(?P<id>\d+)/$', 'views.comment_show'),
                       (r'^comment/delete/(?P<id>\d+)/$', 'views.comment_delete'),                    
)
