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
<hr>
<h3>Запуск проекта</h3>
Для запуска проекта нужен один из дистрибутивов Linux или WSL, установленная СУБД PostgreSQL, docker и python:3.9.<br>
Далее все по инструкции ниже.

<ol>
  <li>
    <p>клонируем репозиторий:</p>
      <ul>
          <li>git clone git@github.com:EgorK39/weather_api_with_bot.git или git clone https://github.com/EgorK39/weather_api_with_bot.git</li>
      </ul>
  </li>
  <li>
    <h4>cd weather_api_with_bot</h4>
  </li>
  <li>
    <p>создаем виртуальное окружение:</p>
    <ul>
      <li><h4>python3 -m venv venv</h4></li>
    </ul>
  </li>
  <li>
    <p>активируем venv:</p>
    <ul>
      <li><h4>source venv/bin/activate</h4></li>
    </ul>
  </li>
  <li>
    <p>устанавливаем зависимости:</p>
    <ul>
      <li><h4>python -m pip install -r requirements.txt</h4></li>
      <li>Если возникнет конфликт с библиотекой backports.zoneinfo, то просто удалите ее из requirements.txt и повторите еще раз 
команду: <h4>python -m pip install -r requirements.txt</h4></li>
    </ul>
  </li>
  <li>
    <p>запускаем в терминале службу postgresql:</p>
    <ul>
      <li><h4>sudo service postgresql start</h4></li>
    </ul>
  </li>
  <li>
    <p>заходим в postgres:</p>
    <ul>
      <li><h4>sudo -u postgres psql</h4></li>
    </ul>
  </li>
  <li>
    <p>создаем БД:</p>
    <ul>
      <li><h4>CREATE DATABASE bot;</h4></li>
    </ul>
  </li>
  <li>
    <p>cоздаем файлик в корне проекта под названием .env:</p>
    <ul>
      <li><h4>sudo vi .env</h4></li>
    </ul>
  </li>
  <li>
    <p>в .env добавляем константы по образцу с .env.example:</p>
    <ul>
      <li>SECRET_KEY='django-icue-zsm4kp=fhysjst=!024p^yrddackx%4@f01-uvpa' - секретный ключ (тут указан нерабочий ключ), можно взять из других приложений на django;</li>
      <li>DATABASE_NAME='new_bot' - имя базы данных, которое мы только что придумали;</li>
      <li>USER_NAME='postgres' - имя пользователя БД (по дефолту это postgres);</li>
      <li>DATABASE_PASSWORD='qwerty1234' - пароль от БД;</li>
      <li>X-Yandex-API-Key='key' - секретный ключ для работы с API yandex. Его можно получить по <a href="https://yandex.ru/dev/weather/doc/dg/concepts/forecast-info.html">ссылке</a></li>
      <li>token='612279:AAGOLax5auLSzs4x42hT2pVZr8' - токен телеграм бота (тут указан нерабочий токен), необходимо зарегистрировать своего бота.
      <a href="https://t.me/BotFather">BotFather</a></li>
    </ul>
  </li>
   <li>
     <p>Запускаем службу Docker:</p>
    <ul>
      <li><h4>sudo service docker start</h4></li>
    </ul>
  </li>
  <li>
    <p>Запускаем image RabbitMQ. У меня он используется в качестве брокера сообщений:</p>
    <ul>
      <li><h4>sudo docker run -d -p 5672:5672 rabbitmq</h4></li>
    </ul>
  </li>
  <li>
    <ul>
      <li><h4>cd project</h4></li>
    </ul>
  </li>
  <li>
    <p>формируем  миграции:</p>
    <ul>
      <li><h4>python manage.py makemigrations</h4></li>
    </ul>
  </li>
  <li>
    <p>делаем миграции:</p>
    <ul>
      <li><h4>python manage.py migrate</h4></li>
    </ul>
  </li>
  <li>
    <p>создаем супер пользователя:</p>
    <ul>
      <li><h4>python manage.py createsuperuser</h4></li>
    </ul>
  </li>
  <li>
    <p>далее опять заходим в postgres. Чтобы вручную не вводить начальные данные, я подготовил файл с данными (городами):</p>
    <ul>
      <li><h4>sudo -u postgres psql</h4></li>
    </ul>
  </li>
  <li>
    <p>заходим в нашу бзу данных:</p>
    <ul>
      <li><h4>\c bot</h4></li>
    </ul>
  </li>
  <li>
    <p>выполняем следующую команду, но перед этим поменяйте путь до файла <b>initialState.csv</b>. Путь до файла должен быть <b>абсолютный</b>.
Команда выглядит так:</p>
    <ul>
      <li><h4>COPY backend_citymodel FROM '/mnt/d/USER/Documents/ALL_PROJECTS/bot/initialData/initialState.csv' DELIMITER ';' CSV HEADER encoding 'windows-1251';</h4></li>
      <li>Вам нужно вместо "/mnt/d/USER/Documents/ALL_PROJECTS/bot/initialData" вставить свой путь.</li>
    </ul>
  </li>
  <li>
    <p>Далее делаем так, чтобы можно было без каких-либо ошибок добавлять данные в эту таблицу . Выполняем команду:</p>
    <ul>
      <li><h4>ALTER SEQUENCE backend_citymodel_id_seq restart with 49;</h4></li>
    </ul>
  </li>
   <li>
     <p>выходим из бд:</p>
    <ul>
      <li><h4>\q</h4></li>
    </ul>
  </li>
  <li>
    <h4>Осталось только запустить приложение</h4>
    <ul>
      <li>в одном терминале выполняем команду:</li>
      <li><h4>python manage.py runserver</h4></li>
    </ul>
    <ul>
      <li>во втором открытом терминале выполняем команду (запускаем celery):</li>
      <li><h4>celery -A project worker -l INFO</h4></li>
    </ul>
    <ul>
      <li>в третьем окне выполняем команду (запуск телеграм бота):</li>
      <li><h4>python telegramBot/botMain.py</h4></li>
    </ul>
  </li>
</ol>
<hr>
<ul>
  <h4>Работа с ботом:</h4>
  <li><b>/start</b> - начать работу с ботом</li>
  <li><b>/help</b> - помощь</li>
  <li>Список городов, которые обрабатывает бот, Вы можете найти в <b><a href="https://github.com/EgorK39/weather_api_with_bot/blob/main/initialData/initialState.xlsx">initialState.xlsx</a></b> (Калининград, Москва, Санкт-Петербург и др.)</li>
</ul>
<hr>
<ul>
  <h4>Запуск тестов:</h4>
  <li>python manage.py test</li>
</ul>
