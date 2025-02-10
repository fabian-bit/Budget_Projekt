<template>
  <div>
    <h2 class="mt-4">Budget Tabelle</h2>
    <table class="table table-bordered table-striped">
      <thead class="table-light">
        <tr>
          <th>Kategorie</th>
          <th v-for="month in 12" :key="month">{{ month }}</th>
          <th>Summe</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cat in categories" :key="cat.id">
          <td>{{ cat.name }}</td>
          <td v-for="month in 12" :key="month">
            <input type="number"
                   class="form-control form-control-sm"
                   v-model.number="budgetValues[cat.id][month]">
          </td>
          <td>{{ calculateSum(budgetValues[cat.id]) }}</td>
        </tr>
      </tbody>
    </table>
    <div class="text-end">
      <button @click="saveBudget" class="btn btn-success">Budget speichern</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "BudgetTable",
  props: {
    categories: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      // Hier speichern wir die Budgetwerte pro Kategorie und Monat
      budgetValues: {}
    }
  },
  // Ein Watcher reagiert auf Änderungen an den Kategorien und initialisiert die Einträge
  watch: {
    categories: {
      immediate: true,
      handler(newCategories) {
        newCategories.forEach(cat => {
          if (!this.budgetValues[cat.id]) {
            this.$set(this.budgetValues, cat.id, {});
            for (let month = 1; month <= 12; month++) {
              this.$set(this.budgetValues[cat.id], month, 0);
            }
          }
        });
      }
    }
  },
  methods: {
    // Diese Methode stellt sicher, dass für die Kategorie und den Monat ein Wert existiert
    getBudgetValue(catId, month) {
      if (!this.budgetValues[catId]) {
        this.$set(this.budgetValues, catId, {});
      }
      if (this.budgetValues[catId][month] === undefined) {
        this.$set(this.budgetValues[catId], month, 0);
      }
      return this.budgetValues[catId][month];
    },
    calculateSum(values) {
      if (!values) return 0;
      return Object.values(values).reduce((sum, current) => sum + current, 0);
    },
    async saveBudget() {
      try {
        // Speichere für jede Kategorie die Budgetwerte per API
        for (let catId in this.budgetValues) {
          await axios.post('/budgets', {
            category_id: parseInt(catId),
            values: this.budgetValues[catId]
          });
        }
        alert("Budget gespeichert!");
      } catch (error) {
        console.error("Fehler beim Speichern des Budgets", error);
      }
    }
  }
}
</script>

<style scoped>
table {
  font-size: 0.9rem;
}
</style>