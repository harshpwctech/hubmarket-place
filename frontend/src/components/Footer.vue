<template>
    <div class="bg-white">
        <footer aria-labelledby="footer-heading" class="bg-white">
            <h2 id="footer-heading" class="sr-only">Footer</h2>
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 lg:py-12">
                <div class="border-t border-gray-200 py-16 xl:grid xl:grid-cols-3 xl:gap-8">
                    <div class="grid grid-cols-2 gap-8 xl:col-span-2">
                        <div class="space-y-8 md:grid md:grid-cols-2 md:gap-8 md:space-y-0">
                            <div>
                                <h3 class="text-sm font-medium text-gray-900">Company</h3>
                                <ul role="list" class="mt-6 space-y-6">
                                    <li v-for="item in footerNavigation.company" :key="item.name" class="text-sm">
                                        <a :href="item.href" class="text-gray-500 hover:text-gray-600">{{ item.name }}</a>
                                    </li>
                                </ul>
                            </div>
                            <div>
                                <h3 class="text-sm font-medium text-gray-900">Seller Central</h3>
                                <ul role="list" class="mt-6 space-y-6">
                                    <li v-for="item in footerNavigation.seller" :key="item.name" class="text-sm">
                                        <a :href="item.href" class="text-gray-500 hover:text-gray-600">{{ item.name }}</a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="space-y-16 md:grid md:grid-cols-2 md:gap-8 md:space-y-0">
                            <div>
                                <h3 class="text-sm font-medium text-gray-900">Buyer Central</h3>
                                <ul role="list" class="mt-6 space-y-6">
                                    <li v-for="item in footerNavigation.buyer" :key="item.name" class="text-sm">
                                        <a :href="item.href" class="text-gray-500 hover:text-gray-600">{{ item.name }}</a>
                                    </li>
                                </ul>
                            </div>
                            <div>
                                <h3 class="text-sm font-medium text-gray-900">Connect</h3>
                                <ul role="list" class="mt-6 space-y-6">
                                    <li v-for="item in footerNavigation.connect" :key="item.name" class="text-sm">
                                        <a :href="item.href" class="text-gray-500 hover:text-gray-600">{{ item.name }}</a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="mt-16 md:mt-16 xl:mt-0">
                        <h3 class="text-sm font-medium text-gray-900">Sign up for our newsletter</h3>
                        <p class="mt-6 text-sm text-gray-500">The latest deals and savings, sent to your inbox weekly.</p>
                        <form class="mt-2 flex sm:max-w-md">
                            <label for="email-address" class="sr-only">Email address</label>
                            <input id="email-address" type="text" autocomplete="email" required=""
                                class="w-full min-w-0 appearance-none rounded-md border border-gray-300 bg-white px-4 py-2 text-base text-indigo-500 placeholder-gray-500 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
                            <div class="ml-4 flex-shrink-0">
                                <button type="submit"
                                    class="flex w-full items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" :style="{ backgroundColor: 'var(--theme-color)'}">Sign
                                    up</button>
                            </div>
                        </form>
                    </div>
                </div>

                <div class="border-t border-gray-200 py-10">
                    <p class="text-sm text-gray-500">Copyright &copy; 2021 Your Company, Inc.</p>
                </div>
            </div>
        </footer>
    </div>
</template>

<script setup>
const footerNavigation = {
  company: [
    { name: 'Who we are', href: '#' },
    { name: 'Careers', href: '#' },
    { name: 'Terms & Conditions', href: '#' },
    { name: 'Privacy', href: '#' },
  ],
  seller: [
    { name: 'Seller Categories', href: '/hub_marketplace/seller_categories' },
    { name: 'Sell on Hub Marketplace', href: 'https://hubmarket.place/join-as-seller' },
  ],
  buyer: [
    { name: 'Manage Account', href: '#' },
    { name: 'Returns & Exchanges', href: '#' },
    { name: 'Redeem a Gift Card', href: '#' },
  ],
  connect: [
    { name: 'Contact Us', href: '#' },
    { name: 'Facebook', href: '#' },
    { name: 'Instagram', href: '#' },
    { name: 'Pinterest', href: '#' },
  ],
}
</script>