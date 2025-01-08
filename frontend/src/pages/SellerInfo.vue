<template>
    <div class="navbar">
        <NavBar />
    </div>
    <div class="content">
        <div v-if="!isLoading">
            <div class="mx-auto max-w-7xl overflow-hidden px-4 pt-10 sm:px-6 lg:px-8">
                <div class="flex items-center space-x-6">
                    <!-- Seller Logo -->
                    <div class="border border-gray-300 rounded-full w-20 h-20 bg-white">
                        <img :src="sellerDetails.logo" :alt="sellerDetails.seller_name" class="object-contain w-full h-full" loading="lazy" />
                    </div>
                    <!-- Seller Name -->
                    <div>
                        <h2 class="text-2xl font-bold">{{ sellerDetails.seller_name }}</h2>
                        <p>Mumbai, India</p>
                    </div>
                </div>
            </div>
            <SellerFilters :seller="sellerDetails" />
        </div>
        <Footer />
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue';
import SellerFilters from '../components/SellerFilters.vue';
import Footer from '../components/Footer.vue';
import { internalServices } from '../services/internalServices'

const isLoading = ref(true)
const useInternalServices = internalServices();
const props = defineProps({
    seller: {
        type: String,
        required: true
    }
});
const sellerDetails = ref({})

onMounted(() => {
    getSeller(props.seller);
});

const getSeller = async (seller) => {
    try {
        const data = await useInternalServices.getSeller.fetch({
            hub_seller: seller
        });
        sellerDetails.value = data
        isLoading.value = false
    }
    catch (error) {
        console.error(`Failed to fetch seller:`, error);
    }

};

</script>
  
  