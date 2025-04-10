import { createRouter, createWebHistory } from "vue-router";

import TodoList from "@/components/todo/TodoList.vue";
import TodoForm from "@/components/todo/TodoForm.vue";
import AuthView from "@/components/auth/AuthView.vue";

import { useAuthStore } from "@/store/auth";

/**
 * Определение маршрутов приложения.
 */
const routes = [
    {
        path: '/',
        name: 'Home',
        component: TodoList,
        meta: { requiresAuth: true },
    },
    {
        path: '/new',
        name: 'NewTodo',
        component: TodoForm,
        meta: { requiresAuth: true },
    },
    {
        path: '/edit/:id',
        name: 'EditTodo',
        component: TodoForm,
        props: true, // Пробрасываем :id как пропс в компонент
        meta: { requiresAuth: true },
    },
    {
        path: '/login',
        name: 'Login',
        component: AuthView,
        meta: { requiresGuest: true },
    },
];


const router = createRouter({
    history: createWebHistory(),
    routes,
});

/**
 * Глобальный navigation guard.
 * Выполняется перед каждым переходом.
 * Проверяет:
 * - если маршрут требует авторизации и пользователь не вошёл — перенаправляет на login
 * - если маршрут только для гостей, но пользователь уже авторизован — отправляет на главную
 */
router.beforeEach((to, from, next) => {
    const auth = useAuthStore();

    if (to.meta.requiresAuth && !auth.user) {
        next({ name: 'Login' });
    } else if (to.meta.requiresGuest && auth.user) {
        next({ name: 'Home' });
    } else {
        next();
    }
});

export default router;
