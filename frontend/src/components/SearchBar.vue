<template>
  <div>
    <input
      v-model="searchQuery"
      :placeholder="placeholder"
      class="mb-4 p-2 border border-gray-300 rounded"
    />
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from "vue";

// Define props for the placeholder
const props = defineProps({
  placeholder: {
    type: String,
    default: "Search by table name",
  },
});

// Emit the search query to the parent component
const emit = defineEmits(["update:searchQuery"]);

const searchQuery = ref("");

// Watch the search query and emit the value to the parent
watch(searchQuery, (newQuery) => {
  emit("update:searchQuery", newQuery);
});
</script>
