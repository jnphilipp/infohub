from django.shortcuts import get_object_or_404, render
from feeds.models import Feed, Document

def feeds(request):
	feeds = Feed.objects.order_by('alive', 'title')
	return render(request, 'feeds/feeds.html', locals())

def feed(request, slug):
	feed = get_object_or_404(Feed, slug=slug)
	return render(request, 'feeds/feed.html', locals())