<template>
  <div>
    <div class="input-keyboard flex flex-row justify-content-center gap-1">
      <InputNumber
        v-model="amount"
        mode="currency"
        currency="NTD"
        locale="zh-TW"
        :minFractionDigits="0"
      />
      <!--
      <input type="number" v-model="amount" /> -->
      <!-- <button @click="addTransLog()" class="btn-enter">OK</button> -->
      <Button @click="addTransLog()" icon="pi pi-plus" />
    </div>
    <div class="keyboard gap-1">
      <Button
        v-for="(key, index) in keys"
        :icon="btnInfo[index].icon"
        :label="btnInfo[index].label"
        @click="press(key)"
        size="large"
        :severity="btnInfo[index].severity"
      >
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import InputNumber from "primevue/inputnumber";
import Button from "primevue/button";

const TWDollar = new Intl.NumberFormat("zh-TW", {
  style: "currency",
  currency: "NTD",
  minimumFractionDigits: 0,
});
const props = defineProps({
  amount: {
    type: Number,
    default: 0,
  },
});
const amount = ref(props.amount);
const keys = ref([7, 8, 9, 4, 5, 6, 1, 2, 3, "C", 0, "←"]);
const btnInfo = computed({
  get: () => {
    return keys.value.map((i) => ({
      icon: i === "←" ? "pi pi-delete-left" : "",
      label: i === "←" ? "\u200b" : i.toString(),
      severity: i === "←" ? "warning" : i === "C" ? "info" : "secondary",
    }));
  },
});
const press = (key) => {
  if (key == "C") amount.value = 0;
  else if (key == "←") amount.value = Math.floor(amount.value / 10);
  else amount.value = amount.value * 10 + key;
};

const emit = defineEmits(["addTransLog"]);
const addTransLog = () => {
  console.log(amount.value);
  emit("addTransLog", amount.value);
  amount.value = 0;
};
</script>

<style scoped>
.keyboard {
  display: grid;
  grid-template-columns: auto auto auto;
  grid-gap: 2px;
}
.btn-keyboard {
  background-color: #80b6ff;
  color: #ffffff;
  border: none;
  padding: 20px;
  font-size: large;
}
.input-keyboard {
  margin-bottom: 5px;
}
.btn-enter {
  background-color: rgb(255 184 50);
  color: #ffffff;
  border: none;
}
</style>

<style>
.input-keyboard .p-inputnumber {
  width: 80%;
}
.input-keyboard .p-inputnumber .p-inputnumber-input {
  max-width: 100%;
}
.p-button-icon.pi.pi-delete-left {
  width: 0.5em;
  position: relative;
}
.p-button-icon.pi.pi-delete-left::before {
  width: 0.5em;
  /* transform: translateX(-8px); */
  position: absolute;
  /* width: 10px; */
  top: 0;
  left: 50%;
  transform: translate(-55%, -9px);
  /* margin-left: -5px; */
}
.p-button-warning .p-button-label {
  display: none;
}
</style>