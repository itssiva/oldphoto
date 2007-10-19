from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('apps.tag',
                       (r'^$', 'views.index'),
                       (r'^(?P<tag_id>\d+)/$', 'views.index'),
)
