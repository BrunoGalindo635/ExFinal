from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse
from .models import publicacion, comentario, datosUsuario
import json
import base64
from django.contrib.auth.models import User


def ingresoUsuario(request):
    if request.method == 'POST':
        nombreUsuario = request.POST.get('nombreUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        usrObj = authenticate(request,username=nombreUsuario, password=contraUsuario)
        if usrObj is not None:
            login(request,usrObj)
            return HttpResponseRedirect(reverse('app3:informacionUsuario'))
        else:
            return HttpResponseRedirect(reverse('app3:ingresoUsuario'))
    return render(request,'ingresoUsuario.html')

##@login_required(login_url='/')
def informacionUsuario(request):
    return render(request,'informacionUsuario.html',{
        'allPubs':publicacion.objects.all()
    })


##@login_required(login_url='/')
def cerrarSesion(request):
    logout(request)
    return render(request,'ingresoUsuario.html')

def ejemploJs(request):
    return render(request,'ejemploJs.html')

def devolverDatos(request):
    return JsonResponse(
        {
            'nombreCurso':'DesarroloWebPython',
            'horario':{
                'martes':'7-10',
                'jueves':'7-10'
            },
            'backend':'django',
            'frontend':'reactjs',
            'cantHoras':24
        }
    )

def devolverAllPubs(request):
    objPub = publicacion.objects.all()
    listaPublicacion = []
    for obj in objPub:
        listaPublicacion.append(
            {
                'titulo':obj.titulo,
                'descripcion':obj.descripcion
            }
        )
    return JsonResponse({
        'listaPublicacion':listaPublicacion
    })

def devolverPublicacion(request):
    idPub = request.GET.get('idPub')
    try:
        datosComentarios = []
        objPub = publicacion.objects.get(id=idPub)
        comentariosPub = objPub.comentario_set.all()
        for comentarioInfo in comentariosPub:
            datosComentarios.append({
                'autor': f"{comentarioInfo.autoCom.first_name} {comentarioInfo.autoCom.last_name}",
                'descripcion': comentarioInfo.descripcion
            })
        try:
            with open(objPub.imagenPub.path,'rb') as imgFile:
                imgPub = base64.b64encode(imgFile.read()).decode('UTF-8')
        except:
            imgPub = None

        return JsonResponse({
            'titulo': objPub.titulo,
            'autor':f"{objPub.autorPub.first_name} {objPub.autorPub.last_name}",
            'descripcion':objPub.descripcion,
            'datosComentarios': datosComentarios,
            'imgPub':imgPub
        })
    except:
        return JsonResponse({
            'titulo':'SIN DATOS',
            'autor':'SIN DATOS',
            'descripcion':'SIN DATOS',
            'datosComentarios':None,
            'imgPub':None
        })
    
def publicarComentario(request):
    datosComentario = json.load(request)
    print(datosComentario)
    comentarioTexto = datosComentario.get('comentario')
    idPublicacion = datosComentario.get('idPublicacion')
    objPublicacion = publicacion.objects.get(id=idPublicacion)
    comentario.objects.create(
        descripcion = comentarioTexto,
        pubRel = objPublicacion,
        autoCom = request.user
    )
    return JsonResponse({
        'resp':'ok'
    })

def crearPublicacion(request):
    if request.method == 'POST':
        tituloPub = request.POST.get('tituloPub')
        descripcionPub = request.POST.get('descripcionPub')
        autorPub = request.user
        imagenPub = request.FILES.get('imagenPub')

        publicacion.objects.create(
            titulo=tituloPub,
            descripcion=descripcionPub,
            autorPub = autorPub,
            imagenPub = imagenPub
        )

        return HttpResponseRedirect(reverse('app3:informacionUsuario'))
    
def inicioReact(request):
    return render(request, 'inicioReact.html')



"""
PREGUNTA 1 - B
CREAR EL IF QUE PERMITA RECONOCER EL MÉTODO DE LA PETICION:
IF REQUEST.METHOD == ....
DENTRO DE LA SELECTIVA CAPTURAR LOS DATOS DEL FORMULARIO : 
USERNAMEUSUARIO = REQUEST.POST.GET('USE ...
...

CREAR EL OBJETO USER CON USERNAME E EMAIL : 

OBJUSR = USER.OBJECTS.CREATE(
    USERNAME = ... ,
    EMAIL = ... 
)

LUEGO SETEAR LA CONTRASEÑA CON LA FUNCION SET_PASSWORD:
CONTRAUSUARIO = REQUEST.POST.GET('CONTRAUSUARIO')
OBJUSR.SET_PASSWORD(CONTRAUSUARIO) ...

FINALMENTE CREAR EL REGISTRO EN DATOSUSUARIO Y RELACIONARLO CON EL
OBJETO OBJUSR - RECORDAR LA RELACION ONE TO ONE Y COMO SE CREO
EL USUARIO EN LA CLASES 5 Y 6

FINALMENTE REDIRECCIONAR A LA MISMA RUTA DE CONSOLAADMINISTRADOR - return HttpResponseRedirect(reverse('app3:consolaAdministrador'))

EJEMPLO DE CREACION DE NUEVO USUARIO:

usernameUsuario = request.POST.get('usernameUsuario')
contraUsuario = request.POST.get('contraUsuario')
nombreUsuario = request.POST.get('nombreUsuario')
apellidoUsuario = request.POST.get('apellidoUsuario')
emailUsuario = request.POST.get('emailUsuario')
profesionUsuario = request.POST.get('profesionUsuario')
nroCelular = request.POST.get('nroCelular')
perfilUsuario = request.POST.get('perfilUsuario')

nuevoUsuario = User.objects.create(
    username=usernameUsuario,
    email=emailUsuario
)
nuevoUsuario.set_password(contraUsuario)
nuevoUsuario.first_name = nombreUsuario
nuevoUsuario.last_name = apellidoUsuario
nuevoUsuario.is_staff = True
nuevoUsuario.save()


datosUsuario.objects.create(
    profesion=profesionUsuario,
    nroCelular=nroCelular,
    perfilUsuario=perfilUsuario,
    usrRel=nuevoUsuario
)

"""
@login_required(login_url='/')
def consolaAdministrador(request):
    if request.method == 'POST':
        usernameUsuario = request.POST.get('username')
        contraUsuario = request.POST.get('contraUsuario')
        nombreUsuario = request.POST.get('nombreUsuario')
        apellidoUsuario = request.POST.get('apellidoUsuario')
        profesionUsuario = request.POST.get('profesionUsuario')
        emailUsuario = request.POST.get('emailUsuario')
        nroCelular = request.POST.get('nroCelular')
        perfilUsuario = request.POST.get('perfilUsuario')

        if User.objects.filter(username=usernameUsuario).exists():
            return render(request, 'consolaAdministrador.html', {
                'usuariosTotales': User.objects.all(),
                'error_message': 'El nombre de usuario ya está en uso.'
            })
        usuarioNuevo = User.objects.create(
            username=usernameUsuario,
            email=emailUsuario
        )
        usuarioNuevo.set_password(contraUsuario)
        usuarioNuevo.first_name = nombreUsuario
        usuarioNuevo.last_name = apellidoUsuario
        usuarioNuevo.is_staff = True  
        usuarioNuevo.save()

        datosUsuario.objects.create(
            usrRel=usuarioNuevo,
            nroCelular=nroCelular,
            profesion=profesionUsuario,
            perfilUsuario=perfilUsuario
        )
        
        return HttpResponseRedirect(reverse('app3:consolaAdministrador'))
    
    return render(request, 'consolaAdministrador.html', {
        'usuariosTotales': User.objects.all()
})


def obtenerDatosUsuario(request):
    idUsuario = request.GET.get('idUsuario')
    """
    Pregunta 3
    Esta funcion devolvera los campos que se necesitan 
    cargar en la ventana modal para poder ser editados
    Con el id del usuario se puede obtener el objeto y devolver
    el objeto Json con la informacion necesaria.
    """
    usuarioEditar = User.objects.get(id=idUsuario)
    usuarioExtendido = datosUsuario.objects.get(usrRel=usuarioEditar)

    return JsonResponse({
        'resp':'200',
        'idUsuario': usuarioEditar.id,
        'usernameUsuario': usuarioEditar.username,
        'nombreUsuario': usuarioEditar.first_name,
        'apellidoUsuario': usuarioEditar.last_name,
        'profesionUsuario': usuarioExtendido.profesion,
        'emailUsuario': usuarioEditar.email,
        'nroCelular': usuarioExtendido.nroCelular,
        'perfilUsuario': usuarioExtendido.perfilUsuario
     })

def actualizarUsuario(request):
    """
    Pregunta 5
    En esta funcion recibira los datos del formulario de actualizacion de usuario
    Debe capturar dichos datos, recuerde que en el input con atributo name idUsuario
    se ha cargado el id del usuario correspondiente lo que le permitira obtener el objeto
    de la base de datos. Con el objeto capturado modificar los campos respectivos y finalmente
    ejecutar el metodo save() para su respectiva actualizacion
    """
    if request.method == 'POST':
        nombreUsuarioDetalle = request.POST.get('nombreUsuarioDetalle')
        apellidoUsuarioDetalle = request.POST.get('apellidoUsuarioDetalle')
        profesionUsuarioDetalle = request.POST.get('profesionUsuarioDetalle')
        nroCelularDetalle = request.POST.get('nroCelularDetalle')
        perfilUsuarioDetalle = request.POST.get('perfilUsuarioDetalle')
        idUsuario = request.POST.get('idUsuario')
        usuarioEdit = User.objects.get(id=idUsuario)
        usuarioExt = datosUsuario.objects.get(usrRel=usuarioEdit)

        usuarioEdit.first_name = nombreUsuarioDetalle
        usuarioEdit.last_name = apellidoUsuarioDetalle
        usuarioEdit.save()
        usuarioExt.profesion = profesionUsuarioDetalle
        usuarioExt.nroCelular = nroCelularDetalle
        usuarioExt.perfilUsuario = perfilUsuarioDetalle
        usuarioExt.save()
    return HttpResponseRedirect(reverse('app3:consolaAdministrador'))