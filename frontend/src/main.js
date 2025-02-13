import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import './assets/styles.css'; // Global styles

axios.defaults.baseURL = 'http://localhost:5500/api';

createApp(App).use(router).mount('#app');