<template>
  <div class="form-group">
    <!-- Название поля -->
    <label :for="id">{{ label }}</label>

    <!-- Слот для поля ввода (input, textarea, select и т.п.) -->
    <slot />

    <!-- Сообщение об ошибке (если передано) -->
    <p
        v-if="error"
        class="error-message"
        :aria-live="'polite'"
        :id="`${id}-error`"
    >
      {{ error }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'FormGroup',
  props: {
    /**
     * ID для привязки label -> input
     */
    id: {
      type: String,
      required: true,
    },
    /**
     * Название поля, отображается в label
     */
    label: {
      type: String,
      required: true,
    },
    /**
     * Сообщение об ошибке. Если пусто — блок не отображается.
     */
    error: {
      type: String,
      default: '',
    },
  },
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.95rem;
  margin-top: 0.3rem;
}
</style>
