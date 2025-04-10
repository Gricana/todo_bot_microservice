import { defineStore } from "pinia";
import todoApi from "@/services/api";

/**
 * Todo Store
 * Хранит состояние задач и управляет всеми запросами к API
 */
export const useTodoStore = defineStore('todos', {
    state: () => ({
        todos: [],        // Список задач
        loading: false,   // Индикатор загрузки
        error: null,      // Сообщение об ошибке (если есть)
    }),

    actions: {
        /**
         * Обёртка для асинхронных API-запросов с общим обработчиком состояния
         * @param {Function} apiCall - функция запроса
         * @param {Function} onSuccess - обработчик успешного ответа
         */
        async performApiCall(apiCall, onSuccess) {
            this.loading = true;
            this.error = null;
            try {
                const response = await apiCall();
                onSuccess(response.data);
            } catch (err) {
                this.error = err.message;
                throw err;
            } finally {
                this.loading = false;
            }
        },

        /**
         * Получение всех задач с сервера
         */
        async fetchTodos() {
            await this.performApiCall(
                () => todoApi.get('/api/tasks'),
                (data) => {
                    this.todos = data.tasks;
                }
            );
        },

        /**
         * Добавление новой задачи
         * @param {Object} todoData - данные новой задачи
         */
        async addTodo(todoData) {
            await this.performApiCall(
                () => todoApi.post('/api/tasks', todoData),
                (data) => {
                    this.todos.push(data);
                }
            );
        },

        /**
         * Обновление существующей задачи
         * @param {string} todoId - ID задачи
         * @param {Object} todoData - обновлённые данные
         */
        async updateTodo(todoId, todoData) {
            await this.performApiCall(
                () => todoApi.patch(`/api/tasks/${todoId}`, todoData),
                (data) => {
                    this.todos = this.todos.map(todo => (todo.id === todoId ? data : todo));
                }
            );
        },

        /**
         * Удаление задачи
         * @param {string} todoId - ID задачи
         */
        async deleteTodo(todoId) {
            await this.performApiCall(
                () => todoApi.delete(`/api/tasks/${todoId}`),
                () => {
                    this.todos = this.todos.filter(todo => todo.id !== todoId);
                }
            );
        },

        /**
         * Смена статуса задачи (TODO, IN_PROGRESS, DONE)
         * @param {string} todoId
         * @param {string} newStatus
         */
        async toggleTodoStatus(todoId, newStatus) {
            const statuses = ["TODO", "IN_PROGRESS", "DONE"];
            if (!statuses.includes(newStatus)) return;

            await this.performApiCall(
                () => todoApi.patch(`/api/tasks/${todoId}`, { status: newStatus }),
                (data) => {
                    this.todos = this.todos.map(todo => (todo.id === todoId ? data : todo));
                }
            );
        }
    }
});
