<template>
	<h1>社保计算器 <a href="#/">[返回目录]</a></h1>
	<div id="app">
		<table id="getinfo">
			<tr>
				<td>参保城市</td>
				<td>
					<select v-model="province" @change="change_province();">
						<option v-for="city in citys" :value="city.code">{{city.name}}</option>
					</select>
				</td>
				<td>
					<select v-model="city" @change="change_city();">
						<option v-for="child in children" :value="child.code">{{child.name}}</option>
					</select>
				</td>
				<td>您的IP地址：<span style="color: red;">{{ip}}</span></td>
				<td>您的参考地址：<span style="color: red;">{{address}}</span></td>
			</tr>
			<tr>
				<td>社保基数</td>
				<td>
					<input v-model="insure" />
				</td>
				<td><span>（范围：{{info[city].insure[0].minBase}} - {{info[city].insure[0].maxBase}}）</span></td>
			</tr>
			<tr>
				<td>公积金基数</td>
				<td>
					<input v-model="fund" />
				</td>
				<td><span>（范围：{{info[city].fund[0].minBase}} - {{info[city].fund[0].maxBase}}）</span></td>
			</tr>
		</table>
		<table class="show">
			<caption>社会保险</caption>
			<thead>
				<tr>
					<th rowspan="2" class="w92">缴费项目</th>
					<th colspan="3">个人缴纳</th>
					<th colspan="3">企业缴纳</th>
					<th width="100" rowspan="2">小计</th>
				</tr>
				<tr>
					<th class="w92">基数</th>
					<th class="w92">缴费比例</th>
					<th class="w92">金额</th>
					<th class="w92">基数</th>
					<th class="w92">缴费比例</th>
					<th class="w92">金额</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="item in info[city].insure[0].list">
					<td class="w92">{{item.name}}</td>
					<td class="w92">{{insure < item.uMin ? item.uMin : insure > item.uMax ? item.uMax : insure}}</td>
					<td class="w92">{{parseFloat((item.uRatio * 100).toFixed(2))}}%</td>
					<td class="w92 blue">
						{{parseFloat(((insure < item.uMin ? item.uMin : insure > item.uMax ? item.uMax : insure) * item.uRatio).toFixed(2))}}
					</td>
					<td class="w92">{{insure < item.cMin ? item.cMin : insure > item.cMax ? item.cMax : insure}}</td>
					<td class="w92">{{parseFloat((item.cRatio * 100).toFixed(2))}}%</td>
					<td class="w92 blue">
						{{parseFloat(((insure < item.cMin ? item.cMin : insure > item.cMax ? item.cMax : insure) * item.cRatio).toFixed(2))}}
					</td>
					<td class="blue">
						{{parseFloat(((insure < item.uMin ? item.uMin : insure > item.uMax ? item.uMax : insure) * item.uRatio + (insure < item.cMin ? item.cMin : insure > item.cMax ? item.cMax : insure) * item.cRatio).toFixed(2))}}
					</td>
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<td></td>
					<td colspan="3">个人缴纳：<span
							style="color: #f56954;">{{parseFloat(info[city].insure[0].list.map(item => parseFloat(((insure < item.uMin ? item.uMin : insure > item.uMax ? item.uMax : insure) * item.uRatio).toFixed(2))).reduce((p, n) => p + n).toFixed(2))}}</span>
					</td>
					<td colspan="3">公司缴纳：<span
							style="color: #f56954;">{{parseFloat(info[city].insure[0].list.map(item => parseFloat(((insure < item.cMin ? item.cMin : insure > item.cMax ? item.cMax : insure) * item.cRatio).toFixed(2))).reduce((p, n) => p + n).toFixed(2))}}</span>
					</td>
					<td>合计：<span
							style="color: #f56954;">{{parseFloat(info[city].insure[0].list.map(item => parseFloat(((insure < item.uMin ? item.uMin : insure > item.uMax ? item.uMax : insure) * item.uRatio + (insure < item.cMin ? item.cMin : insure > item.cMax ? item.cMax : insure) * item.cRatio).toFixed(2))).reduce((p, n) => p + n).toFixed(2))}}</span>
					</td>
				</tr>
			</tfoot>
		</table>
		<table class="show">
			<caption>住房公积金</caption>
			<thead>
				<tr>
					<th rowspan="2" class="w92">缴费项目</th>
					<th colspan="3">个人缴纳</th>
					<th colspan="3">企业缴纳</th>
					<th rowspan="2">小计</th>
				</tr>
				<tr>
					<th class="w92">基数</th>
					<th class="w92">缴费比例</th>
					<th class="w92">金额</th>
					<th class="w92">基数</th>
					<th class="w92">缴费比例</th>
					<th class="w92">金额</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="item in info[city].fund[0].list">
					<td class="w92">{{item.name}}</td>
					<td class="w92">{{fund < item.uMin ? item.uMin : fund > item.uMax ? item.uMax : fund}}</td>
					<td class="w92">{{parseFloat((item.uRatio * 100).toFixed(2))}}%</td>
					<td class="w92 blue">
						{{parseFloat(((fund < item.uMin ? item.uMin : fund > item.uMax ? item.uMax : fund) * item.uRatio).toFixed(2))}}
					</td>
					<td class="w92">{{fund < item.cMin ? item.cMin : fund > item.cMax ? item.cMax : fund}}</td>
					<td class="w92">{{parseFloat((item.cRatio * 100).toFixed(2))}}%</td>
					<td class="w92 blue">
						{{parseFloat(((fund < item.cMin ? item.cMin : fund > item.cMax ? item.cMax : fund) * item.cRatio).toFixed(2))}}
					</td>
					<td class="blue">
						{{parseFloat(((fund < item.uMin ? item.uMin : fund > item.uMax ? item.uMax : fund) * item.uRatio + (fund < item.cMin ? item.cMin : fund > item.cMax ? item.cMax : fund) * item.cRatio).toFixed(2))}}
					</td>
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<td></td>
					<td colspan="3">个人缴纳：<span
							style="color: #f56954;">{{parseFloat(info[city].fund[0].list.map(item => parseFloat(((fund < item.uMin ? item.uMin : fund > item.uMax ? item.uMax : fund) * item.uRatio).toFixed(2))).reduce((p, n) => p + n).toFixed(2))}}</span>
					</td>
					<td colspan="3">公司缴纳：<span
							style="color: #f56954;">{{parseFloat(info[city].fund[0].list.map(item => parseFloat(((fund < item.cMin ? item.cMin : fund > item.cMax ? item.cMax : fund) * item.cRatio).toFixed(2))).reduce((p, n) => p + n).toFixed(2))}}</span>
					</td>
					<td>合计：<span
							style="color: #f56954;">{{parseFloat(info[city].fund[0].list.map(item => parseFloat(((fund < item.uMin ? item.uMin : fund > item.uMax ? item.uMax : fund) * item.uRatio + (fund < item.cMin ? item.cMin : fund > item.cMax ? item.cMax : fund) * item.cRatio).toFixed(2))).reduce((p, n) => p + n).toFixed(2))}}</span>
					</td>
				</tr>
			</tfoot>
		</table>
	</div>
