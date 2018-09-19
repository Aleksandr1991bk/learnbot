from glob import glob
import logging
from random import choice

from emoji import emojize                                
from telegram import ReplyKeyboardMarkup, KeyboardButton           
                                                                    
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters       

import setting
import ephem
import datetime

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
 


def greet_user(bot, update):
  text = 'Вызван /start'
  logging.info(text)                                                  
  contact_button = KeyboardButton('Прислать контакты',request_contact=True)       
  location_button = KeyboardButton('Прислать координаты', request_location=True)
  my_keyboard = ReplyKeyboardMarkup([['Прислать картинку', 'Сменить аватар'],     
                                        [contact_button, location_button]])            
  update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
  emo = get_user_emo(user_data)
  user_text = 'Привет {} {}! ты написал: {}'.format(update.message.chat.first_name, emo, update.message.text)      
  logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,                         
         update.message.chat.id, update.message.text)
  update.message.reply_text(user_text, reply_markup=get_keyboard())                                                                      
                                                                                                          

def get_planet_info(planet_name):         
  
  if planet_name == 'Mars':
    m = ephem.Mars(datetime.datetime.now())                                  
    planet_system = ephem.constellation(m)                                   
  
  elif planet_name == 'Venus':
    m = ephem.Venus(datetime.datetime.now())
    planet_system = ephem.constellation(m)

  elif planet_name == 'Mercury':
    m = ephem.Mercury(datetime.datetime.now())
    planet_system = ephem.constellation(m)

  elif planet_name == 'Jupiter':
    m = ephem.Jupiter(datetime.datetime.now())
    planet_system = ephem.constellation(m)

  elif planet_name == 'Saturn':
    m = ephem.Saturn(datetime.datetime.now())
    planet_system = ephem.constellation(m)

  elif planet_name == 'Uran':
    m = ephem.Uran(datetime.datetime.now())
    planet_system = ephem.constellation(m)

  elif planet_name == 'Neptune':
    m = ephem.Neptune(datetime.datetime.now())
    planet_system = ephem.constellation(m)

  elif planet_name == 'Pluto':
    m = ephem.Pluto(datetime.datetime.now())
    planet_system = ephem.constellation(m)

  else:
    planet_system = 'I have no idea'
                                                                         
  return planet_system


def answer_with_planet_system(bot=None, update=None):                 
  planet_name = update.message.text                                     
  planet_name = planet_name.split()[-1]
  planet_system = get_planet_info(planet_name)                          
  
  user_text = 'Привет User! ты ищешь планету: {}, сегодня она находится в созвездии {}'.format(planet_name, planet_system)      
                                                                                                                             
  update.message.reply_text(user_text)     
                                      



def send_picture(bot, update, user_data):
  picture_list = glob('images/one*.jp*g')                              
  pic_list = choice(picture_list)                                      
  bot.send_photo(chat_id=update.message.chat_id, photo=open(pic_list, 'rb'), reply_markup=get_keyboard())
                                                                                  


def emo_user(bot, update, user_data):
  emo = get_user_emo(user_data)         
  user_data['emo'] = emo
  text = 'Привет {}'.format(emo)
  update.message.reply_text(text, reply_markup=get_keyboard())                          


def get_user_emo(user_data):                                                   
  if 'emo' in user_data:                                                      
    return user_data['emo']                                                    
  else:                                                                       
    user_data['emo'] = emojize(choice(setting.USER_EMOJI), use_aliases=True)
    return user_data['emo']

def change_avatar(bot, update, user_data):       
    if 'emo' in user_data:                                     
      del user_data['emo']
    emo = get_user_emo(user_data)                  
    update.message.reply_text('Готово: {}'.format(emo), reply_markup=get_keyboard())      

def get_contact(bot, update, user_data):
  print(update.message.contact)
  update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
  print(update.message.location)
  update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_keyboard():
  contact_button = KeyboardButton('Прислать контакты',request_contact=True)       
  location_button = KeyboardButton('Прислать координаты', request_location=True)
  my_keyboard = ReplyKeyboardMarkup([['Прислать картинку', 'Сменить аватар'],     
                                        [contact_button, location_button]],
                                         resize_keyboard=True)                 
  return my_keyboard                               

def main():
    mybot = Updater(setting.API_KEY, request_kwargs=setting.PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('emoji', emo_user, pass_user_data=True))         
    dp.add_handler(CommandHandler('picture', send_picture,pass_user_data=True))     
    dp.add_handler(RegexHandler('^(Прислать картинку)$', send_picture, pass_user_data=True)) 
    dp.add_handler(RegexHandler('^(Сменить аватар)$', change_avatar, pass_user_data=True))  
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))   
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))                                                      
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True ))           

    mybot.start_polling()
    mybot.idle()

main()