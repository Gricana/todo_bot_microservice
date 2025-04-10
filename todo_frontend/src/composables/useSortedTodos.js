import { computed, ref, onMounted } from 'vue';

/**
 * Кастомный хук для управления сортировкой и фильтрацией списка задач.
 * @param {Ref<Array>} todos - Список задач
 * @returns {Object} - Реактивные свойства и методы управления
 */
export function useSortedTodos(todos) {
    // Инициализация реактивных переменных
    const showCompleted = ref(true);
    const sortField = ref('');
    const sortDirection = ref('asc');

    // Загрузка сохранённых значений из localStorage
    onMounted(() => {
        const storedShowCompleted = localStorage.getItem('showCompleted');
        const storedSortField = localStorage.getItem('sortField');
        const storedSortDirection = localStorage.getItem('sortDirection');

        if (storedShowCompleted !== null) {
            try {
                showCompleted.value = JSON.parse(storedShowCompleted);
            } catch (e) {
                console.warn('Ошибка парсинга showCompleted из localStorage');
            }
        }

        if (storedSortField !== null) {
            sortField.value = storedSortField;
        }

        if (storedSortDirection !== null) {
            sortDirection.value = storedSortDirection;
        }
    });

    // Вычисляемое свойство — отсортированный и отфильтрованный список
    const sortedTodos = computed(() => {
        const filtered = showCompleted.value
            ? todos.value
            : todos.value.filter(todo => todo.status !== 'DONE');

        if (!sortField.value) return filtered;

        return [...filtered].sort((a, b) => {
            const aValue = a[sortField.value];
            const bValue = b[sortField.value];

            // Если одно из значений undefined — сортировка невозможна
            if (aValue === undefined || bValue === undefined) return 0;

            if (aValue > bValue) return sortDirection.value === 'asc' ? 1 : -1;
            if (aValue < bValue) return sortDirection.value === 'asc' ? -1 : 1;
            return 0;
        });
    });

    // Методы управления

    /**
     * Переключает отображение выполненных задач
     */
    const toggleShowCompleted = () => {
        showCompleted.value = !showCompleted.value;
        localStorage.setItem('showCompleted', JSON.stringify(showCompleted.value));
    };

    /**
     * Меняет направление сортировки и сохраняет его
     */
    const toggleSortDirection = () => {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
        localStorage.setItem('sortDirection', sortDirection.value);
    };

    /**
     * Устанавливает поле сортировки и сохраняет его
     * @param {string} field - имя поля (например, 'name' или 'date')
     */
    const setSortField = (field) => {
        sortField.value = field;
        localStorage.setItem('sortField', field);
    };

    return {
        showCompleted,
        sortField,
        sortDirection,
        sortedTodos,
        toggleShowCompleted,
        toggleSortDirection,
        setSortField,
    };
}
