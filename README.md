# Pogodniy Bot

Этот телеграм-бот позволяет пользователям узнавать погодные условия по их местоположению или введенному адресу.

## Основные функции

- Получение погоды по геолокации пользователя.
- Получение погоды по введенному адресу.

## Используемые библиотеки и сервисы

- Telebot — для работы с Telegram API.
- Requests — для выполнения HTTP-запросов.
- Geopy — для геокодирования адресов.
- Yandex Weather API — для получения погодной информации.

## Установка

1. Клонируйте репозиторий:

        git clone https://github.com/your-username/your-repository-name.git

2. Установите необходимые зависимости:

        pip install telebot requests geopy

3. Замените YOUR_BOT_TOKEN и YOUR_YANDEX_TOKEN в коде на ваши реальные токены.
4. Запустите бота:

        python your_script_name.py

## Использование

После запуска бота:

1. Откройте Telegram и начните диалог с вашим ботом.
2. Нажмите на кнопку "Гео", чтобы получить погоду по вашему текущему местоположению или "Адрес", чтобы ввести адрес
   вручную.

Примечание: Не забудьте заменить your-username, your-repository-name и your_script_name.py на реальные значения,
соответствующие вашему проекту. Также убедитесь, что вы не делитесь своими токенами в общедоступных репозиториях на
GitHub или в других местах.