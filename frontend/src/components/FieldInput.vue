<template>
  <div class="flex flex-col sm:flex-row gap-4 items-end mb-4">
    <input
      :value="field.name"
      type="text"
      placeholder="Field Name"
      class="p-2 border rounded w-full sm:w-48"
      required
      @input="handleNameChange($event.target.value)"
    />

    <select
      :value="field.type"
      class="p-2 border rounded w-full sm:w-48"
      @change="handleTypeChange($event.target.value)"
    >
      <option v-for="type in fieldTypes" :key="type" :value="type">
        {{ type }}
      </option>
    </select>

    <div class="relative w-full sm:w-48">
      <input
        type="text"
        readonly
        :value="updateConstraintsInput(field)"
        class="p-2 border rounded w-full cursor-pointer"
        @click="handleToggleDropdown"
      />
      <div
        :id="`constraints-dropdown-${index}`"
        class="hidden absolute z-10 mt-1 w-full bg-white border rounded shadow-lg"
      >
        <div class="p-2">
          <label class="flex items-center">
            <input
              type="checkbox"
              :checked="field.constraints.includes('UNIQUE')"
              @change="handleConstraintsChange('UNIQUE', $event.target.checked)"
              class="mr-2"
            />
            UNIQUE
          </label>
          <label class="flex items-center">
            <input
              type="checkbox"
              :checked="field.constraints.includes('NOT NULL')"
              @change="handleConstraintsChange('NOT NULL', $event.target.checked)"
              class="mr-2"
            />
            NOT NULL
          </label>
        </div>
      </div>
    </div>

    <button
      type="button"
      @click="handleRemoveField"
      class="bg-red-500 text-white p-2 rounded hover:bg-red-600 transition-colors w-full sm:w-auto"
    >
      Remove
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  field: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["updateField", "removeField", "toggleDropdown", "updateConstraints"]);

// Define field types in an array and sort them alphabetically
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

const updateConstraintsInput = (field) => {
  if (!Array.isArray(field.constraints)) {
    field.constraints = [];
  }

  return field.constraints.join(", ") || "Select Constraints";
};

const handleToggleDropdown = () => {
  emit("toggleDropdown", props.index);
};

const handleRemoveField = () => {
  emit("removeField", props.index);
};

// Handle constraints change and emit the updated value
const handleConstraintsChange = (constraint, checked) => {
  const constraints = [...props.field.constraints];

  if (checked) {
    constraints.push(constraint);
  } else {
    const index = constraints.indexOf(constraint);
    if (index !== -1) constraints.splice(index, 1);
  }

  emit("updateConstraints", { field: props.field, constraints });
};

// Emit the field update when name or type changes
const handleNameChange = (newName) => {
  emit("updateField", { field: props.field, key: "name", value: newName });
};

const handleTypeChange = (newType) => {
  emit("updateField", { field: props.field, key: "type", value: newType });
};
</script>

<style scoped>
.hidden {
  display: none;
}
</style>
