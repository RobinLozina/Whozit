<template>
  <div class="flex min-h-screen flex-col items-center justify-center gap-4 p-4">
    <p
      v-if="opponentLeft"
      role="status"
      class="w-full max-w-md rounded-lg bg-zap px-4 py-3 font-medium text-tray"
    >
      Your opponent left the game.
    </p>

    <form
      v-if="isCreator"
      @submit.prevent="startGame"
      class="panel w-full max-w-md p-6"
    >
      <fieldset>
        <legend class="mb-4 font-display text-4xl tracking-wide">
          Choose a character set
        </legend>
        <div class="flex flex-col gap-2">
          <label
            v-for="folder in filteredFolders"
            :key="folder"
            class="flex cursor-pointer items-center gap-3 rounded-lg border-2 px-4 py-3 text-lg transition-colors"
            :class="
              selectedFolder === folder
                ? 'border-zap bg-board'
                : 'border-white/30 hover:border-white'
            "
          >
            <input
              type="radio"
              name="folder"
              :value="folder"
              v-model="selectedFolder"
              class="h-5 w-5 accent-zap"
            />
            {{ folder }}
          </label>
        </div>
      </fieldset>
      <button type="submit" :disabled="!selectedFolder" class="btn mt-6 w-full">
        Start game
      </button>
    </form>

    <p v-else class="text-center font-display text-4xl tracking-wide">
      Waiting for the host to start the game…
    </p>
  </div>
</template>

<script>
import axios from "axios";
import { API_URL, WS_URL } from "../backend";

export default {
  data() {
    return {
      roomCode: this.$route.params.code,
      players: [],
      isCreator: false,
      ws: null, // WebSocket connection
      availableFolders: [], // List of available character folders
      selectedFolder: null, // Folder selected by the creator
      isCouilloumVisible: false, // Visibility flag for "Couilloum" folder
      typedKeys: "", // Track user key inputs
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

    // If the player is the creator, fetch the available character folders
    this.fetchAvailableFolders();

    // Add keydown event listener
    window.addEventListener("keydown", this.handleKeyPress);
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close(); // Close WebSocket when component is destroyed
    }
    // Remove keydown event listener
    window.removeEventListener("keydown", this.handleKeyPress);
  },
  computed: {
    opponentLeft() {
      return this.$route.query.left === "1";
    },
    filteredFolders() {
      return this.availableFolders.filter((folder) => {
        return folder !== "Couilloum" || this.isCouilloumVisible;
      });
    },
    shortRoomCode() {
      if (this.roomCode.length <= 4) {
        return this.roomCode;
      }
      return "*".repeat(this.roomCode.length - 4) + this.roomCode.slice(-4);
    },
  },
  methods: {
    async joinRoom() {
      try {
        const response = await axios.post(
          `${API_URL}/api/join/${this.roomCode}/`,
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
          `${API_URL}/api/waiting/${this.roomCode}/?player_id=${playerId}`,
        );

        this.players = response.data.room.players;
        this.isCreator = response.data.is_creator;

        if (this.isCreator) {
          this.fetchAvailableFolders();
        }
      } catch (error) {
        console.error("Error fetching room details:", error);
      }
    },
    async fetchAvailableFolders() {
      try {
        // Fetch the list of available character folders
        const response = await axios.get(`${API_URL}/api/character_folders/`);
        this.availableFolders = response.data.folders; // Assuming response returns an array of folder names
      } catch (error) {
        console.error("Error fetching character folders:", error);
      }
    },
    connectWebSocket() {
      const wsUrl = `${WS_URL}/ws/waiting/${this.roomCode}/`;
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
        console.log("WebSocket connection closed for waiting room.");
      };
    },
    startGame() {
      if (this.ws && this.selectedFolder) {
        // Send message via WebSocket to signal that the game is starting with the selected folder
        this.ws.send(
          JSON.stringify({
            event: "start_game",
            folder: this.selectedFolder,
          }),
        );
      }
    },
    handleKeyPress(event) {
      // Track typed keys
      this.typedKeys += event.key;

      // If the user types "c!", reveal the "Couilloum" folder
      if (this.typedKeys.includes("c!")) {
        this.isCouilloumVisible = true;
        this.typedKeys = ""; // Reset the key tracker after detection
      }

      // Limit the length of `typedKeys` to prevent it from growing indefinitely
      if (this.typedKeys.length > 2) {
        this.typedKeys = this.typedKeys.slice(-2);
      }
    },
  },
};
</script>
