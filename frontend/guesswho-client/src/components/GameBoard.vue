<template>
  <div class="game-board">
    <GamePiece
      v-for="(character, index) in characters"
      :key="index"
      :character="character"
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
  },
  methods: {
    selectCharacter(character) {
      // Emit the character that was clicked to the parent component
      this.$emit("character-selected", character);
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
