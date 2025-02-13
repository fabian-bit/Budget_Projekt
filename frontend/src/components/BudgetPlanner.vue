<template>
  <div class="container mt-4">
    <h2 class="text-center mb-4">Budget Planner for {{ year }}</h2>
    <div class="table-container">
      <table class="table table-bordered table-hover">
        <thead>
          <tr>
            <th>Category</th>
            <th v-for="month in 12" :key="month">{{ monthName(month) }}</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id">
            <td>{{ cat.name }}</td>
            <td v-for="month in 12" :key="month">
              <template v-if="budgetValues[cat.id]">
                <input
                  type="number"
                  class="form-control"
                  v-model.number="budgetValues[cat.id][month]"
                />
              </template>
              <template v-else>
                Loading...
              </template>
            </td>
            <td>{{ calculateTotal(budgetValues[cat.id]) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="text-center">
      <button class="btn btn-success" @click="saveAllBudgets">
        Save All Budgets
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted, watch } from "vue";

export default {
  name: "BudgetPlanner",
  props: {
    year: {
      type: Number,
      default: new Date().getFullYear(),
    },
  },
  setup(props) {
    const categories = ref([]);
    const budgetValues = ref({});

    const initializeValues = () => {
      const values = {};
      for (let month = 1; month <= 12; month++) {
        values[month] = 0;
      }
      return values;
    };

    const fetchCategories = async () => {
      try {
        const res = await axios.get("/categories");
        categories.value = res.data;
        for (let cat of categories.value) {
          // Initialize budget values for each category reactively
          budgetValues.value = {
            ...budgetValues.value,
            [cat.id]: initializeValues(),
          };
          await fetchBudgetForCategory(cat.id);
        }
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    };

    const fetchBudgetForCategory = async (catId) => {
      try {
        const res = await axios.get("/budgets", {
          params: { category_id: catId, year: props.year },
        });
        const fetched = res.data.values || {};
        if (budgetValues.value[catId]) {
          for (let month = 1; month <= 12; month++) {
            if (fetched[String(month)] !== undefined) {
              budgetValues.value[catId][month] = Number(fetched[String(month)]);
            }
          }
        }
      } catch (error) {
        console.warn(
          `No budget data for category ${catId} for year ${props.year}`
        );
      }
    };

    const calculateTotal = (values) => {
      if (!values) return 0;
      return Object.values(values).reduce(
        (sum, val) => sum + Number(val || 0),
        0
      );
    };

    const monthName = (month) => {
      const names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
      ];
      return names[month - 1];
    };

    const saveAllBudgets = async () => {
      try {
        const savePromises = categories.value.map((cat) => {
          const payload = {
            category_id: cat.id,
            year: props.year,
            values: budgetValues.value[cat.id],
          };
          return axios.post("/budgets", payload);
        });
        await Promise.all(savePromises);
        alert("Budgets saved successfully!");
      } catch (error) {
        console.error("Error saving budgets:", error);
        alert("Error saving budgets.");
      }
    };

    onMounted(() => {
      fetchCategories();
    });
    watch(() => props.year, () => {
      categories.value.forEach((cat) => {
        fetchBudgetForCategory(cat.id);
      });
    });

    return {
      categories,
      budgetValues,
      calculateTotal,
      monthName,
      saveAllBudgets,
    };
  },
};
</script>