</template>

<script setup>
	import {
		ref,
		onMounted
	} from 'vue'
	import {
		dataList,
		dataMap
	} from '../assets/data.js'
	const ip = ref("")
	const address = ref("")
	const citys = ref(dataList)
	const province = ref(dataList[0].code)
	const children = ref(dataList[0].children)
	const city = ref(dataList[0].children[0].code)
	const info = ref(dataMap)
	const insure = ref(dataMap["110001"].insure[0].minBase)
	const fund = ref(dataMap["110001"].fund[0].minBase)
	onMounted(() => {
		fetch("http://110.42.181.215:16666/get_city")
			.then(response => response.json())
			.then(json => {
				if (json.code == 200) {
					ip.value = json.data.ip;
					address.value = json.data.address;
					for (var prov in dataList) {
						prov = dataList[prov];
						for (var child in prov.children) {
							child = prov.children[child];
							if (child.name == address.value.split(" ").slice(-2, -1)[0] + "市") {
								province.value = prov.code;
								children.value = prov.children;
								city.value = child.code;
								change_city();
							}
						}
					}
				}
			})
	})
	const change_city = () => {
		insure.value = info.value[city.value].insure[0].minBase;
		fund.value = info.value[city.value].fund[0].minBase;
	}
	const change_province = () => {
		for (var prov in dataList) {
			prov = dataList[prov];
			if (prov.code == province.value) {
				children.value = prov.children;
				city.value = children.value[0].code;
				change_city();
				break;
			}
		}
	}
</script>

<style scoped>
	a {
		color: blue;
		font-size: 20px;
		list-style: none;
		text-decoration: none;
	}

	#app {
		color: #555;
		width: 800px;
		margin: 0 auto;
		text-align: center;
	}

	#getinfo {
		width: 100%;
		padding: 20px;
		border: 1px solid #dbdbdb;
	}

	#getinfo td {
		width: 148px;
		float: left;
		height: 30px;
		line-height: 30px;
	}

	#getinfo select {
		width: 100%;
		height: 100%;
		border: 1px solid #ebebeb;
	}

	#getinfo input {
		width: 95%;
		height: 95%;
		border: 1px solid #ebebeb;
	}

	#getinfo span {
		white-space: nowrap;
		line-height: 30px;
		font-size: 14px;
		font-family: Arial, Helvetica, "Microsoft Yahei";
	}

	.show {
		width: 100%;
		font-size: 13px;
		border-spacing: 0;
		table-layout: fixed;
		border-collapse: collapse;
	}

	.show th,
	.show td {
		border: 1px solid #cee1ee;
		text-align: center;
		font-weight: normal;
		white-space: nowrap;
		line-height: 30px;
	}

	.show caption {
		padding: 20px 0 10px;
		line-height: 22px;
		font-size: 16px;
		text-align: center;
	}

	.w92 {
		width: 92px;
	}

	.blue {
		color: #2095f2;
	}
</style>
