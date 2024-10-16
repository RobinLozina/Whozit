<template>
  <div class="waiting-room">
    <h1>Waiting Room: {{ roomCode }}</h1>
    <ul>
      <li v-for="player in players" :key="player.id">
        Player ID: {{ player.id }}
        <span v-if="player.is_creator">(Creator)</span>
      </li>
    </ul>
    <div v-if="isCreator">
      <button @click="startGame">Start Game</button>
      <!-- Add additional controls for the creator here -->
    </div>
    <div v-else>
      <p>Waiting for the creator to start the game...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      roomCode: this.$route.params.code,
      players: [],
      isCreator: false,
      ws: null, // WebSocket connection
    };
  },
  created() {
    const playerId = sessionStorage.getItem("playerId");

    if (!playerId) {
      this.joinRoom();
    } else {
      this.fetchRoomDetails();
    }

    // Establish WebSocket connection to listen for game start
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close(); // Close WebSocket when component is destroyed
    }
  },
  methods: {
    async joinRoom() {
      try {
        const response = await axios.post(
          `http://127.0.0.1:8000/api/join/${this.roomCode}/`
        );

        sessionStorage.setItem("playerId", response.data.player_id);
        this.fetchRoomDetails();
      } catch (error) {
        console.error("Error joining room:", error);
      }
    },
    async fetchRoomDetails() {
      try {
        const playerId = sessionStorage.getItem("playerId");
        const response = await axios.get(
          `http://127.0.0.1:8000/api/waiting/${this.roomCode}/?player_id=${playerId}`
        );

        this.players = response.data.room.players;
        this.isCreator = response.data.is_creator;
      } catch (error) {
        console.error("Error fetching room details:", error);
      }
    },
    connectWebSocket() {
      const wsUrl = `ws://127.0.0.1:8000/ws/waiting/${this.roomCode}/`;
      this.ws = new WebSocket(wsUrl);

      // Listen for messages from the server
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.message.event === "game_started") {
          // Redirect both players to the GameRoom
          this.$router.push(`/game/${this.roomCode}`);
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket connection closed.");
      };
    },
    startGame() {
      if (this.ws) {
        // Send message via WebSocket to signal that the game is starting
        this.ws.send(JSON.stringify({ event: "start_game" }));
      }
    },
  },
};
</script>

<style scoped>
/* Add any styles you need for the waiting room */
</style>
