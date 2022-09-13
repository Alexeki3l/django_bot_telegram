from configparser import InterpolationError
from multiprocessing import managers
from unittest.mock import call
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from business.models import Product, Business
from multimedia.models import Multimedia
from user.models import Profile
from django.contrib.auth.models import User, UserManager

import telebot
import os
# ForceReply:Para citar un mensaje
from telebot.types import ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
#Para usar los botones Inline
from telebot.types import InlineKeyboardButton # Para definir botones
from telebot.types import InlineKeyboardMarkup # Para crear la botonera inline
from telebot.types import KeyboardButton
from telebot.types import Contact
from bot.utils import All_Products, get_image

import requests
import pickle
from bs4 import BeautifulSoup

#===============CONSTANTES PARA EL EJEMPLO DE LOS BOTONES=====================>

N_RES_PAG=5 # numero de resultados a mostrar en cada pagina
MAX_ANCHO_ROW = 8 # maximo de botones por fila(limitacion de telegram)
DIR = {"busquedas" : "./busquedas/"}# donde se guardan los archivos de las busquedas
for key in DIR:
    try:
        os.mkdir(key)
    except:
        pass

# =========================================================================================>

TOKEN = '5624106945:AAEtyM4J_WWANDi6H6aYSeB0JU65hW2RSpg'
bot = telebot.TeleBot(TOKEN)
# telebot.types.Chat
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
# ===================================START=================================================>
"""
Formato html
    mensaje = "<pre>Casi igual que la etiqueta code</pre>\n"
    mensaje += "<b>negrita</b>\n"
    mensaje += "<u>subrayado</u>\n"
    mensaje += "<i>cursiva</i>\n"
    mensaje += "<s>tachado</s>\n"
    mensaje += "<code>modo codigo</code>\n"
    mensaje += "<span class='tg-spoiler'>Spoiler</span>\n"
    mensaje += "<a href='https://youtube.com'>enlace</a>\n"
"""
"""@bot.message_handler(commands=["start"])
def start(message):
    mensaje  = "<b>Hola, ¿Como estas?</b>\n\n"
    mensaje += "<i>Soy un Bot de Gestion. Con los comandos que tengo predefinido espero que tengas una agradable interaccion conmigo.</i>\n"
    mensaje += "\n"
    bot.send_message(message.chat.id, mensaje, parse_mode="html")
    commands(message=message)"""

@bot.message_handler(commands=['start'])
def cmd_start(message):

    if not Profile.objects.filter(chat_id = int(message.chat.id)).exists():
        
        mensaje  = "<b>Hola, ¿Como estas?</b>\n\n"
        mensaje += "<i>Soy un Bot de Gestion. Con los comandos que tengo predefinido espero que tengas una agradable interaccion conmigo.</i>\n"
        mensaje += "\n"
        # Muestra un mensaje con botones inline(a continuacion del mensaje)
        markup = InlineKeyboardMarkup(row_width=3) # numero de botones en cada fila(3 por defecto)
        b1=InlineKeyboardButton("👤 Registrarte", callback_data="sign_up")
        b2=InlineKeyboardButton("🔍 Buscar", callback_data="search")
        b3=InlineKeyboardButton("🔔 Notificar", callback_data="notify")
        b4=InlineKeyboardButton("🛂 Contacto", callback_data="contact")
        b5=InlineKeyboardButton("🆘 Ayuda", callback_data="help")
        # Esto por atras al programa de python el mensaje "cerrar"
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close")
        markup.add(b1,b2,b3,b4,b5,b_cerrar)
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")

    else:
        usuario = Profile.objects.get(chat_id = int(message.chat.id))
        mensaje = f"Hola, <b>{usuario}</b>"
        markup = InlineKeyboardMarkup(row_width=2) # numero de botones en cada fila(3 por defecto)
        b1=InlineKeyboardButton("👤 Perfil", callback_data="profile")
        b2=InlineKeyboardButton("🛰️ Mis Negocios", callback_data="my_services")
        b3=InlineKeyboardButton("🛄 Mis Productos", callback_data="my_products")
        b4=InlineKeyboardButton("🔍 Buscar", callback_data="search")
        b5=InlineKeyboardButton("🔔 Notificar", callback_data="notify")
        b6=InlineKeyboardButton("🛂 Contacto", callback_data="contact")
        b7=InlineKeyboardButton("🆘 Ayuda", callback_data="help")
        # Esto por atras al programa de python el mensaje "cerrar"
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close")
        markup.add(b1,b2,b3,b4,b5,b6,b7,b_cerrar)
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")


