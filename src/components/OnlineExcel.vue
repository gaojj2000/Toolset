<template>
	<div id="sheet" style="margin:0px;padding:0px;position:absolute;width:100%;height:100%;left: 0px;top: 0px;"></div>
</template>

<script setup>
	import {
		onMounted
	} from 'vue'
	onMounted(() => {
		//配置项
		var options = {
			container: 'sheet', // 设定DOM容器的id
			title: '工作簿1', // 设定表格名称
			lang: 'zh', // 设定表格语言
			myFolderUrl: '#/', // 返回按钮链接
		}
		luckysheet.create(options);
		const logo = document.querySelector('.luckysheet-share-logo');
		logo.className = '';
		logo.innerHTML = '<h1>Excel表格编辑器 <a href="#/">[返回目录]</a></h1>';
	})
</script>

<style>
	a {
		color: blue;
		font-size: 20px;
		list-style: none;
		text-decoration: none;
	}
</style>
