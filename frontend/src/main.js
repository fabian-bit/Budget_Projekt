import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';

// Setze den Basis‑URL für alle axios-Anfragen
axios.defaults.baseURL = 'http://localhost:5500';

createApp(App).mount('#app');