<template>
  <div class="container mt-4">
    <h2 class="text-center mb-4">Category Manager</h2>
    <!-- Card to add a new category -->
    <div class="card mb-4">
      <div class="card-header">Add New Category</div>
      <div class="card-body">
        <form @submit.prevent="createCategory">
          <div class="mb-4">
            <label for="catName" class="form-label">Category Name</label>
            <input
              type="text"
              id="catName"
              v-model="newCategory.name"
              class="form-control"
              placeholder="Enter category name"
              required
            />
          </div>
          <div class="mb-4">
            <label for="catType" class="form-label">Type</label>
            <select id="catType" v-model="newCategory.typ" class="form-select custom-select">
              <option value="Einnahme">Income</option>
              <option value="Ausgabe">Expense</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Add Category</button>
        </form>
      </div>
    </div>

    <!-- List existing categories -->
    <div>
      <h3>Existing Categories</h3>
      <ul class="list-group">
        <li
          v-for="cat in categories"
          :key="cat.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          {{ cat.name }} ({{ cat.typ }})
          <button class="btn btn-danger btn-sm" @click="deleteCategory(cat.id)">
            Delete
          </button>
        </li>
      </ul>
      <div class="text-center mt-3">
        <button class="btn btn-danger" @click="deleteAllCategories">
          Delete All Categories
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";

export default {
  name: "CategoryManager",
  setup() {
    const categories = ref([]);
    const newCategory = ref({ name: "", typ: "Ausgabe" });

    const fetchCategories = async () => {
      try {
        const response = await axios.get("/categories");
        categories.value = response.data;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    };

    const createCategory = async () => {
      try {
        await axios.post("/categories", newCategory.value);
        // Reset form fields
        newCategory.value.name = "";
        newCategory.value.typ = "Ausgabe";
        await fetchCategories();
      } catch (error) {
        console.error("Error creating category:", error);
      }
    };

    const deleteCategory = async (id) => {
      try {
        await axios.delete(`/categories/${id}`);
        await fetchCategories();
      } catch (error) {
        console.error("Error deleting category:", error);
      }
    };

    const deleteAllCategories = async () => {
      try {
        await axios.delete("/categories/delete_all");
        await fetchCategories();
      } catch (error) {
        console.error("Error deleting all categories:", error);
      }
    };

    onMounted(() => {
      fetchCategories();
    });

    return {
      categories,
      newCategory,
      createCategory,
      deleteCategory,
      deleteAllCategories,
    };
  },
};
</script>