<template>
  <div>
    <select
      v-model="selectedSortField"
      @change="updateSortField"
      class="mb-4 p-2 border border-gray-300 rounded"
    >
      <option value="table_name">Sort by Table Name</option>
      <option value="created_at">Sort by Created At</option>
    </select>
  </div>
</template>

<script setup>
import { ref, defineEmits } from "vue";

const emit = defineEmits(["update:sortField"]);

const selectedSortField = ref("table_name");

const updateSortField = () => {
  emit("update:sortField", selectedSortField.value);
};
</script>
