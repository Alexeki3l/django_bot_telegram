from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from tienda.models import Producto, Tienda
from usuario.models import Profile
from django.contrib.auth.models import User, UserManager

import telebot
import os
# ForceReply:Para citar un mensaje
from telebot.types import ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
#Para usar los botones Inline
from telebot.types import InlineKeyboardButton # Para definir botones
from telebot.types import InlineKeyboardMarkup # Para crear la botonera inline
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
    if Profile.objects.filter(chat_id = int(message.chat.id)).exists():
        bot.send_message(message.chat.id, "Este comando aun no lo tengo funcional")
    else:
        bot.send_message(message.chat.id, "No puedes usar estes comando. No estas registrado. Usa /create_user para hacerlo.")
#=============================================================================================>
@bot.message_handler(commands=["list_productos"])
def list_productos(message):
    if Profile.objects.filter(chat_id = int(message.chat.id)).exists():
        perfil = Profile.objects.get(chat_id = int(message.chat.id))
        tiendas = Tienda.objects.filter(encargado=User.objects.get(username=perfil))
        if tiendas.count():
            pass
        else:
            bot.send_message(message.chat.id, "No tienes ninguna tienda o servicio.")
    else:
        bot.send_message(message.chat.id, "No puedes usar este comando. No estas registrado. Usa /create_user para hacerlo.")
            

@bot.message_handler(commands=["delete_all_products"])
def delete_all_products(message):
    if Profile.objects.filter(chat_id = int(message.chat.id)).exists():
        productos = Producto.objects.all()
        productos.delete()
        
    else:
        bot.send_message(message.chat.id, "No puedes usar estes comando. No estas registrado. Usa /create_user para hacerlo.")

#========ESTE ES PARA PROBAR LOS BOTONES==========================================>
@bot.message_handler(commands=["info"])
def info(message):
    # Para citar
    # markup = ForceReply()
    # bot.send_message(message.chat.id,"Como te llamas?",reply_markup=markup)
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa el boton",resize_keyboard=True)
    markup.add("Hombre","Mujer")
    msg=bot.send_message(message.chat.id, "¿Cual es tu sexo?",reply_markup=markup)
    bot.register_next_step_handler(msg,aux)

def aux(message):
    if message.text == "Hombre" or message.text=="Mujer":
        markup=ReplyKeyboardRemove()
        bot.send_message(message.chat.id,"OK",reply_to_message_id=message.message_id,reply_markup=markup)
    else:
        pass
#==================================================================================>
#===============BOTONES INLINE====================================================>
@bot.message_handler(commands=['botones'])
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
    bot.send_message(message.chat.id, "Mis canales de ofertas",reply_markup=markup)

@bot.callback_query_handler(func=lambda x:True)
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
        return

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
        telebot.types.BotCommand("/list_productos","Muestra todos tus productos")
    ])

