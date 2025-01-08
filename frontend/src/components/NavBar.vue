<template>
    <div class="bg-white">
        <header class="relative bg-white">
            <div id="banner" v-if="showBanner"
                class="flex h-8 items-center justify-center bg-[var(--theme-color)] px-4 text-sm font-medium text-gray-800 sm:px-6 lg:px-8">
                <p class="text-white">
                    Get listed as a Seller (<a href="https://hubmarket.place/join-as-seller" target="_blank">click here</a>).
                </p>
                <button @click="closeBanner" class="text-gray-800 absolute right-4">
                    <XMarkIcon class="h-5 w-5 text-white" aria-hidden="true" />
                </button>
            </div>
            <nav aria-label="Top" class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div class="border-b border-gray-200">
                    <div class="flex h-16 items-center">
                        <button @click="openMenu" class="relative rounded-md bg-white p-2 text-gray-400">
                            <span class="absolute -inset-0.5" />
                            <span class="sr-only">Open menu</span>
                            <Bars3Icon class="h-6 w-6" aria-hidden="true" />
                        </button>
                        <CategoryMenu />

                        <!-- Logo -->
                        <div class="ml-2">
                            <a class="flex" href="/hub_marketplace/">
                                <span class="sr-only">Hub-Marketplace</span>
                                <BuildingStorefrontIcon class="h-8 w-8 text-gray-800"
                                    alt="hub" />
                                    <h1 class="hidden lg:block p-2 text-xl text-gray-800 font-mono font-medium tracking-widest">hubmarket.place</h1>
                            </a>
                        </div>
                        
                        <div class="ml-auto flex items-center">
                            <!-- Search -->
                            <div class="flex lg:ml-6">
                                <button @click="showSearch = !showSearch" class="p-2 text-gray-400 hover:text-gray-500">
                                    <span class="sr-only">Search</span>
                                    <MagnifyingGlassIcon class="h-6 w-6" aria-hidden="true" />
                                </button>
                            </div>

                            <!-- Cart -->
                            <div v-if="session.isLoggedIn">
                                <div class="ml-4 flow-root lg:ml-6">
                                    <button @click="openCart" class="group -m-2 flex items-center p-2">
                                        <ShoppingBagIcon class="h-6 w-6 flex-shrink-0 text-gray-400 group-hover:text-gray-500"
                                            aria-hidden="true" />
                                        <span class="ml-2 text-sm font-medium text-gray-700 group-hover:text-gray-800">0</span>
                                        <span class="sr-only">items in cart, view bag</span>
                                    </button>
                                </div>
                            </div>
                            
                            <div v-if="!session.isLoggedIn">
                                <div class="flex ml-4 lg:ml-6">
                                    <button @click="openLoginComponent" class="text-sm font-medium text-gray-700 hover:text-gray-800">Sign in</button>
                                </div>

                            </div>
                            <div v-else>
                                <Dropdown
                                    :options="[
                                        {
                                            label: 'My Wishlist',
                                            onClick: () => {},
                                        },
                                        {
                                            label: 'My Orders',
                                            onClick: () => {},
                                        },
                                        {
                                            label: 'My Profile',
                                            onClick: () => navigateToProfile(),
                                        },
                                        {
                                            label: 'Logout',
                                            onClick: () => logout.fetch(),
                                        },
                                    ]"
                                    >
                                    <Avatar class="ml-4 flow-root lg:ml-6" shape="circle" :image="userInfo.image" size="xl" :label="userInfo.full_name" style="cursor: pointer;"/>
                                </Dropdown>
                            </div>

                        </div>
                    </div>
                </div>
            </nav>
        </header>
        <SearchComponent v-model="showSearch"/>
        <Cart />
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { Avatar, Dropdown } from 'frappe-ui';
import { useRouter } from 'vue-router';
import { Bars3Icon, MagnifyingGlassIcon, ShoppingBagIcon, XMarkIcon } from '@heroicons/vue/24/outline';
import { BuildingStorefrontIcon } from '@heroicons/vue/24/solid';
import { eventBus } from '../eventBus';
import SearchComponent from '../components/SearchComponent.vue';
import Cart from '../components/Cart.vue';
import CategoryMenu from '../components/CategoryMenu.vue';
import { sessionStore } from '@/services/session';

const showBanner = ref(true);
const showSearch = ref(false);
const session = sessionStore();
const { logout } = sessionStore();
const userInfo = ref({
    image: '',
    full_name: '',
    user_id: ''
})
const closeBanner = () => {
  showBanner.value = false;
  sessionStorage.setItem('bannerClosed', 'true');
};
onMounted(() => {
  if (sessionStorage.getItem('bannerClosed') === 'true') {
    showBanner.value = false;
  }
  if (session.isLoggedIn){
    let cookies = new URLSearchParams(document.cookie.split('; ').join('&'))
    userInfo.value.image = cookies.get("user_image")
    userInfo.value.full_name = cookies.get("full_name")
    userInfo.value.user_id = cookies.get("user_id")
    // TODO: fetch the cart values and set it in the internal services cart items
  }
});
const router = useRouter()

const openCart = () => {
    eventBus.cartOpen = true;
};
const openMenu = () => {
    eventBus.menuOpen = true;
};
const openLoginComponent = () => {
    const currentUrl = window.location.pathname + window.location.search;
    window.location.href = `/login?redirect-to=${encodeURIComponent(currentUrl)}`;
};

const navigateToProfile = () => {
    window.location.href = `/update-profile/${userInfo.value.user_id}`;
};

</script>