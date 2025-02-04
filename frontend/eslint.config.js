import js from "@eslint/js";
import pluginVue from "eslint-plugin-vue";

export default [
  {
    name: "app/files-to-lint",
    files: ["**/*.{js,mjs,jsx,vue}"],
  },
  {
    name: "app/files-to-ignore",
    ignores: ["**/dist/**", "**/dist-ssr/**", "**/coverage/**"],
  },
  {
    name: "app/vue-rules",
    rules: {
      "vue/multi-word-component-names": "off",
    },
  },
  js.configs.recommended,
  {
    ...pluginVue.configs["flat/essential"],
    rules: {
      ...pluginVue.configs["flat/essential"].rules,
      "vue/multi-word-component-names": "off",
    },
  },
];
