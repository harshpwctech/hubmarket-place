<template>
  <div class="navbar">
      <NavBar />
  </div>
  <div class="content">
  <div v-if="!isLoading">
    <div v-for="(items, category) in productList" :key="category">
      <div class="mx-auto max-w-7xl overflow-hidden py-8 px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-bold tracking-tight text-gray-900">{{ category }}</h2>
          <button @click="navigateToProductList(category)"
            class="text-sm font-medium text-indigo-600 hover:text-indigo-500">
            View All
            <span aria-hidden="true"> &rarr;</span>
          </button>
        </div>
      </div>
      <ProductsGrid :products="items.products" />
      <div class="mx-auto max-w-7xl overflow-hidden px-4 py-8 sm:px-6 lg:px-8">
        <h2 class="text-4xl font-bold tracking-tight text-gray-900">Top {{ category }} Sellers</h2>
      </div>
      <SellersGrid :sellers="items.sellers" />
    </div>
    <HubPromo />
  </div>
  <div v-else>
    <SkeletonGrid />
  </div>
  <Footer />
</div>
</template>

<script setup>
import { reactive, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue';
import ProductsGrid from '../components/ProductsGrid.vue';
import SellersGrid from '../components/SellersGrid.vue';
import HubPromo from '../components/HubPromo.vue';
import Footer from '../components/Footer.vue';
import { internalServices } from '../services/internalServices'
import SkeletonGrid from '../components/SkeletonGrid.vue'

const useInternalServices = internalServices();
const hubCategories = useInternalServices.hubCategories;
const productList = reactive({})
const isLoading = ref(true)

onMounted(() => {
  hubCategories.value.forEach((category) => {
    fetchSellersAndProducts(category.name);
  });
});

const fetchSellersAndProducts = async (category) => {
  try {
    const data = await useInternalServices.getTopSellersAndProducts.fetch({
      "category": category
    });
    if (data && data.sellers.length > 0 && data.products.length > 0) {
      productList[category] = {
        sellers: data.sellers,
        products: data.products
      };
    }
    isLoading.value = false
  } catch (error) {
    console.error(`Failed to fetch sellers and products for ${category}:`, error);
  }
};
const router = useRouter()
function navigateToProductList(categoryName) {
  router.push({ name: 'ProductList', params: { categoryName } });
}

</script>

