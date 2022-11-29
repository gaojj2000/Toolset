<template>
	<h1>万能工具箱</h1>
	<div id="app">
		<div class="table">
			<div class="cell" v-for="(title, hash) in titles"><a :href="'#' + hash">{{title}}</a></div>
			<!-- <div class="cell"><a href="#/dab">点格棋</a></div>
			<div class="cell"><a href="#/cmc">颜色转换</a></div>
			<div class="cell"><a href="#/ssc">社保计算器</a></div>
			<div class="cell"><a href="#/excel">Excel表格编辑器</a></div>
			<div class="cell"><a href="#/shell">在线Shell终端</a></div>
			<div class="cell"><a href="#/debounce">实现防抖函数</a></div>
			<div class="cell"><a href="#/words">字符串处理</a></div>
			<div class="cell"><a href="#/diff">字符串对比</a></div>
			<div class="cell"><a href="#/yuanshen">原神抽卡分析</a></div>
			<div class="cell"><a href="#/404">访问不到的页面</a></div>
			<div class="cell"><a href="#/">其他功能开发中...</a></div> -->
		</div>
	</div>
</template>

<script setup>
	import {titles} from '../routers.js'
</script>

<style scoped>
	#app {
		width: 800px;
	}

	a {
		color: black;
		font-size: 20px;
		list-style: none;
		text-decoration: none;
	}

	.table {
		width: 100%;
		min-height: 60px;
	}

	.cell {
		float: left;
		width: 175px;
		height: 40px;
		margin: 10px;
		line-height: 40px;
		text-align: center;
		border: 1px solid black;
	}
</style>
