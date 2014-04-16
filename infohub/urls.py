from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'feeds.views.feeds', name='home'),
	url(r'^feed/$', 'feeds.views.feeds', name='feeds'),
	url(r'^feed/(?P<slug>[\w-]+)/$', 'feeds.views.feed', name='feed'),
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)