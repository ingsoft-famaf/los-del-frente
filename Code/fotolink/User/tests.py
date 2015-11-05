from django.test import TestCase, Client

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
