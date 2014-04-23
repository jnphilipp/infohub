from django.shortcuts import get_object_or_404, render
from feeds.models import Feed, Report

def feeds(request):
	feeds = Feed.objects.order_by('alive', '-updated_at')
	return render(request, 'feeds/feeds.html', locals())

def feed(request, slug):
	feed = get_object_or_404(Feed, slug=slug)
	return render(request, 'feeds/feed.html', locals())

def reports(request):
	reports = Report.objects.order_by('-created_at')
	return render(request, 'feeds/reports.html', locals())

def report(request, slug):
	report = get_object_or_404(Report, slug=slug)
	return render(request, 'feeds/report.html', locals())