@bot.callback_query_handler(func=lambda x:True)
def respuesta_botones_inline(call):
    # Gestiona las acciones de los botones callback_data
    cid=call.from_user.id
    mid=call.message.id
    # Aqui verifico si se envio el mensaje "cerrar"
    if call.data =="close":
        # Aqui cierro la botonera
        bot.delete_message(cid,mid)
        return
    
    elif call.data =="sign_up":
        crear_usuario(call.message)
        return

    elif call.data=="profile":
        try:
            profile(call.message)
            bot.delete_message(cid,mid)
            return
        except:
            bot.delete_message(cid,mid)
            cmd_start(call.message)

    elif call.data=="close_return_start":
        cmd_start(call.message)
        bot.delete_message(cid,mid)
        return

    elif call.data=="edit_profile":
        edit_user(call.message)
        bot.delete_message(cid,mid)
        return

    elif call.data=="edit_profile_name":
        mensaje = "Escriba el nuevo nombre"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,edit_profile_name)
        return

    elif call.data=="edit_profile_last_name":
        mensaje = "Escriba sus apellidos"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,edit_profile_last_name)
        return

    elif call.data=="edit_profile_username":
        mensaje = "El usuario es unico. Lo cual no se puede cambiar. Por lo menos por ahora."
        bot.send_message(call.message.chat.id, mensaje)
        edit_user(call.message)
        return
    
    elif call.data=="edit_profile_email":
        mensaje = "Escriba el correo"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,edit_profile_email)
        return

    elif call.data=="edit_profile_phone":
        mensaje = "Escriba su numero de telefono"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,edit_profile_phone)
        return

    elif call.data=="edit_profile_bio":
        mensaje = "Escriba en su Bio."
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,edit_profile_bio)
        return

    elif call.data=="edit_profile_address":
        mensaje = "Escriba su direccion."
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,edit_profile_address)
        return

    elif call.data=="edit_profile_image":
        mensaje = "Envieme su foto"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,edit_profile_image)
        return

    elif call.data=="delete_profile":
        mensaje ="Si elimina si cuenta perdera todos los datos asociados a la misma."
        mensaje += "<b>¿Estas seguro de querer eliminarla?</b>\n"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(name,delete_profile)
        return

    # Business
    elif call.data=="my_services":
        menu_business(call.message)
        bot.delete_message(cid,mid)
        return

    elif call.data=="create_business":
        mensaje = "¿Que nombre tendra su negocio?.\n"
        # mensaje += "Y en la descripcion de la imagen envieme lo que sera el nombre de su negocio."
        msg=bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(msg,create_business)
        
    

#=============================================================================================>
#=====================================COMANDOS================================================>  
@bot.message_handler(commands=["comandos"])
def commands(message):
    mensaje  = "<strong><u>COMANDOS</u>:</strong>\n\n"
    mensaje += "<u>USUARIOS</u>:\n"
    mensaje += "/start - Da la Bienvenida.\n"
    mensaje += "/comandos - Lista todos los comandos del bot.\n"
    mensaje += "/notificar - Notifica sobre algun evento en especifico.\n"
    mensaje += "/buscar - Busca algun servicio o producto.\n"
    mensaje += "/the_bot - Informacion sobre el BOT.\n"
    mensaje += "/contacto - Contacto del desarrolador.\n"
    mensaje += "/crear_usuario - Crea un usuario.\n\n"

    mensaje += "<u>USUARIOS REGISTRADOS</u>:\n"
    mensaje += "<code>Gestion de Usuario</code>\n"
    mensaje += "/editar_usuario - Edita tu usuario.\n"
    mensaje += "/eliminar_usuario - Elimina tu usuario.\n"
    mensaje += "/detalle_usuario - Muestra mas detalles de tu perfil.\n"
    mensaje += "<code>Gestion de Servicios</code>\n"
    mensaje += "/crear_servicio - Crea servicio.\n"
    mensaje += "/editar_servicio - Edita servicio.\n"
    mensaje += "/eliminar_servicio - Elimina servicio.\n"
    mensaje += "/detalle_servicio - Muestra mas detalles de servicio.\n"
    mensaje += "/servicios - Lista servicios.\n"
    mensaje += "<code>Gestion de Productos</code>\n"
    mensaje += "/crear_prod - Crea un nuevo producto.\n"
    mensaje += "/editar_prod - Edita un producto.\n"
    mensaje += "/eliminar_prod - Elimina un producto.\n"
    mensaje += "/detalle_prod - Muestra mas detalles de un producto.\n"
    mensaje += "/productos - Muestra mas detalles de un producto.\n"
    bot.send_message(message.chat.id, mensaje, parse_mode="html")

