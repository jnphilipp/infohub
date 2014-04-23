from django.shortcuts import get_object_or_404, render
from documents.models import Document

def documents(request):
	documents = Document.objects.order_by('-created_at')
	return render(request, 'documents/documents.html', locals())

def document(request, slug):
	document = get_object_or_404(Document, slug=slug)
	return render(request, 'documents/document.html', locals())