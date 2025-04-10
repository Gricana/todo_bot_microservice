<template>
  <div class="form-group">
    <label :for="id">{{ label }}</label>
    <slot />
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'FormGroup',
  props: {
    id: String,
    label: String,
    error: String,
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
