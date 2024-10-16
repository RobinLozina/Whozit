<template>
  <div
    class="game-piece"
    :class="{ lowered: isLowered }"
    @click="toggleLowered"
  >
    <img
      :src="character.image_url"
      :alt="character.name"
      class="character-image"
    />
    <p>{{ character.name }}</p>
    <p>HELLO</p>
  </div>
</template>

<script>
export default {
  props: {
    character: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isLowered: this.character.isLowered || false, // Local state to manage lowered status
    };
  },
  methods: {
    toggleLowered() {
      this.isLowered = !this.isLowered;

      // Emit an event to notify the GameBoard component that the character was clicked
      this.$emit("character-clicked", {
        ...this.character,
        isLowered: this.isLowered,
      });
    },
  },
};
</script>

<style scoped>
.game-piece {
  width: 100px;
  height: 150px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s;
}

.game-piece.lowered {
  transform: translateY(20px);
  opacity: 0.7;
}
.character-image {
  width: 100%;
  height: auto;
}
</style>
