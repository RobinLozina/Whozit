<template>
  <div
    class="game-piece"
    :class="{ lowered: isLowered, selected: isSelected }"
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
.game-piece {
  width: 100px; /* Fixed width */
  height: 150px; /* Fixed height */
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.game-piece.lowered {
  transform: translateY(20px);
  opacity: 0.7;
}

.game-piece.selected {
  border-color: rebeccapurple;
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
