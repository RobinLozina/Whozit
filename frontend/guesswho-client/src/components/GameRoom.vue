<template>
  <div class="game">
    <h2 class="text-center text-2xl font-bold">Game Room: {{ roomCode }}</h2>

    <!-- Guess button or "The other player is guessing!" message -->
    <button
      v-if="!isGuessMode && !opponentIsGuessing && !showReturnButton"
      @click="toggleGuessMode"
      class="guess-button"
    >
      Guess
    </button>
    <p v-else-if="opponentIsGuessing" class="guessing-message">
      The other player is guessing!
    </p>

    <!-- Confirm Guess and Quit Guessing buttons -->
    <div v-if="isGuessMode" class="guess-mode-controls">
      <button
        v-if="selectedCharacter"
        @click="confirmGuess"
        class="confirm-guess-button"
      >
        Confirm Guess
      </button>
      <button @click="quitGuessMode" class="quit-guess-button">
        Quit Guessing
      </button>
    </div>

    <!-- Return to Waiting Room button -->
    <div v-if="showReturnButton" class="return-waiting-room">
      <button @click="returnToWaitingRoom" class="return-waiting-button">
        Return to Waiting Room
      </button>
    </div>

    <GameBoard
      :characters="characters"
      :is-guess-mode="isGuessMode"
      :selected-character="selectedCharacter"
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
      playerCharacter: null,
      otherPlayerCharacter: null,
      isGuessMode: false,
      opponentIsGuessing: false,
      selectedCharacter: null,
      showReturnButton: false, // To control visibility of return button
      ws: null,
      playerId:
        sessionStorage.getItem("playerId") || Math.floor(Math.random() * 100),
    };
  },
  mounted() {
    this.connectToWebSocket();
    sessionStorage.setItem("playerId", this.playerId);
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

          const playerIndex = this.playerId % 2;
          this.playerCharacter = data.message.player_characters[playerIndex];
          this.otherPlayerCharacter =
            data.message.player_characters[1 - playerIndex];
        } else if (data.message.event === "chat") {
          this.messages.push(data.message.message);
        } else if (data.message.event === "guess_result") {
          alert(`Guess was ${data.message.correct ? "correct" : "incorrect"}!`);
          // Show return button after guess is made
          this.showReturnButton = true;
        } else if (data.message.event === "guess_mode") {
          if (data.message.is_guessing) {
            if (data.message.player_id !== this.playerId) {
              this.opponentIsGuessing = true;
            }
          } else {
            this.opponentIsGuessing = false;
          }
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
      this.selectedCharacter = null;

      this.ws.send(
        JSON.stringify({
          event: "guess_mode",
          player_id: this.playerId,
        })
      );
    },
    handleCharacterSelection(character) {
      if (this.isGuessMode) {
        this.selectedCharacter = character;
      }
    },
    confirmGuess() {
      if (this.selectedCharacter) {
        console.log(`Character guessed: ${this.selectedCharacter.name}`);
        this.ws.send(
          JSON.stringify({
            event: "guess_character",
            character_name: this.selectedCharacter.name,
            player_id: this.playerId,
          })
        );
        console.log("guessed character sent");

        // Exit guess mode
        this.quitGuessMode();
      }
    },
    quitGuessMode() {
      console.log("Guessing canceled");
      this.isGuessMode = false;
      this.selectedCharacter = null;

      this.ws.send(
        JSON.stringify({
          event: "quit_guessing",
        })
      );
    },
    returnToWaitingRoom() {
      // Redirect the user to the waiting room
      this.$router.push(`/waiting/${this.roomCode}`);
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

.guess-mode-controls {
  margin-top: 20px;
}

.confirm-guess-button {
  margin-right: 10px;
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
.confirm-guess-button:hover {
  background-color: #218838;
}

.quit-guess-button {
  padding: 10px 20px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
.quit-guess-button:hover {
  background-color: #c82333;
}

.return-waiting-room {
  margin-top: 20px;
  text-align: center;
}
.return-waiting-button {
  padding: 10px 20px;
  background-color: #ffcc00;
  color: black;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
.return-waiting-button:hover {
  background-color: #e6b800;
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
