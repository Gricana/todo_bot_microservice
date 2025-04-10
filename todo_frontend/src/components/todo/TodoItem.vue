<template>
  <!-- Элемент задачи. При клике вызывает модалку -->
  <div
      class="todo-item"
      :class="{ 'is-done': todo.status === 'DONE' }"
      :style="{ borderLeft: '4px solid ' + statusColor }"
      @click="emitViewDetails"
  >
    <!-- Левая часть: заголовок и дата -->
    <div class="todo-info">
      <h3 class="todo-title">{{ todo.title }}</h3>
      <p class="todo-due">{{ formattedDueDate }}</p>
    </div>

    <!-- Правая часть: кнопка ⋯ с меню -->
    <div class="actions">
      <button class="menu-btn" @click.stop="toggleMenu">⋯</button>

      <!-- Выпадающее меню с действиями -->
      <transition name="fade">
        <div v-if="showMenu" class="dropdown-menu" @click.stop>
          <button @click="$emit('edit', todo.id)">Редактировать</button>
          <button @click="$emit('delete', todo.id)">Удалить</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { computed, onBeforeUnmount, onMounted } from 'vue';

export default {
  name: 'TodoItem',
  props: {
    /**
     * Задача, которую нужно отобразить
     */
    todo: {
      type: Object,
      required: true,
    },
  },
  emits: ['edit', 'delete', 'view'],
  data() {
    return {
      showMenu: false, // Состояние открытия выпадающего меню
    };
  },
  computed: {
    /**
     * Форматирование даты задачи (вывод в МСК)
     */
    formattedDueDate() {
      if (!this.todo.due_date) return 'Нет данных';
      try {
        const date = new Date(this.todo.due_date);
        return new Intl.DateTimeFormat('ru-RU', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          timeZone: 'Europe/Moscow',
        }).format(date);
      } catch {
        return this.todo.due_date;
      }
    },

    /**
     * Цвет левой полосы задачи в зависимости от статуса
     */
    statusColor() {
      const map = {
        TODO: '#dc3545',        // красный
        IN_PROGRESS: '#ffc107', // жёлтый
        DONE: '#28a745',        // зелёный
      };
      return map[this.todo.status] || '#ccc';
    },
  },
  methods: {
    /**
     * Показывает/скрывает меню
     */
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },

    /**
     * Эмит события для открытия подробного просмотра
     */
    emitViewDetails() {
      this.$emit('view', this.todo.id);
    },

    /**
     * Скрытие меню по клавише Escape
     */
    handleEscKey(e) {
      if (e.key === 'Escape') this.showMenu = false;
    },
  },
  mounted() {
    document.addEventListener('keydown', this.handleEscKey);
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscKey);
  },
};
</script>

<style scoped>
/* Основной контейнер задачи */
.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s ease;
  cursor: pointer;
}

.todo-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Текст задачи и дата */
.todo-info {
  flex-grow: 1;
}

.todo-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.todo-due {
  font-size: 0.9rem;
  color: #555;
  margin-top: 0.3rem;
}

/* Если задача выполнена — стилизуем */
.is-done {
  opacity: 0.2;
  filter: grayscale(0.1);
}

/* Правая часть: ⋯ */
.actions {
  position: relative;
}

.menu-btn {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.3rem;
}

/* Выпадающее меню */
.dropdown-menu {
  position: absolute;
  top: 2rem;
  right: 0;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  z-index: 10;
  min-width: 140px;
}

.dropdown-menu button {
  background: none;
  border: none;
  text-align: left;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  width: 100%;
}

.dropdown-menu button:hover {
  background-color: #f2f2f2;
}

/* Анимация появления/скрытия dropdown */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
