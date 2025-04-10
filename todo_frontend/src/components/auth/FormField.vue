<template>
  <div class="form-field">
    <label :for="id">{{ label }}</label>
    <input
        :type="type"
        :id="id"
        :placeholder="placeholder"
        :maxlength="maxlength"
        :pattern="pattern"
        :inputmode="inputmode"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        required
    />
  </div>
</template>

<script>
export default {
  name: 'FormField',
  props: {
    modelValue: [String, Number],
    label: String,
    id: String,
    type: {
      type: String,
      default: 'text'
    },
    placeholder: String,
    maxlength: Number,
    pattern: String,
    inputmode: String
  },
  emits: ['update:modelValue'],
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