#===========================================================================================>
#=================================SOBRE EL BOT==============================================>
@bot.message_handler(commands=["the_bot"])
def the_Bot(message):
    mensaje = "Hola. ¿Como estas?\n\n"
    mensaje += "Si has llegado hasta aqui es que has husmeando ha fondo."
    mensaje += " Es broma!!. Aqui te contare sobre el surgimiento de esta idea.\n"
    mensaje += "La idea de crear este <b>bot</b> surje con el problema de que las personas que brindan determinados productos o servicios no llegan a la mayor cantidad de personas posibles."
    mensaje += " Y dadas las bondades que nos da la <a href='https://https://core.telegram.org/bots/api'>API</a> de Telegram y dado que este cliente de mensajeria es uno de los mas usados.\n"
    mensaje += "Para no decir el <b>mas usado</b>.\n Nos vino la idea de crear un Bot lo suficientemente versatil como para gestionar dichos servicios.\n\n"
    mensaje += "Pero, <b>¿Que tiene este Bot que lo hace diferente a una APK o los demas Bots?</b>\n"
    mensaje += "Bueno, diferente a otros Bots no tiene mucha diferencia. Digamos que la diferencia la marca en el enfasis de desarrollo o sentido de desarrollo que se le ha dado al crear este Bot."
    mensaje += "Y el sistema tendra una APK pero por ahora hemos usado a Telegram como interfaz de nuestro software.\n\n"
    mensaje += "<b>¿Que beneficios le da el uso de este Bot a las personas comunes y aquellas que tengan un servicio que ofertar?</b>\n"
    mensaje += "[Por escribir]"
    bot.send_message(message.chat.id, mensaje, parse_mode="html") 

#===========================================================================================>
#=================================CONTACTO==============================================>
@bot.message_handler(commands=["contacto"])
def contacto(message):
    bot.send_message(message.chat.id, "nada")

#===========================================================================================>
#=================================CREAR UN USUARIO==========================================>
# @bot.message_handler(commands=["crear_usuario"])
def crear_usuario(message):
    bot.send_chat_action(message.chat.id, "typing")
    if Profile.objects.filter(chat_id = int(message.chat.id)).exists():
        usuario = Profile.objects.get(chat_id = int(message.chat.id))
        bot.send_message(message.chat.id,f"<b>{usuario}</b>. Ya usted está registrado.", parse_mode="html")
    else:
        mensaje = "Este comando sirve para registrarte en nuestro sistema.\n"
        mensaje += "¿Quieres registrarte en nuestra Base de Datos?\n\n"
        mensaje += "<i>Espero respuesta de <b>SI</b> o <b>NO</b></i>"
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa el boton",resize_keyboard=True)
        markup.add("Si","No")
        msg = bot.send_message(message.chat.id, mensaje, parse_mode="html", reply_markup=markup)
        bot.register_next_step_handler(msg, aux_create_user)

def aux_create_user(message):
    if message.text =="No" or message.text == "NO" or message.text == "no":
        markup=ReplyKeyboardRemove()
        bot.send_chat_action(message.chat.id, "typing")
        mensaje = "<b>OK</b>\n"
        mensaje += "En caso que quieras. No podras registrar ningun servicio"
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")

    elif message.text =="Si" or message.text == "SI" or message.text == "si":
        bot.send_chat_action(message.chat.id, "typing")
        mensaje = "¿Quieres que lo cree apartir de tus datos de <b>Telegram</b>?\n\n"
        mensaje += "<i>Espero respuesta de <b>SI</b> o <b>NO</b></i>"
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa el boton",resize_keyboard=True)
        markup.add("Si","No")
        msg=bot.send_message(message.chat.id, mensaje, parse_mode="html", reply_markup=markup)
        bot.register_next_step_handler(msg,auxiliar)
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"No son las palabras exactas que esperaba.")
        mensaje = "¿Quieres o no quieres registrarte?"
        msg = bot.send_message(message.chat.id, mensaje)
        bot.register_next_step_handler(msg, aux_create_user)

