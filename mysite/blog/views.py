from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# Create your views here.

def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" \
                        f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'alexkllin6@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', 
                  {'post': post, 'form': form, 'sent': sent})

class PostListView(ListView):
    #alternativ view posts list
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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
    #added functional for comments
    #list of active comments to this post
    comments = post.comments.filter(active=True)
    #form for comments
    form = CommentForm()

    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    
    comment = None
    #comment sent
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #create object class Comment, without save him in DB
        comment = form.save(commit=False)
        #Assign post to comment
        comment.post = post
        #save comment in DB
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post':post,
                   'form': form,
                   'comment': comment})

