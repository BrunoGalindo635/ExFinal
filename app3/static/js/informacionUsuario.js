
function cargarPub(idPub)
{
    fetch(`/devolverPublicacion?idPub=${idPub}`)
    .then(response => response.json())
    .then(data => {
        tituloPub = document.getElementById('tituloPub')
        autorPub = document.getElementById('autorPub')
        descripcionPub = document.getElementById('descripcionPub')
        idPublicacion = document.getElementById('idPublicacion')
        comentariosTotales = document.getElementById('comentariosTotales')

        imagenPub = document.getElementById('imagenPub')

        if(data.imgPub !== null)
        {
            imagenPub.src = `data:image/jpeg;base64,${data.imgPub}`
            imagenPub.style.display = 'block'
        }
        else
        {
            imagenPub.style.display = 'none'
        }

        tituloPub.value = ''
        autorPub.value = ''
        descripcionPub.value = ''
        idPublicacion.innerHTML = ''
        comentariosTotales.innerHTML = ''

        tituloPub.value = data.titulo
        autorPub.value = data.autor
        descripcionPub.value = data.descripcion
        idPublicacion.innerHTML = String(idPub)

        for(let j = 0; j < data.datosComentarios.length; j++)
        {
            seccionComentario = `
            <div class="row mb-3">
                <div class="col-3">
                    ${data.datosComentarios[j].autor}
                </div>
                <div class="col-9">
                    ${data.datosComentarios[j].descripcion}
                </div>
            </div>
            `
            comentariosTotales.innerHTML = comentariosTotales.innerHTML + seccionComentario
        }
    })
}

function enviarComentario()
{
    comentarioUsuario = document.getElementById('comentarioUsuario')
    idPublicacion = document.getElementById('idPublicacion')

    datos = {
        'comentario':comentarioUsuario.value,
        'idPublicacion': idPublicacion.innerHTML
    }

    fetch('/publicarComentario',
    {
        method:"POST",
        headers:
        {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body:JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('comentarioUsuario').value = ''
        cargarPub(idPublicacion.innerHTML)
    })
}

function getCookie(name)
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== "")
    {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++)
        {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "="))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function cargarInformacionUsuario(idUsuario)
{
    /*
    PREGUNTA 4
    DESARROLLAR LA FUNCION DE JAVASCRIPT QUE PERMITA CONSULTAR LA RUTA 
    OBTENERDATOSUSUARIO?IDUSUARIO=${IDUSUARIO}

    REVISAR LA IMPLEMENTACION REALIZADA PARA EDITAR MOSTRAR PUBLICACIONES

    TENER EN CUENTA EL INPUT QUE ESTA OCULTO Y CARGAR AHI EL ID DEL USUARIO
    PARA PODER ENVIARLO AL SERVIDOR COMO PARTE DE LOS DATOS Y ASI PODER
    RECUPERAR EL OBJETO USUARIO Y ACTUALIZAR LOS DATOS
    */
    console.log("Se cargara la informacion del usuario %s",idUsuario)
    fetch(`/obtenerDatosUsuario?idUsuario=${idUsuario}`)
    .then(response => response.json())
    .then(data => {
        usernameUsuarioDetalle = document.getElementById('usernameUsuarioDetalle')
        nombreUsuarioDetalle = document.getElementById('nombreUsuarioDetalle')
        apellidoUsuarioDetalle = document.getElementById('apellidoUsuarioDetalle')
        profesionUsuarioDetalle = document.getElementById('profesionUsuarioDetalle')
        emailUsuarioDetalle = document.getElementById('emailUsuarioDetalle')
        perfilUsuarioDetalle = document.getElementById('perfilUsuarioDetalle')
        nroCelularDetalle = document.getElementById('nroCelularDetalle')
        idUsuarioDetalle = document.getElementById('idUsuario')

        usernameUsuarioDetalle.value = ''
        nombreUsuarioDetalle.value = ''
        apellidoUsuarioDetalle.value = ''
        profesionUsuarioDetalle.value = ''
        emailUsuarioDetalle.value = ''
        perfilUsuarioDetalle.value = ''
        nroCelularDetalle.value = ''
        idUsuarioDetalle.value = ''
        
        usernameUsuarioDetalle.value = data.usernameUsuario
        nombreUsuarioDetalle.value = data.nombreUsuario
        apellidoUsuarioDetalle.value = data.apellidoUsuario
        profesionUsuarioDetalle.value = data.profesionUsuario
        emailUsuarioDetalle.value = data.emailUsuario
        perfilUsuarioDetalle.value = data.perfilUsuario
        nroCelularDetalle.value = data.nroCelular
        idUsuarioDetalle.value = data.idUsuario

    })
}