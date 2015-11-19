from django.views.generic import ListView, CreateView
from django.views.generic import DetailView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from .forms import PhotoForm
from .models import Photo, Place, Notification, Tag



def tagsAjax(request):
    getDict = dict(request.GET.iterlists()) 
    photo_id = int(getDict['photo_id'][0])
    photoInstance = Photo.objects.get(pk=photo_id)
    tags_anteriores = Tag.objects.all().filter(photo = photoInstance)
    response = {'result':'error'}
    if getDict['action'][0] == "add":
        x = int(getDict['x'][0])
        y = int(getDict['y'][0])                
        oldtag = tags_anteriores.filter(user = request.user)

        if len(oldtag) == 0:
            tag = Tag(photo=photoInstance, user=request.user, x_pos=x, y_pos=y)
            tag.save()
        else:
            oldtag[0].x_pos= x
            oldtag[0].y_pos= y
            oldtag[0].save()

        for each in tags_anteriores:
            if each.user != request.user:
                notification = Notification(sender=request.user,receiver=each.user,
                                            tagged_photo=photoInstance,
                                            notif_type='tag')
                notification.save() 
        response = {'result':'OK'}              
    elif getDict['action'][0] == "getlist":  
        response = {'tags':[]}                        
        for each in tags_anteriores:
            response['tags'].append({
                'x':each.x_pos,
                'y':each.y_pos,
                'user':each.user.username
            })
    elif getDict['action'][0] == "remove":                
        tags_anteriores.filter(user = request.user).delete()
        response = {'result':'OK'}
    return JsonResponse(response)

def notifications(request):
    allNotis = Notification.objects.get_queryset()
    notiForUser = allNotis.filter(receiver = request.user)
    if request.GET.get('action') == "all_seen":
        for each in notiForUser:
            each.seen = True
            each.save()
        return JsonResponse({'status':'OK'})
    else:
        notisJson = {'notif_list':[], 'me':request.user.username}
        for each in notiForUser:
            data = {
                'id':each.pk, 
                'time':each.dateTime, 
                'text': each.text , 
                'sender': str(each.sender),                 
                'type': each.notif_type,
                'seen': each.seen,
            }            
            if each.sender:
                data['sender_id'] = each.sender.pk
            if each.tagged_photo:
                data['tagged_photo_id'] = each.tagged_photo.pk
            notisJson['notif_list'].append(data)
        return JsonResponse(notisJson)


class CancelUpload(DeleteView):
    """
    Preview de upload con posibilidad de cancelar
    """
    model = Photo
    template_name = 'PhotoApp/cancel_upload.html'
    success_url = '/upload/'


class PhotoDelete(DeleteView):
    """
    Vista de eliminacion de una foto para uso de django. Hereda de
    django.views.generic.DeleteView
    """
    model = Photo
    template_name = 'PhotoApp/photo_delete.html'
    success_url = '/photos/'


class PhotoDetail(DetailView):
    """
    Vista de detalle de una foto para uso de django.Requiere login previo.
    Hereda de django.views.generic.DetailView
    """
    model = Photo
    template_name = 'PhotoApp/photo_detail.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class PhotoUpload(CreateView):
    """
    Vista para subir una nueva foto, para uso de django. Requiere login previo.
    Hereda de django.views.generic.CreateView
    """
    template_name = 'PhotoApp/photo_form.html'
    form_class = PhotoForm

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Retorna un html para confirmar el subir una foto dado un primarykey
        """
        return reverse('photos:cancelupload', kwargs={'pk': self.object.pk})


class PhotoList(ListView):
    """
    Vista para listar fotos disponibles, para uso de django. Requiere login
    previo. Hereda de django.views.generic.ListView
    """
    model = Photo
    template_name = 'PhotoApp/photo_list.html'
    paginate_by = 8

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Retorna el contexto de todas las fotos en PhotoList
        """
        context = super(PhotoList, self).get_context_data()
        return context

    def get_queryset(self):
        '''
        Filtra segun el formulario enviado por el usuario y retorna una lista
        de objetos con las caracteristicas adecuadas.
        '''
        qPlace = self.request.GET.get('place', '')
        qTime = self.request.GET.get('time', '')
        qYear = self.request.GET.get('year', '')
        qMonth = self.request.GET.get('month', '')
        qDay = self.request.GET.get('day', '')
        qset = super(PhotoList, self).get_queryset()
        if qTime != "":
            qset = qset.filter(time__startswith=qTime)
        if qYear != "":
            qset = qset.filter(date__year=qYear)
        if qMonth != "":
            qset = qset.filter(date__month=qMonth)
        if qDay != "":
            qset = qset.filter(date__day=qDay)
        if qPlace != "":
            qset = qset.filter(place__placeName__startswith=qPlace)
        return qset
