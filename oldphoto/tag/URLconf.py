from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('oldphoto.tag',
                       (r'^$', 'views.index'),
                       (r'^(?P<tag_id>\d+)/$', 'views.index'),
)
