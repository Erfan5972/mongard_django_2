from django.shortcuts import render, redirect
from django.views import View
from post.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm
from django.utils.text import slugify
from comment.forms import CommentCreateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        # posts = Post.objects.order_by('?') # این برای انتخاب رندوم است
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    form_class = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        comments = post.pcomments.filter(is_reply=False)
        form = self.form_class()
        return render(request, 'home/post_detail.html', {'post': post, 'comments': comments, 'form': form})
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()

            return redirect('home:post_detail', post_id=self.post_instance.id, post_slug=self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'error')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this object', 'error')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post
        form = self.form_class(instance=post)
        return render(request, 'home/post_update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post
        form = self.form_class(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(form.cleaned_data['body'][:30])
            post.save()
            messages.success(request, 'post updated successfully', 'success')
            return redirect('home:post_detail', post_id=post.id, post_slug=post.slug)
        return render(request, 'home/post_update.html', {'form': form})


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'home/post_create.html', {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'you create a post successfully', 'success')
            return redirect('accounts:profile', request.user.id)
        return render(request, 'home/post_create.html', {'form': form})
