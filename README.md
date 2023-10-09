Реализовано API, которое на HTTP-запрос GET /weather/?city=<city_name>, где 
<city_name> - это название города на русском языке, возвращает текущую 
температуру в этом городе в градусах Цельсия, атмосферное давление (мм рт.ст.) и
скорость ветра (м/с). При первом запросе, приложение получает данные через "API Яндекс.Погоды" 
о погоде в городе (кстати погоду можно получить только из заранее определенных городах
в модели CityModel, т.е. количество городов, которые пользователь может вписать на место <city_name>
нарямую зависит от того, что определено в CityModel) и добавляет в собственную БД, вешается task библиотеки 
Celery на поле isReady модели  CityModel, чтобы через 30 мин из положения True, перевести в False. 
Это позволяет не совершать запросы на сервис yandex при последующих запросах для этого города в течение получаса.


Также реализован телеграм бот, который после нажатия кнопки "Узнать погоду" и получения названия города
присылает в ответ прогноз погоды.

Написано два unit-теста для проверки моделей в Django и проверки корректности ответа приложения на GET запрос.

Запуск проекта
Для запуска проекта нужен один из дистрибутивов Linux или WSL, установленная СУБД PostgreSQL и docker.
Далее все по инструкции ниже.
1. клонируем репозиторий
git clone git@github.com:EgorK39/weather_api_with_bot.git или git clone https://github.com/EgorK39/weather_api_with_bot.git
2. cd weather_api_with_bot
3. создаем виртуальное окружение
python3 -m venv venv
4. активируем venv
source venv/bin/activate
5. устанавливаем зависимост
python -m pip install -r requirements.txt
Если возникнет конфликт с библиотекой backports.zoneinfo, то просто удалите ее из requirements.txt и повторите еще 
команду python -m pip install -r requirements.txt
6. запускаем в терминале службу postgresql
sudo service postgresql start
7. заходим в postgres
sudo -u postgres psql
8. создаем БД
CREATE DATABASE bot;
9. подключаемся к БД bot
10. Создаем файлик в корне проекта под названием .env
sudo vi .env
11. В .env добавляем константы по образцу с .env.example
SECRET_KEY='django-icue-zsm4kp=fhysjst=!024p^yrddackx%4@f01-uvpa' - секретный ключ (тут указан нерабочий ключ), можно взять из других приложений на django;
DATABASE_NAME='new_bot' - имя базы данных, которое мы только что придумали;
USER_NAME='postgres' - имя пользователя БД (по дефолту это postgres);
DATABASE_PASSWORD='qwerty1234' - пароль от БД;
X-Yandex-API-Key='key' - секретный ключ для работы с API yandex.
Его можно получить по ссылке https://yandex.ru/dev/weather/doc/dg/concepts/forecast-info.html
token='612279:AAGOLax5auLSzs4x42hT2pVZr8' - токен телеграм бота (тут указан нерабочий токен), необходимо зарегистрировать своего бота.
12. Запускаем службу Docker
sudo service docker start
13. Запускаем image RabbitMQ. У меня он используется в качестве брокера сообщений.
sudo docker run -d -p 5672:5672 rabbitmq
14. cd project
15. формируем  миграции 
python manage.py makemigrations
16. делаем миграции
python manage.py migrate
17. создаем супер пользователя
python manage.py createsuperuser
18. далее опять заходим в postgres. Чтобы вручную не вводить начальные данные, я подготовил файл с данными (городами)
sudo -u postgres psql
19. заходим в нашу бзу данных
\c bot
20. и выполняем следующую команду, но перед этим поменяйте путь до файла initialState.csv. Путь до файла должен быть абсолютный.
Команда выглядит так: COPY backend_citymodel FROM '/mnt/d/USER/Documents/ALL_PROJECTS/bot/initialData/initialState.csv' DELIMITER ';' CSV HEADER encoding 'windows-1251';
Вам нужно вместо "/mnt/d/USER/Documents/ALL_PROJECTS/bot/initialData" вставить свой путь.
21. Далее делаем так, чтобы можно было без каких-либо ошибок добавлять данные в эту таблицу . Выполняем команду:
ALTER SEQUENCE backend_citymodel_id_seq restart with 49;
22. выходим из бд
\q
23. Осталось только запустить приложение:
в одном терминале выполняем команду 
python manage.py runserver
во втором открытом терминале выполняем команду (запускаем celery)
celery -A project worker -l INFO
в третьем окне выполняем команду (запуск телеграм бота)
python telegramBot/botMain.py

24. Работа с ботом:
/start - начать работу с ботом
/help - помощь
Список городов, которые обрабатывает бот, Вы можете найти в initialState.xlsx (Калининград, Москва, Санкт-Петербург и др.)
25. Запуск тестов:
python manage.py test