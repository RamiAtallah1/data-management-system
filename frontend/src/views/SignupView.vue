<template>
  <div class="flex items-center justify-center h-screen bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-md w-96">
      <h2 class="text-2xl font-bold text-center mb-6">Sign Up</h2>
      <p v-if="errorMessage" class="text-red-500 text-center mt-4">{{ errorMessage }}</p>
      <form @submit.prevent="handleSignUp">
        <div class="mb-4">
          <label class="block text-gray-700">Name</label>
          <input v-model="name" type="text" class="w-full p-2 border rounded" required />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">Email</label>
          <input v-model="email" type="email" class="w-full p-2 border rounded" required />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">Password</label>
          <input v-model="password" type="password" class="w-full p-2 border rounded" required />
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
          Sign Up
        </button>
      </form>
      <p class="text-center text-sm text-gray-600 mt-4">
        Already have an account?
        <router-link to="/signin" class="text-blue-500 hover:underline">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { signinUser, signupUser } from "@/services/userServices";
import { ref } from "vue";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const router = useRouter();

const handleSignUp = async () => {
  errorMessage.value = "";

  try {
    const signupData = await signupUser(name.value, email.value, password.value);

    if (!signupData) {
      const errorData = await signUpResponse.json();
      errorMessage.value = errorData.email?.[0] || "Sign-up failed.";
      return;
    }

    const signinData = await signinUser(email.value, password.value);

    if (!signinData) {
      errorMessage.value = "Sign-in failed after registration.";
      return;
    }

    localStorage.setItem("access_token", signinData.access);
    router.push("/");
  } catch (error) {
    errorMessage.value = "Network error. Please try again.";
    console.error(error);
  }
};
</script>