def auxiliar(message):
    markup=ReplyKeyboardRemove()

    if message.text == "Si" or message.text == "SI" or message.text == "si":
        
        mensaje = "Entre un correo y su contraseña.\n"
        mensaje += "Ejemplo:\n"
        mensaje += "<code>ejemplo@dominio.com</code>\n"
        mensaje += "<code>mipassword</code>\n"
        mensaje += "Los demas datos se obtendran de su perfil de <b>Telegram</b>"
        msg=bot.send_message(message.chat.id, mensaje, reply_markup=markup ,parse_mode="html")
        bot.register_next_step_handler(msg, create_user)

    elif message.text == "No" or message.text == "NO" or message.text == "no":
        try:
            mensaje = "Pon tus datos de la siguiente forma. En el mismo orden que te indico:\n"
            mensaje += "<code>nombre_usuario</code>\n"
            mensaje += "<code>tu_correo</code>\n"
            mensaje += "<code>password</code>\n\n"
            mensaje += "<b>NOTA:</b>El correo tiene que ser funcional lo usare para notificarte de algun problema en caso que no pueda hacerlo por aqui."
            print(mensaje)
            msg=bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
        except:
            print("error")
        bot.register_next_step_handler(msg, create_user)

    else:
        mensaje = "Haz salido de la opcion /crear_usuario"
        bot.send_message(message.chat.id, mensaje, reply_markup=markup)

def create_user(message):
    lista = message.text.split("\n")
    print(lista)

    if len(lista)==3:
        try:
            user = User.objects.create_user(lista[0], lista[1], lista[2])
            Profile.objects.filter(user_id = user.id).update(chat_id = message.chat.id)
            bot.send_message(message.chat.id,
            "Falta registrar una foto tuya con tu verdadero nombre y apellidos.\nPor cuestiones de etica hacia tus proveedores.\nTu nombre y apellidos escribelos con salto de linea.En la descripcion de la foto que envies\nASI:")
            bot.send_chat_action(message.chat.id, "upload_photo")
            foto = open(path_project+"/media/send_image.jpg","rb")
            msg = bot.send_photo(message.chat.id, foto)
            bot.register_next_step_handler(msg,set_image_name_user)
        except:
            bot.send_message(message.chat.id,"Ups...No puede registrarte.Intenta de nuevo.")  
            User.obejcts.filter(id=user.id).dele

    elif len(lista)==2:
        if len(lista[0].split("@"))==2 and len(lista[1])>=8:
            try:
                info_chat = bot.get_chat(message.chat.id)
                
                usuario = User.objects.create_user(info_chat.username, lista[0], lista[1])
                if info_chat.first_name:
                    usuario.first_name = info_chat.first_name
                    usuario.save()
                if info_chat.last_name:
                    usuario.last_name  = info_chat.last_name
                    usuario.save() 
                Profile.objects.filter(user_id = usuario.id).update(bio= info_chat.bio, chat_id= message.chat.id)  
                profile = Profile.objects.get(user_id=usuario.id)
            except:
                bot.send_message(message.chat.id,"Ups..Ah ocurrido un error. Intenta de nuevo.")
                cmd_start(message)

            try:
                url_image = bot.get_file_url(info_chat.photo.big_file_id)
                image = get_image("\profile", url_image)
                multimedia = Multimedia(profiles=profile, file=image, type="1")
                multimedia.save()

            except:
                multimedia=Multimedia(profiles=profile, file="profile/sin-foto.png", type="1")
                multimedia.save()
                bot.send_message(message.chat.id,"Deberias actualizar tu perfil y añadir una imagen.")
                cmd_start(message)
                
            mensaje = "Te has registrado <b>satisfactoriamente</b>!!!"
            bot.send_message(message.chat.id, mensaje, parse_mode="html")
            cmd_start(message)

        else:
            mensaje = "El correo debe ser:\n"
            mensaje += "Ejemplo:\n"
            mensaje += "<code>ejemplo@dominio.com</code>\n\n"
            mensaje += "La contraseña debe tener:\n"
            mensaje += "Ejemplo:\n"
            mensaje += "<code>Debe tener mas de 8 caracteres y debe tener caracteres extraños</code>\n\n"
            msg = bot.send_message(message.chat.id, mensaje, parse_mode="html")
            bot.register_next_step_handler(msg,create_user)
    
    else:
        mensaje = f"Esto:\n<pre>{message.text}</pre>\nNo cumple con lo que te dije.\nIntente de nuevo"
        bot.send_message(message.chat.id, mensaje, parse_mode = "html")
        cmd_start(message)

