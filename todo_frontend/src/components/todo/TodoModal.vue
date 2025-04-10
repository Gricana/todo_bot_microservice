<template>
  <!-- Затемнённый фон, при клике на него — закрытие модального окна -->
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal">
      <!-- Заголовок модального окна -->
      <div class="modal-header">
        <h2>{{ todo.title }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <!-- Основная информация о задаче -->
      <div class="modal-body">
        <p><strong>Описание:</strong> {{ todo.description }}</p>
        <p><strong>Статус:</strong> {{ getStatusLabel(todo.status) }}</p>
        <p>
          <strong>Категории:</strong>
          <!-- Отображаем список категорий или текст "Нет категорий" -->
          <span v-if="todo.categories?.length">
            {{ todo.categories.map((cat) => cat.name).join(', ') }}
          </span>
          <span v-else>Нет категорий</span>
        </p>
        <p><strong>Дата выполнения:</strong> {{ formatDate(todo.due_date) }}</p>
      </div>

      <!-- Кнопки действия: редактирование и удаление -->
      <div class="modal-actions">
        <button class="action-btn" @click="$emit('edit', todo.id)">Редактировать</button>
        <button class="action-btn delete" @click="$emit('delete', todo.id)">Удалить</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TodoModal',
  props: {
    todo: {
      type: Object,
      required: true,
    },
  },
  emits: ['close', 'edit', 'delete'],
  methods: {
    // Метод форматирует дату в московском часовом поясе
    formatDate(dateString) {
      if (!dateString) return 'Не установлена';
      try {
        return new Intl.DateTimeFormat('ru-RU', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          timeZone: 'Europe/Moscow',
        }).format(new Date(dateString));
      } catch {
        return dateString;
      }
    },
    // Метод возвращает читаемое название статуса
    getStatusLabel(status) {
      const map = {
        TODO: 'Сделать',
        IN_PROGRESS: 'На выполнении',
        DONE: 'Сделано',
      };
      return map[status] || status;
    },
  },
};
</script>

<style scoped>
/* Затемнение фона */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 999;
  display: flex;
  justify-content: flex-end;
  animation: fadeIn 0.3s ease;
}

/* Сама модалка */
.modal {
  background: #fff;
  width: 460px;
  height: 100%;
  padding: 0;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease;
  overflow: hidden;
}

/* Заголовок модального окна */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
}

/* Содержимое модалки */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.modal-body p {
  margin-bottom: 0.8rem;
  line-height: 1.4;
}

/* Нижняя панель с кнопками */
.modal-actions {
  position: sticky;
  bottom: 0;
  background: #fff;
  border-top: 1px solid #eee;
  padding: 1rem 1.5rem;
  display: flex;
  gap: 1rem;
}

/* Стили кнопок */
.action-btn {
  flex: 1;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  transition: background-color 0.2s ease;
}

.action-btn:hover {
  background-color: #0056b3;
}

.action-btn.delete {
  background-color: #dc3545;
}

.action-btn.delete:hover {
  background-color: #b02a37;
}

/* Анимации */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
</style>
