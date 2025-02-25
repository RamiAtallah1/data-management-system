<template>
  <div class="flex items-center justify-center h-screen bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-md w-96">
      <h2 class="text-2xl font-bold text-center mb-6">Sign In</h2>
      <p v-if="errorMessage" class="text-red-500 text-center mt-4">{{ errorMessage }}</p>

      <form @submit.prevent="handleSignIn">
        <div class="mb-4">
          <label class="block text-gray-700">Email</label>
          <input v-model="email" type="email" class="w-full p-2 border rounded" required />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">Password</label>
          <input v-model="password" type="password" class="w-full p-2 border rounded" required />
        </div>
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Sign In
        </button>
      </form>
      <p class="text-center text-sm text-gray-600 mt-4">
        Don't have an account?
        <router-link to="/signup" class="text-blue-500 hover:underline">Sign Up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { signinUser } from "@/services/userServices";
import { ref } from "vue";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);
const router = useRouter();

const handleSignIn = async () => {
  errorMessage.value = "";
  isLoading.value = true;
  try {
    const data = await signinUser(email.value, password.value);

    if (!data) {
      errorMessage.value = "Invalid email or password.";
      return;
    }

    localStorage.setItem("access_token", data.access);
    router.push("/");
  } catch (error) {
    errorMessage.value = "Network error. Please try again.";
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};
</script>
