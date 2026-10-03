<template>
  <!-- Fixed 3:4 card with a one-line name, so every card is the same size -->
  <button
    type="button"
    class="group relative block aspect-[3/4] w-full [perspective:600px] focus-visible:outline-none"
    :aria-label="character.name"
    :aria-pressed="isGuessMode ? isSelected : isLowered"
    @click="toggleLowered"
  >
    <div
      class="card absolute inset-0 flex flex-col overflow-hidden rounded-lg border-4 bg-plate shadow-md group-focus-visible:ring-4 group-focus-visible:ring-white"
      :class="[
        isSelected ? 'border-zap ring-4 ring-zap' : 'border-white',
        { lowered: isLowered, 'hover:border-zap': isGuessMode },
      ]"
    >
      <img
        :src="character.image_url"
        alt=""
        class="min-h-0 w-full flex-1 bg-white object-contain"
        draggable="false"
      />
      <p
        class="truncate px-1 pb-1 pt-1.5 font-display text-sm leading-none sm:text-base"
        :title="character.name"
      >
        {{ character.name }}
      </p>
    </div>
  </button>
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
  emits: ["character-clicked"],
  data() {
    return {
      isLowered: false,
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
/* Lowered cards tip backwards like the flaps on the real board */
.card {
  transform-origin: bottom;
  transition: transform 250ms cubic-bezier(0.2, 0.8, 0.2, 1), filter 250ms;
}

.card.lowered {
  transform: rotateX(62deg);
  filter: brightness(0.45) saturate(0.4);
}

@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
}
</style>
