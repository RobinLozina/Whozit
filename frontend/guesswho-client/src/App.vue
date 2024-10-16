<template>
  <div id="app" class="bg-gray-100 min-h-screen flex flex-col">
    <header class="bg-blue-600 text-white p-4 text-center">
      <h1 class="text-3xl font-bold">Guess Who?</h1>
    </header>

    <main class="flex-grow container mx-auto p-4">
      <router-view />
      <!-- This will render the current route component (Home or Game) -->
    </main>

    <footer class="bg-gray-800 text-white text-center p-2">
      <p>&copy; 2024 Guess Who? Game</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Optional global styles */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding: 0 20px;
}
</style>
