from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from documents.models import Document

@login_required(login_url='/admin/')
def documents(request):
	documents = Document.objects.order_by('-created_at')
	return render(request, 'documents/documents.html', locals())

@login_required(login_url='/admin/')
def document(request, slug):
	document = get_object_or_404(Document, slug=slug)
	return render(request, 'documents/document.html', locals())