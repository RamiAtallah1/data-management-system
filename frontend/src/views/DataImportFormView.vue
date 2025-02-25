<template>
  <div class="p-6 bg-white shadow-md rounded-lg mt-6">
    <FlashMessage
      :message="message.text"
      :type="message.type"
      :visible="message.visible"
      @closeMessage="closeMessage"
    />
    <h2 class="text-2xl font-bold mb-4">Import Data</h2>
    <form @submit.prevent="importData">
      <div class="mb-4">
        <label class="block text-gray-700">CSV File</label>
        <input
          type="file"
          class="block w-full border border-gray-200 shadow-sm rounded-lg text-sm focus:z-10 focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 file:bg-gray-50 file:border-0 file:me-4 file:py-3 file:px-4 dark:file:bg-neutral-700 dark:file:text-neutral-400"
          :onchange="handleFileUpload"
          accept=".csv"
          required
        />
      </div>
      <button
        type="submit"
        :disabled="isLoading"
        class="bg-blue-500 text-white p-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Import
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { postData } from "@/services/schemaService";
import { useRoute } from "vue-router";
import FlashMessage from "@/components/FlashMessage.vue";

const file = ref(null);
const message = ref({
  text: "",
  type: "success",
  visible: false,
});
const isLoading = ref(false);

const route = useRoute();
const tableName = route.params.table_name;

const showMessage = (text, type = "success") => {
  message.value = { text, type, visible: true };
};

const closeMessage = () => {
  message.value.visible = false;
};

const handleFileUpload = (event) => {
  file.value = event.target.files[0];
};

const importData = async () => {
  isLoading.value = true;
  const formData = new FormData();
  formData.append("file", file.value);

  try {
    const data = await postData(tableName, formData);

    if (data) {
      showMessage("Data import started. You will receive an email upon completion.");
    } else {
      showMessage("Failed to start data import.", "error");
    }
  } catch (error) {
    showMessage("Failed to start data import.", "error");
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};
</script>
