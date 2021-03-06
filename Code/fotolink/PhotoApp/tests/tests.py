from django.test import TestCase, Client
from django.contrib.auth.models import User
from PhotoApp.models import Place, Photo, Notification, Tag
from django.core.files import File


class PhotoAppTestCase(TestCase):
    """Tests para PhotoApp."""

    def setUp(self):
        """
        Configuracion inicial creo lugares y usuarios
        Agrego "Neuquen" y "Catamarca" a los lugares y creo admin (admin,admin)
        Creo usuario para iniciar sesion
        """
        self.place = Place.objects.create(placeName="Neuquen")
        self.place = Place.objects.create(placeName="Catamarca")
        self.adminuser = User.objects.create_superuser('admin',
                                                       'admin@test.com',
                                                       'admin')
        self.user = User.objects.create_user(username="matias1",
                                             email=None,
                                             password="matias1")

    def test_create_place_success(self):
        """
        Verificacion para crear un objeto place distinto a los existentes
        """
        self.place = Place.objects.create(placeName="Mendoza")
        self.assertEqual(len(Place.objects.filter(placeName="Mendoza")), 1)

    def test_create_photo_success(self):
        '''
        Verificacion para crear un objeto photo vinculado a "Neuquen"
        '''
        lenPhoto = len(Photo.objects.all())
        photo1 = Photo.objects.create(picture="./PhotoApp/tests/picture.jpg",
                                      date="2015-10-1",
                                      time="20:15",
                                      place=Place.objects.get
                                      (placeName="Neuquen"))
        self.assertEqual(lenPhoto + 1, len(Photo.objects.all()))

    def test_reg_place_success(self):
        """
        Verifico la creacion de "Buenos Aires" a traves de la red, via /admin/
        """
        cliente = Client()
        cliente.login(username="admin", password="admin")
        response = cliente.post('/admin/PhotoApp/place/add/',
                                {'placeName': 'Buenos Aires'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Place.objects.filter(placeName="Santa Cruz")), 0)

        response = cliente.post('/admin/PhotoApp/place/add/',
                                {'placeName': 'Buenos Aires'})
        self.assertEqual(response.status_code, 200)

    def test_reg_Photo_success(self):
        '''
        Verifico la creacion de una Photo con lugar = Neuquen mediante la red
        via /admin/
        '''
        cliente = Client()
        cliente.login(username="admin", password="admin")
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/admin/PhotoApp/photo/add/',
                                {'picture': pictureFile,
                                 'date': '2015-10-10',
                                 'time': '20:15',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 302)

    def test_reg_Photo_failed_badDateTime(self):
        '''
        Verifico la falla justificada de una creacion de foto por malos
        atributos seteados de fecha y hora
        '''
        cliente = Client()
        cliente.login(username="admin", password="admin")
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/admin/PhotoApp/photo/add/',
                                {'picture': pictureFile,
                                 'date': '2015-18-10',
                                 'time': '20:15',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 200)
        response = cliente.post('/admin/PhotoApp/photo/add/',
                                {'picture': pictureFile,
                                 'date': '2015-12-10',
                                 'time': '20:65',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 200)

    def test_reg_Photo_success_with_login(self):
        '''
        Verifico la subida de una foto por medio del entorno usuario con login
        '''
        cliente = Client()
        cliente.login(username="matias1", password="matias1")
        # Subo una foto de Neuquen
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2015-10-10',
                                 'time': '20:15',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 302)
        response = cliente.get("/%2Fphotos/1")
        self.assertEqual(response.status_code, 301)

    def test_reg_Photo_failed_badDateTime_with_login(self):
        '''
        Verifico la falla justificada de una creacion de foto por malos
        atributos seteados de fecha y hora con login propio
        '''
        cliente = Client()
        cliente.login(username="matias1", password="matias1")
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2015-15-10',
                                 'time': '20:10',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 200)
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2015-10-10',
                                 'time': '20:98',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Enter a valid time" in str(response))

    def test_reg_Photo_failed_badFile_with_login(self):
        '''
        Verifico la falla justificada de una creacion de foto por malos
        atributos seteados de fecha y hora con login propio
        '''
        cliente = Client()
        cliente.login(username="matias1", password="matias1")
        pictureFile = File(open("./PhotoApp/tests/picture.pdf"))
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2015-15-10',
                                 'time': '20:10',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 200)

    def test_get_photoList_success(self):
        '''
        Creo 2 fotos y obtengo la lista de fotos
        '''
        cliente = Client()
        cliente.login(username="matias1", password="matias1")
        # Subo una foto de Neuquen
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2015-10-10',
                                 'time': '20:15',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 302)
        response = cliente.get("/%2Fphotos/1")
        self.assertEqual(response.status_code, 301)
        # Subo una foto de Catamarca
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2014-10-10',
                                 'time': '00:15',
                                 'place': Place.objects.get
                                 (placeName='Catamarca')})
        self.assertEqual(response.status_code, 302)
        response = cliente.get("/%2Fphotos/2")
        self.assertEqual(response.status_code, 301)
        # Obtengo photolist
        response = cliente.get('/photos/')
        # Me fijo si estan mis fotos
        for foto in response.context['photo_list']:
            self.assertTrue(foto.place_id == 'Neuquen' or
                            foto.place_id == 'Catamarca')

    def test_get_photoList_filtered_success(self):
        '''
        Creo 2 fotos, una en Neuquen, otra en Catamarca;
        quiero ver solo la de Neuquen
        '''
        cliente = Client()
        cliente.login(username="matias1", password="matias1")
        # Subo una foto de Neuquen
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2015-10-10',
                                 'time': '20:15',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 302)
        response = cliente.get("/%2Fphotos/1")
        self.assertEqual(response.status_code, 301)
        # Subo una foto de Catamarca
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/upload/',
                                {'picture': pictureFile,
                                 'date': '2014-10-10',
                                 'time': '00:15',
                                 'place': Place.objects.get
                                 (placeName='Catamarca')})
        self.assertEqual(response.status_code, 302)
        response = cliente.get("/%2Fphotos/2")
        self.assertEqual(response.status_code, 301)
        # Obtengo photolist
        response = cliente.get('/photos/')
        # Filtro solo Neuquen
        response = cliente.get('/photos/?csrfmiddlewaretoken=fSuRgFpRXVPd7OsA'
                               'Vpsc6tnFBWo9bokb&place=neu&year=&mon'
                               'th=&day=&time=&submit=Filter')
        for foto in response.context['photo_list']:
            self.assertTrue(foto.place_id == 'Neuquen')
            self.assertFalse(foto.place_id == 'Catamarca')


