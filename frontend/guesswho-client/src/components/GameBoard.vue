<template>
  <div class="grid grid-cols-4 gap-2 sm:grid-cols-6 sm:gap-3 xl:grid-cols-8">
    <GamePiece
      v-for="(character, index) in characters"
      :key="index"
      :character="character"
      :is-guess-mode="isGuessMode"
      :is-selected="
        isGuessMode &&
        !!selectedCharacter &&
        selectedCharacter.name === character.name
      "
      @character-clicked="$emit('character-selected', $event)"
    />
  </div>
</template>

<script>
import GamePiece from "./GamePiece.vue";

export default {
  components: {
    GamePiece,
  },
  props: {
    characters: {
      type: Array,
      required: true,
    },
    isGuessMode: {
      type: Boolean,
      required: true,
    },
    selectedCharacter: {
      type: Object,
      required: false,
      default: null,
    },
  },
  emits: ["character-selected"],
};
</script>
