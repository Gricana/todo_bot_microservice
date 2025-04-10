<template>
  <div id="app">
    <header>
      <h1>Todo App</h1>
      <nav>
        <template v-if="auth.user">
          <router-link to="/">Список задач</router-link>
          <router-link to="/new">Создать задачу</router-link>
        </template>
        <div v-if="auth.user" class="user-menu" @click="toggleDropdown">
          <span class="username">@{{ auth.user }}</span>
          <div v-if="dropdownOpen" class="dropdown">
            <button @click.stop="logout">Выход</button>
          </div>
        </div>
        <router-link v-else to="/login">Войти</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import {useTodoStore} from "@/store/tasks.js";
import {onMounted, ref} from "vue";
import {useRouter} from "vue-router";

export default {
  name: 'App',
  setup() {
    const auth = useAuthStore()
    const store = useTodoStore()
    const router = useRouter()

    const dropdownOpen = ref(false);
    const toggleDropdown = () => {
      dropdownOpen.value = !dropdownOpen.value;
    };

    const logout = async () => {
      auth.logout();
      await router.push('/login');
    };

    onMounted(() => {
      store.fetchTodos()
    })
    return { auth, dropdownOpen, toggleDropdown, logout };
  },
};
</script>

<style scoped>
#app {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

header {
  background-color: #007bff;
  color: #fff;
  padding: 1rem;
}

nav {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
}

nav a {
  color: #fff;
  margin-right: 1rem;
  text-decoration: none;
}

nav a.router-link-active {
  font-weight: bold;
}

/* Стили для блока пользователя и выпадающего меню */
.user-menu {
  position: relative;
  cursor: pointer;
  user-select: none;
}

.username {
  margin-left: 1rem;
  font-weight: bold;
  color: #ffe;
}

/* Стили для выпадающего меню */
.dropdown {
  position: absolute;
  top: 120%;
  right: 0;
  background: #fff;
  border: 1px solid #ccc;
  padding: 0.5rem;
  z-index: 100;
}

.dropdown button {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #007bff;
  font-size: 1rem;
  padding: 0;
}
</style>
