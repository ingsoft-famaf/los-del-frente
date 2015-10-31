from forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import views


class Register(CreateView):
    template_name = 'User/register.html'
    form_class = UserCreationForm
    success_url = '/reg_ok/'


