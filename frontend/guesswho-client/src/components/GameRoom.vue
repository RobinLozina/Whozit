<template>
  <div class="relative min-h-screen flex flex-row p-4">
    <!-- Game Board and Controls -->
    <div class="flex flex-col w-3/4 pr-4">
      <GameBoard
        :characters="characters"
        :is-guess-mode="isGuessMode"
        :selected-character="selectedCharacter"
        @character-selected="handleCharacterSelection"
      />

      <!-- Opponent Character Info -->
      <div v-if="otherPlayerCharacter" class="mt-2 text-center">
        <h3 class="text-xl font-bold mb-2 text-white">
          Your Opponent's Character to Guess
        </h3>
        <div
          class="border-4 w-28 h-36 inline-block rounded-lg pt-1 pb-4 px-4 bg-red-600 text-white"
        >
          <p class="mb-2 text-sm font-bold">
            {{ otherPlayerCharacter.name }}
          </p>
          <img
            :src="otherPlayerCharacter.image_url"
            :alt="otherPlayerCharacter.name"
            class="w-20 h-20 object-cover rounded-lg"
          />
        </div>
      </div>

      <!-- Guess button or "The other player is guessing!" message -->
      <div class="flex items-center justify-center mt-4">
        <button
          v-if="!isGuessMode && !opponentIsGuessing && !showReturnButton"
          @click="toggleGuessMode"
          class="custom-button"
        >
          Guess
        </button>
        <p
          v-else-if="opponentIsGuessing"
          class="text-2xl text-center font-bold"
        >
          The other player is guessing!
        </p>
      </div>

      <!-- Confirm Guess and Quit Guessing buttons -->
      <div v-if="isGuessMode" class="flex justify-center">
        <button
          v-if="selectedCharacter"
          @click="confirmGuess"
          class="mr-2 custom-button"
        >
          Confirm Guess
        </button>
        <button @click="quitGuessMode" class="custom-button">
          Quit Guessing
        </button>
      </div>

      <!-- Return to Waiting Room button -->
      <div v-if="showReturnButton" class="flex justify-center">
        <button @click="returnToWaitingRoom" class="custom-button">
          Return to Waiting Room
        </button>
      </div>
    </div>

    <!-- Chat Messages and Input -->
    <div class="chat-container w-1/4 flex flex-col">
      <div
        class="messages border-2 border-gray-400 rounded p-4 bg-gray-800 text-white overflow-y-auto flex-grow"
      >
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="message mb-2"
        >
          <div
            class="p-2 rounded-md"
            :class="{
              'bg-blue-500 text-white ml-auto w-2/3 text-right':
                message.player_id === playerId,
              'bg-yellow-500 text-black mr-auto w-2/3 text-left':
                message.player_id !== playerId,
            }"
          >
            {{ message.text }}
          </div>
        </div>
      </div>

      <!-- Input Section - Fixed at the Bottom -->
      <div class="mt-2">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Type your question or guess..."
          class="p-2 border-2 border-gray-300 text-black rounded w-full"
        />
      </div>
    </div>

    <!-- Winner Modal -->
    <div
      v-if="showWinnerModal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg text-center">
        <h2 class="text-3xl text-black font-bold mb-4">{{ winnerMessage }}</h2>
        <button @click="closeWinnerModal" class="custom-button mt-4">OK</button>
      </div>
    </div>
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
      showWinnerModal: false, // Control visibility of winner modal
      winnerMessage: "", // Message to show in the winner modal
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
          this.messages.push({
            text: data.message.message,
            player_id: data.message.player_id,
          });
        } else if (data.message.event === "guess_result") {
          // Different message for guesser and opponent
          console.log(data.message);
          if (data.message.player_id === this.playerId) {
            // The player who made the guess
            this.showWinnerModal = true;
            this.winnerMessage = data.message.correct
              ? "Congratulations! You guessed correctly!"
              : "Oops! Your guess was incorrect.";
            console.log(this.winnerMessage);
          } else {
            // The opponent
            this.showWinnerModal = true;
            this.winnerMessage = data.message.correct
              ? "The other player's guess was correct. You lose!"
              : "Nice! The other player's guess was wrong. You win!";
          }
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
          JSON.stringify({
            event: "chat",
            message: this.newMessage,
            player_id: this.playerId,
          })
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
        this.ws.send(
          JSON.stringify({
            event: "guess_character",
            character_name: this.selectedCharacter.name,
            player_id: this.playerId,
          })
        );

        // Exit guess mode
        this.quitGuessMode();
      }
    },
    quitGuessMode() {
      this.isGuessMode = false;
      this.selectedCharacter = null;

      this.ws.send(
        JSON.stringify({
          event: "quit_guessing",
        })
      );
    },
    returnToWaitingRoom() {
      this.$router.push(`/waiting/${this.roomCode}`);
    },
    closeWinnerModal() {
      this.showWinnerModal = false;
      this.winnerMessage = "";
    },
  },
};
</script>

<style scoped>
.custom-button {
  padding: 8px;
  width: 200px;
  color: #ffffff;
  border: 4px solid #e0e300;
  background-color: #1156fc;
  border-radius: 4px;
  font-size: 16px;
  text-transform: uppercase;
  font-weight: 600;
  cursor: pointer;
  z-index: 1000;
  transition: all linear 100ms;
}

.chat-container {
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.messages {
  flex-grow: 1;
}

.message {
  word-wrap: break-word; /* Ensure long words break */
  word-break: break-word; /* Handle overflow gracefully */
  max-width: 100%; /* Make sure the message doesn't exceed its container width */
}

.custom-button:hover {
  background-color: #e0e300;
  color: #1156fc;
  border-color: #e0e300;
  box-shadow: 0px 0px 10px 4px #e0e300;
}
</style>
