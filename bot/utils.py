from business.models import Product
import requests
import cv2
import os


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
    ruta = os.path.dirname(__file__)
    ruta = ruta[:-3]
    print(ruta)
    
    ruta = os.path.join(ruta, 'media')
    ruta_folder = ruta+ folder_name
    print(ruta)
    # Creo una carpeta en caso de no existir en dicha ruta para guardar las imagenes.
    if not os.path.exists(ruta_folder):
        os.mkdir(ruta_folder)
        fullname = ruta_folder + "/" + name
        open(fullname +'.jpg', 'wb').write(imagen)
        print('descargando:{}.jpg'.format(name))
    else:
        # list_archivos = os.listdir(ruta)
        # if name in list_archivos:
        #     print("Ya existe este archivo")
        # else:
        fullname = ruta_folder + "/" + name
    
        open(fullname +'.jpg', 'wb').write(imagen)
        print('descargando:{}.jpg'.format(name))

    folder_name=folder_name[1:]

    # Normalizando todas las imagenes del mismo tamaño
    src = cv2.imread(fullname +'.jpg', cv2.IMREAD_UNCHANGED)
    #Porcentaje en el que se redimensiona la imagen
    #scale_percent = 60
    #calcular el 50 por ciento de las dimensiones originales
    #width = int(src.shape[1] * scale_percent / 100)
    #height = int(src.shape[0] * scale_percent / 100)
    width=564
    height=761
    # dsize
    dsize = (width, height)
    # cambiar el tamaño de la image
    output = cv2.resize(src, dsize)
    cv2.imwrite(fullname +'.jpg',output) 

    # Retorno la ruta de la imagen apartir de la carpeta creada con nombre del Item para DJANGO la encuentre
    print("Retornando: ",folder_name + "/" + "{}.jpg".format(name))
    return folder_name + "/" + "{}.jpg".format(name)
            

