# RESTful API сервис для реферальной системы.
API позволяет пользователям регистрироваться, опционально указывая реферальный код другого пользователя(реферера).

# Функционал
<ul>
  <li>Регистрация и аутентификация пользователя (JWT);</li>
  <li>Аутентифицированный пользователь имеет возможность создать или удалить свой реферальный код. 
    Одновременно может быть активен только 1 код. 
    При создании кода обязательно должен быть задан его срок годности;</li>
  <li>Возможность получения реферального кода по email адресу реферера;</li>
  <li>Возможность регистрации по реферальному коду в качестве реферала;</li>
  <li>Получение информации о рефералах по id 	реферера;</li>
  <li>UI документация (Swagger).</li>
  <li>Все основные контроллеры написаны с использованием асинхронных решений</li>
</ul>

# Основной стек
- Python 3.12
- Django 4.2
- djangorestframework 3.15.2
- djangorestframework-simplejwt 5.5.0
- drf-spectacular 0.28.0
- daphne 4.1.2
- adrf 0.1.9
- SMTP

## Запуск на локальной машине
Клонируем репозиторий:
```
~ git clone https://github.com/NailKalimov/ReferralAPI.git
```

Далее устанавливаем и активируем виртуальное окружение из папки с проектом
```
~ python -3.12 -m venv venv
~ . venv/Scripts/activate
```

Устанавливаем требуемые зависимости:
```
~ pip install -r requirements.txt
```

В файле settings.py инициализировать следующие параметры под вашу инфраструктуру:
```
- EMAIL_HOST = <Адрес почтового сервиса>
- EMAIL_PORT = <Порт используемый почтовым сервисом>
- EMAIL_USE_SSL = <True/False - выбрать использует ли данный протокол почтовый сервис>
- EMAIL_USE_TLS = <True/False - выбрать использует ли данный протокол почтовый сервис>
```
Требуется создать файл env.py в каталоге referralAPI/referralAPI/ и создать в нем переменные login и password для подключения SMTP

Переходим в папку
```
~ cd referralAPI
```

Перед первым запуском выполняем миграции:
```
python manage.py migrate
```

Создаем суперпользователя:
```
python manage.py createsuperuser
```

Запуск сервиса производится командой:
```
py manage.py runserver [--nothreding]
```

# Адресные пути
- [Документация к API базе данных](http://127.0.0.1:8000/api/schema/swagger-ui/)
- [Админ-панель базы данных](http://127.0.0.1:8000/admin)
