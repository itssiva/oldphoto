from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^OldPhoto/', include('OldPhoto.apps.foo.urls.foo')),
    #(r'^avatar/(.*)$', 'django.views.static.serve',{'document_root': settings.SITE_AVATAR}),
    #(r'^style/(.*)$', 'django.views.static.serve',{'document_root': settings.SITE_STYLE}),
    #(r'^images/(.*)$', 'django.views.static.serve',{'document_root': settings.SITE_IMAGES}),
    (r'^userpanel/', include('apps.userpanel.URLconf')),
    (r'^space/', include('apps.space.URLconf')),
    (r'^photos/', include('apps.photos.URLconf')),
    (r'^tags/', include('apps.tag.URLconf')),
    (r'^msgbox/', include('apps.msgbox.URLconf')),
    (r'^$', 'apps.portal.views.index'),
    (r'^base/$', 'apps.portal.views.base'),
    (r'^base_3col/$', 'apps.portal.views.base_3col'),
    (r'^base_2col/$', 'apps.portal.views.base_2col'),
    (r'^sec/$', 'apps.portal.views.sec'),
    (r'^test/$', 'apps.portal.views.test'),
    (r'^allcomments/$', 'apps.portal.views.allcomments'),
    (r'^allrecommends/$', 'apps.portal.views.allrecommends'),
    (r'^allhotphotos/$', 'apps.portal.views.allhotphotos'),
    (r'^allnewphotos/$', 'apps.portal.views.allnewphotos'),
    (r'^search/$', 'apps.portal.views.search'),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
