<template>
  <div class="flex flex-col sm:flex-row gap-4 items-end mb-4">
    <input :value="field.name" type="text" class="p-2 border rounded w-full sm:w-48" readonly />

    <input :value="field.type" class="p-2 border rounded w-full sm:w-48" readonly />
  </div>
</template>

<script setup>
const props = defineProps({
  field: {
    type: Object,
    required: true,
  },
});

const fieldTypes = [
  "SERIAL",
  "INTEGER",
  "BIGINT",
  "SMALLINT",
  "NUMERIC",
  "VARCHAR(255)",
  "TEXT",
  "BOOLEAN",
  "DATE",
  "TIMESTAMP",
  "JSONB",
].sort();
</script>
