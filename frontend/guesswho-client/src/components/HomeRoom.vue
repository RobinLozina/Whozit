<template>
  <div class="home-room">
    <h1 v-if="roomCode">Room Code: {{ roomCode }}</h1>
    <div>
      <button @click="copyRoomLink" v-if="roomCode">Copy Room Link</button>
      <button @click="generateNewRoom">Generate New Room</button>
    </div>
    <div v-if="isWaiting">
      <p>Waiting for another player to join...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      roomCode: "",
      isWaiting: false, // Track if the player is waiting for another player
      intervalId: null, // To store the interval ID for clearing later
      socket: null, // WebSocket connection
    };
  },
  created() {
    const playerId = sessionStorage.getItem("playerId");

    if (this.$route.params.code) {
      // Player is joining an existing room using a shared link
      this.roomCode = this.$route.params.code;
      if (!playerId) {
        // If there's no player ID, the player hasn't joined yet
        this.joinRoom();
      } else {
        // If player has already joined, start fetching room details
        this.checkForPlayers();
      }
    } else {
      // If there is no code in the URL, generate a new room
      this.generateNewRoom();
    }
  },
  beforeUnmount() {
    // Clear interval when the component is destroyed to prevent memory leaks
    clearInterval(this.intervalId);
    if (this.socket) {
      this.socket.close(); // Close WebSocket connection
    }
  },
  methods: {
    async generateNewRoom() {
      try {
        // Create a new room via the backend API
        const response = await axios.post("http://127.0.0.1:8000/api/rooms/");
        this.roomCode = response.data.code;
        this.isWaiting = true; // Set waiting state to true

        // Store the creator player ID in local storage
        sessionStorage.setItem("playerId", response.data.players[0].id);
        console.log("generated a new room");
        // Set up WebSocket connection for real-time updates
        this.connectWebSocket();
      } catch (error) {
        console.error("Error creating room:", error);
      }
    },
    async joinRoom() {
      try {
        // Join the existing room with the room code
        const response = await axios.post(
          `http://127.0.0.1:8000/api/join/${this.roomCode}/`
        );

        // Store player ID in local storage for later use
        sessionStorage.setItem("playerId", response.data.player_id);
        this.isWaiting = true;

        // Set up WebSocket connection for real-time updates
        this.connectWebSocket();
      } catch (error) {
        console.error("Error joining room:", error);
      }
    },
    async checkForPlayers() {
      // This function is kept for compatibility but WebSocket is now the preferred way.
      this.intervalId = setInterval(async () => {
        try {
          const playerId = sessionStorage.getItem("playerId");
          const response = await axios.get(
            `http://127.0.0.1:8000/api/waiting/${this.roomCode}/?player_id=${playerId}`
          );
          if (response.data.room.players.length > 1) {
            clearInterval(this.intervalId); // Stop checking if another player has joined
            // Redirect to waiting room if more than one player is present
            this.$router.push(`/waiting/${this.roomCode}`);
          }
        } catch (error) {
          console.error("Error checking players:", error);
        }
      }, 2000); // Check every 2 seconds
    },
    copyRoomLink() {
      const link = `${window.location.origin}/waiting/${this.roomCode}`;
      navigator.clipboard.writeText(link);
      console.log("copy link and room code is : " + this.roomCode);
      alert("Room link copied!");
    },
    connectWebSocket() {
      console.log("trying to connect to web socket");
      const socketUrl = `ws://127.0.0.1:8000/ws/waiting/${this.roomCode}/`;
      this.socket = new WebSocket(socketUrl);

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.message.event === "player_joined") {
          // Redirect to the waiting room as another player has joined
          clearInterval(this.intervalId); // Stop polling, as WebSocket takes over
          this.$router.push(`/waiting/${this.roomCode}`);
        }
      };

      this.socket.onopen = () => {
        console.log("WebSocket connection established");
      };

      this.socket.onclose = () => {
        console.log("WebSocket connection closed");
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },
  },
};
</script>

<style scoped>
.buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>

<style scoped>
.buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
