<!-- src/App.vue -->
<template>
    <div class="container mt-4">
      <h1 class="text-center mb-4">Budget Planung</h1>
      <CategoryForm @category-created="fetchCategories" />
      <BudgetTable :categories="categories" />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import CategoryForm from './components/CategoryForm.vue';
  import BudgetTable from './components/BudgetTable.vue';
  
  export default {
    name: "App",
    components: {
      CategoryForm,
      BudgetTable
    },
    data() {
      return {
        categories: []
      }
    },
    created() {
      this.fetchCategories();
    },
    methods: {
      async fetchCategories() {
        try {
          const res = await axios.get('api/categories');
          this.categories = res.data;
        } catch (error) {
          console.error("Fehler beim Laden der Kategorien", error);
        }
      }
    }
  }
  </script>
  
  <style>
  /* Globale Styles, z. B. ein dezenter Hintergrund */
  body {
    background-color: #f8f9fa;
  }
  </style>