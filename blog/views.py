from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render_to_response, HttpResponse
from django.shortcuts import render, redirect
import json
import random
from django.forms.models import model_to_dict
from django.http import JsonResponse


# Post.objects.get(pk=pk)
# Create your views here.
def post_list(request):

    return render(request, 'blog/post_list.html', {'posts': Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


class createuser(CreateView):
    model = User
    template_name = "blog/createuser.html"
    fields = "username", "password", "email", "first_name"


def get_success_url(self):
    return reverse_lazy('post_list')


# def anlikveri(request):
#     # Ajax istediği gelirse kontrol et
#     data = {'anlik': Post.objects.all().values()}
#     print(request.is_ajax())
#     if request.is_ajax():
#         return HttpResponse(data, content_type="application/json")

#     return HttpResponse('hello', content_type="application/json")


def anlikveri(request):
    if request.is_ajax():
        data = list(Post.objects.filter(
            published_date__lte=timezone.now()).values())
        print(type(data))
        return JsonResponse(
            {
                # istek gelirse, rastgele sayı yolla
                'anlik':  data
            }
        )
    return render(request, 'anlikveri.html', locals())


# class AnlikVeri:
#     def post(self, *args, **kwargs):
#         data = Post.objects.all().values()
#         return HttpResponse(data)
