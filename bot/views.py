from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from tienda.models import Producto, Tienda
from usuario.models import Profile
from django.contrib.auth.models import User, UserManager

import telebot
# Para citar un mensaje
from telebot.types import ForceReply
from bot.utils import All_Products, get_image


# =========================================================================================>

TOKEN = '5624106945:AAEtyM4J_WWANDi6H6aYSeB0JU65hW2RSpg'
bot = telebot.TeleBot(TOKEN)
telebot.types.Chat
path_project = "D:\Alexei-Todo\Python\Estacion de Trabajo\Proyectos_Django\django_telebot"


# For free PythonAnywhere accounts
# tbot = telebot.TeleBot(TOKEN, threaded=False)

@csrf_exempt
def tbot(request):
    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])

        return HttpResponse("")

    else:
        raise PermissionDenied

# =========================================================================================>

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "¿Que puedo hacer por ti?\n\nTengo los siguientes comandos para ayudarte\n")

@bot.message_handler(commands=["commands"])
def commands(message):
    bot.send_message(message.chat.id, "/start - Da la Bienvenida.\n/commands - Lista todos los comandos del bot\n/create_product - Crea un nuevo producto\n/productos - Muestra todos los productos")

#==================CREAR UN USUARIO=========================================================>
@bot.message_handler(commands=["create_user"])
def create_new_user(message):
    bot.send_chat_action(message.chat.id, "typing")
    if Profile.objects.filter(chat_id = int(message.chat.id)).exists():
        bot.send_message(message.chat.id,"Ya usted está registrado.")
    else:
        msg = bot.send_message(message.chat.id,"¿Quieres que te registre en nuestra Base de Datos?\nAsi lograre que registres tu negocio y promocianarlo con mi ayuda.\nEspero una respuesta de Si o No.")
        bot.register_next_step_handler(msg, aux_create_user)

def aux_create_user(message):
    if message.text =="No" or message.text == "NO" or message.text == "no":
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"OK. Como quieras.")
    if message.text =="Si" or message.text == "SI" or message.text == "si":
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"BIEN")
        msg=bot.send_message(message.chat.id,
        "Pon tus datos de la siguiente forma. En el mismo orden que te indico\n<nombre_usuario>\n<tu_correo>\n<password>\nNOTA:El correo tiene que ser funcional lo usare para notificarte de algun problema en caso que no pueda hacerlo por aqui.")
        bot.register_next_step_handler(msg,create_user)
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"No son las palabras exactas que esperaba.\nSi te quieres registrar vas tener activar /create_new_user otra vez.")

def create_user(message):
    lista = message.text.split("\n")
    print(lista)
    if len(lista)==3:
        try:
            user = User.objects.create_user(lista[0], lista[1], lista[2])
            Profile.objects.filter(user_id = user.id).update(chat_id = message.chat.id)
            bot.send_message(message.chat.id,"Todo el proceso ha sido satisfactorio")
            bot.send_message(message.chat.id,"Ups...Espera")
            bot.send_message(message.chat.id,
            "Falta registrar una foto tuya con tu verdadero nombre y apellidos.\nPor cuestiones de etica hacia tus proveedores.\nTu nombre y apellidos escribelos con salto de linea.En la descripcion de la foto que envies\nASI:")
            bot.send_chat_action(message.chat.id, "upload_photo")
            foto = open("media/send_image.jpg","rb")
            msg = bot.send_photo(message.chat.id, foto)
            bot.register_next_step_handler(msg,set_image_name_user)
        except:
            bot.send_message(message.chat.id,"Ups...No puede registrarte.Intenta de nuevo.")   
    else:
        bot.send_message(message.chat.id,"hay algo mal")

def set_image_name_user(message):
    file_info1 = bot.get_file_url(message.photo[-1].file_id)
    image = get_image("\perfil",file_info1)
    caption = message.caption.split("\n")
    Profile.objects.filter(chat_id= message.chat.id).update(imagen = image)
    username = Profile.objects.get(chat_id=message.chat.id)
    User.objects.filter(username=username).update(first_name=caption[0],last_name=caption[1])
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id,"Perfecto!!!....Ya puedes hacer uso de mis servicios.")
#=============================================================================================>
#=================EDITAR USUARIO==============================================================>
@bot.message_handler(commands=["edit_user"])
def edit_user(message):
    bot.send_message(message.chat.id, "Este comando aun no lo tengo funcional")
#=============================================================================================>
@bot.message_handler(commands=["productos"])
def product(message):
    bot.types
    # if Profile.objects.get(chat_id=message.chat.id):
    #     username = Profile.objects.get(chat_id=message.chat.id)
    #     if Tienda.objects.filter(encargado=username).count()==0:
    #         bot.send_chat_action(message.chat.id, "No tienes ningun negocio activo.")
    #     else:
            

@bot.message_handler(commands=["delete_product"])
def delete_product(message):
    productos = Producto.objects.all()
    productos.delete()

    content= All_Products()
    # foto = open("2da51ecfc2163740880424721d9a0114.jpg","rb")
    # bot.send_photo(message.chat.id, foto, "Sueña en grande Cesar.jajaja")
    bot.send_message(message.chat.id, str(content))
"""
@bot.message_handler(commands=["create_product"])
def create_product(message):
    print("El id es:" + str(message.chat.id))
    bot.send_chat_action(message.chat.id, "typing")
    msg = bot.send_message(message.chat.id, "¿Quieres agragar un producto?\nBien.\nSigue los siguientes pasos:\n1ro.Enviame en un solo texto y separado por comas el nombre,precio y descripcion del producto.\nEjemplo:\n\nPollo Frito,12.50,Es un pollo grande.\n\n2do.Despues de enviar el texto anterior enviame la imagen que quieres que tenga tu producto.\nAsi de facil. COMENCEMOS")
    bot.register_next_step_handler(msg, create_prod)
    """
"""
def create_prod(message):
    
    file_info1 = bot.get_file_url(message.photo[-1].file_id)
    file_info2 = bot.get_file_url(message.photo[-2].file_id)
    file_info3 = bot.get_file_url(message.photo[-3].file_id)
    caption = message.caption
    info_prod = caption.split(",")
    image1 = get_image("\producto",file_info1)
    image2 = get_image("\producto",file_info2)
    image3 = get_image("\producto",file_info3)
    
    try:
        producto = Producto(
                    nombre = info_prod[0].strip(),
                    precio = float(info_prod[1].strip()),
                    image1 = image1,
                    image2 = image2,
                    image3 = image3,
                    descripcion = info_prod[2].strip(),
                    cantidad = int(info_prod[3].strip()),
                    tienda = 
                    )
        producto.save()
        bot.send_message(message.chat.id,"Bien!!!...Producto creado satisfactoriamente.")
    except:
        bot.send_message(message.chat.id,"Ups...Ocurrio un error.")
"""
@bot.message_handler(content_types=["text"])
def bot_message_texto(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "No tengo registrado ese comando. Fijese bien en el listado")
    else:
        print(message.text)
        bot.send_message(message.chat.id, message.text)


bot.set_my_commands([
        telebot.types.BotCommand("/start","Da la Bienvenida"),
        telebot.types.BotCommand("/commands","Lista todos los comandos del bot"),
        telebot.types.BotCommand("/create_user","Crearte un usuario."),
        telebot.types.BotCommand("/edit_user","Editar tu usuario."),
        telebot.types.BotCommand("/create_product","Crea un nuevo producto."),
        telebot.types.BotCommand("/delete_product","Elimina todos tus productos"),
        telebot.types.BotCommand("/productos","Muestra todos tus productos")
    ])

