<script setup>
import TransLog from "../components/TransLog.vue";
import CategorySelection from "../components/CategorySelection.vue";
import NumberKeyboard from "../components/NumberKeyboard.vue";
import { ref } from "vue";
import axios from "axios";
import DatePicker from "../components/DatePicker.vue";
import SelectButton from "primevue/selectbutton";

const apihost = ref("http://127.0.0.1:5000/");
const INCOME = ref(0);
const EXPENSE = ref(1);
const selectedType = ref(EXPENSE.value);
const sections = ref([]);
const categories = ref([]);
const selectedSection = ref({});
const selectedCategory = ref({});
const amount = ref(0);
const date = ref(new Date());
const selectedTypeName = ref("EXPENSE");
const types = ref(["INCOME", "EXPENSE"]);
const setCtegory = (type) => {
  axios
    .post(apihost.value + "categoryListGet", {
      type: type,
    })
    .then((res) => {
      selectedType.value = type;
      sections.value = res.data;
      selectedSection.value = sections.value[0];
      categories.value = sections.value[0].option;
      selectedCategory.value = categories.value[0];
      //console.log(res.data);
      //console.log(sections.value);
      //console.log(categories.value);
      //console.log(selectedSectionId.value);
      //console.log(selectedCategoryId.value);
    });
};
const setCtegoryName = (name) => {
  selectedType.value = name == "EXPENSE" ? EXPENSE.value : INCOME.value;
  setCtegory(selectedType.value);
};
const transLogs = ref([]);

const getTransLogs = (res) => {
  axios
    .post(apihost.value + "transLogsGet", {
      startDate: formatAsDateString(date.value),
      endDate: formatAsDateString(getEndDate()),
    })
    .then((res) => {
      transLogs.value = res.data;
      //console.log(res.data);
    });
};
const getEndDate = () => {
  const newDate = new Date(date.value);
  newDate.setDate(newDate.getDate() + 1);
  return newDate;
};
const formatAsDateString = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day} 00:00:00.000`;
};

getTransLogs();
setCtegory(selectedType.value);

const sectionChange = (res) => {
  selectedSection.value = res;
  categories.value = sections.value.find(
    (x) => x.id === selectedSection.value.id
  ).option;
  selectedCategory.value = categories.value[0];
};

const categoryChange = (res) => {
  //console.log(res);
  selectedCategory.value = res;
};
const addTransLog = (res) => {
  amount.value = res;
  axios
    .post(apihost.value + "transLogSet", {
      id: 0,
      transDate: formatAsDateString(date.value),
      categoryId: selectedCategory.value.id,
      amount: amount.value,
      memo: "",
    })
    .then((res) => {
      amount.value = 0;
      // alert(res.data.message);
      console.log(amount.value);
      getTransLogs();
    });
};
const deleteTransLog = (res) => {
  //console.log(res);
  axios
    .post(apihost.value + "transLogDelete", {
      id: res,
    })
    .then((res) => {
      // alert(res.data.message);
      getTransLogs();
    });
};
const onDateChange = (res) => {
  date.value = res;
  getTransLogs();
};
</script>

<template>
  <div class="container">
    <div class="box p-2 gap-2">
      <div
        class="overflow-auto surface-overlay p-3 border-primary-500 border-2 border-round"
        style="height: 400px; min-width: 64%"
      >
        <TransLog :transLogs="transLogs" @deleteTransLog="deleteTransLog" />
      </div>

      <div class="section-right w-4 p-2">
        <DatePicker :date="date" @onDateChange="onDateChange" />
      </div>
      <!-- <div v-for="log in transLogs">
        <TransLog
          :id="log.id"
          :type="log.type"
          :categorySectionName="log.categorySectionName"
          :categoryName="log.categoryName"
          :amount="log.amount"
          @deleteTransLog="deleteTransLog"
        />
      </div> -->
    </div>
    <div class="box p-2 justify-content-start">
      <SelectButton
        v-model="selectedTypeName"
        :options="types"
        aria-labelledby="basic"
        @click="setCtegoryName(selectedTypeName)"
      />
    </div>
    <!-- <div class="field col-12">
    <button @click="setCtegory(INCOME)">收入</button>
    <button @click="setCtegory(EXPENSE)">支出</button>
  </div> -->
    <div class="box gap-2 p-2">
      <div class="w-6 section p-2">
        <CategorySelection
          :sections="sections"
          :categories="categories"
          :selectedCategory="selectedCategory"
          :selectedSection="selectedSection"
          @onSectionChange="sectionChange"
          @onCategoryChange="categoryChange"
        />
      </div>
      <div class="w-6 section p-2">
        <NumberKeyboard :amount="amount" @addTransLog="addTransLog" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: space-around;
}
.box {
  display: flex;
  flex-direction: row;
  /* justify-content: center; */
  width: 100%;
}
.section-right {
  background-color: #19573a;
  border-radius: 10px;
}
.section {
  background-color: #19573a;
  border-radius: 10px;
  /* padding: 20px; */
}
</style>

<style>
.p-selectbutton .p-button:not(.p-highlight) {
  filter: brightness(75%);
  color: var(--vt-c-text-light-2);
}
span.p-dropdown-label.p-inputtext {
  width: 3.5em;
}
</style>
