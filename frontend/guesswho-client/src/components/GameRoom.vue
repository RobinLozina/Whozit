<template>
  <div class="mx-auto flex min-h-screen max-w-7xl flex-col gap-4 p-3 sm:p-5">
    <header class="flex items-center justify-between gap-4">
      <h1 class="font-display text-4xl tracking-wide drop-shadow">Whozit?</h1>
      <button @click="leaveGame" class="btn btn-quiet">Leave game</button>
    </header>

    <p
      v-if="!characters.length"
      class="m-auto text-center font-display text-3xl tracking-wide"
    >
      Waiting for your opponent…
    </p>

    <div v-else class="grid flex-1 items-start gap-4 lg:grid-cols-[1fr_20rem]">
      <!-- Board -->
      <section class="rounded-2xl bg-tray/50 p-3 sm:p-4" aria-label="Board">
        <p
          v-if="isGuessMode"
          class="mb-3 rounded-lg bg-zap px-3 py-2 font-medium text-tray"
        >
          Pick the character you think your opponent has.
        </p>
        <p
          v-else-if="opponentIsGuessing"
          class="mb-3 rounded-lg bg-white/15 px-3 py-2 font-medium"
        >
          Your opponent is making a guess…
        </p>
        <GameBoard
          :key="gameKey"
          :characters="characters"
          :is-guess-mode="isGuessMode"
          :selected-character="selectedCharacter"
          @character-selected="handleCharacterSelection"
        />
      </section>

      <aside class="flex flex-col gap-4">
        <!-- The character the opponent has to guess -->
        <div v-if="myCharacter" class="panel flex items-center gap-4">
          <img
            :src="myCharacter.image_url"
            alt=""
            class="h-28 w-20 shrink-0 rounded-lg border-4 border-white bg-white object-contain"
          />
          <div class="min-w-0">
            <p class="text-sm text-white/75">Your character</p>
            <p
              class="break-words font-display text-3xl leading-tight tracking-wide"
            >
              {{ myCharacter.name }}
            </p>
            <p class="text-sm text-white/75">
              Your opponent is trying to guess it.
            </p>
          </div>
        </div>

        <!-- Guess controls -->
        <div v-if="isGuessMode" class="flex gap-2">
          <button
            @click="confirmGuess"
            :disabled="!selectedCharacter"
            class="btn flex-1"
          >
            Confirm guess
          </button>
          <button @click="quitGuessMode" class="btn btn-quiet">Cancel</button>
        </div>
        <button
          v-else
          @click="toggleGuessMode"
          :disabled="opponentIsGuessing || gameOver"
          class="btn w-full"
        >
          Make a guess
        </button>

        <!-- Chat -->
        <div class="panel flex flex-col">
          <h2 class="mb-2 font-display text-2xl tracking-wide">Questions</h2>
          <div
            ref="messages"
            class="flex max-h-[45vh] min-h-[10rem] flex-col gap-2 overflow-y-auto pr-1"
          >
            <p v-if="!messages.length" class="text-sm text-white/75">
              Ask yes-or-no questions, like “Does your character wear glasses?”
            </p>
            <p
              v-for="(message, index) in messages"
              :key="index"
              class="max-w-[85%] break-words rounded-lg px-3 py-2"
              :class="
                message.player_id === playerId
                  ? 'self-end bg-board'
                  : 'self-start bg-zap text-tray'
              "
            >
              {{ message.text }}
            </p>
          </div>
          <form @submit.prevent="sendMessage" class="mt-3 flex gap-2">
            <input
              v-model="newMessage"
              aria-label="Message"
              placeholder="Type a question or answer"
              class="min-w-0 flex-1 rounded-md px-3 py-2 text-tray placeholder:text-tray/50 focus-visible:outline focus-visible:outline-4 focus-visible:outline-zap"
            />
            <button type="submit" class="btn px-3 text-lg">Send</button>
          </form>
        </div>
      </aside>
    </div>

    <!-- Result -->
    <div
      v-if="winnerMessage"
      class="fixed inset-0 z-10 flex items-center justify-center bg-tray/70 p-4"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="result-title"
        class="w-full max-w-md rounded-2xl border-4 border-zap bg-board p-6 text-center shadow-2xl"
      >
        <h2 id="result-title" class="font-display text-4xl tracking-wide">
          {{ winnerMessage }}
        </h2>
        <p v-if="opponentCharacterName" class="mt-2 text-white/85">
          Your opponent had {{ opponentCharacterName }}.
        </p>
        <button @click="leaveGame" class="btn mt-6">
          Back to waiting room
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import GameBoard from "./GameBoard.vue";
import { API_URL, WS_URL } from "../backend";

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
      myCharacter: null, // The character the opponent has to guess
      gameKey: 0, // Bumped on every new game so the cards start fresh
      isGuessMode: false,
      opponentIsGuessing: false,
      selectedCharacter: null,
      gameOver: false,
      ws: null,
      playerId:
        sessionStorage.getItem("playerId") || Math.floor(Math.random() * 100),
      winnerMessage: "", // Shown in the result dialog when set
      opponentCharacterName: "",
    };
  },
  mounted() {
    this.connectToWebSocket();
    sessionStorage.setItem("playerId", this.playerId);
  },
  beforeUnmount() {
    // Closing the socket tells the server we left, which sends the opponent back too
    if (this.ws) {
      this.ws.onmessage = null;
      this.ws.close();
    }
  },
  methods: {
    connectToWebSocket() {
      const wsUrl = `${WS_URL}/ws/game/${this.roomCode}/`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.message.event === "game_started") {
          // Backend sends /media/... paths; resolve them against the backend host
          [
            ...data.message.characters,
            ...data.message.player_characters,
          ].forEach((c) => (c.image_url = new URL(c.image_url, API_URL).href));
          const playerIndex = this.playerId % 2;
          this.characters = data.message.characters;
          this.myCharacter = data.message.player_characters[1 - playerIndex];
          this.gameKey++;
          this.isGuessMode = false;
          this.opponentIsGuessing = false;
          this.selectedCharacter = null;
          this.gameOver = false;
          this.winnerMessage = "";
        } else if (data.message.event === "chat") {
          this.messages.push({
            text: data.message.message,
            player_id: data.message.player_id,
          });
          this.$nextTick(() => {
            const box = this.$refs.messages;
            if (box) box.scrollTop = box.scrollHeight;
          });
        } else if (data.message.event === "guess_result") {
          const { correct, player_id } = data.message;
          if (player_id === this.playerId) {
            this.winnerMessage = correct
              ? "You win!"
              : "Wrong guess, you lose!";
            this.opponentCharacterName = data.message.actual_character;
          } else {
            this.winnerMessage = correct
              ? "They guessed it, you lose!"
              : "They guessed wrong, you win!";
            this.opponentCharacterName = data.message.guesser_character;
          }
          this.gameOver = true;
          this.isGuessMode = false;
          this.opponentIsGuessing = false;
        } else if (data.message.event === "guess_mode") {
          this.opponentIsGuessing =
            data.message.is_guessing &&
            data.message.player_id !== this.playerId;
        } else if (data.message.event === "player_left") {
          // Tell the waiting room why we're back, unless the game was already over
          this.$router.push({
            path: `/waiting/${this.roomCode}`,
            query: this.gameOver ? {} : { left: "1" },
          });
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
          }),
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
        }),
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
          }),
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
        }),
      );
    },
    leaveGame() {
      this.$router.push(`/waiting/${this.roomCode}`);
    },
  },
};
</script>
