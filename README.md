Fotolink
========

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ingsoft-famaf/los-del-frente?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

### Resumen 

Fotolink consiste en un sistema capaz de conectar a personas que estuvieron 
presentes en un lugar a una determinada hora. 

### Descripción 

Consiste en un sistema web con gestión de usuarios. Un usuario podrá registrarse
 en el sitio sin la aprobación de ningún moderador. Al registrarse deberá 
proveer datos personales, nombre de usuario y contraseña. También podrá 
seleccionar una foto utilizada como Avatar.

Para poder utilizar el sistema el usuario deberá autenticarse con las 
credenciales definidas en el proceso de registro. Una vez autenticado, el 
usuario puede subir fotos, buscar fotos o modificar datos personales. Los datos 
personales del usuario podrán ser definidos como públicos o privados. Cualquier 
usuario puede ver el perfil público de otro usuario. Solamente aquellos usuarios
 que hayan formado un vínculo de amistad podrán acceder a los datos de perfil 
privado. 

Cuando un usuario seleccione “buscar fotos”, le debe suministrar al sistema 
datos acerca de criterios de búsqueda: lugar, fecha, “fotos en las que estoy 
etiquetado” serán criterios válidos. El sistema mostrará al usuario las fotos 
que cumplan con los criterios de búsqueda (si hay alguna). Cuando el usuario se 
encuentre visualizando una foto, podrá si lo desea etiquetarse en la misma. 
Al etiquetarse, el sistema enviará notificaciones a todos lo usuarios 
previamente etiquetados en dicha foto. Si el usuario lo desea, podrá a través 
de las etiquetas ver perfil público o bien enviar una solicitud de amistad. 
La solicitud de amistad disparará un tipo especial de notificación, que deberá 
ser confirmada para que se establezca el vínculo. Una vez establecido el 
vínculo, los usuarios en dicha amistad podrán consultarse el perfil privado 
entre sí.

En la opción subir fotos, el usuario proveerá al sistema una foto y deberá 
completar datos de la misma: nombre, lugar, fecha y hora. Tendrá la opción de 
auto­etiquetarse en la misma antes de cumplir con el proceso de carga. El 
sistema realizará validaciones mínimas sobre las fotos en correlación con los 
datos: fecha y hora, lugar válido (opcional). Una vez que el usuario suba la 
foto, la misma pertenecerá al sistema fotolink y el usuario ya no podrá borrar 
la foto.

En el sistema habrá usuarios especiales (que podrán realizar las mismas acciones
 que cualquier usuario) con permisos de administrador, que serán capaces de 
borrar fotos que consideren inapropiadas. Los usuarios con permisos de 
administrador serán definidos por el web administrator.

[+Modificar documentacion](https://www.draw.io/#G0B2VNcg_DK-gkbml1TEpRcGpkdlk)

### IMPORTANTE:
* Instalar libreria *python-dev*

    `$ sudo apt-get install python-dev`

### Instrucciones para usar entorno virtual

* Crear environment

    `$ virtualenv env`

* Activar environment

    `$ source env/bin/activate`

* Instalar requerimientos de *requirements.txt*

    `$ pip install -r requirements.txt`

* Para salir del env

    `$ deactivate`

### Instrucciones para trabajar en branch por issue

* Una vez clonado el documento crear un branch nuevo e ingresar

    `$ git checkout -b newBranch`

* Luego de hacer las modificaciones... 
 
    `$ git add ...` y `$ git commit ...` 

* ...hacer primer push en nuestra rama 

    `$ git push -u origin newBranch`

* Cuando el trabajo este listo para ser verificado realizar **pull-request** online y esperar la verificacion de los compañeros luego hacer **merge** online

### Instrucciones para correr tests de PhotoApp

    `$ python manage test PhotoApp/tests