def set_image_name_user(message):
    try:
        url_image = bot.get_file_url(message.photo[-1].file_id)
        image = get_image("\profile",url_image)
        caption = message.caption.split("\n")
        profile = Profile.objects.get(chat_id=message.chat.id)
        multimedia = Multimedia(profiles=profile, file=image, type="1")
        multimedia.save()
        User.objects.filter(username=profile).update(first_name=caption[0],last_name=caption[1])
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"Perfecto!!!....Ya puedes hacer uso de mis servicios.")
        cmd_start(message)
    except:
        profile = Profile.objects.get(chat_id=message.chat.id)
        User.objects.filter(username = profile).delete()
        bot.send_message(message.chat.id,"🚫 Ocurrio un error 🚫.\n🚫 Valores enviados no eran correctos. 🚫")
        cmd_start(message)
#=============================================================================================>
#================================INTERFACE PROFILE===============================================>

def profile(message):
    username = Profile.objects.get(chat_id = int(message.chat.id))
    usuario = User.objects.get(username = username)
    if Multimedia.objects.filter(profiles = username).exists():
        multimedia = Multimedia.objects.get(profiles = username)
        mensaje = "❎⚜️⚜️⚜️❎<b>PERFIL</b>❎⚜️⚜️⚜️❎\n\n"
        if usuario.first_name:
            mensaje += f"✅ <b>Nombre</b>- - --: {usuario.first_name}\n"
        if usuario.last_name:
            mensaje += f"✅ <b>Apellidos</b>- --: {usuario.last_name}\n"
        if username:
            mensaje += f"✅ <b>Username</b>- -: {username}\n"
        if usuario.email:
            mensaje += f"✅ <b>Email</b>- - - - --: {usuario.email}\n"
        if username.phone:
            mensaje += f"✅ <b>Telefono</b>- ---: {username.phone}\n"
        if username.bio:
            mensaje += f"✅ <b>Bio</b>- - - - - - --: {username.bio}\n"
        if username.address:
            mensaje += f"✅ <b>Direccion</b>- --: {username.address}\n"
        multimedia = "../django_telebot/"+str(multimedia.file.url)[1:]
        markup = InlineKeyboardMarkup(row_width=1) # numero de botones en cada fila(3 por defecto)
        b1=InlineKeyboardButton("🖋️ Editar", callback_data="edit_profile")
        b_delete=InlineKeyboardButton("🗑️ Eliminar",callback_data="delete_profile")
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
        markup.add(b1,b_delete,b_cerrar)
        bot.send_chat_action(message.chat.id, "upload_photo")
        foto = open(multimedia,"rb")
        bot.send_photo(message.chat.id, foto, mensaje, reply_markup=markup, parse_mode="html")

    else:
        bot.send_message(message.chat.id, "🚫 Upss...Pasa algo con su perfil.🚫\nComuniquese con soporte.")
#================================INTERFACE EDIT USER===============================================>

def edit_user(message):
    username = Profile.objects.get(chat_id = int(message.chat.id))
    usuario = User.objects.get(username = username)
    multimedia = Multimedia.objects.get(profiles = username)
    multimedia = "../django_telebot/"+str(multimedia.file.url)[1:]
    markup=InlineKeyboardMarkup(row_width=1)

    mensaje = "❎⚜️⚜️❎<b>EDITAR PERFIL</b>❎⚜️⚜️❎\n\n"
    mensaje += f"1️⃣☑️ <b>Nombre</b>- - --: {usuario.first_name}\n"
    mensaje += f"2️⃣☑️ <b>Apellidos</b>- --: {usuario.last_name}\n"
    mensaje += f"3️⃣☑️ <b>Username</b>- -: {username}\n"
    mensaje += f"4️⃣☑️ <b>Email</b>- - - - --: {usuario.email}\n"
    mensaje += f"5️⃣☑️ <b>Telefono</b>- ---: {username.phone}\n"
    mensaje += f"6️⃣☑️ <b>Bio</b>- - - - - - --: {username.bio}\n"
    mensaje += f"7️⃣☑️ <b>Direccion</b>- --: {username.address}\n"
    mensaje += f"8️⃣☑️ <b>Imagen</b>\n"

    b1=InlineKeyboardButton("1",callback_data="edit_profile_name")
    b2=InlineKeyboardButton("2",callback_data="edit_profile_last_name")
    b3=InlineKeyboardButton("3",callback_data="edit_profile_username")
    b4=InlineKeyboardButton("4",callback_data="edit_profile_email")
    b5=InlineKeyboardButton("5",callback_data="edit_profile_phone")
    b6=InlineKeyboardButton("6",callback_data="edit_profile_bio")
    b7=InlineKeyboardButton("7",callback_data="edit_profile_address")
    b8=InlineKeyboardButton("8",callback_data="edit_profile_image")
    
    b_cerrar=InlineKeyboardButton("❌ Cerrar",callback_data="profile")
    markup.row(b1,b2,b3,b4,b5,b6,b7,b8,b_cerrar)
    
    bot.send_chat_action(message.chat.id, "upload_photo")
    foto = open(multimedia,"rb")
    bot.send_photo(message.chat.id, foto, mensaje, reply_markup=markup, parse_mode="html")

