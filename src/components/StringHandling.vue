<template>
	<h1>字符串处理 <a href="#/">[返回目录]</a></h1>
	<div id="app">
		<div>
			请输入字符串：
			<input v-model="inp" type="text" />
		</div>
		<div>
			全大写：
			<div>{{inp.toUpperCase()}}</div>
		</div>
		<div>
			全小写：
			<div>{{inp.toLowerCase()}}</div>
		</div>
		<div>
			大小写互换：
			<div>{{swapcase(inp)}}</div>
		</div>
	</div>
</template>

<script setup>
	import {
		ref
	} from 'vue'
	const inp = ref('')
	const swapcase = function(value) {
		// let new_value = ''
		// for (let i = 0; i < value.length; i++) {
		// 	new_value += value[i].toUpperCase() == value[i] ? value[i].toLowerCase() : value[i].toUpperCase()
		// }
		// return new_value
		return Array.from(value).map((v) => {return v.toUpperCase() == v ? v.toLowerCase() : v.toUpperCase()}).join('')
	}
</script>

<style scoped>
	#app {
		width: 250px;
		padding: 12px;
		margin: 0 auto;
		text-align: center;
		border: 1px solid black;
	}

	#app>div:not(:first-child) {
		border-bottom: 1px solid black;
	}

	#app>div:not(:first-child)>div {
		min-height: 20px;
	}
</style>
