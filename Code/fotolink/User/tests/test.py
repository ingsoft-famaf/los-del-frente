from django.test import TestCase, Client
from User.models import Perfil, User
from django.core.files import File

""" Pegandole al Register """


class RegistrationTestCase(TestCase):

    """ Registrar un nuevo usuario """
    def test_reg_success(self):
        cliente = Client()
        response = cliente.post('/register/', {'username': 'locotito',
                                'password1': 'lala', 'password2': 'lala'})
        """ Si esta todo OK, debiera ser redirigido(HTTP 302) """
        self.assertEqual(response.status_code, 302)

    """ Me olvide de poner nombre y password"""
    def test_name_and_psw_missing(self):
        cliente = Client()
        response = cliente.post('/register/', {})
        """ Todo OK, pero te muestra la misma pagina(HTTP 200) """
        self.assertEqual(response.status_code, 200)


""" Pegandole al login """


class LoginTestCase(TestCase):

    """ loguearse como locotito, a quien registro antes """
    def test_login_success(self):
        cliente = Client()
        response = cliente.post('/register/', {'username': 'locotito',
                                'password1': 'lala', 'password2': 'lala'})
        response = cliente.post('/login/', {'username': 'locotito',
                                'password': 'lala'})
        """ Si esta todo OK, debiera ser redirigido(HTTP 302) """
        self.assertEqual(response.status_code, 302)

    """ Me olvide de poner el nombre de usuario """
    def test_login_name_missing(self):
        cliente = Client()
        response = cliente.post('/login/', {'password': 'lala'})
        """ Todo OK, pero te muestra la misma pagina(HTTP 200) """
        self.assertEqual(response.status_code, 200)

    """ El usuario no existe """
    def test_login_not_such_user(self):
        cliente = Client()
        response = cliente.post('/login/', {'username': 'chaclacayo',
                                'password': 'lala'})
        """ Todo OK, pero te muestra la misma pagina(HTTP 200) """
        self.assertEqual(response.status_code, 200)


class EditProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="dummy",
                                             email=None,
                                             password="dummy")
        self.cliente = Client()
        self.cliente.login(username="dummy", password="dummy")

    def test_edit_charFields(self):
        response = self.cliente.post('/accounts/profile/edit/', {'nombre':
                                     'alfredo',
                                     'residencia': 'Siempre Viva 23'})
        self.assertEqual(response.status_code, 302)
        dbuser = User.objects.get(username="dummy")
        nomb = dbuser.perfil.nombre
        residencia = dbuser.perfil.residencia
        self.assertEqual(nomb, 'alfredo')
        self.assertEqual(residencia, 'Siempre Viva 23')

    def test_edit_BoolFields(self):
        response = self.cliente.post('/accounts/profile/edit/',
                                     {'edad_privacidad': True,
                                      'residencia_privacidad': False,
                                      'mail_privacidad': True,
                                      'facebook_privacidad': False,
                                      'web_privacidad': True})
        self.assertEqual(response.status_code, 302)
        dbuser = User.objects.get(username="dummy")
        edad = dbuser.perfil.edad_privacidad
        residencia = dbuser.perfil.residencia_privacidad
        mail = dbuser.perfil.mail_privacidad
        facebook = dbuser.perfil.facebook_privacidad
        web = dbuser.perfil.web_privacidad
        self.assertEqual(edad, True)
        self.assertEqual(mail, True)
        self.assertEqual(web, True)
        self.assertEqual(residencia, False)
        self.assertEqual(facebook, False)

    def test_chage_profile_picture(self):
        pictureFile = File(open("./User/tests/picture.jpg"))
        response = self.cliente.post('/accounts/profile/edit/',
                                     {'avatar': pictureFile})
        self.assertEqual(response.status_code, 302)
