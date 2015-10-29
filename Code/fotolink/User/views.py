from forms import UserForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect


def register(request):
    print "oime"
    if request.method == "POST":
        print "aca toy"
        form = UserForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['name']
            password= form.cleaned_data['password']
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('reg_ok.html')
    else:
        form = UserForm()
        return render(request, 'User/register.html', {'form': form})
