// Set VUE_APP_BACKEND_URL (e.g. https://whozit-api.onrender.com) when deploying.
// Locally, the backend runs on port 8000 of whatever machine served this page.
export const API_URL =
  process.env.VUE_APP_BACKEND_URL || `http://${window.location.hostname}:8000`;
export const WS_URL = API_URL.replace(/^http/, "ws"); // https -> wss
