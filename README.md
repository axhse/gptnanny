
### Прототип проекта GPT-консультанта для родителей

Текущие возможности:
1. Получение ответа на вопрос об уходе за ребенком
2. Редактирование статей, на основе которых формируется ответ

Ответ формируется внешним GPT-based сервисом на основе составляемой нами базы знаний  
Для перевода вопросов и ответов на русский язык используется внешний сервис-переводчик  

### Сборки

Существует 2 варианта сборки приложения:
1. `prod` - полноценная сборка, для которой необходимо подключение к внешним сервисам (указание API-ключей)
2. `mock` - cборка, в которой симулируется работа внешних сервисов, сохраняется структура сайта. Не требуются внешние зависимости, но функционал ограничен

Варинат сборки нужно указывать в переменной окружения `APPCONF` (по умолчанию `mock`)  

### Запуск (локально)

Клонирование репозитория
```
git clone https://github.com/axhse/gptnanny

```

#### Docker

Можно собрать проект в Docker и запустить  

1. Сборка
```
docker build -t gptnanny .

```

2. Запуск `mock` сборки
```
docker run -it -p 8000:8000 -e MANAGER_TOKEN=4444 gptnanny

```
Приложение должно запуститься на http://localhost:8000  
Вход в панель менеджера — http://localhost:8000/manage  
Токен (пароль) менеджера — `4444`

3. Запуск `prod` сборки

Создать файл **.env** по шаблону **.env.example**, в котором определить:  
1) MANAGER_TOKEN — токен для менеджера
2) XATA_API_KEY — api-ключ для сервиса xata.io
3) LECTO_API_KEY — api-ключ для сервиса-переводчика lecto.ai

```
docker run -it -p 8000:8000 --env-file .env gptnanny

```

4. Дополнительно

Можно использовать уже собранный образ
```
docker pull axhse/gptnanny

```

Запуск тех же контейнеров в режиме **detached**
```
docker run -d -p 8000:8000 -e MANAGER_TOKEN=4444 gptnanny

```
```
docker run -d -p 8000:8000 --env-file .env gptnanny

```

#### PyCharm

1. Установить Python3.9.10 (может подойти любая версия 3.9 и выше)
2. Открыть папку с кодом как PyCharm-проект (версия PyСharm должна поддерживать Python3.9, например Community 2021+), добавить виртуальную среду  
*Альтернатива: Использовать напрямую терминал, находясь внутри папки с проектом (можно в виртуальной среде, можно нет)*  

3. Выставление переменных окружения

Обязательно установить MANAGER_TOKEN

Linux
```
export MANAGER_TOKEN=4444

```

Windows
```
set MANAGER_TOKEN=4444

```

Для `prod` сборки обязательно выставить:  
1) APPCONF=prod
2) XATA_API_KEY — api-ключ для сервиса xata.io
3) LECTO_API_KEY — api-ключ для сервиса-переводчика lecto.ai

4. Установка зависимостей
```
pip install -r requirements.txt

```

5. Подготовка проекта
```
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py setup

```

6. Запуск проекта
```
python manage.py runserver 0.0.0.0:8000

```

http://localhost:8000  
http://localhost:8000/manage  

### Demo

Страница поиска  
<img src="img/search.png" width="683"/>

Страница со списком использующихся статей  
<img src="img/articles.png" width="683"/>

Страница редактирования статьи  
<img src="img/edit_article.png" width="683"/>
