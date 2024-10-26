<template>
  <div
    class="game-piece w-28 h-36 rounded-lg border-4 pt-1 pb-4 px-4 bg-red-600 text-white flex flex-col items-center cursor-pointer transition-transform transform hover:scale-105"
    :class="{
      'opacity-70 translate-y-2': isLowered,
      'is-selected': isSelected,
    }"
    @click="toggleLowered"
  >
    <p class="mb-2 text-sm font-bold">{{ character.name }}</p>
    <img
      :src="character.image_url"
      :alt="character.name"
      class="w-20 h-20 object-cover rounded-lg"
    />
  </div>
</template>

<script>
export default {
  props: {
    character: {
      type: Object,
      required: true,
    },
    isGuessMode: {
      type: Boolean,
      required: false,
      default: false,
    },
    isSelected: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      isLowered: this.character.isLowered || false,
    };
  },
  methods: {
    toggleLowered() {
      if (this.isGuessMode) {
        // Emit the selected character to the GameBoard
        this.$emit("character-clicked", this.character);
      } else {
        // Toggle the lowered state if not in guess mode
        this.isLowered = !this.isLowered;
      }
    },
  },
};
</script>

<style scoped>
.is-selected {
  border: 4px solid #e0e300;
}
</style>
