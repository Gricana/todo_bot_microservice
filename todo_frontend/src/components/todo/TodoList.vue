<template>
  <div class="todo-list">
    <header class="todo-header">
      <!-- Заголовок списка -->
      <div class="header-left">
        <h1>Список задач</h1>
      </div>

      <!-- Кнопки управления задачами -->
      <div class="header-actions">
        <!-- Переключение отображения выполненных задач -->
        <button
            @click="toggleShowCompleted"
            :class="['toggle-btn', showCompleted ? 'active' : 'inactive']"
        >
          {{ showCompleted ? 'Скрыть' : 'Показать' }} выполненные
        </button>

        <!-- Кнопка перехода к созданию новой задачи -->
        <button @click="navigateToNewTodo" class="new-todo-btn">Новая задача</button>
      </div>

      <!-- Сортировка задач -->
      <div class="sort-controls">
        <label for="sortField">Сортировать по:</label>
        <select id="sortField" v-model="sortField">
          <option value="">Без сортировки</option>
          <option value="status">Статус</option>
          <option value="title">Название</option>
          <option value="due_date">Дата</option>
        </select>

        <!-- Смена направления сортировки -->
        <button @click="toggleSortDirection" class="toggle-btn">
          {{ sortDirection === 'asc' ? 'По возрастанию ↑' : 'По убыванию ↓' }}
        </button>
      </div>
    </header>

    <!-- Содержимое: список задач или сообщения -->
    <div class="content">
      <div v-if="loading" class="loading-message">Загрузка задач...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>

      <!-- Список задач -->
      <ul v-else class="todos">
        <li v-for="todo in sortedTodos" :key="todo.id">
          <TodoItem
              :todo="todo"
              @deleteTodo="deleteTodoHandler"
              @editTodo="editTodoHandler"
              @toggleStatus="toggleStatusHandler"
              @view="openDetails"
          />
        </li>
      </ul>
    </div>

    <!-- Модальное окно просмотра задачи -->
    <TodoModal
        v-if="selectedTodo"
        :todo="selectedTodo"
        @close="selectedTodo = null"
        @edit="editTodoHandler"
        @delete="deleteTodoHandler"
    />
  </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useTodoStore } from '@/store/tasks.js';
import { storeToRefs } from 'pinia';
import { useSortedTodos } from '@/composables/useSortedTodos.js';
import TodoItem from '@/components/todo/TodoItem.vue';
import TodoModal from '@/components/todo/TodoModal.vue';

export default {
  name: 'TodoList',
  components: {
    TodoItem,
    TodoModal,
  },
  setup() {
    const router = useRouter();
    const store = useTodoStore();
    const { todos, loading, error } = storeToRefs(store);
    const selectedTodo = ref(null);

    const {
      sortedTodos,
      sortField,
      sortDirection,
      showCompleted,
      toggleShowCompleted,
      toggleSortDirection,
      setSortField,
    } = useSortedTodos(todos);

    // Сохраняем изменения в сортировке при выборе поля
    watch(sortField, (newValue) => {
      setSortField(newValue);
    });

    // Сохраняем изменения направления сортировки
    watch(sortDirection, (newValue) => {
      localStorage.setItem('sortDirection', newValue);
    });

    onMounted(() => {
      store.fetchTodos();
    });

    const deleteTodoHandler = (id) => {
      store.deleteTodo(id);
      selectedTodo.value = null;
    };

    const editTodoHandler = (id) => {
      router.push(`/edit/${id}`);
    };

    const toggleStatusHandler = (id, newStatus) => {
      store.toggleTodoStatus(id, newStatus);
    };

    const navigateToNewTodo = () => {
      router.push('/new');
    };

    const openDetails = (id) => {
      const todo = todos.value.find((t) => t.id === id);
      selectedTodo.value = todo;
    };

    return {
      loading,
      error,
      sortedTodos,
      sortField,
      sortDirection,
      showCompleted,
      toggleShowCompleted,
      toggleSortDirection,
      navigateToNewTodo,
      deleteTodoHandler,
      editTodoHandler,
      toggleStatusHandler,
      selectedTodo,
      openDetails,
    };
  },
};
</script>

<style scoped>
/* Общий контейнер */
.todo-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
  font-family: 'Arial', sans-serif;
}

/* Заголовок с кнопками */
.todo-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-left h1 {
  margin: 0;
  font-size: 1.8rem;
}

/* Блоки кнопок и фильтров */
.header-actions,
.sort-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Фильтр сортировки */
.sort-controls label {
  font-weight: bold;
}

.sort-controls select {
  padding: 0.4rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

/* Кнопки */
.new-todo-btn,
.toggle-btn {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.new-todo-btn:hover {
  background-color: #0056b3;
}

.toggle-btn:hover {
  background-color: #495057;
}

/* Цвета состояний кнопки "Показать выполненные" */
.toggle-btn.active {
  background-color: #28a745;
}

.toggle-btn.inactive {
  background-color: #ffc107;
  color: black;
}

/* Содержимое */
.content {
  margin-top: 1rem;
}

.loading-message,
.error-message {
  margin: 1rem 0;
  font-size: 1.2rem;
  color: #dc3545;
}

/* Список задач */
.todos {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>