def edit_profile_name(message):
    
    username = Profile.objects.get(chat_id = int(message.chat.id))
    User.objects.filter(username = username).update(first_name = str(message.text))
    bot.send_message(message.chat.id, "Nombre guardado satisfactoriamente")
    edit_user(message)

def edit_profile_last_name(message):
    
    username = Profile.objects.get(chat_id = int(message.chat.id))
    User.objects.filter(username = username).update(last_name = str(message.text))
    bot.send_message(message.chat.id, "Apellidos guardados satisfactoriamente")
    edit_user(message)

def edit_profile_email(message):
    mensaje = message.text.split("@")
    if len(mensaje)==2:
        username = Profile.objects.get(chat_id = int(message.chat.id))
        User.objects.filter(username = username).update(email = str(message.text))
        bot.send_message(message.chat.id, "Correo guardado satisfactoriamente")
        edit_user(message)
    else:
        bot.send_message(message.chat.id, "Correo invalido.")
        edit_user(message)

def edit_profile_phone(message):
    Profile.objects.get(chat_id = int(message.chat.id))
    mensaje = message.text[1:]
    if mensaje.isdigit():
        Profile.objects.filter(chat_id = int(message.chat.id)).update(phone=message.text)
        bot.send_message(message.chat.id, "Numero de telefono guardado satisfactoriamente.")
        edit_user(message)
    else:
        bot.send_message(message.chat.id, "Tienes que enviarme tu numero de telefono.")
        edit_user(message)

def edit_profile_bio(message):
    Profile.objects.filter(chat_id = int(message.chat.id)).update(bio=message.text)
    bot.send_message(message.chat.id, "Su Bio fue actualizadda satisfactoriamente.")
    edit_user(message)

def edit_profile_address(message):
    Profile.objects.filter(chat_id = int(message.chat.id)).update(address=message.text)
    bot.send_message(message.chat.id, "Su Direccion fue actualizadda satisfactoriamente.")
    edit_user(message)

def edit_profile_image(message):
    url_image = bot.get_file_url(message.photo[-1].file_id)
    image = get_image("\profile",url_image)
    username = Profile.objects.get(chat_id = int(message.chat.id))
    Multimedia.objects.filter(profiles = username).update(file=image)
    bot.send_message(message.chat.id, "Imagen guardada satisfactoriamente")
    edit_user(message)

#================================ELIMINAR USUARIO===============================================>
def delete_profile(message):
    pass

#==============================================================================================>
#==================================INTERFACE MENU BUSINESS=======================================>
def menu_business(message):
    mensaje = "❎⚜️❎<b>Mis Servicios/Negocios</b>❎⚜️❎\n\n"
    username = Profile.objects.get(chat_id = int(message.chat.id))
    markup = InlineKeyboardMarkup(row_width=5)
    if Business.objects.filter(manager=username).count()==0:
        
        b1=InlineKeyboardButton("➕ Negocio", callback_data="create_business")
        b2=InlineKeyboardButton("🆘 Ayuda", callback_data="help_services")
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
        markup.row(b1,b2)
        markup.row(b_cerrar)
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
    
    else:  
        n=1
        buttons=[]
        for business in Business.objects.filter(manager=username):
            buttons.append(InlineKeyboardButton(str(n),callback_data="profile"))
            mensaje +=f'[<b>{n}</b>] {business.name}\n'
            n+=1
        if n <= 5:
            b1=InlineKeyboardButton("➕ Negocio", callback_data="create_business")
            b2=InlineKeyboardButton("🆘 Ayuda", callback_data="help_services")
            b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
            markup.add(*buttons)
            markup.row(b1,b2)
            markup.row(b_cerrar)
        else:
            b2=InlineKeyboardButton("🆘 Ayuda", callback_data="help_services")
            b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
            markup.add(*buttons)
            markup.row(b2)
            markup.row(b_cerrar)
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")

