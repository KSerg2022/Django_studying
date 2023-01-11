from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect


from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserSettingsForm


def signup(request):
    signup_form = UserCreationForm()

    if request.method == 'POST':
        signup_form = UserCreationForm(data=request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            login(request, new_user)
            messages.success(request, 'Welcome to site',
                             extra_tags='list-group-item list-group-item-success')
        else:
            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')
            url = request.build_absolute_uri()
            return HttpResponseRedirect(url)

        return redirect('blog:index')

    context = {'signup_form': signup_form}
    return render(request, 'registration/signup.html', context)


@login_required
def settings(request):
    user = get_object_or_404(User, pk=request.user.id)
    settings_form = UserSettingsForm(instance=user)

    if request.method == 'POST':
        settings_form = UserSettingsForm(data=request.POST)
        if settings_form.is_valid():
            user.first_name = settings_form.data.get('first_name')
            user.last_name = settings_form.data.get('last_name')
            user.email = settings_form.data.get('email')
            user.save()

            messages.success(request, 'You change your settings.',
                             extra_tags='list-group-item list-group-item-success')
        else:
            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')
        context = {'settings_form': settings_form, 'action': 'Save settings'}
        return render(request, 'registration/settings.html', context)

    context = {'settings_form': settings_form, 'action': 'Save settings'}
    return render(request, 'registration/settings.html', context)
