<template>
  <transition name="fade">
    <div
      v-if="visible"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-lg font-semibold mb-4">{{ title }}</h2>
        <p class="text-gray-700">{{ message }}</p>
        <div class="flex justify-end mt-4">
          <button
            @click="emit('cancel')"
            class="px-4 py-2 bg-gray-300 text-gray-800 rounded-md mr-2"
          >
            Cancel
          </button>
          <button @click="emit('confirm')" class="px-4 py-2 bg-red-600 text-white rounded-md">
            Confirm
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

defineProps({
  visible: Boolean,
  title: {
    type: String,
    default: "Are you sure?",
  },
  message: {
    type: String,
    default: "This action cannot be undone.",
  },
});

const emit = defineEmits(["confirm", "cancel"]);
</script>
