<template #node="{ node, hasChildren, isCollapsed, toggleCollapsed }">
    <div class="navbar">
        <NavBar />
    </div>
    <div class="content">
        <div class="mx-auto max-w-7xl overflow-hidden px-4 pt-8 sm:px-6 lg:px-4">
            <div class="mb-8">
                <p class="text-xl text-center mb-2 text-gray">Categories available for sellers on hubmarket.place</p>
                <p class="text-sm text-center text-gray-600">New categories shall be added periodically as per the demand from the sellers.</p>
            </div>
            <!-- <div class="px-4 pb-8 sm:px-6 lg:px-4">
            <TextInput
                :type="'search'"
                :ref_for="true"
                size="sm"
                variant="subtle"
                placeholder="Search categories..."
                :disabled="false"
                v-model="searchQuery"
            />
            </div> -->
            <div v-if="isLoading" class="space-y-4 px-4">
                <!-- Skeleton Loader -->
                <div v-for="i in 10" :key="i" class="h-8 bg-gray-200 rounded animate-pulse"></div>
            </div>
            <div v-else>
                <div v-for="(categoryNode, index) in filteredCategories" :key="index" class="mb-2 px-4 sm:px-4 lg:px-8">
                    <Tree :options="{
                        showIndentationGuides: categoryNode.showIndentationGuides,
                        rowHeight: categoryNode.rowHeight,
                        indentWidth: categoryNode.indentWidth,
                    }" nodeKey="name" :node="categoryNode.node" />

                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from 'vue'
import { Tree, TextInput } from 'frappe-ui'
import { internalServices } from '../services/internalServices'
import NavBar from '../components/NavBar.vue';

const isCollapsed = ref(false);
const isLoading = ref(true);
const searchQuery = ref('');
const state = reactive([]);
const useInternalServices = internalServices();

const filteredCategories = computed(() => {
    if (!searchQuery.value) {
        return state; // If no search query, return all categories
    }
    const query = searchQuery.value.toLowerCase();

    // Recursively filter categories and their children
    const filterTree = (nodes) =>
        nodes
            .map((categoryNode) => {
                const { node } = categoryNode;
                const children = node.children.length > 0 ? filterTree(node.children) : [];
                const matchesNode =
                    node.label.toLowerCase().includes(query) ||
                    children.length > 0; // Include if label matches or has matching children

                return matchesNode
                    ? {
                          ...categoryNode,
                          node: {
                              ...node,
                              children,
                          },
                      }
                    : null;
            })
            .filter(Boolean); // Remove null entries

    return filterTree(state);
});

const fetchCategories = async () => {
    try {
        let categories = await useInternalServices.getSellerCategories.fetch();
        const transformArrayToNodes = (dataArray) => {
            return dataArray
                .sort((a, b) => a.category.localeCompare(b.category))
                .map((category) => ({
                    showIndentationGuides: true,
                    rowHeight: '35px',
                    indentWidth: '25px',
                    node: {
                        name: category.name,
                        label: category.category,
                        isCollapsed: false,
                        children: category.sub_category
                            ? category.sub_category
                                .sort((a, b) => a.category.localeCompare(b.category))    
                                .map((subCategory) => ({
                                    name: subCategory.name,
                                    label: subCategory.category,
                                    isCollapsed: false,
                                    children: [],
                                }))
                        : [],
                }
            }));
        };
        state.push(...transformArrayToNodes(categories));

    }
    catch (error) {
        console.error("Failed to fetch categories:", error);
    } finally {
        isLoading.value = false;
    }
};
onMounted(() => {
    fetchCategories()
});
</script>