# Микросервис для управления комментариями

## Описание
Этот микросервис создан для управления комментариями к задачам.

Интегрирован с основным API по управлению задачами [todo_api](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_api)

## Технологии

* _**Python 3.13**_
* **_FastApi_**
* **_SQLAlchemy_**
* _**Redis**_
* **_Docker_**

## Архитектура проекта

* **api/** - API-endpoints.
* **cache/** - класс для управления хранением комментариев в кеше Redis.
* **dependencies/** - зависимости, передаваемые в качетстве параметров к 
  endpoint-ам, в том числе провека принадлежности задачи текущему клиенту.
* **models/** - модель, описывающая сущность Комментарий.
* **repositories/** - взаимодействие с ORM SQLAlchemy при управлении 
  комментариями.
* **schemas/** - Pydanctic-модели для описания схемы отправляемых / 
  получаемых данных.
* **services/** - обобщённый сервис для реализации бизнес-логики совместно 
  на уровне БД и кеша Redis.
* **infra/** - инфраструктура для подготовки и деплоя бота в docker-compose

## Инструкция по запуску

1. Клонирование всего репозитория и переход в корневую директорию проекта
    ```bash 
       git clone https://github.com/Gricana/todo_bot_microservice.git && cd todo_bot_microservice
    ```

2. Настройка переменных окружения

   Перейдите сначала в файл [comments_api.env](https://github.com/Gricana/todo_bot_microservice/blob/main/comments_api/infra/api/comments_api.env) и
   укажите [пароль к БД](https://github.com/Gricana/todo_bot_microservice/blob/4fe7d93f5809100fa4602f5f850c19d879ad844b/comments_api/infra/api/comments_api.env#L7),
   а затем продублируйте [этот же пароль](https://github.com/Gricana/todo_bot_microservice/blob/4fe7d93f5809100fa4602f5f850c19d879ad844b/comments_api/infra/db/db.env#L3) в файл [db.env](https://github.com/Gricana/todo_bot_microservice/blob/main/comments_api/infra/db/db.env):

    ```bash 
    DB_PASSWORD=<DB_PASSWORD>
    ```
3. Запуск через Docker Compose

   Убедитесь, что у вас установлены Docker и Docker Compose, и Вы
   находитесь **в корневой директории проекта**.
   Затем выполните команду:

    ```bash
    docker-compose --env-file comments_api/infra/api/comments_api.env -f comments_api/infra/docker/docker-compose.comments.yml up -d
    ```

   Это поднимет сам микросервис, БД PostgreSQL и кеш Redis.

   ### Важные замечания! ⚠️
- Дайте разрешение всем bash-скриптам на выполнение в директориях [api](https://github.com/Gricana/todo_bot_microservice/tree/main/comments_api/infra/api) 
   и [db](https://github.com/Gricana/todo_bot_microservice/tree/main/comments_api/infra/db).
  
  Это можно сделать **из корневой директории проекта** с помощью команды:

  ```bash
  chmod +x comments_api/infra/api/*.sh && chmod +x comments_api/infra/db/*.sh
  ```

## Трудности и их решения

1. **Проверка принадлежности задачи пользователю / авторизация**

   Требовалось гарантировать, что пользователь может работать только с 
   комментариями к своим задачам, а ~~не к чужим~~. API не знает, кто 
   является владельцем задачи -> этой инфо обладает [todo_api](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_api).
   
   Рассматриваемые варианты - закешировать в том же Redis, но права могут поменяться / отозваться. 
   Передавать user_id в URL / теле запроса, но тогда придётся пренебречь проверкой принадлежности.

   #### Решение

    - При отправке каждого endpoint-a клиенту нужно передавать JWT-токен в 
      заголовке Authorization, [полученный из основного backend-a](https://github.com/Gricana/todo_bot_microservice/blob/4fe7d93f5809100fa4602f5f850c19d879ad844b/todo_api/users/urls.py#L10), 
      который управляет авторизацией.
      Для этого была реализована зависимость FastApi [check_task_ownership](https://github.com/Gricana/todo_bot_microservice/blob/4fe7d93f5809100fa4602f5f850c19d879ad844b/comments_api/dependencies/auth.py#L21), 
      которая добавляется к каждому запросу. 
   
      В ней сразу отправляется запрос к указанной в запросе задаче. 
      Данный endpoint основного API сразу проверяет авторизацию и 
      принадлежность задачи юзеру.
   
      Если вернул ответ с HTTP-кодом 200 - задача принадлежит клиенту. 
      
      В противном случае, API укажет, что либо передан неверный токен, либо 
      вернёт код 404, говорящий об отсутствии задачи с таким task_id у клиента.
      
      Инструментарий библиотеки _httpx_ позволяет сразу выбросить ошибку при неудаче.
   
   В результате была обеспечена актуальность данных основного API, 
   избежав при этом дублирования авторизации по микросервисам.