def create_business(message):
    if Business.objects.filter(name=message.text).count()<5:
        if Business.objects.filter(name=message.text):
            mensaje = "Este nombre ya esta siendo usado.\n"
            mensaje += "La diferencia empieza con un simple nombre.\n"
            mensaje += "Envie otro nombre."
            msg= bot.send_message(message.chat.id, mensaje)
            bot.register_next_step_handler(msg, create_business)

        else:
            try:
                mensaje ="Negocio creado satisfactoriamente"
                business = Business(
                    name = str(message.text),
                    manager = Profile.objects.get(chat_id = message.chat.id)
                )
                business.save()
                msg = bot.send_message(message.chat.id, mensaje)
                menu_business(message)
                
            except:
                mensaje ="Error!!!"
                bot.send_message(message.chat.id, mensaje)
    else:
        mensaje = "La cantidad exacta de <b>Negocios</b> por usuario es de 5.\n"
        mensaje = "Escribale a soporte para mas informacion."
        bot.send_message(message.chat.id, mensaje, parse_mode="html")
    



#==================================================================================>
#===============BOTONES INLINE====================================================>
"""@bot.message_handler(commands=['botones'])
def cmd_botones(message):
    # Muestra un mensaje con botones inline(a continuacion del mensaje)
    markup = InlineKeyboardMarkup(row_width=2) # numero de botones en cada fila(3 por defecto)
    b1=InlineKeyboardButton("TOP Descuentazos",url="https://t.me/top_descuentazos")
    b2=InlineKeyboardButton("TOP hgjgf",url="https://t.me/top_descuentazos")
    b3=InlineKeyboardButton("TOP vcnvcbc",url="https://t.me/top_descuentazos")
    b4=InlineKeyboardButton("TOP nvcbvnb",url="https://t.me/top_descuentazos")
    b5=InlineKeyboardButton("TOP vcbnvbnvcb",url="https://t.me/top_descuentazos")
    # Esto por atras al programa de python el mensaje "cerrar"
    b_cerrar=InlineKeyboardButton("CERRAR",callback_data="cerrar")
    markup.add(b1,b2,b3,b4,b5,b_cerrar)
    bot.send_message(message.chat.id, "Mis canales de ofertas",reply_markup=markup)"""

"""@bot.callback_query_handler(func=lambda x:True)
def respuesta_botones_inline(call):
    # Gestiona las acciones de los botones callback_data
    cid=call.from_user.id
    mid=call.message.id
    # Aqui verifico si se envio el mensaje "cerrar"
    if call.data =="cerrar":
        # Aqui cierro la botonera
        bot.delete_message(cid,mid)
        return 
    datos = pickle.load(open(f'{DIR["busquedas"]}{cid}_{mid}','rb'))
    if call.data =="anterior":
        if datos["pag"]==0:
            bot.answer_callback_query(call.id,"Ya estas en la primera pagina")
        else:
            datos["pag"]-=1
            pickle.dump(datos, open(f'{DIR["busquedas"]}{cid}_{mid}','wb'))
            mostrar_pagina(datos["lista"],cid,datos["pag"],mid)
        return
    elif call.data=="siguiente":
        # Si ya estamos en la ultima pagina
        if datos["pag"]*N_RES_PAG+N_RES_PAG >=len(datos["lista"]):
            bot.answer_callback_query(call.id,"Ya estas en la ultima pagina")
        else:
            datos["pag"]+=1
            pickle.dump(datos, open(f'{DIR["busquedas"]}{cid}_{mid}','wb'))
            mostrar_pagina(datos["lista"],cid,datos["pag"],mid)
        return"""

