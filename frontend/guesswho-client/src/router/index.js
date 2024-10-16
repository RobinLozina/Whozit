import { createRouter, createWebHistory } from "vue-router";
import HomeRoom from "../components/HomeRoom.vue";
import GameRoom from "../components/GameRoom.vue";
import WaitingRoom from "../components/WaitingRoom.vue";

// Define the routes
const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeRoom, // Use the HomeRoom
  },
  {
    path: "/waiting/:code",
    name: "Waiting",
    component: WaitingRoom, // Use the WaitingRoom
  },
  {
    path: "/game/:code",
    name: "Game",
    component: GameRoom, // Use the GameRoom
  },
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(), // Use history mode
  routes,
});

// Export the router
export default router;