class NotificationTagTestCase(TestCase):
    """
    Notification testing.
    """
    def setUp(self):
        """
        Configuracion inicial creo lugares y usuarios
        Agrego "Neuquen" y "Catamarca" a los lugares y creo admin (admin,admin)
        Creo usuario para iniciar sesion
        """
        self.place = Place.objects.create(placeName="Neuquen")
        self.place = Place.objects.create(placeName="Catamarca")
        self.adminuser = User.objects.create_superuser('admin',
                                                       'admin@test.com',
                                                       'admin')
        self.user = User.objects.create_user(username="matias1",
                                             email=None,
                                             password="matias1")

    def test_welcome_notification(self):
        """
        Registrar un nuevo usuario y chequear creacion automatica de
        notificacion de bienvenida
        """
        cliente = Client()
        response = cliente.post('/register/', {'username': 'locotito',
                                'password1': 'lala', 'password2': 'lala'})
        actualUser = User.objects.get(username='locotito')
        welcomeNoti = Notification.objects.get(receiver=actualUser)
        self.assertTrue("Bienvenido" in str(welcomeNoti))
        self.assertEqual(response.status_code, 302)

    def test_Photo_Tag(self):
        '''
        Creo una photo, me etiqueto como usuario 'admin'.
        Reviso no tener notificaciones de tipo TAG como 'admin'
        Me etiqueto como usuario 'matias1'
        Reviso las notificaciones de 'admin' y encuentro una de tipo TAG
        '''
        cliente = Client()
        cliente.login(username="admin", password="admin")
        pictureFile = File(open("./PhotoApp/tests/picture.jpg"))
        response = cliente.post('/admin/PhotoApp/photo/add/',
                                {'picture': pictureFile,
                                 'date': '2015-10-10',
                                 'time': '20:15',
                                 'place': Place.objects.get
                                 (placeName='Neuquen')})
        self.assertEqual(response.status_code, 302)
        response = cliente.get('/%2Fphotos/1/')
        self.assertTrue("Neuquen" in str(response))
        # response = cliente.get("/tagajax?photo_id=1&x=500&y=100")
        # self.assertTrue("OK" in str(response))
        response = cliente.get('/notification')
        self.assertTrue("admin" in str(response))
        self.assertFalse("tag" in str(response))
        cliente.logout()
        cliente = Client()
        cliente.login(username="matias1", password="matias1")
        response = cliente.get('/%2Fphotos/1/')
        self.assertTrue("Neuquen" in str(response))
        # response = cliente.get("/tagajax?photo_id=1&x=500&y=100")
        # self.assertTrue("OK" in str(response))
        response = cliente.get('/notification')
        self.assertTrue("matias1" in str(response))
        cliente.logout()
        cliente = Client()
        cliente.login(username="admin", password="admin")
        response = cliente.get('/notification')
        # self.assertTrue("tag" in str(response))
