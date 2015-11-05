from django.test import TestCase, Client
from django.contrib.auth.models import User
from PhotoApp.models import Place, Photo



class PhotoAppTestCase(TestCase):
    """Tests para model de PhotoApp."""

    def setUp(self):
        """
        Configuracion inicial creo lugares y usuarios
        """
        self.place = Place.objects.create(placeName="Neuquen")
        self.adminuser = User.objects.create_superuser('admin', 'admin@test.com', 'admin')

    def test_create_place_success(self):
        """
        Verificacion para crear un objeto place distinto a los existentes
        """
        self.place = Place.objects.create(placeName="Mendoza")
        self.assertEqual(len(Place.objects.filter(placeName="Mendoza")), 1)

    def test_reg_place_success(self):
        """
        Si esta todo OK, debiera ser redirigido(HTTP 302)
        No existe ningun elemento Santa Cruz
        """
        cliente = Client()
        cliente.login(username="admin", password="admin")
        response = cliente.post('/admin/PhotoApp/place/add/',
                                {'placeName': 'Buenos Aires',})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Place.objects.filter(placeName="Santa Cruz")), 0)

        response = cliente.post('/admin/PhotoApp/place/add/',
                                {'placeName': 'Buenos Aires',})
        self.assertEqual(response.status_code, 200)

'''
    def test_reg_Photo_success(self):
        cliente = Client()
        cliente.login(username="admin", password="admin")
        response = cliente.post('/admin/PhotoApp/photo/add/',
                                {'Picture': 'picture.jpg',
                                 'Date': '2015-10-10',
                                 'Time': '20:15',
                                 'Place': Place.objects.get(placeName='Neuquen').pk})
        self.assertEqual(response.status_code, 302)

    def test_reg_Photo_failed_placeNotFound(self):
        cliente = Client()
        cliente.login(username="admin", password="admin")
        response = cliente.post('/admin/PhotoApp/photo/add/',
                                {'Picture': 'picture.jpg',
                                 'Date': '2015-10-10',
                                 'Time': '20:15',
                                 'Place': 'as'})
        self.assertEqual(response.status_code, 200)
'''

