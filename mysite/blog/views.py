from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    #posts = Post.published.all()
    
    post_list =Post.published.all()
    #for 3 post on page
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page', 1)
    #exeption error 
    try:
        posts = paginator.page(page_number)
    #if user try indicate page like string
    except PageNotAnInteger:
        posts = paginator.page(1)
    #if user try indicate non-existent page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 
                  'blog/post/list.html', 
                  {'posts': posts})

'''def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No Post found.")

'''
#old urls look 
#def post_detail(request, id):
#   post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

#new function for extract post with parameters what we need, for a new look urls
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                              status=Post.Status.PUBLISHED,
                              slug=post,
                              publish__year=year,
                              publish__month=month,
                              publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})