from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models.functions import Greatest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage, Page

from taggit.models import Tag

from .forms import *
from .models import *

# Create your views here.


def index(request):
    return render(request, 'Social/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='login')
def user_edit(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Social:index')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'registration/edit_user.html', {'form': form})


@login_required(login_url='login')
def ticket(request):
    sent = False
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['author_name']}\n{cd['phone']}\n{cd['email']}\n\n{cd['message']}"
            send_mail(
                cd['subject'],
                message,
                'mehdifarajise666@gmail.com',
                ['mahdifaraji13mf82@gmail.com'],
                fail_silently=False,
            )
            sent = True
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form, 'sent': sent})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'tag': tag}
    return render(request, 'social/list.html', context)

@login_required(login_url='login')
def post_create(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        return redirect('Social:index')
    else:
        form = CreatePostForm()
    return render(request, 'forms/post_create.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(pk=pk)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')
    commented = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        commented = True
    else:
        form = CommentForm()
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'form': form,
        'commented': commented,
    }
    return render(request, 'social/detail.html', context)


def post_search(request):
    query = None
    result = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # search_query = SearchQuery(query)
            # search_vector = SearchVector('caption', weight='A') + SearchVector('tags', weight='B')
            # search_rank = SearchRank(search_vector, search_query)
            # result = Post.objects.annotate(search=search_vector, rank=search_rank).filter(search=search_query)

            result = (Post.objects.annotate(similarity=Greatest(TrigramSimilarity('caption', query),
                                                               TrigramSimilarity('tags__name', query)))
                      .filter(similarity__gte=0.1).order_by('-similarity'))

    context = {
        'query': query,
        'result': result,
    }
    return render(request, 'social/search.html', context)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('Social:post_detail', pk=pk)
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/post_create.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('Social:index')
    return render(request, 'forms/post_delete.html', {'post': post})

