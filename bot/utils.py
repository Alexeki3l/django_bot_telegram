from tienda.models import Producto
import requests
import os

def All_Products():
    content = " "
    try:
        if Producto.objects.count():
            for producto in Producto.objects.all():
                content += "Nombre: "+str(producto.nombre)+"\n"+"Precio: "+str(producto.precio)+"\n"+"Descripcion: "+str(producto.descripcion)+"\n"+"########\n"
                print(content)
        else:
            content = "Lo sentimos. Ahora mismo no tenemos nada que ofertarle."

    except:
        print("no pincha")
        
    return content


def get_image(folder_name, url_image):

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language":"en",
    }

    # Obtengo la imagen de dicha url_image  
    imagen = requests.get(url_image, headers).content
    # Obtengo el mismo nombre de la imagen de la URL para descargarla con el mismo nombre
    name = url_image.split('/')
    name = name[-1]
    name = name[:-4]
    print("Nombre de la imagen:",name)
    # Obtengo la ruta del projecto para guardar las imagenes
    # ruta = os.path.dirname(__file__)
    # ruta = ruta.split("\bot")
    # ruta = ruta[0]
    ruta = "D:\Alexei-Todo\Python\Estacion de Trabajo\Proyectos_Django\django_telebot"
    ruta = os.path.join(ruta, 'media')
    ruta = ruta + folder_name
    print(ruta)
    # Creo una carpeta en caso de no existir en dicha ruta para guardar las imagenes.
    if not os.path.exists(ruta):
        os.mkdir(ruta)
        fullname = ruta + "/" + name
        open(fullname +'.jpg', 'wb').write(imagen)
        print('descargando:{}.jpg'.format(name))
    else:
        # list_archivos = os.listdir(ruta)
        # if name in list_archivos:
        #     print("Ya existe este archivo")
        # else:
            fullname = ruta + "/" + name
    
            open(fullname +'.jpg', 'wb').write(imagen)
            print('descargando:{}.jpg'.format(name))

    folder_name=folder_name
    # Retorno la ruta de la imagen apartir de la carpeta creada con nombre del Item para DJANGO la encuentre
    return folder_name + "/" + "{}.jpg".format(name)
            

