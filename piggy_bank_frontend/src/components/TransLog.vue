
<template>
  <DataView :value="transLogs">
    <template #list="slotProps">
      <div class="grid grid-nogutter">
        <div v-for="(log, index) in transLogs" :key="index" class="col-12">
          <div
            class="flex flex-column xl:flex-row xl:align-items-start p-1 gap-4 fadeindown animation-duration-100"
            :class="{ 'border-top-1 surface-border': index !== 0 }"
          >
            <div
              class="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-1"
            >
              <div
                class="flex flex-column align-items-center sm:align-items-start gap-2"
              >
                <div class="text-base font-bold text-900">
                  {{ log.categoryName }}
                </div>
                <div class="flex align-items-center gap-3">
                  <span class="flex align-items-center gap-2">
                    <span>{{ log.categorySectionName }}</span>
                  </span>
                </div>
              </div>
              <span class="text-base font-semibold"
                >${{ TWDollar.format(log.amount) }}</span
              >
              <Button
                icon="pi pi-trash"
                rounded
                @click="deleteTransLog(log.id)"
              ></Button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DataView>
  <!-- <div class="list-item"> -->
  <!-- <p>{{ props.type }}</p> -->
  <!-- <p>{{ categoryName }}</p>
    <p>${{ amount }}</p>
    <button @click="deleteTransLog()">delete</button>
  </div> -->
</template>

<script setup>
import DataView from "primevue/dataview";
import Button from "primevue/button";

import { ref } from "vue";
const TWDollar = new Intl.NumberFormat("zh-TW", {
  style: "currency",
  currency: "NTD",
  minimumFractionDigits: 0,
});
const props = defineProps({
  transLogs: {
    type: Array,
    default: () => {},
  },
  // id: {
  //   type: Number,
  //   default: 0,
  // },
  // type: {
  //   type: Number,
  //   default: 0,
  // },
  // categorySectionName: {
  //   type: String,
  //   default: "",
  // },
  // categoryName: {
  //   type: String,
  //   default: "",
  // },
  // amount: {
  //   type: Number,
  //   default: 0,
  // },
});
// const id = ref(props.id);
const emit = defineEmits(["deleteTransLog"]);
const deleteTransLog = (id) => {
  emit("deleteTransLog", id);
};
</script>
