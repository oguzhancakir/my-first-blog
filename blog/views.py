from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
# Post.objects.get(pk=pk)
# Create your views here.
def post_list(request):
    
    return render(request, 'blog/post_list.html', {'posts':Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})