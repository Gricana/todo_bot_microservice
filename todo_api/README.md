# Cервис для управления задачами + авторизация

## Описание
Этот сервис создан для управления задачами, а также проведением процесса 
авторизации.


## Технологии

* _**Python 3.13**_
* **_Django 5.1.6_**
* **_Djangorestframework 3.15.2_**
* **_Celery_**
* _**Redis**_
* **_Docker_**

## Архитектура проекта

* **celery_tasks/** - Celery-задача для отправки уведомлений о наступлении 
  выполнения задачи.
* **tasks/** - Django-приложение для управления задачами + проверка прав.
* **users/** - Django-приложение для управления процессом авторизации и 
  создания нового пользователя.
* **infra/** - инфраструктура для подготовки и деплоя бота в docker-compose

## Инструкция по запуску

1. Клонирование всего репозитория и переход в корневую директорию проекта
    ```bash 
       git clone https://github.com/Gricana/todo_bot_microservice.git && cd todo_bot_microservice
    ```

2. Настройка переменных окружения

   Перейдите сначала в файл [tasks_api.env](https://github.com/Gricana/todo_bot_microservice/blob/main/todo_api/infra/api/tasks_api.env) 
   и укажите [секретный ключ](https://github.com/Gricana/todo_bot_microservice/blob/729780c71c528f59be0644609d68502b3ea0d14e/todo_api/infra/api/tasks_api.env#L5), 
   [учетные данные администратора](https://github.com/Gricana/todo_bot_microservice/blob/729780c71c528f59be0644609d68502b3ea0d14e/todo_api/infra/api/tasks_api.env#L10), 
   [пароль БД](https://github.com/Gricana/todo_bot_microservice/blob/729780c71c528f59be0644609d68502b3ea0d14e/todo_api/infra/api/tasks_api.env#L18).
    ```bash 
    SECRET_KEY=<SECRET_KEY>
    
    # Admin user credentials
    ADMIN_USERNAME=<ADMIN_USERNAME>
    ADMIN_PASSWORD=<ADMIN_PASSWORD>
    ADMIN_EMAIL=<ADMIN_EMAIL>
    
    # DB vars
    DB_PASSWORD=<DB_PASSWORD>
    ```
    В файле [db.env](https://github.com/Gricana/todo_bot_microservice/blob/main/todo_api/infra/db/db.env) продублируйте [пароль БД](https://github.com/Gricana/todo_bot_microservice/blob/729780c71c528f59be0644609d68502b3ea0d14e/todo_api/infra/db/db.env#L3).

3. Запуск через Docker Compose

   Убедитесь, что у вас установлены Docker и Docker Compose, и Вы
   находитесь **в корневой директории проекта**.
   Затем выполните команду:

    ```bash
   docker-compose --env-file todo_api/infra/api/tasks_api.env -f todo_api/infra/docker/docker-compose.tasks.yml up -d
    ```

   Это поднимет основной backend, БД PostgreSQL, кеш Redis, а также 
   прокси-сервер Nginx для рендеринга статики.

   ### Важные замечания! ⚠️

   - **HTTP-порт 80 должен быть свободен!**

     Если данный порт занят - выполните команду:
     ```bash 
     sudo kill -9 $(sudo lsof -t -i:80)
     ```
   - Дайте разрешение всем bash-скриптам на выполнение в директориях [api](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_api/infra/api) 
     и [db](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_api/infra/db). 
  
     Это можно сделать **из корневой директории проекта** с помощью команды:

     ```bash
     chmod +x todo_api/infra/api/*.sh && chmod +x todo_api/infra/db/*.sh
     ```

4. Перейдите в [административную панель](http://localhost/admin)

## Трудности и их решения

1. **Связывание учётной записи пользователя Telegram с профилем 
   пользователя в системе**

   Обеспечить связь между данными пользователя из Telegram и существующей 
   системой пользователей, чтобы идентифицировать и аутентифицировать пользователей 
   на основе их Telegram-аккаунтов.

   #### Решение

    - Вместо полной замены стандартной модели пользователя Django через `AbstractBaseUser`, 
      было решено расширить её функциональность. 
   
      Создана модель [`UserProfile`](https://github.com/Gricana/todo_bot_microservice/blob/083b038d47955e5cbe5eaa6cd5185609e0031310/todo_api/users/models.py#L8), 
      которая использует OneToOneField для связи с моделью User. 
      Это позволило добавить дополнительные поля, специфичные для интеграции 
      с Telegram, без изменения основной модели пользователя.
   
    -  В представлении [`TelegramRegisterView`](https://github.com/Gricana/todo_bot_microservice/blob/083b038d47955e5cbe5eaa6cd5185609e0031310/todo_api/users/views.py#L15) 
       была реализована логика обработки запросов на регистрацию 
       пользователей через Telegram. Для регистрации требуется передать 
       только id telegram-чата и username пользователя в Telegram.

   В результате удалось эффективно интегрировать систему с Telegram, 
   обеспечивая seamless-авторизацию пользователей и управление их профилями,
   при этом сохраняя гибкость и расширяемость системы в будущем.


2. **Переопределение процесса выдачи JWT-токенов для пользователей Telegram**

   В стандартной реализации библиотеки djangorestframework-simplejwt для получения JWT-токена 
   требуется ввод имени пользователя и пароля. 
   Однако в случае взаимодействия через Telegram-бота пользователи не имеют пароля, 
   что делает стандартный процесс аутентификации неприменимым.

   #### Решение

    - Были созданы классы [`TokenObtainPairFromBotView`](https://github.com/Gricana/todo_bot_microservice/blob/083b038d47955e5cbe5eaa6cd5185609e0031310/todo_api/users/views.py#L49) 
      и [`TokenRefreshFromBotView`](https://github.com/Gricana/todo_bot_microservice/blob/083b038d47955e5cbe5eaa6cd5185609e0031310/todo_api/users/views.py#L74), 
      наследующиеся от `TokenObtainPairView` и `TokenRefreshView` соответственно. 
      Эти классы переопределяют методы для обработки токенов без необходимости ввода пароля.
   
      - `TokenObtainPairFromBotView`: Этот класс переопределяет метод post, 
        чтобы принимать данные от Telegram-бота, идентифицировать пользователя 
        только по username и выдавать JWT-токены без требования пароля. 
      - `TokenRefreshFromBotView`: Этот класс переопределяет метод post, чтобы 
        обновлять JWT-токены на основе предоставленного refresh-токена, 
        без необходимости повторной аутентификации пользователя с 
        использованием пароля. При этом учтена ошибка передачи невалидного
        токена при его обновлении.
    
    Таким образом, был сделан ещё один шаг к переходу от cтандартной 
   к seamless-авторизации. 


3. **Каскадное удаление комментариев при удалении задачи**

   При удалении задачи необходимо отправить запрос к [API комментариев](https://github.com/Gricana/todo_bot_microservice/blob/083b038d47955e5cbe5eaa6cd5185609e0031310/comments_api/api/comments.py#L63), 
   для удаления связанных с этой задачей комментариев. 
   Первоначально планировалось использовать сигнал pre_delete модели Task для 
   автоматизации этого процесса. 
   Однако возникла проблема: API требует передачи JWT-токена для 
   проверки принадлежности задачи клиенту, а в контексте сигнала доступ к текущему токену, 
   сгенерированному simplejwt, отсутствует.

   #### Решение
   
   - Решено было при удалении задачи в боте вызывать [отдельную функцию](https://github.com/Gricana/todo_bot_microservice/blob/083b038d47955e5cbe5eaa6cd5185609e0031310/bot/handlers/tasks.py#L300), 
     которая отправляет запрос к API комментариев для удаления связанных с задачей комментариев.


   В результате вместо усложнения модели Task дополнительной логикой, 
   связанной с внешними API, вся необходимая функциональность сосредоточена в боте, 
   что делает код более понятным и поддерживаемым.
 
   Такой подход позволяет более гибко управлять процессом удаления 
   комментариев и обрабатывать возможные ошибки при взаимодействии со сторонним API 
   непосредственно в боте.