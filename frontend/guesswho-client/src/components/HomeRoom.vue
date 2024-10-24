<template>
  <div class="home-room relative min-h-screen p-5">
    <div
      class="top-right absolute top-6 right-6 flex flex-col items-center w-72"
    >
      <h1 v-if="roomCode" class="info-text text-center mb-2 text-xl">
        <span>Room: </span>
        <span class="font-futura">{{ shortRoomCode }}</span>
      </h1>
      <button @click="generateNewRoom" class="custom-button">
        Generate New Room
      </button>
    </div>

    <div
      class="centered absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
    >
      <div v-if="isWaiting" class="info-text text-center mb-5 text-4xl">
        <p>Waiting for another player to join...</p>
      </div>
      <button @click="copyRoomLink" v-if="roomCode" class="custom-button">
        Copy Room Link
      </button>
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
  computed: {
    shortRoomCode() {
      if (this.roomCode.length <= 4) {
        return this.roomCode;
      }
      return "*".repeat(this.roomCode.length - 4) + this.roomCode.slice(-4);
    },
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
.custom-button {
  padding: 8px;
  width: 300px;
  margin: 16px;
  color: #ffffff;
  border: 4px solid #e0e300; /* Yellow border */
  background-color: #1156fc; /* Blue background */
  border-radius: 4px;
  font-size: 16px;
  font-family: "Futura PT", sans-serif;
  text-transform: uppercase;
  font-weight: 600;
  cursor: pointer;
  z-index: 1000;
  transition: all linear 100ms;
}

.custom-button:hover {
  background-color: #e0e300; /* Yellow background */
  color: #1156fc; /* Blue text */
  border-color: #e0e300; /* Keep the border yellow */
  box-shadow: 0px 0px 10px 4px #e0e300; /* Yellow shadow around the button */
}
</style>
