from forms import UserForm
from django.views.generic import CreateView
from django.contrib.auth import views


class Register2(CreateView):
    template_name = 'User/register.html'
    form_class = UserForm
    success_url = '/reg_ok/'

def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response
