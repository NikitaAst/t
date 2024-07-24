# Суть проекта

Необходимо написать небольшое приложение на Django и Django Rest Framework для получения списка объявлений.

## Models
* Category - категории объявлений, поля: name
* City - город объявления, поля: name
* Advert - объявление, поля: created_at, title, description, city, category, views

## Views
* {{ base_url }}/api/adverts/ - JSON список объявлений со всеми полями + название города + название категории

Просмотр одного объекта реализован через фильтрацию по UUID. 
Для инкрементации количества просмотров используется функция внутри PostgreSQL, 
которая может быть вынесена в pgcron для дальнейшей оптимизации.

## Запрос можно фильтровать и сортировать по следующим полям:
* title
* description
* views
* category__name
* city__name
* created_at
* uuids(список через азпятую, например: ?uuids=02707811-6147-4540-becd-87d80929114b,689ec1f5-080f-4f8f-8020-a4afc0162d06)

## Обоснование выбора метода запроса
Выбранный метод запроса оптимизирован под скорость и требует мало памяти, но мощный CPU. 
Возможно, при высоких RPS он будет не самым оптимальным. 
Создание views для PostgreSQL было бы очевидным и неинтересным путем, 
к тому же при уходе от views можно реализовать partitioning и еще больше оптимизировать скорость и нагрузку.


# Запуск проекта

## Клонируйте репозиторий:
* git clone <URL>
* cd <в папку проекта>

## Постройте и запустите контейнеры с помощью Docker Compose:

* docker-compose up --build

## В другом окне терминала:
* docker-compose exec web /bin/sh
* python manage.py migrate

Во время миграции будут созданны 2 миллиона записей, это может занять некоторое время.


# Производительность

## Скорость выполнения запросов на базовом MBP M1 Pro по базе с 2М записей.


#### Запрос без фильтров: http://127.0.0.1:8002/api/adverts/ 
* Query took 0.4401 seconds
* Total request processing took 0.4445 seconds
* Total records count: 2000000

#### http://127.0.0.1:8002/api/adverts/?page=1000
* Query took 0.3429 seconds
* Total request processing took 0.3467 seconds
* Total records count: 2000000


#### http://127.0.0.1:8002/api/adverts/?category__name=HiryQyLvSG&ordering=-views
* Query took 0.4786 seconds
* Total request processing took 0.4821 seconds
* Total records count: 200042


#### http://127.0.0.1:8002/api/adverts/?ordering=-views&city__name=zcoRmXNHZT
* Query took 0.5992 seconds
* Total request processing took 0.6031 seconds
* Total records count: 199810


#### http://127.0.0.1:8002/api/adverts/?uuids=514ca109-d004-4b38-80b9-8894f5984ab3
* Query took 0.0014 seconds
* Total request processing took 0.0117 seconds
* Total records count: 1
