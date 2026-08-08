from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Follow


@login_required
@require_POST
def toggle_follow_view(request, username):
    target = get_object_or_404(User, username=username)

    if target == request.user:
        messages.error(request, "You can't follow yourself.")
        return redirect('users:profile', username=username)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        messages.info(request, f'Unfollowed {target.username}.')
    else:
        messages.success(request, f'You are now following {target.username}.')

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('users:profile', username=username)


def followers_list_view(request, username):
    target = get_object_or_404(User, username=username)
    follows = Follow.objects.filter(following=target).select_related('follower', 'follower__profile')
    return render(request, 'followers/user_list.html', {
        'profile_user': target,
        'title': f'People following {target.username}',
        'users': [f.follower for f in follows],
    })


def following_list_view(request, username):
    target = get_object_or_404(User, username=username)
    follows = Follow.objects.filter(follower=target).select_related('following', 'following__profile')
    return render(request, 'followers/user_list.html', {
        'profile_user': target,
        'title': f'People {target.username} follows',
        'users': [f.following for f in follows],
    })
