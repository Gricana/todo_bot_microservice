<template>
  <div class="todo-form">
    <h1>{{ isEditMode ? 'Редактировать задачу' : 'Создать новую задачу' }}</h1>

    <form @submit.prevent="handleSubmit">
      <FormGroup id="title" label="Название задачи:" :error="getErrorMessage('title')">
        <input id="title" v-model="form.title" type="text" required />
      </FormGroup>

      <FormGroup id="description" label="Описание задачи:">
        <textarea id="description" v-model="form.description" required />
      </FormGroup>

      <FormGroup id="status" label="Статус:">
        <select id="status" v-model="form.status" required>
          <option value="TODO">Сделать</option>
          <option value="IN_PROGRESS">На выполнении</option>
          <option value="DONE">Сделано</option>
        </select>
      </FormGroup>

      <FormGroup id="categories" label="Категории (через запятую):" :error="getErrorMessage('categories')">
        <input
            id="categories"
            v-model="form.categories"
            type="text"
            placeholder="Например, Работа, Личное"
        />
      </FormGroup>

      <FormGroup id="dueDate" label="Дата и время выполнения:" :error="getErrorMessage('due_date')">
        <input
            id="dueDate"
            v-model="form.dueDate"
            type="datetime-local"
        />
      </FormGroup>

      <button type="submit" class="submit-btn">{{ isEditMode ? 'Сохранить' : 'Создать' }}</button>
    </form>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useTodoStore } from "@/store/tasks.js";
import todoApi from "@/services/api.js";
import { DateTime } from 'luxon';
import FormGroup from '@/components/todo/FormGroup.vue';

function convertToZonedISO(localDateTime, zone = 'America/Adak') {
  if (!localDateTime) return null;
  return DateTime.fromISO(localDateTime, { zone: 'local' })
      .setZone(zone)
      .toISO();
}

export default {
  name: 'TodoForm',
  components: { FormGroup },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useTodoStore();
    const isEditMode = Boolean(route.params.id);
    const formErrors = reactive({});

    const form = reactive({
      title: '',
      description: '',
      status: 'TODO',
      categories: '',
      dueDate: '',
    });

    // При редактировании задачи — загружаем данные
    onMounted(async () => {
      if (isEditMode) {
        try {
          const { data } = await todoApi.get(`/api/tasks/${route.params.id}`); // 🛠️ здесь была ошибка — пропущены кавычки
          form.title = data.title;
          form.description = data.description;
          form.status = data.status;
          form.categories = data.categories?.map(cat => cat.name).join(', ') || '';
          form.dueDate = data.due_date
              ? DateTime.fromISO(data.due_date).setZone('Europe/Moscow').toFormat("yyyy-MM-dd'T'HH:mm")
              : '';
        } catch (error) {
          console.error('Ошибка загрузки задачи: ', error);
        }
      }
    });

    const getErrorMessage = (field) => {
      const err = formErrors[field];
      return Array.isArray(err) ? err.join(', ') : err;
    };

    const handleSubmit = async () => {
      try {
        // очищаем старые ошибки
        Object.keys(formErrors).forEach(key => delete formErrors[key]);

        const payload = { ...form };

        if (payload.categories?.trim()) {
          payload.categories = payload.categories.split(',').map(s => s.trim());
        } else {
          delete payload.categories;
        }

        if (payload.dueDate) {
          payload.due_date = convertToZonedISO(payload.dueDate, 'America/Adak');
          delete payload.dueDate;
        }

        if (isEditMode) {
          await store.updateTodo(route.params.id, payload);
        } else {
          await store.addTodo(payload);
        }

        await router.push('/');

      } catch (error) {
        if (error.response?.data && typeof error.response.data === 'object') {
          Object.assign(formErrors, error.response.data);
        } else {
          console.error('Ошибка сохранения данных:', error);
        }
      }
    };

    return {
      isEditMode,
      form,
      formErrors,
      handleSubmit,
      getErrorMessage,
    };
  }
}
</script>


<style scoped>
.todo-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
  font-family: 'Arial', sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input[type="text"],
input[type="number"],
input[type="datetime-local"],
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 1rem 0;
}

.submit-btn {
  width: 100%;
  padding: 0.8rem;
  font-size: 1.2rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.error-message {
  color: #dc3545;
  font-size: 0.95rem;
  margin-top: 0.3rem;
}

</style>
