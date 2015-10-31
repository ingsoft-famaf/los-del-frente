from forms import UserForm
from django.views.generic import CreateView


class Register2(CreateView):
    template_name = 'User/register.html'
    form_class = UserForm
    success_url = '/reg_ok/'
