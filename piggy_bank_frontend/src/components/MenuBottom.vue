<template>
  <div class="nav-bottom">
    <div class="nav-bar">
      <div
        v-for="(otherTab, i) in otherTabs"
        class="item nav_btn"
        :key="i"
        @click="changeComponent(i)"
      >
        <!-- <div class="justify-content-center">
          <i :class="otherTab.icon"></i>
          {{ otherTab.text }}
        </div> -->
        <Button
          :class="focusedClass[i]"
          :icon="otherTab.icon"
          :label="otherTab.text"
        >
        </Button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { reactive, ref, computed } from "vue";
import Button from "primevue/button";
const props = defineProps({
  activeIndex: {
    type: Number,
    default: 0,
  },
});
const activeIndex = ref(props.activeIndex);
const otherTabs = reactive([
  {
    text: "Track Expenses",
    icon: "pi pi-book",
  },
  {
    text: "Month Report",
    icon: "pi pi-chart-bar",
  },
  // {
  //   text: "More",
  //   icon: "pi pi-ellipsis-h",
  // },
]);
const focusedClass = computed(() => {
  return otherTabs.map((_, index) =>
    props.activeIndex === index ? "nav-bottom-focused" : ""
  );
});
const emit = defineEmits(["changeComponent"]);
const changeComponent = (idx) => {
  activeIndex.value = idx;
  emit("changeComponent", activeIndex.value);
};
</script>

<style scoped>
.nav-bottom {
  position: fixed;
  bottom: 0;
  box-sizing: border-box;
  z-index: 20;
  width: 520px;
}

.nav-bottom .nav-bar {
  display: flex;
  background-color: #10b981;
  text-align: center;
  font-size: 1rem;
  position: relative;
  height: 49px;
  justify-content: center;
  align-items: center;
  flex-flow: row nowrap;
  color: white;
}

.nav-bottom .nav-bar > .btn {
  position: absolute;
  left: 0;
  top: -35px;
  z-index: 19;
  cursor: pointer;
}

.nav-bottom .nav-bar .item {
  flex: 1 1 25%;
  z-index: 999;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* .nav-bottom .nav-bar .item:hover {
  background-color: #059669;
  cursor: pointer;
  height: 100%;
  width: 100%;
} */
</style>

<style >
.nav-bottom-focused {
  color: var(--vt-c-text-light-1);
}
.nav-bar .p-button-icon {
  padding-right: 5px;
  margin-bottom: -2px;
}
.nav-bottom-focused .p-button-label {
  /* color: var(--vt-c-text-light-1); */
  text-decoration: underline;
  text-underline-offset: 0.3em;
  /* border-bottom: black 1px; */
}
</style>