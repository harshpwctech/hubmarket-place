<template>
  <div class="navbar">
    <NavBar />
  </div>
  <div class="content">
    <div :key="key">
      <ProductDetails :productName="productName"/>
      <section aria-labelledby="reviews-heading" class="mx-auto max-w-7xl overflow-hidden">
          <!-- <h2 id="reviews-heading" class="text-lg font-medium text-gray-900 sm:px-6 lg:px-8">Recent reviews</h2> -->
          <ProductReview :productName="productName"/>
      </section>
      <div v-if="relatedItems.length">
        <section aria-labelledby="related-heading" class="mx-auto max-w-7xl overflow-hidden">
            <h2 id="related-heading" class="mx-auto max-w-2xl px-4 py-8 sm:px-6 sm:py-24 lg:max-w-7xl lg:py-8 lg:px-8 text-2xl font-bold tracking-tight text-gray-900">Customers also purchased</h2>
            <ProductsGrid :products="relatedItems"/>
        </section>
      </div>
    </div>
    <Footer />
  </div>
</template>
  
<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router';
import NavBar from '../components/NavBar.vue';
import ProductDetails from '../components/ProductDetails.vue';
import ProductReview from '../components/ProductReview.vue';
import ProductsGrid from '../components/ProductsGrid.vue';
import Footer from '../components/Footer.vue';
import { internalServices } from '../services/internalServices'

const props = defineProps({
    productName: {
        type: String,
        required: true
    }
});
onMounted(() => {
    fetchRelatedItems(props.productName)
});
const route = useRoute();
const key = computed(() => route.fullPath);
const isLoading = ref(false)
const useInternalServices = internalServices();
const productName = ref(props.productName);
const relatedItems = ref([]);
const fetchRelatedItems = async (itemName) => {
  isLoading.value = true;
  relatedItems.value = [];
  try {
    const data = await useInternalServices.getRelatedItems.fetch({
      "item_name": itemName
    });
    relatedItems.value = data
  } catch (error) {
    console.error(`Failed to fetch related products for ${props.productName}:`, error);
    isLoading.value = false;
  }

};
watch(
  () => props.productName,
  (newProduct) => {
    productName.value = newProduct; 
    fetchRelatedItems(newProduct)
  }
);


</script>
  
  