<template>
  <div class="p-6 bg-white shadow-md rounded-lg max-w-4xl mx-auto">
    <FlashMessage
      :message="message.text"
      :type="message.type"
      :visible="message.visible"
      @closeMessage="closeMessage"
    />
    <h2 class="text-2xl font-bold mb-4">Create Schema</h2>
    <form @submit.prevent="createSchema">
      <div class="mb-4">
        <label class="block text-gray-700">Table Name</label>
        <input
          v-model="tableName"
          type="text"
          class="w-full p-2 border rounded max-w-md"
          required
        />
      </div>

      <div class="mb-4">
        <label class="block text-gray-700">Fields</label>
        <div v-for="(field, index) in fields" :key="index">
          <FieldInput
            :field="field"
            :index="index"
            @updateField="updateField"
            @removeField="removeField"
            @toggleDropdown="toggleDropdown"
            @updateConstraints="updateConstraints"
          />
        </div>

        <button
          type="button"
          @click="addField"
          class="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition-colors w-full sm:w-auto"
        >
          Add Field
        </button>
      </div>

      <button
        type="submit"
        :disabled="isLoading"
        class="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition-colors w-full sm:w-auto disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Create Schema
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { postSchema } from "@/services/schemaService";
import FieldInput from "@/components/FieldInput.vue";
import FlashMessage from "@/components/FlashMessage.vue";

const tableName = ref("");
const fields = ref([{ name: "", type: "VARCHAR(255)", constraints: [] }]);
const message = ref({
  text: "",
  type: "success",
  visible: false,
});
const isLoading = ref(false);

const showMessage = (text, type = "success") => {
  message.value = { text, type, visible: true };
};

const closeMessage = () => {
  message.value.visible = false;
};

const addField = () => {
  fields.value.push({
    name: "",
    type: "VARCHAR(255)",
    constraints: [],
  });
};

const removeField = (index) => {
  fields.value.splice(index, 1);
};

const createSchema = async () => {
  isLoading.value = true;
  try {
    const data = await postSchema(tableName.value, fields.value);
    if (data) {
      tableName.value = "";
      fields.value = [{ name: "", type: "VARCHAR(255)", constraints: [] }];
      showMessage("Schema created successfully.");
    } else {
      showMessage("Failed to create schema.", "error");
    }
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const toggleDropdown = (index) => {
  const dropdown = document.getElementById(`constraints-dropdown-${index}`);
  dropdown.classList.toggle("hidden");
};

const updateConstraints = ({ field, constraints }) => {
  field.constraints = constraints;
};

const updateField = (payload) => {
  const { field, key, value } = payload;
  field[key] = value;
};
</script>
