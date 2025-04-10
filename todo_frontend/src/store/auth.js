import { defineStore } from 'pinia';
import todoApi from '@/services/api';

/**
 * Auth Store
 * Управляет авторизацией, хранит access/refresh токены и данные пользователя.
 */
export const useAuthStore = defineStore('auth', {
    state: () => ({
        access: localStorage.getItem('access') || null,
        refresh: localStorage.getItem('refresh') || null,
        user: localStorage.getItem('user') || null,
    }),

    actions: {
        /**
         * Регистрация нового пользователя
         * @param {Object} credentials - { username, telegram_id }
         */
        async register(credentials) {
            try {
                console.log(credentials);
                const res = await todoApi.post('/auth/register/', credentials);
                this.user = res.data.username;
                localStorage.setItem('user', res.data.username);
            } catch (error) {
                console.error('Ошибка регистрации:', error);
                throw error;
            }
        },

        /**
         * Логин пользователя
         * @param {Object} credentials - { username }
         */
        async login(credentials) {
            try {
                const res = await todoApi.post('/auth/token/', {
                    username: credentials.username,
                    password: credentials.password,
                });
                this.setTokens(res.data.access, res.data.refresh);

                this.user = credentials.username;
                localStorage.setItem('user', credentials.username);
            } catch (error) {
                console.error('Ошибка логина:', error);
                throw error;
            }
        },

        /**
         * Обновление access токена по refresh токену
         */
        async refreshToken() {
            try {
                const res = await todoApi.post('/auth/token/refresh/', {
                    refresh: this.refresh,
                });
                this.setTokens(res.data.access, this.refresh);
            } catch (err) {
                console.warn('Не удалось обновить токен, выполняем logout');
                this.logout();
            }
        },

        /**
         * Выход пользователя
         * Очищает state и localStorage
         */
        logout() {
            this.access = null;
            this.refresh = null;
            this.user = null;
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            localStorage.removeItem('user');
            delete todoApi.defaults.headers.common['Authorization'];
        },

        /**
         * Устанавливает токены и заголовки авторизации
         * @param {string} access
         * @param {string} refresh
         */
        setTokens(access, refresh) {
            this.access = access;
            this.refresh = refresh;
            localStorage.setItem('access', access);
            localStorage.setItem('refresh', refresh);
            todoApi.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        },
    },
});
