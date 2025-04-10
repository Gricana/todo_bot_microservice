<template>
  <div class="form-field">
    <label :for="id">{{ label }}</label>
    <input
        :id="id"
        :type="type"
        :placeholder="placeholder"
        :inputmode="inputmode"
        :maxlength="maxlength"
        :pattern="pattern"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script>
export default {
  name: 'FormField',
  props: {
    label: { type: String, required: true },
    id: { type: String, required: true },
    type: { type: String, default: 'text' },
    placeholder: String,
    inputmode: String,
    maxlength: Number,
    pattern: String,
    modelValue: String
  },
  emits: ['update:modelValue']
};
</script>



<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
  width: 100%;
}

label {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
