<template>
  <div id="app" class="bg-animated-gradient min-h-screen">
    <main class="flex-grow">
      <router-view />
      <!-- This will render the current route component (Home or Game) -->
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style scoped>
/* Optional global styles */
#app {
  font-family: "Futura PT", "Bangers", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}

/* Background gradient and animation */
.bg-animated-gradient {
  background: linear-gradient(200deg, #1156fc 35%, hsl(169, 100%, 50%) 100%);
  background-size: 200% 200%;
  animation: colorTransition 5s alternate infinite;
}

@keyframes colorTransition {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
