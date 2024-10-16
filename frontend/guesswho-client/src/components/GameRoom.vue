<template>
  <div class="game">
    <h2 class="text-center text-2xl font-bold">Game Room: {{ roomName }}</h2>
    <GameBoard
      :characters="characters"
      @character-selected="handleCharacterSelection"
    />
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
      roomName: this.$route.params.roomName,
      newMessage: "",
      messages: [],
      characters: [],
      ws: null,
    };
  },
  created() {
    this.connectToWebSocket();
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  },
  methods: {
    connectToWebSocket() {
      const wsUrl = `ws://127.0.0.1:8000/ws/game/${this.roomName}/`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.message.event === "game_started") {
          this.characters = data.message.characters; // Set character data when game starts
        } else if (data.message.event === "chat") {
          this.messages.push(data.message.message);
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket connection closed.");
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
    handleCharacterSelection(character) {
      // Update game state when a character is selected
      console.log(`Character selected: ${character.name}`);
      // Send character selection update to server (optional)
      this.ws.send(JSON.stringify({ event: "character_selected", character }));
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
</style>
