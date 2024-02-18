<template>
  <!-- <VueDatePicker
    v-model="date"
    :enable-time-picker="false"
    @update:model-value="onDateChange()"
  /> -->
  <Calendar
    v-model="date"
    dateFormat="yy/mm/dd"
    @update:model-value="onDateChange()"
  />
</template>

<script setup>
import Calendar from "primevue/calendar";

import { ref, watch } from "vue";
// import VueDatePicker from "@vuepic/vue-datepicker";
// import "@vuepic/vue-datepicker/dist/main.css";
const props = defineProps({
  date: {
    type: Date,
    default: new Date(),
  },
});
const date = ref(props.date);
const emit = defineEmits(["onDateChange"]);
const onDateChange = () => {
  emit("onDateChange", date.value);
};
watch(
  () => props.date,
  (newVal) => {
    date.value = newVal;
  }
);
</script>

  <!-- https://vue-scroll-picker.dist.be/ -->
