<template>
  <div>
    <template v-if="authenticated">
      <button
        @click="logout"
        class="py-3 px-4 text-white bg-red-600 hover:bg-red-700 rounded-md shadow"
      >
        Logout
      </button>
    </template>
    <template v-else>
      <a
        href="/signin"
        class="py-3 px-4 text-white bg-indigo-600 hover:bg-indigo-700 rounded-md shadow"
      >
        Sign In
      </a>
    </template>
  </div>
</template>

<script setup>
import { isAuthenticated } from "@/services/authenticatedService";
import { ref, onMounted } from "vue";

const authenticated = ref(false);

const checkAuth = async () => {
  authenticated.value = await isAuthenticated();
};

const logout = () => {
  localStorage.removeItem("access_token");
  authenticated.value = false;
  window.location.href = "/signin";
};

onMounted(checkAuth);
</script>
