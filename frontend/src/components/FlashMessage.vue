<template>
  <transition name="fade">
    <div
      v-if="visible"
      :class="[
        'fixed top-5 right-5 px-4 py-2 rounded-lg shadow-lg flex items-center justify-between w-64 text-white',
        type === 'success' ? 'bg-green-500' : 'bg-red-500',
      ]"
    >
      <span>{{ message }}</span>
      <button @click="emit('closeMessage')" class="ml-3 text-xl font-bold focus:outline-none">
        &times;
      </button>
    </div>
  </transition>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: "success",
  },

  visible: Boolean,
});

const emit = defineEmits(["closeMessage"]);
</script>
