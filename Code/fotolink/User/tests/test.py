from django.test import TestCase, Client
from User.models import Perfil, User, Friendship
from django.core.files import File


class RegistrationTestCase(TestCase):
    """
    Registration Testing
    """
    def setUp(self):
        """
        Configuracion inicial creo usuarios y perfiles
        """
        self.user = User.objects.create_user(username="user",
                                             email=None,
                                             password="user")
        self.user2 = User.objects.create_user(username="user2",
                                              email=None,
                                              password="user2")
        self.adminuser = User.objects.create_superuser('admin',
                                                       'admin@test.com',
                                                       'admin')
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.perfil2 = Perfil.objects.get(usuario=self.user2)

    def test_reg_success(self):
        """
        Registrar un nuevo usuario y chequear su existencia
        """
        cliente = Client()
        response = cliente.post('/register/', {'username': 'locotito',
                                'password1': 'lala', 'password2': 'lala'})
        User.objects.get(username='locotito')
        self.assertEqual(response.status_code, 302)

    def test_name_and_psw_missing(self):
        """
        Me olvide de poner nombre y password deberia mostrar mensaje de
        error
        """
        cliente = Client()
        response = cliente.post('/register/', {})
        self.assertTrue('This field is required' in
                        str(response.context['form']))
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):
    """
    Login testing
    """
    def setUp(self):
        """
        Configuracion inicial creo usuarios y perfiles
        """
        self.user = User.objects.create_user(username="user",
                                             email=None,
                                             password="user")
        self.user2 = User.objects.create_user(username="user2",
                                              email=None,
                                              password="user2")
        self.adminuser = User.objects.create_superuser('admin',
                                                       'admin@test.com',
                                                       'admin')
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.perfil2 = Perfil.objects.get(usuario=self.user2)

    def test_login_success(self):
        """
        loguearse como 'user', a quien registre antes
        """
        cliente = Client()
        response = cliente.post('/login/', {'username': 'user',
                                'password': 'user'})
        self.assertEqual(response.status_code, 302)

    def test_login_name_missing(self):
        """
        Me olvide de poner el nombre de usuario
        """
        cliente = Client()
        response = cliente.post('/login/', {'password': 'lala'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("This is an error" in str(response))

    def test_login_not_such_user(self):
        """
        El usuario no existe
        """
        cliente = Client()
        response = cliente.post('/login/', {'username': 'chaclacayo',
                                'password': 'lala'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("This is an error" in str(response))


class EditProfileTestCase(TestCase):
    """
    Edit profile testing.
    """
    def setUp(self):
        """
        Configuracion inicial creo usuarios y perfiles
        """
        self.user = User.objects.create_user(username="user",
                                             email=None,
                                             password="user")
        self.user2 = User.objects.create_user(username="user2",
                                              email=None,
                                              password="user2")
        self.adminuser = User.objects.create_superuser('admin',
                                                       'admin@test.com',
                                                       'admin')
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.perfil2 = Perfil.objects.get(usuario=self.user2)
        self.cliente = Client()
        self.cliente.login(username="user", password="user")

    def test_edit_charFields(self):
        """
        Chequeo que cambien los parametros CharFields
        """
        datos = {'nombre': 'alfredo', 'residencia': 'Siempre Viva 23'}

        response = self.cliente.post('/accounts/profile/edit/', datos)

        self.assertEqual(response.status_code, 302)
        dbuser = User.objects.get(username="user")
        nomb = dbuser.perfil.nombre
        residencia = dbuser.perfil.residencia
        self.assertEqual(nomb, 'alfredo')
        self.assertEqual(residencia, 'Siempre Viva 23')

    def test_edit_BoolFields(self):
        """
        Chequeo que cambien los parametros BoolFields
        """
        response = self.cliente.post('/accounts/profile/edit/',
                                     {'edad_privacidad': True,
                                      'residencia_privacidad': False,
                                      'mail_privacidad': True,
                                      'facebook_privacidad': False,
                                      'web_privacidad': True})
        self.assertEqual(response.status_code, 302)
        dbuser = User.objects.get(username="user")
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
        """
        Chequeo cambiar mi foto de perfil
        """
        pictureFile = File(open("./User/tests/picture.jpg"))
        response = self.cliente.post('/accounts/profile/edit/',
                                     {'avatar': pictureFile})
        self.assertEqual(response.status_code, 302)


class FriendsProfileTestCase(TestCase):
    """
    Edit profile testing.
    """
    def setUp(self):
        """
        Configuracion inicial creo usuarios y perfiles
        """
        self.user = User.objects.create_user(username="user",
                                             email=None,
                                             password="user")
        self.user2 = User.objects.create_user(username="user2",
                                              email=None,
                                              password="user2")
        self.adminuser = User.objects.create_superuser('admin',
                                                       'admin@test.com',
                                                       'admin')
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.perfil2 = Perfil.objects.get(usuario=self.user2)
        self.perfilAdmin = Perfil.objects.get(usuario=self.adminuser)
        self.friendship = Friendship.objects.create(to_user=self.user,
                                                    from_user=self.user2)

    def test_check_friendship(self):
        """
        Chequeo que exista la relacion creada antes.
        """
        self.cliente = Client()
        self.cliente.login(username="user", password="user")
        fs = Friendship.objects.get(to_user=self.user)
        self.assertEqual(fs.from_user, self.user2)

    def test_view_friend_empty_profile(self):
        """
        Chequeo mensaje en perfil vacio de amigo
        """
        self.cliente = Client()
        self.cliente.login(username="user", password="user")
        response = self.cliente.get('/accounts/2/')
        self.assertTrue("Dont have profile data yet" in str(response))

    def test_view_public_profile(self):
        """
        Agrego datos privados al perfil de admin
        Chequeo vista publica de perfil de no amigo
        """
        self.cliente = Client()
        self.cliente.login(username="admin", password="admin")
        response = self.cliente.post('/accounts/profile/edit/',
                                     {'nombre': "Administrador",
                                      'residencia': "Lugar",
                                      'edad': "12",
                                      'residencia_privacidad': True,
                                      'edad_privacidad': False})
        self.assertEqual(response.status_code, 302)
        self.cliente.logout()
        self.cliente.login(username="user", password="user")
        response = self.cliente.get('/accounts/3/')
        self.assertTrue("'s public profile" in str(response))
        self.assertTrue("are not friends yet" in str(response))
        self.assertTrue("Lugar" in str(response))
        self.assertFalse("Edad" in str(response))

    def test_view_friend_profile(self):
        """
        Agrego datos a user2 y chequeo el muestreo para amigos
        """
        self.cliente = Client()
        self.cliente.login(username="user2", password="user2")
        response = self.cliente.post('/accounts/profile/edit/',
                                     {'nombre': "Amigo",
                                      'residencia': "Lugar",
                                      'edad': "12"})
        self.assertEqual(response.status_code, 302)
        self.cliente.logout()
        self.cliente.login(username="user", password="user")
        response = self.cliente.get('/accounts/2/')
        self.assertTrue("Amigo" in str(response))
        self.assertTrue("Lugar" in str(response))
        self.assertTrue("12" in str(response))
