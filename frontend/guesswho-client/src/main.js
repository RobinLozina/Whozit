import { createApp } from "vue";
import App from "./App.vue";
import "./assets/styles.css";
import router from "./router"; // Import the router configuration

const app = createApp(App); // Create a Vue app instance
app.use(router); // Use the router
app.mount("#app"); // Mount the app to the DOM
