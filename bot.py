import requests
import telebot
from telebot import types
import json
from geopy import geocoders

# Токен бота
bot_token = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(bot_token)


# Функция для получения геолокации по адресу
def get_location_by_address(message):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    location = geolocator.geocode(message.text)
    if location is None:
        bot.send_message(message.chat.id, 'Я не знаю адрес, который вы ввели')
    else:
        latitude, longitude = location.latitude, location.longitude
        weather_info = get_weather_info(latitude, longitude)
        send_weather_response(weather_info, message)


# Функция для получения погоды по координатам
def get_weather_info(latitude, longitude):
    yandex_token = 'YOUR_YANDEX_TOKEN'
    url = f'https://api.weather.yandex.ru/v2/forecast/?lat={latitude}&lon={longitude}&[lang=ru_RU]'

    headers = {'X-Yandex-API-Key': yandex_token}
    yandex_weather_response = requests.get(url, headers=headers, verify=True)
    yandex_data = json.loads(yandex_weather_response.text)

    # Словари для перевода условий погоды и направления ветра
    conditions_translation = {
        'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
        'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
        'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
        'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
        'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
        'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
        'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
    }

    wind_direction_translation = {
        'nw': 'северо-западный', 'n': 'северный', 'ne': 'северо-восточный', 'e': 'восточный',
        'se': 'юго-восточный', 's': 'южный', 'sw': 'юго-западный', 'w': 'западный', 'с': 'штиль'
    }

    # Обработка температурных значений
    if int(yandex_data['fact']['temp']) < 0:
        yandex_data['fact']['temp'] = '-' + str(yandex_data['fact']['temp']) + '°'
    elif int(yandex_data['fact']['temp']) > 0:
        yandex_data['fact']['temp'] = '+' + str(yandex_data['fact']['temp']) + '°'
    if int(yandex_data['fact']['feels_like']) < 0:
        yandex_data['fact']['feels_like'] = '-' + str(yandex_data['fact']['feels_like']) + '°'
    elif int(yandex_data['fact']['feels_like']) > 0:
        yandex_data['fact']['feels_like'] = '+' + str(yandex_data['fact']['feels_like']) + '°'

    # Перевод условий и направления ветра
    yandex_data['fact']['condition'] = conditions_translation[yandex_data['fact']['condition']]
    yandex_data['fact']['wind_dir'] = wind_direction_translation[yandex_data['fact']['wind_dir']]

    weather_details = dict(
        temp=yandex_data['fact']['temp'],
        feels=yandex_data['fact']['feels_like'],
        condition=yandex_data['fact']['condition'],
        wind=yandex_data['fact']['wind_dir'],
        wind_speed=yandex_data['fact']['wind_speed'],
        pressure_mm=yandex_data['fact']['pressure_mm'],
    )

    return weather_details


# Функция для отправки погодных данных пользователю
def send_weather_response(weather_info, message):
    bot.send_message(message.chat.id, f'На улице {weather_info["condition"]}')
    bot.send_message(message.chat.id, f'{weather_info["temp"]} градусов, по ощущениям {weather_info["feels"]}')
    bot.send_message(message.chat.id, f'Ветер {weather_info["wind"]} {weather_info["wind_speed"]}м/с')
    bot.send_message(message.chat.id, f'Давление {weather_info["pressure_mm"]}мм ртутного столба')


# Обработчики сообщений для команд и текста
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создание клавиатуры
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    geo_btn = types.KeyboardButton(text='Гео', request_location=True)
    address_btn = types.KeyboardButton(text='Адрес')
    help_btn = types.KeyboardButton(text='Помощь')
    keyboard.add(geo_btn, address_btn, help_btn)

    bot.send_message(message.chat.id, f'Я погодный бот, чем могу вам помочь?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if message.text == 'Помощь':
        bot.send_message(message.chat.id, 'Я могу показать погодные данные по вашему местоположению')
        bot.send_message(message.chat.id, 'Вы можете отправить адрес или геолокацию')
    elif message.text == 'Адрес':
        bot.send_message(message.chat.id, 'Пример: "город", "улица" "номер дома"')
        msg_prompt = bot.send_message(message.chat.id, 'Введите адрес:')
        bot.register_next_step_handler(msg_prompt, get_location_by_address)


@bot.message_handler(content_types=['location'])
def handle_location_message(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    weather_info = get_weather_info(latitude, longitude)
    send_weather_response(weather_info, message)


bot.polling()