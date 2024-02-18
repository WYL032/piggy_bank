
<template>
  <div class="container">
    <div class="box w-12 p-2">
      <Calendar
        inline
        v-model="date"
        view="month"
        dateFormat="mm/yy"
        @update:modelValue="setChartData()"
      />
    </div>
    <div class="box w-12 p-1">
      <DataTable :value="reportData" tableStyle="min-width:27rem;">
        <Column
          field="expenseAmount"
          header="expense"
          class="text-center"
          headerClass="column-text-right"
        ></Column>
        <Column
          field="incomeAmount"
          header="income"
          class="text-center"
          headerClass="column-text-right"
        ></Column>
        <Column
          field="balanceAmount"
          header="balance"
          class="text-center"
          headerClass="column-text-right"
        ></Column>
      </DataTable>
    </div>
    <div class="box w-full p-2">
      <Fieldset legend="EXPENSE">
        <Chart
          style="width: 375px"
          type="doughnut"
          :data="chartDataExpense"
          :options="chartOptions"
        />
      </Fieldset>
    </div>
    <div class="box w-full p-2 pb-8">
      <Fieldset legend="INCOME">
        <Chart
          style="width: 375px"
          type="doughnut"
          :data="chartDataIncome"
          :options="chartOptions"
        />
      </Fieldset>
    </div>
  </div>
</template>

<script setup>
import Calendar from "primevue/calendar";
import { ref, onMounted } from "vue";
import Chart from "primevue/chart";
import axios from "axios";
import Fieldset from "primevue/fieldset";
import DataTable from "primevue/datatable";
import Column from "primevue/column";

onMounted(() => {
  setChartData();
  setReportData();
  chartOptions.value = setChartOptions();
});

const INCOME = ref(0);
const EXPENSE = ref(1);
const chartDataIncome = ref();
const chartDataExpense = ref();
const reportData = ref();
const chartOptions = ref(null);
const date = ref(new Date());

const formatAsDateString = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day} 00:00:00.000`;
};

const setReportData = () => {
  axios
    .post("http://127.0.0.1:5000/monthReportGet", {
      date: formatAsDateString(date.value),
    })
    .then((res) => {
      console.log(res.data);
      //return res.data;
      reportData.value = res.data;
    });
};

const setChartData = () => {
  axios
    .post("http://127.0.0.1:5000/monthReportChartGet", {
      date: formatAsDateString(date.value),
      type: EXPENSE.value,
    })
    .then((res) => {
      console.log(res.data);
      //return res.data;
      chartDataExpense.value = {
        labels: res.data.labels,
        datasets: res.data.datasets,
      };
    });
  axios
    .post("http://127.0.0.1:5000/monthReportChartGet", {
      date: formatAsDateString(date.value),
      type: INCOME.value,
    })
    .then((res) => {
      console.log(res.data);
      //return res.data;
      chartDataIncome.value = {
        labels: res.data.labels,
        datasets: res.data.datasets,
      };
    });
};

const setChartOptions = () => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColor = documentStyle.getPropertyValue("--text-color");

  return {
    plugins: {
      legend: {
        labels: {
          cutout: "60%",
          color: textColor,
        },
      },
    },
  };
};
</script>

<style scoped>
.container {
  /* min-width: 100%; */
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
}
</style>
<style >
.column-text-right .p-column-header-content {
  text-align: center;
  display: block !important;
}
.p-fieldset-legend {
  background-color: #10b981;
  border-color: #10b981;
  color: #ffffff;
}
.p-datatable-table {
  border: 1px solid #d1d5db;
  border-radius: 6px;
  overflow: hidden;
}
</style>