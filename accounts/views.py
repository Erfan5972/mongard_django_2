from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, UserEditProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'],
                                     email=cd['email'],
                                     password=cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home')
        else:
            return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'Invalid username or password', 'error')
                if self.next:
                    return redirect(self.next)
                return redirect('accounts:login')
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        posts = user.posts.all()
        is_following = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'accounts/profile.html',
                      {'user': user, 'posts': posts,
                       'is_following': is_following})


class UserResetPasswordView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html' #ایمیل ارسالی به کاربر چگونه باشد:



class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if user.id != request.user.id:
            relation = Relation.objects.filter(from_user=request.user, to_user=user)
            if relation.exists():
                messages.error(request, 'you have been followed this user', 'error')
            else:
                Relation.objects.create(from_user=request.user, to_user=user)
                messages.success(request, 'user followed successfully', 'success')
                return redirect('accounts:profile', user_id)
        else:
            messages.error(request, 'you cant follow yours', 'error')
            return redirect('accounts:profile', user_id)


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if user.id != request.user.id:
            relation = Relation.objects.filter(from_user=request.user, to_user=user)
            if relation.exists():
                relation.delete()
                messages.success(request, 'user unfollowed successfully', 'success')
            else:
                messages.error(request, 'you did not followed this user yet', 'error')
            return redirect('accounts:profile', user_id)
        else:
            messages.error(request, 'you cant follow yours', 'error')
            return redirect('accounts:profile', user_id)


class UserEditProfileView(LoginRequiredMixin, View):
    form_class = UserEditProfileForm

    def get(self, request):
        profile = request.user.profile
        form = self.form_class(instance=profile, initial={'email': request.user.email})
        return render(request, 'accounts/user_edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'your information changed successfully', 'success')
            return redirect('accounts:profile', request.user.id)
        return redirect('accounts:profile', request.user.id)