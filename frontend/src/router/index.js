import { createRouter, createWebHistory } from "vue-router";
import { isAuthenticated } from "@/services/authenticatedService"; // Import our secure function
import SignIn from "@/views/SigninView.vue";
import SignUp from "@/views/SignupView.vue";
import DataManagementView from "@/views/DataManagementView.vue";
import SchemaFormView from "@/views/SchemaFormView.vue";
import DataImportFormView from "@/views/DataImportFormView.vue";

const routes = [
  { path: "/signin", component: SignIn },
  { path: "/signup", component: SignUp },
  {
    path: "/",
    name: "home",
    component: DataManagementView,
  },
  {
    path: "/createSchema",
    name: "create",
    component: SchemaFormView,
  },
  {
    path: "/importData/:table_name",
    name: "importData",
    component: DataImportFormView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const auth = await isAuthenticated();

  if (!auth && to.path !== "/signin" && to.path !== "/signup") {
    next("/signin");
  } else if (auth && (to.path === "/signin" || to.path === "/signup")) {
    next("/");
  } else {
    next();
  }
});

export default router;
