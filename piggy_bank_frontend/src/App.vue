<script setup>
import TrackExpenses from "./views/TrackExpenses.vue";
import MonthReport from "./views/MonthReport.vue";
import MenuBottom from "./components/MenuBottom.vue";
import { ref, computed } from "vue";
const activeIndex = ref(0);
const Component = computed(() => {
  switch (activeIndex.value) {
    case 0:
      return TrackExpenses;
    case 1:
      return MonthReport;
    default:
      return TrackExpenses;
  }
});
const changeComponent = (idx) => {
  activeIndex.value = idx;
};
</script>

<template>
  <component :is="Component" />
  <MenuBottom :activeIndex="activeIndex" @changeComponent="changeComponent" />
</template>

<style scoped>
</style>
