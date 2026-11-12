/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Composables
import { createVuetify } from "vuetify";
// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { type ThemeDefinition } from "vuetify";

const quackparserDarkTheme = {
  dark: true,
  colors: {
    background: "#0a0c14",
    surface: "#161b26",
    "surface-variant": "#080a0f",
    primary: "#facc15",
    secondary: "#f97316",
  },
};

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: "quackparserDarkTheme",
    themes: {
      quackparserDarkTheme,
    },
  },
});
