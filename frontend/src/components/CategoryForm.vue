<!-- src/components/CategoryForm.vue -->
<template>
  <div class="card mb-3">
    <div class="card-header">
      Neue Kategorie hinzufügen
    </div>
    <div class="card-body">
      <form @submit.prevent="createCategory">
        <div class="mb-3">
          <label for="name" class="form-label">Kategorie Name</label>
          <input v-model="name" type="text" class="form-control" id="name" required>
        </div>
        <div class="mb-3">
          <label for="typ" class="form-label">Typ</label>
          <select v-model="typ" class="form-select" id="typ">
            <option value="Einnahme">Einnahme</option>
            <option value="Ausgabe">Ausgabe</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Speichern</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "CategoryForm",
  data() {
    return {
      name: '',
      typ: 'Ausgabe'
    }
  },
  methods: {
    async createCategory() {
      try {
        const response = await axios.post('api/categories', {
          name: this.name,
          typ: this.typ
        });
        // Signalisiere dem Elternteil, dass eine neue Kategorie erstellt wurde
        this.$emit('category-created', response.data);
        this.name = '';
      } catch (error) {
        console.error("Fehler beim Erstellen der Kategorie", error);
      }
    }
  }
}
</script>

<style scoped>
.card {
  max-width: 500px;
  margin: auto;
}
</style>