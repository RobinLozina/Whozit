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
  justify-content: space-between; /* Ensure even spacing between elements */
}

.game-piece.lowered {
  transform: translateY(20px);
  opacity: 0.7;
}

.character-image {
  width: 80px; /* Consistent width for all images */
  height: 80px; /* Consistent height for all images */
  object-fit: cover; /* Ensure the image covers the area without distortion */
  border-radius: 50%; /* Makes the image round, optional */
}

.character-name {
  margin-top: 5px; /* Add some space between the image and the name */
  font-size: 12px; /* Make the font size suitable for the container */
  white-space: nowrap; /* Prevent the text from wrapping to the next line */
  overflow: hidden; /* Hide overflowing text */
  text-overflow: ellipsis; /* Add an ellipsis (...) if the text overflows */
  width: 100%; /* Ensure the text takes the full width of the container */
}
</style>
