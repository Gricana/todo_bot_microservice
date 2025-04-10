import { createRouter, createWebHistory } from "vue-router";
import TodoList from "@/components/todo/TodoList.vue";
import TodoForm from "@/components/todo/TodoForm.vue";
import AuthView from "@/components/auth/AuthView.vue";
import { useAuthStore } from "@/store/auth";

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
        props: true,
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
