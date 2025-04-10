# Todo Bot Microservice

## Обзор

**Todo Bot Microservice** — это модульная система, предназначенная для управления задачами 
и связанными с ними комментариями через интерфейс Telegram-бота. 

Она использует микросервисную архитектуру для обеспечения масштабируемости и удобства сопровождения, состоящую из трех основных компонентов:

* [**_Telegram-бот_**](https://github.com/Gricana/todo_bot_microservice/tree/main/bot): 
  Обеспечивает взаимодействие с пользователем для управления задачами через 
  Telegram.

* [**_API управления задачами (todo_api)_**](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_api): 
  Отвечает за основные операции, связанные с задачами и аутентификацией пользователей.

* [**_API комментариев (comments_api)_**](https://github.com/Gricana/todo_bot_microservice/tree/main/comments_api): 
  Управляет комментариями, связанными с задачами.
* [**_Фронтенд (todo_frontend)_**](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_frontend):
  Реализует клиентскую часть сервиса управления задачами.

## Особенности

* _Управление задачами_: Создание, обновление, удаление и получение задач.
* _Работа с комментариями_: Добавление, просмотр и удаление комментариев, связанных с конкретными задачами.
* _Интеграция с Telegram_: Взаимодействие с системой через friendly UI Telegram-бота.
* _Веб-интерфейс_: Дополнительное взаимодействие с системой через friendly Web UI.
* _Микросервисная архитектура_: Каждый компонент работает как независимый сервис, что повышает модульность и упрощает сопровождение.

## Развёртывание

Каждый сервис в составе Todo Bot Microservice упакован в свой перечень
Docker-контейнеров, что упрощает развёртывание и масштабирование. 

Подробные инструкции по настройке каждого компонента доступны в соответствующих директориях:

* **Telegram-бот (bot)**: [Инструкция по запуску](https://github.com/Gricana/todo_bot_microservice/tree/main/bot#%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D1%83)
* **API управления задачами (todo_api)**: [Инструкция по запуску](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_api#%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D1%83)
* **API комментариев (comments_api)**: [Инструкция по запуску](https://github.com/Gricana/todo_bot_microservice/tree/main/comments_api#%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D1%83)
* **Фронтенд (todo_frontend)**: [Инструкция по запуску](https://github.com/Gricana/todo_bot_microservice/tree/main/todo_frontend#%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D1%83)

Для полноценного развертывания убедитесь, что каждый сервис настроен 
и запущен в соответствии с предоставленными рекомендациями.