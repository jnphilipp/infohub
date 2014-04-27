from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from documents.models import Document
from feeds.models import Feed, Report
from datetime import datetime, date, time
from pytz import utc

@login_required(login_url='/admin/')
def feeds(request):
	feeds = Feed.objects.order_by('alive', '-updated_at')
	return render(request, 'feeds/feeds.html', locals())

@login_required(login_url='/admin/')
def feed(request, slug):
	feed = get_object_or_404(Feed, slug=slug)
	return render(request, 'feeds/feed.html', locals())

@login_required(login_url='/admin/')
def reports(request):
	reports = Report.objects.order_by('-created_at')
	return render(request, 'feeds/reports.html', locals())

@login_required(login_url='/admin/')
def report(request, slug):
	report = get_object_or_404(Report, slug=slug)
	return render(request, 'feeds/report.html', locals())

@login_required(login_url='/admin/')
def statistics(request):
	today_min = datetime.combine(date.today(), time.min).replace(tzinfo=utc)
	today_max = datetime.combine(date.today(), time.max).replace(tzinfo=utc)

	feeds = Feed.objects.count()

	documents = Document.objects.count()
	today_documents = Document.objects.filter(created_at__range=(today_min, today_max)).count()

	reports = Report.objects.count()
	today_reports = Report.objects.filter(created_at__range=(today_min, today_max))

	return render(request, 'feeds/statistics.html', locals())