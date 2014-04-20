from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'feeds.views.feeds', name='home'),
	url(r'^feeds/$', 'feeds.views.feeds', name='feeds'),
	url(r'^feeds/(?P<slug>[\w-]+)/$', 'feeds.views.feed', name='feed'),
	url(r'^documents/$', 'feeds.views.documents', name='documents'),
	url(r'^documents/(?P<slug>[\w-]+)/$', 'feeds.views.document', name='document'),
	url(r'^reports/$', 'feeds.views.reports', name='reports'),
	url(r'^reports/(?P<slug>[\w-]+)/$', 'feeds.views.report', name='report'),
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)