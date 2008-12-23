from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^OldPhoto/', include('OldPhoto.oldphoto.foo.urls.foo')),
    #(r'^avatar/(.*)$', 'django.views.static.serve',{'document_root': settings.SITE_AVATAR}),
    #(r'^style/(.*)$', 'django.views.static.serve',{'document_root': settings.SITE_STYLE}),
    #(r'^images/(.*)$', 'django.views.static.serve',{'document_root': settings.SITE_IMAGES}),
    # Uncomment this for admin:
    ('^admin/(.*)', admin.site.root),
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^userpanel/', include('oldphoto.userpanel.URLconf')),
    (r'^space/', include('oldphoto.space.URLconf')),
    (r'^photos/', include('oldphoto.photos.URLconf')),
    (r'^tags/', include('oldphoto.tag.URLconf')),
    (r'^msgbox/', include('oldphoto.msgbox.URLconf')),
    (r'^$', 'oldphoto.portal.views.index'),
    (r'^base/$', 'oldphoto.portal.views.base'),
    (r'^base_3col/$', 'oldphoto.portal.views.base_3col'),
    (r'^base_2col/$', 'oldphoto.portal.views.base_2col'),
    (r'^sec/$', 'oldphoto.portal.views.sec'),
    (r'^test/$', 'oldphoto.portal.views.test'),
    (r'^allcomments/$', 'oldphoto.portal.views.allcomments'),
    (r'^allrecommends/$', 'oldphoto.portal.views.allrecommends'),
    (r'^allhotphotos/$', 'oldphoto.portal.views.allhotphotos'),
    (r'^allnewphotos/$', 'oldphoto.portal.views.allnewphotos'),
    (r'^search/$', 'oldphoto.portal.views.search'),
)
