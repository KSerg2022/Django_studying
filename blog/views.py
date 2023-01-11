from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.views import generic

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Post, Tag
from .forms import CommentForm, TagForm, PostForm
from .utils import create_slug


def index(request):
    return render(request, './index.html')


class PostListView(generic.ListView):
    model = Post
    # queryset = Post.published.all()
    queryset = Post.objects.filter(status='published')
    paginate_by = 3
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Published posts'
        return context


class PostDraftListView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status='draft')
    paginate_by = 3
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Draft posts'
        return context


def post_detail(request, year, month, day, post):
    """Post detail"""
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        tag_form = TagForm(data=request.POST)
        comment_form = CommentForm(data=request.POST)

        if 'tag_name' in request.POST:
            if tag_form.is_valid():
                new_tag = tag_form.save(commit=False)
                new_tag.save()
                new_tag.post_set.add(post)
                messages.success(request, 'You create new tag and added it to current post',
                                 extra_tags='teg list-group-item list-group-item-success')
            elif post in Tag.objects.get(tag_name=tag_form.data.get('tag_name')).post_set.all():
                messages.warning(request, 'This tag already added.',
                                 extra_tags='tag list-group-item list-group-item-warning')
            else:
                if tag := Tag.objects.get(tag_name=tag_form.data.get('tag_name')):
                    tag.post_set.add(post)
                    messages.success(request, 'You added tag to current post',
                                     extra_tags='tag list-group-item list-group-item-success')

        if 'body' in request.POST:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                messages.success(request, 'You added new comment to current post',
                                 extra_tags='list-group-item list-group-item-success')

        url = request.build_absolute_uri()
        return HttpResponseRedirect(url)

    else:
        comment_form = CommentForm()
        tag_form = TagForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status='published').filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:5]

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'tag_form': tag_form,
        'similar_posts': similar_posts
    }
    return render(
        request,
        'blog/post_detail.html',
        context)


def post_list_for_(request, tag=None, author=None, user=None):
    """List of published posts with teg."""
    object_list = None
    add_to_context = {}
    if tag:
        tag = Tag.objects.get(tag_name=tag)
        object_list = tag.post_set.filter(status='published')
        add_to_context['tag'] = tag

    if author:
        object_list = Post.objects.filter(status='published').filter(author=User.objects.get(username=author).id)
        add_to_context['author'] = author

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': posts,
        'post_list': posts,
    }
    context.update(add_to_context)
    return render(request, 'blog/post_list_for_teg.html', context)


@login_required
def add_post(request):
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.slug = create_slug(post_form.cleaned_data['title'])
            new_post.author = request.user
            new_post.save()

            for tag in post_form.cleaned_data['tags']:
                tag = Tag.objects.get(tag_name=tag)
                tag.post_set.add(new_post)

            messages.success(request, 'You added new post',
                             extra_tags='list-group-item list-group-item-success')
        else:
            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')

            context = {'post_form': post_form, 'action': 'Add post', 'title': 'You can add new post: '}
            return render(request, 'blog/add_post.html', context)

        return redirect('blog:get_user_posts')

    context = {'post_form': post_form, 'action': 'Add post', 'title': 'You can add new post: '}
    return render(request, 'blog/add_post.html', context)


@login_required
def get_user_posts(request, published=None, draft=None):
    user_posts = Post.objects.filter(author=request.user)

    if not user_posts:
        messages.warning(request, 'You have not created any post yet.',
                         extra_tags='list-group-item list-group-item-success')
        return redirect('blog:add_post')
    context_status = {}
    if published:
        user_posts = Post.objects.filter(author=request.user).filter(status=published)
        context_status['status'] = published
    if draft:
        user_posts = Post.objects.filter(author=request.user).filter(status=draft)
        context_status['status'] = draft

    paginator = Paginator(user_posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': request.user,
        'post_list': posts,
        'page': posts,
        'logged_user': request.user
    }
    context.update(context_status)
    return render(request, 'blog/post_list_user.html', context)


def user_posts_for_(request, user=None, tag=None):
    """List of published posts with teg."""
    object_list = None
    add_to_context = {}
    if tag:
        tag = Tag.objects.get(tag_name=tag)
        object_list = tag.post_set.filter(author=request.user)
        add_to_context['tag'] = tag

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': posts,
        'post_list': posts,
        'logged_user': request.user
    }
    context.update(add_to_context)
    return render(request, 'blog/posts_user_for_.html', context)


@login_required
def edit_post(request, post_id=None):
    post = get_object_or_404(Post, id=post_id)
    if Post.objects.get(id=post_id).author != request.user:
        raise Http404

    post_form = PostForm(instance=post)
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)

        if post_form.is_valid():
            post.title = post_form.cleaned_data.get('title')
            post.user = post_form.cleaned_data.get('author')
            post.body = post_form.cleaned_data.get('body')
            post.publish = post_form.cleaned_data.get('publish')
            post.status = post_form.cleaned_data.get('status')

            for tag in post_form.cleaned_data['tags']:
                tag = Tag.objects.get(tag_name=tag)
                tag.post_set.add(post)

            for tag in Post.objects.get(id=post.id).tags.all():
                if tag not in post_form.cleaned_data['tags']:
                    tag.post_set.remove(post)

            post.save()
            messages.success(request, 'Post updated.',
                             extra_tags='list-group-item list-group-item-success')
        else:

            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')
            context = {'post_form': post_form}
            return render(request, 'blog/add_post.html', context)

        url = post.get_absolute_url()
        return HttpResponseRedirect(url)

    context = {'post_form': post_form,
               'post': post,
               'action': 'Save change',
               'delete': 'Delete',
               'title': 'You can edit post: '}
    return render(request, 'blog/add_post.html', context)


def delete_post(request, post_id=None):
    post = get_object_or_404(Post, id=post_id)
    if Post.objects.get(id=post_id).author != request.user:
        raise Http404

    if request.GET.get('yes') == 'yes':
        post.delete()
        messages.success(request, f'Your post "{post.title}" was deleted',
                         extra_tags='list-group-item list-group-item-success')
        return redirect('blog:get_user_posts')

    context = {'post': post, 'delete': 'Delete'}
    return render(request, 'blog/delete_post.html', context)
