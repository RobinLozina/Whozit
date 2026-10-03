<template>
  <div class="flex min-h-screen flex-col items-center justify-center gap-6 p-4 text-center">
    <h1 class="font-display text-7xl tracking-wide drop-shadow-lg sm:text-8xl">
      Whozit?
    </h1>

    <template v-if="roomCode">
      <p v-if="isWaiting" class="text-xl">
        Send the invite link to a friend. The game opens when they join.
      </p>
      <button @click="copyRoomLink" class="btn w-72">
        {{ linkCopied ? "Link copied" : "Copy invite link" }}
      </button>
      <p class="text-sm text-white/75">Room {{ shortRoomCode }}</p>
    </template>

    <button @click="generateNewRoom" class="btn btn-quiet">New room</button>
  </div>
</template>

<script>
import axios from "axios";
import { API_URL, WS_URL } from "../backend";

export default {
  data() {
    return {
      roomCode: "",
      isWaiting: false, // Track if the player is waiting for another player
      intervalId: null, // To store the interval ID for clearing later
      socket: null, // WebSocket connection
      linkCopied: false, // Track if the link has been copied
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
      return "…" + this.roomCode.slice(-4);
    },
  },
  methods: {
    async generateNewRoom() {
      try {
        // Create a new room via the backend API
        const response = await axios.post(`${API_URL}/api/rooms/`);
        this.roomCode = response.data.code;
        this.isWaiting = true; // Set waiting state to true

        // Store the creator player ID in local storage
        sessionStorage.setItem("playerId", response.data.players[0].id);
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
          `${API_URL}/api/join/${this.roomCode}/`
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

    copyRoomLink() {
      const link = `${window.location.origin}/waiting/${this.roomCode}`;
      navigator.clipboard.writeText(link);

      // Set linkCopied to true to update the button text
      this.linkCopied = true;

      // Set a timer to revert the button text back to 'Copy Room Link' after 3 seconds
      setTimeout(() => {
        this.linkCopied = false;
      }, 3000);
    },
    connectWebSocket() {
      const socketUrl = `${WS_URL}/ws/waiting/${this.roomCode}/`;
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

