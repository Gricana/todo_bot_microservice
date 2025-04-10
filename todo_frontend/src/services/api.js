import axios from 'axios'


const todoApi = axios.create({
    baseURL: import.meta.env.VITE_BASE_TODO_API || 'http://localhost:8000',
})

/**
 * Interceptor запроса
 * Перед каждым запросом вставляем access token из localStorage,
 * если он существует.
 */
todoApi.interceptors.request.use(config => {
    const access = localStorage.getItem('access')
    if (access) {
        config.headers['Authorization'] = `Bearer ${access}`
    }
    return config
})

/**
 * ❗ Interceptor ответа
 * Если сервер возвращает 401 (Unauthorized), пробуем автоматически
 * обновить access token с помощью refreshToken().
 * Если обновление прошло успешно — повторяем оригинальный запрос.
 * Если нет — выполняем logout и выбрасываем ошибку.
 */
todoApi.interceptors.response.use(
    response => response, // Успешные ответы просто пропускаем
    async error => {
        if (error.response && error.response.status === 401) {
            try {
                const { useAuthStore } = await import('@/store/auth')
                const store = useAuthStore()

                await store.refreshToken()

                const newAccess = localStorage.getItem('access')
                if (newAccess) {
                    error.config.headers['Authorization'] = `Bearer ${newAccess}`
                    return todoApi.request(error.config)
                }
            } catch (_) {
                const { useAuthStore } = await import('@/store/auth')
                useAuthStore().logout()
            }
        }

        return Promise.reject(error)
    }
)

export default todoApi
