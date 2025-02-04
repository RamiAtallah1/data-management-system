<template>
  <div class="p-6">
    <FlashMessage
      :message="message.text"
      :type="message.type"
      :visible="message.visible"
      @closeMessage="closeMessage"
    />

    <div v-if="schemas.length" class="mb-4">
      <div class="flex items-center justify-between mb-2">
        <h2 class="text-xl font-semibold">Schemas</h2>
        <button
          @click="goToCreateSchema"
          class="bg-green-500 text-white px-3 py-1 rounded-md shadow"
        >
          Create Schema
        </button>
      </div>
      <ul class="border rounded p-4 space-y-2">
        <li
          v-for="(schema, index) in paginatedSchemas"
          :key="schema.table_name"
          class="flex justify-between items-start"
        >
          <div class="flex flex-col w-full">
            <div class="flex justify-between items-center mb-2">
              <span class="text-lg font-semibold">{{ schema.table_name }}</span>
              <div class="flex justify-between items-center gap-1">
                <button
                  @click="goToImportData(schema.table_name)"
                  class="bg-blue-500 text-white px-3 py-1 rounded"
                >
                  Import Data
                </button>
                <button @click="showConfirmation" class="bg-red-500 text-white px-3 py-1 rounded">
                  Delete Table
                </button>
              </div>
            </div>
            <ConfirmationModal
              :visible="isModalVisible"
              title="Delete Confirmation"
              message="Are you sure you want to delete this item?"
              @confirm="() => deleteTable(schema.table_name)"
              @cancel="isModalVisible = false"
            />
            <!-- Loop through existing fields and display them in read-only mode -->
            <div v-for="(field, fieldIndex) in schema.fields" :key="fieldIndex">
              <FieldDisplay :field="field" />
            </div>

            <!-- Loop through new fields and display them in editable mode -->
            <div
              v-for="(newField, fieldIndex) in newFields[schema.table_name] || []"
              :key="'new-' + fieldIndex"
            >
              <FieldInput
                :field="newField"
                :index="fieldIndex"
                @removeField="removeNewField(schema.table_name, fieldIndex)"
                @updateField="updateField(schema.table_name, fieldIndex, $event)"
                @toggleDropdown="toggleDropdown"
                @updateConstraints="
                  updateConstraints(schema.table_name, fieldIndex, $event.constraints)
                "
              />
            </div>

            <button
              @click="addNewField(schema.table_name)"
              class="bg-blue-500 text-white px-4 py-2 rounded mt-2"
            >
              + Add Field
            </button>

            <button
              v-if="newFields[schema.table_name] && newFields[schema.table_name].length > 0"
              @click="saveNewFields(schema.table_name)"
              class="bg-green-500 text-white px-4 py-2 rounded mt-2"
            >
              Save New Fields
            </button>
            <hr v-if="index !== schemas.length - 1" class="w-full border-b my-4" />
          </div>
        </li>
      </ul>

      <div class="flex justify-between items-center mt-4">
        <button
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
          class="bg-gray-300 text-black px-4 py-2 rounded-md"
        >
          Previous
        </button>
        <span class="text-lg"> Page {{ currentPage }} of {{ totalPages }} </span>
        <button
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
          class="bg-gray-300 text-black px-4 py-2 rounded-md"
        >
          Next
        </button>
      </div>
    </div>
    <div v-else>
      <SchemaFormView />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import FieldInput from "@/components/FieldInput.vue";
import FieldDisplay from "@/components/FieldDisplay.vue";
import SchemaFormView from "@/views/SchemaFormView.vue";
import { addFields, deleteSchema, getAllSchemas } from "@/services/schemaService";
import { useRouter } from "vue-router";
import FlashMessage from "@/components/FlashMessage.vue";
import ConfirmationModal from "@/components/ConfirmationModal.vue";

const schemas = ref([]);
const newFields = ref({});
const currentPage = ref(1);
const itemsPerPage = 10;
const message = ref({
  text: "",
  type: "success",
  visible: false,
});
const isModalVisible = ref(false);
const router = useRouter();

const showMessage = (text, type = "success") => {
  message.value = { text, type, visible: true };
};

const showConfirmation = () => {
  isModalVisible.value = true;
};

const closeMessage = () => {
  message.value.visible = false;
};

const fetchSchemas = async () => {
  try {
    const data = await getAllSchemas();
    schemas.value = data;
  } catch (error) {
    console.error("Error fetching schemas:", error);
    showMessage("Error fetching schemas", "error");
  }
};

const updateField = (tableName, fieldIndex, update) => {
  const field = newFields.value[tableName][fieldIndex];
  field[update.key] = update.value;
};

const toggleDropdown = (index) => {
  const dropdown = document.getElementById(`constraints-dropdown-${index}`);
  dropdown.classList.toggle("hidden");
};

const updateConstraints = (tableName, fieldIndex, constraints) => {
  const field = newFields.value[tableName][fieldIndex];
  field.constraints = constraints;
};

const addNewField = (tableName) => {
  if (!newFields.value[tableName]) {
    newFields.value[tableName] = [];
  }
  newFields.value[tableName].push({
    name: "",
    type: "VARCHAR(255)",
    constraints: [],
  });
};

const saveNewFields = async (tableName) => {
  const schema = schemas.value.find((s) => s.table_name === tableName);

  if (schema && newFields.value[tableName]) {
    const newFieldsToAdd = newFields.value[tableName];

    try {
      const data = await addFields(tableName, newFieldsToAdd);

      if (data) {
        schema.fields.push(...newFieldsToAdd);
        newFields.value[tableName] = [];
        showMessage("New fields added successfully!");
      }
    } catch (error) {
      console.error("Error adding new fields:", error);
      showMessage("Error adding new fields", "error");
    } finally {
      isModalVisible.value = false;
    }
  }
};

const removeNewField = (tableName, fieldIndex) => {
  if (newFields.value[tableName]) {
    newFields.value[tableName].splice(fieldIndex, 1);
  }
};

const deleteTable = async (tableName) => {
  try {
    await deleteSchema(tableName);
    schemas.value = schemas.value.filter((s) => s.table_name !== tableName);
    showMessage("Table deleted successfully!");
  } catch (error) {
    console.error("Error deleting table:", error);
    showMessage("Error deleting table", "error");
  }
};

const goToCreateSchema = () => {
  router.push("/createSchema");
};

const goToImportData = (tableName) => {
  router.push(`/importData/${tableName}`);
};

const totalPages = computed(() => Math.ceil(schemas.value.length / itemsPerPage));

const paginatedSchemas = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return schemas.value.slice(start, end);
});

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

onMounted(fetchSchemas);
</script>
