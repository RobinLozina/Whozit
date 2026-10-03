<template>
  <div id="app" class="bg-animated-gradient min-h-screen font-body text-white">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style scoped>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.bg-animated-gradient {
  background: linear-gradient(200deg, #1156fc 35%, hsl(169, 100%, 50%) 100%);
  background-size: 200% 200%;
  animation: colorTransition 5s alternate infinite;
}

@media (prefers-reduced-motion: reduce) {
  .bg-animated-gradient {
    animation: none;
  }
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
