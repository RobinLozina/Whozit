<template>
  <div class="game-board">
    <GamePiece
      v-for="(character, index) in characters"
      :key="index"
      :character="character"
      :is-guess-mode="isGuessMode"
      :is-selected="
        selectedCharacter && selectedCharacterName === character.name
      "
      @character-clicked="selectCharacter"
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
  data() {
    return {
      selectedCharacterName: null, // Track the currently selected character by ID
    };
  },
  methods: {
    selectCharacter(character) {
      if (this.isGuessMode) {
        // Set the selected character ID to the current character's ID
        this.selectedCharacterName = character.name;

        // Emit the character that was clicked to the parent component
        this.$emit("character-selected", character);
      }
    },
  },
};
</script>

<style scoped>
.game-board {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-template-rows: repeat(4, auto);
  column-gap: 10px;
  row-gap: 20px;
  padding: 20px;
}
</style>
