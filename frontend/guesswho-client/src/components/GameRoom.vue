<template>
  <div class="game">
    <h2 class="text-center text-2xl font-bold">Game Room: {{ roomCode }}</h2>
    <button @click="toggleGuessMode" class="guess-button">Guess</button>
    <GameBoard
      :characters="characters"
      :is-guess-mode="isGuessMode"
      @character-selected="handleCharacterSelection"
    />
    <div v-if="otherPlayerCharacter" class="player-character">
      <h3>Your Opponent's Character to Guess</h3>
      <div class="assigned-character">
        <img
          :src="otherPlayerCharacter.image_url"
          :alt="otherPlayerCharacter.name"
          class="assigned-character-image"
        />
        <p>{{ otherPlayerCharacter.name }}</p>
      </div>
    </div>
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" class="message">
        {{ message }}
      </div>
    </div>
    <input
      v-model="newMessage"
      @keyup.enter="sendMessage"
      placeholder="Type your question or guess..."
      class="input-message"
    />
  </div>
</template>

<script>
import GameBoard from "./GameBoard.vue";

export default {
  components: {
    GameBoard,
  },
  data() {
    return {
      roomCode: this.$route.params.code,
      newMessage: "",
      messages: [],
      characters: [],
      playerCharacter: null, // Player's assigned character
      otherPlayerCharacter: null, // Opponent's character
      isGuessMode: false, // Track if the player is in guess mode
      ws: null,
      playerId:
        sessionStorage.getItem("playerId") || Math.floor(Math.random() * 100), // Random ID for demo, store if not already present
    };
  },
  mounted() {
    this.connectToWebSocket();
    sessionStorage.setItem("playerId", this.playerId); // Persist player ID
  },
  methods: {
    connectToWebSocket() {
      const wsUrl = `ws://127.0.0.1:8000/ws/game/${this.roomCode}/`;
      console.log("Connecting to WebSocket for Game Room:", wsUrl);
      this.ws = new WebSocket(wsUrl);

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WebSocket Message For Game Received:", data);
        if (data.message.event === "game_started") {
          this.characters = data.message.characters;

          // Assign characters to player and opponent
          const playerIndex = this.playerId % 2;
          this.playerCharacter = data.message.player_characters[playerIndex];
          this.otherPlayerCharacter =
            data.message.player_characters[1 - playerIndex];
        } else if (data.message.event === "chat") {
          this.messages.push(data.message.message);
        } else if (data.message.event === "guess_result") {
          alert(`Guess was ${data.message.correct ? "correct" : "incorrect"}!`);
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket connection closed for Game Room.");
      };
    },
    sendMessage() {
      if (this.newMessage.trim()) {
        this.ws.send(
          JSON.stringify({ event: "chat", message: this.newMessage })
        );
        this.newMessage = "";
      }
    },
    toggleGuessMode() {
      this.isGuessMode = true;
    },
    handleCharacterSelection(character) {
      if (this.isGuessMode) {
        // Send the guess to the backend if in guess mode
        console.log(`Character guessed: ${character.name}`);
        this.ws.send(
          JSON.stringify({
            event: "guess_character",
            character_name: character.name,
            player_id: this.playerId,
          })
        );
        // Disable guess mode after making a guess
        this.isGuessMode = false;
      }
    },
  },
};
</script>

<style scoped>
.game {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}
.guess-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
.guess-button:hover {
  background-color: #0056b3;
}
.messages {
  margin-bottom: 20px;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  background-color: #f9f9f9;
}
.input-message {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.player-character {
  margin-top: 20px;
  text-align: center;
}
.assigned-character {
  display: inline-block;
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
  margin-top: 10px;
}
.assigned-character-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}
</style>
