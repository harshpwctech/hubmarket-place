<template>
    <div class="navbar">
        <NavBar />
    </div>
    <div class="content">
        <div :key="key">
            <div class="mx-auto max-w-7xl overflow-hidden px-4 pt-8 sm:px-6 lg:px-8">
                <h2 class="text-2xl font-bold tracking-tight text-gray-900">{{ categoryName }}</h2>
            </div>
            <ProductFilters :categoryName="categoryName" :subCategoryName="subCategoryName"/>
        </div>
        <Footer />
    </div>
</template>
  
<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router';
import NavBar from '../components/NavBar.vue';
import ProductFilters from '../components/ProductFilters.vue';
import Footer from '../components/Footer.vue';

const props = defineProps({
    categoryName: {
        type: String,
        required: true
    },
    subCategoryName: {
        type: String,
        required: false
    }
});
const route = useRoute();
const key = computed(() => route.fullPath);
const categoryName = ref(props.categoryName);
const subCategoryName = ref(props.subCategoryName);

watch(
  [() => props.categoryName, () => props.subCategoryName],
  ([newCategoryName, newSubCategoryName]) => {
    categoryName.value = newCategoryName;
    subCategoryName.value = newSubCategoryName;
  }
);

</script>
  
  