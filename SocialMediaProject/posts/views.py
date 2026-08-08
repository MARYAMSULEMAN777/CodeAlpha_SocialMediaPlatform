from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from followers.models import Follow
from .forms import PostForm, CommentForm
from .models import Post, Like


def home_view(request):
    feed = request.GET.get('feed', 'all')

    if feed == 'following' and request.user.is_authenticated:
        following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        posts = Post.objects.filter(Q(user_id__in=following_ids) | Q(user=request.user))
    else:
        posts = Post.objects.all()

    posts = posts.select_related('user', 'user__profile').prefetch_related('likes', 'comments')

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    create_form = PostForm() if request.user.is_authenticated else None

    return render(request, 'posts/home.html', {
        'page_obj': page_obj,
        'create_form': create_form,
        'active_feed': feed,
    })


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post is live.')
            return redirect('posts:home')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


def post_detail_view(request, pk):
    post = get_object_or_404(Post.objects.select_related('user', 'user__profile'), pk=pk)
    comments = post.comments.select_related('user', 'user__profile')
    comment_form = CommentForm() if request.user.is_authenticated else None

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden("You can't edit someone else's post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated.')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
@require_POST
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden("You can't delete someone else's post.")
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('posts:home')


@login_required
@require_POST
def like_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_count})


@login_required
@require_POST
def add_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return JsonResponse({
            'success': True,
            'username': comment.user.username,
            'text': comment.text,
            'comment_count': post.comment_count,
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def search_view(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    users = User.objects.none()

    if query:
        posts = Post.objects.filter(caption__icontains=query).select_related('user', 'user__profile')
        users = User.objects.filter(
            Q(username__icontains=query) | Q(profile__bio__icontains=query)
        ).select_related('profile')

    return render(request, 'posts/search.html', {
        'query': query,
        'posts': posts,
        'users': users,
    })
