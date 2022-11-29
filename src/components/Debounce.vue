<template>
	<h1>实现防抖函数 <a href="#/">[返回目录]</a></h1>
	<div id="app">
		<div>
			<input v-model="wait" type="number" />
		</div>
		<div>
			请随意输入内容：
			<input v-model="inp" type="text" />
		</div>
		<div>
			各个字符统计结果：
			<pre>{{show}}</pre>
		</div>
	</div>
</template>

<script setup>
	import {
		ref,
		watch
	} from 'vue'
	const inp = ref('')
	const wait = ref(200)
	const show = ref('')
	const timer = ref(null)
	const debounce = function(func) {
		return function(...args) {
			if (timer.value) clearTimeout(timer.value)
			timer.value = setTimeout(() => {
				func.apply(this, args)
			}, wait.value)
		}
	}
	const handle = function() {
		let dict = {}
		if (inp.value) {
			for (let i = 0; i < inp.value.length; i++) {
				dict[inp.value[i]] = isNaN(dict[inp.value[i]]) ? 1 : dict[inp.value[i]] + 1
			}
		}
		show.value = JSON.stringify(dict, null, 2)
	}
	watch(inp, async (newHex, oldHex) => {
		debounce(handle)()
	})
</script>

<style scoped>
	#app {
		width: 250px;
		padding: 12px;
		margin: 0 auto;
		text-align: center;
		border: 1px solid black;
	}

	#app pre {
		text-align: left;
	}

	#app>div:first-child>input:first-child {
		width: 60px;
	}

	#app>div:first-child::before {
		content: '设置响应延时（毫秒）：';
	}

	#app>div>div:last-child>pre {
		min-height: 80px;
		border: 1px solid black;
		word-wrap: break-word;
	}
</style>
