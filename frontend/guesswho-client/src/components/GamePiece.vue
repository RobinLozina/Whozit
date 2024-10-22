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
    <p class="character-name">{{ character.name }}</p>
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
  },
  data() {
    return {
      isLowered: this.character.isLowered || false,
    };
  },
  methods: {
    toggleLowered() {
      if (this.isGuessMode) {
        this.$emit("character-clicked", this.character);
      } else {
        this.isLowered = !this.isLowered;
        // Optionally keep lowering logic outside guess mode
      }
    },
  },
};
</script>

<style scoped>
.game-piece {
  width: 100px; /* Fixed width */
  height: 150px; /* Fixed height */
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s;
  display: flex; /* Use flexbox to align items */
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.game-piece.lowered {
  transform: translateY(20px);
  opacity: 0.7;
}

.character-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 50%;
}

.character-name {
  margin-top: 5px;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}
</style>