# =========================MISMO TEMA==================================================>
@bot.message_handler(commands=['buscar'])
def cmd_buscar(message):
    texto_buscar=" ".join(message.text.split()[1:])
    if not texto_buscar:
        texto='Debes introducir una busqueda.\n'
        texto+='Ejemplo:\n'
        texto+=f'<code>{message.text} zapatos puma</code>'
        bot.send_message(message.chat.id,texto,parse_mode="html")
        return 1
    else:
        print(f'Buscando en Amazon: "{texto_buscar}"')
        url="https://www.amazon.com/s?k={0}".format(texto_buscar.replace(" ","+"))
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                "Accept-Language":"en",
                }
        response=requests.get(url,headers=headers)
        if response.status_code != 200:
            print(f'ERROR al buscar:{response.status_code} {response.reason}')
            bot.send_message(message.chat.id, "Se ha producido un error. Intentalo mas tarde")
            return 1
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            elementos = soup.find_all('div', {'class':'s-result-item', 'data-component-type':'s-search-result'})
            lista=[]
            for elemento in elementos:
                try:
                    # product_name = result.h2.text
                    product_name = elemento.find('span', {'class':'a-text-normal'}).text 
                    product_url = elemento.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).get('href')
                    product_url = "https://www.amazon.com" + product_url
                    print("No hubo problema")
                    lista.append([product_name, product_url])
                except:
                    print("ERROR")
                    continue
        
        mostrar_pagina(lista,message.chat.id)
        

def mostrar_pagina(lista, cid, pag=0, mid=None):
    #Crea o edita un mensaje de la pagina
    # Creamos botonera
    markup=InlineKeyboardMarkup(row_width=MAX_ANCHO_ROW)
    b_anterior  =InlineKeyboardButton("🡠",callback_data="anterior")
    b_cerrar    =InlineKeyboardButton("🗙",callback_data="cerrar")
    b_siguiente =InlineKeyboardButton("🡢",callback_data="siguiente")
    inicio =pag*N_RES_PAG
    fin=inicio+N_RES_PAG
    if fin > len(lista):
        fin=len(lista)
    mensaje = f'<i>Resultados {inicio+1}-{fin} de {len(lista)}</i>\n\n'
    n=1
    botones =[]
    for item in lista[inicio:fin]:
        botones.append(InlineKeyboardButton(str(n),url=item[1]))
        mensaje+=f'[<b>{n}</b>] {item[0]}\n'
        n+=1
    markup.add(*botones)    
    markup.row(b_anterior,b_cerrar,b_siguiente)
    if mid:
        bot.edit_message_text(mensaje, cid, mid, reply_markup=markup, parse_mode="html",disable_web_page_preview=True)
    else:
        res=bot.send_message(cid,mensaje, reply_markup=markup,parse_mode="html",disable_web_page_preview=True)
        mid=res.message_id
        datos={"pag":0,"lista":lista}
        pickle.dump(datos, open(f'{DIR["busquedas"]}{cid}_{mid}','wb'))
    
            
#======================================================================================>    
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

@bot.message_handler(commands=["localizar"])
def localizar(message):
    bot.send_location(message.chat.id, 22.0221205,-80.8247165, proximity_alert_radius=100)


@bot.message_handler(content_types=['location'])
def prueba(message):
    
    print(message.location.latitude)
    print(message.location.longitude)
    bot.send_message(message.chat.id,f"Tu posicion es: \nlatitud:{message.location.latitude}\nlongitud:{message.location.longitude}")
    

@bot.message_handler(content_types=['venue'])
def pru(message):
    print(message.live_period)
    print(message.location.latitude)
    print(message.location.longitude)
    bot.send_message(message.chat.id,"pasa algo")

@bot.message_handler(content_types=["text"])
def bot_message_texto(message):
    if message.text.startswith("/"):
        print(message)
        bot.send_message(message.chat.id, "No tengo registrado ese comando. Fijese bien en el listado")

    if message.text == "video":
        video = open("C:\Users\Keidy\Downloads\promo.mp4", "rb")
        bot.send_video(message.chat.id, video)
    else:
        print("======MESSAGE======")
        print(message)
        print("======CHAT======")
        print(bot.get_chat(message.chat.id))
        # print(message.contact)
        bot.send_message(message.chat.id, "Lo sentimos servidor reiniciado. Intente su operacion desde el principio")
        cmd_start(message)

@bot.message_handler(content_types=['photo'])
def bot_message_texto(message):
    if message.photo:
        print("======MESSAGE======")
        print(message)
        print("======CHAT======")
        print(bot.get_chat(message.chat.id))
    else:
        pass

bot.set_my_commands([
        telebot.types.BotCommand("/start","Da la Bienvenida"),
        telebot.types.BotCommand("/help","Ayuda")
    ])
