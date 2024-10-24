<template>
  <div
    class="waiting-room container mx-auto p-6 text-white min-h-screen flex items-center justify-center"
  >
    <div
      v-if="isCreator"
      class="creator-controls bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col items-center"
    >
      <p class="text-3xl font-bold mb-4">Select Character Folder:</p>
      <div class="flex flex-col space-y-4 mb-6">
        <div
          v-for="folder in filteredFolders"
          :key="folder"
          class="flex items-center space-x-4"
        >
          <input
            type="checkbox"
            :id="folder"
            :value="folder"
            :checked="selectedFolder === folder"
            @change="selectFolder(folder)"
            class="form-checkbox h-6 w-6 text-blue-600 border-gray-300 rounded focus:ring-0"
          />
          <label :for="folder" class="text-2xl">{{ folder }}</label>
        </div>
      </div>
      <button
        @click="startGame"
        :disabled="!selectedFolder"
        class="custom-button"
      >
        Start Game
      </button>
    </div>

    <div v-else class="text-center text-4xl font-sweaty">
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
        const response = await axios.get(
          `http://127.0.0.1:8000/api/character_folders/`
        );
        this.availableFolders = response.data.folders; // Assuming response returns an array of folder names
      } catch (error) {
        console.error("Error fetching character folders:", error);
      }
    },
    connectWebSocket() {
      const wsUrl = `ws://127.0.0.1:8000/ws/waiting/${this.roomCode}/`;
      this.ws = new WebSocket(wsUrl);

      // Listen for messages from the server
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WebSocket Message For Waiting Received:", data); // Log the entire data to see its content

        if (data.message.event === "game_started") {
          // Redirect both players to the GameRoom
          this.$router.push(`/game/${this.roomCode}`);
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket connection closed for waiting room.");
      };
    },
    selectFolder(folder) {
      // Set the selected folder, unselect any other
      if (this.selectedFolder === folder) {
        // If the same folder is clicked, unselect it
        this.selectedFolder = null;
      } else {
        this.selectedFolder = folder;
      }
    },
    startGame() {
      if (this.ws && this.selectedFolder) {
        // Send message via WebSocket to signal that the game is starting with the selected folder
        this.ws.send(
          JSON.stringify({
            event: "start_game",
            folder: this.selectedFolder,
          })
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
