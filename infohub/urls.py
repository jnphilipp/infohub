from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# url(r'^$', 'posts.views.index', name='home'),
	# url(r'^feed/$', Feed(), name='feed'),
	# url(r'^files/file/(?P<slug>[\w-]+)/$', 'files.views.file', name='file'),
	# url(r'^files/image/(?P<slug>[\w-]+)/$', 'files.views.image', name='image'),
	# url(r'^archive/$', 'posts.views.archive', name='archive'),
	# url(r'^posts/$', 'posts.views.index'),
	# url(r'^posts/(?P<slug>[\w-]+)/$', 'posts.views.post', name='post'),
	# url(r'^pages/(?P<slug>[\w-]+)/$', 'pages.views.page', name='page'),
	# url(r'^tags/(?P<slug>[\w-]+)/$', 'posts.views.tag', name='tag'),
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)