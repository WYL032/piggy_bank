<script setup>
import { ref, watch } from "vue";
import Dropdown from "primevue/dropdown";

const props = defineProps({
  sections: {
    type: Array,
    default: () => {},
  },
  categories: {
    type: Array,
    default: () => {},
  },
  selectedSection: {
    type: Object,
    default: () => {},
  },
  selectedCategory: {
    type: Object,
    default: () => {},
  },
});
const selectedSection = ref(props.selectedSection);
const selectedCategory = ref(props.selectedCategory);
const emit = defineEmits(["onSectionChange", "onCategoryChange"]);
const onSectionChange = (section) => {
  emit("onSectionChange", section);
  selectedCategory.value = props.sections.find(
    (x) => x.id == selectedSection.value.id
  ).option[0];
};
const onCategoryChange = (category) => {
  emit("onCategoryChange", category);
};
watch(
  () => props.selectedSection,
  (newVal) => {
    selectedSection.value = newVal;
  }
);

watch(
  () => props.selectedCategory,
  (newVal) => {
    selectedCategory.value = newVal;
  }
);
</script>

<template>
  <div class="flex flex-column gap-2">
    <Dropdown
      v-model="selectedSection"
      :options="props.sections"
      optionLabel="sectionName"
      class="w-12"
      @change="onSectionChange(selectedSection)"
    />

    <!-- <select
      v-model="selectedSectionId"
      @change="onSectionChange(selectedSectionId)"
    >
      <option v-for="section in props.sections" :value="section.id">
        {{ section.sectionName }}
      </option>
    </select>-->
    <Dropdown
      v-model="selectedCategory"
      :options="props.categories"
      optionLabel="categoryName"
      class="w-12"
      @change="onCategoryChange(selectedCategory)"
    />
    <!-- <select
      v-model="selectedCategoryId"
      @change="onCategoryChange(selectedCategoryId)"
    >
      <option v-for="category in props.categories" :value="category.id">
        {{ category.categoryName }}
      </option>
    </select> -->
  </div>
</template>

<style scoped>
</style>