# Фронтенд для сервиса управления задачами

## Описание
Этот проект реализует клиентскую часть (интерфейс) сервиса управления задачами 
с поддержкой авторизации через Telegram.

## Технологии

* _**Vue 3**_
* **_Vite_**
* **_Pinia_**
* **_Vue Router_**
* _**Luxon**_
* **_Docker_**
* **_Nginx_**

## Архитектура проекта

* **components/** - Основные компоненты (TodoList, TodoItem, TodoForm, AuthView).
* **router/** - Настройка маршрутов Vue Router.
* **store/** - Состояние приложения (auth, tasks).
* **services/** - Настройка API-клиента.
* **infra/** - инфраструктура для подготовки и деплоя бота в docker-compose

## Инструкция по запуску

1. Клонирование всего репозитория и переход в корневую директорию проекта
    ```bash 
       git clone https://github.com/Gricana/todo_bot_microservice.git && cd todo_bot_microservice
    ```

2. Запуск через Docker Compose

   Убедитесь, что у вас установлены Docker и Docker Compose, и Вы
   находитесь **в корневой директории проекта**.
   Затем выполните команду:

    ```bash
   docker-compose -f todo_frontend/infra/docker/docker-compose.frontend.yml up -d
    ```

   Это запустит фронтенд-сервер вместе с Nginx, который будет обслуживать 
 статические файлы.


3. Перейдите на [сайт](http://localhost:8081)
