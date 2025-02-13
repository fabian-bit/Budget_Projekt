// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import BudgetPlanner from '../components/BudgetPlanner.vue';
import CategoryManager from '../components/CategoryManager.vue';

const routes = [
  {
    path: '/',
    name: 'BudgetPlanner',
    component: BudgetPlanner
  },
  {
    path: '/categories',
    name: 'CategoryManager',
    component: CategoryManager
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;