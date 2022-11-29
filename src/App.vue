<script setup>
	// This starter template is using Vue 3 <script setup> SFCs
	// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
	import {
		ref,
		computed
	} from 'vue'
	import {
		routes,
		titles,
		Menu,
		NotFound
	} from './routers.js'

	const currentPath = ref(window.location.hash)

	window.addEventListener('hashchange', () => {
		currentPath.value = window.location.hash;
	})

	const currentView = computed(() => {
		if ((currentPath.value.slice(1) || '/') == '/') {
			document.title = '万能工具箱'
			return Menu
		} else {
			document.title = titles[currentPath.value.slice(1)] ?? 'NotFound';
			return routes[currentPath.value.slice(1)] ?? NotFound
		}
	})
</script>

<template>
	<component :is="currentView" />
</template>

<style>
	#app {
		margin: 0 auto;
	}

	h1 {
		text-align: center;
	}
</style>
