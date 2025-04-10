<template>
  <div class="login-page">
    <h1>Авторизация</h1>
    <form @submit.prevent="onLogin">

      <FormField
          label="ID tg-чата (9 цифр)"
          id="chatId"
          type="text"
          inputmode="numeric"
          maxlength="9"
          pattern="\d{9}"
          placeholder="Введите ID чата"
          v-model="credentials.telegram_id"
      />

      <FormField
          label="Ник пользователя"
          id="username"
          placeholder="Введите ник tg-пользователя"
          v-model="credentials.username"
      />

      <button type="submit">Авторизоваться через Telegram</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth.js';
import { useRouter } from 'vue-router';
import FormField from '@/components/auth/FormField.vue';

export default {
  name: 'Login',
  components: { FormField },
  setup() {
    const auth = useAuthStore();
    const router = useRouter();

    const credentials = ref({
      telegram_id: '',
      username: ''
    });

    // Основной метод входа
    const onLogin = async () => {
      try {
        // Простая клиентская проверка ID
        if (!/^\d{9}$/.test(credentials.value.telegram_id)) {
          alert('ID чата должен содержать ровно 9 цифр.');
          return;
        }

        await auth.register(credentials.value); // регистрация (если требуется)
        await auth.login(credentials.value);    // логин
        await router.push('/');                 // редирект на главную
      } catch (error) {
        console.error('Ошибка при логине:', error);
      }
    };

    return {
      credentials,
      onLogin,
    };
  },
};
</script>

<style scoped>
.login-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  width: 100%;
  box-sizing: border-box;
}

h1 {
  text-align: center;
  margin-bottom: 1rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

button {
  width: 100%;
  padding: 0.8rem;
  font-size: 1.2rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  box-sizing: border-box;
}

button:hover {
  background-color: #0056b3;
}
</style>
