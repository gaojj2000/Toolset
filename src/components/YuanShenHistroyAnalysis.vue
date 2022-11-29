<template>
	<h1>原神抽卡历史分析 <a href="#/">[返回目录]</a></h1>
	<div id="app">
		<div id="up">
			请输入要分析的原神抽卡地址：
			<input v-model="url"
				placeholder="请输入抽卡分析地址,例如https://webstatic.mihoyo.com/hk4e/event/e20190909gacha-v2/index.html?...#/log" />
			<a @click="test(handle)">点击分析</a>
			<p><span style="color: red">{{remind}}</span></p>
		</div>
		<div id="down" v-show="result">
			<table>
				<tr>
					<td>卡池</td>
					<td>五星角色数</td>
					<td>五星武器数</td>
					<td>四星角色数</td>
					<td>四星武器数</td>
					<td>五星平均抽数</td>
					<td>四星平均抽数</td>
					<td>五星已垫抽数</td>
					<td>总抽取数</td>
				</tr>
				<tr v-for="(v, k) in statistics">
					<td>
						<div style="color: blue">{{k}}</div>
					</td>
					<td>
						<div style="color: red">{{v.five_role.length}}</div>
					</td>
					<td>
						<div style="color: red">{{v.five_arms.length}}</div>
					</td>
					<td>
						<div style="color: red">{{v.four_role.length}}</div>
					</td>
					<td>
						<div style="color: red">{{v.four_arms.length}}</div>
					</td>
					<td>
						<div style="color: green">
							{{round((sum(v.five_role) + sum(v.five_arms)) / (v.five_role.length + v.five_arms.length) || 0, 2)}}
						</div>
					</td>
					<td>
						<div style="color: green">
							{{round((sum(v.four_role) + sum(v.four_arms)) / (v.four_role.length + v.four_arms.length) || 0, 2)}}
						</div>
					</td>
					<td>
						<div style="color: purple">{{data[k]?.length - sum(v.five_role) - sum(v.five_arms)}}</div>
					</td>
					<td>
						<div style="color: purple">{{data[k]?.length}}</div>
					</td>
				</tr>
			</table>
			<div id="choose">
				<select v-model="choose" @change="chan()">
					<option v-for="(i, d) in data" :value="d">{{d}}</option>
				</select>
			</div>
			<div id="info">
				<div id="left">
					<div class="cell" style="text-align: center;">
						五星列表
					</div>
					<div class="cell" v-for="f in detail_statistics[choose]?.five">
						<span style="font-size: 32px;color: red;">{{f[0].name}}</span>&ensp;&ensp;
						<span style="font-size: 28px;color: blue;">{{f[0].time.slice(0, 10)}}</span>&ensp;&ensp;
						<span
							style="font-size: 30px;color: green;">{{f[1] < 10 ? '&ensp;' + f[1] : f[1]}}抽</span>&ensp;&ensp;
						<span style="font-size: 34px;color: purple;">{{f[0].item_type}}</span>&ensp;&ensp;
					</div>
				</div>
				<div id="right">
					<div class="cell" style="text-align: center;">
						四星列表
					</div>
					<div class="cell" v-for="f in detail_statistics[choose]?.four">
						<span style="font-size: 32px;color: red;">{{f[0].name}}</span>&ensp;&ensp;
						<span style="font-size: 28px;color: blue;">{{f[0].time.slice(0, 10)}}</span>&ensp;&ensp;
						<span
							style="font-size: 30px;color: green;">{{f[1] < 10 ? '&ensp;' + f[1] : f[1]}}抽</span>&ensp;&ensp;
						<span style="font-size: 34px;color: purple;">{{f[0].item_type}}</span>&ensp;&ensp;
					</div>
				</div>
			</div>
		</div>
	</div>
	<div id="titles">
		<div class="cell" style="text-align: center;">
			五星列表
		</div>
		<div class="cell" style="text-align: center;">
			四星列表
		</div>
	</div>
	<div id="loading" v-show="load">
		<div>
			<img src="http://www.sucaijishi.com/uploadfile/2014/0524/20140524124239682.gif" />
		</div>
	</div>
	<div id="return_top" class="return_button" @click="return_top()">回到顶层</div>
	<div id="return_bottom" class="return_button" @click="return_bottom()">前往底层</div>
</template>

<script setup>
	import {
		ref,
		watch
	} from 'vue'
	var timeover;
	const url = ref('')
	const choose = ref('')
	const data = ref({})
	const timer = ref(null)
	const load = ref(false)
	const result = ref(false)
	const statistics = ref({})
	const pageYOffset = ref(0)
	const detail_statistics = ref({})
	const remind = ref('等待输入正确的抽卡地址...')
	const sum = function(arr) {
		let res = 0
		for (let i in arr) {
			res += arr[i]
		}
		return res
	}
	const round = function(num, nums) {
		for (let n = 0; n < nums; n++) {
			if (parseInt(num) != num) {
				num = parseFloat(num.toFixed(nums))
			} else {
				num = parseInt(num)
			}
		}
		return num
	}
	const debounce = function(func) {
		return function(...args) {
			if (timer.value) clearTimeout(timer.value)
			timer.value = setTimeout(() => {
				func.apply(this, args)
			}, 1000)
		}
	}
	const test = function(func) {
		if (url.value.startsWith('https://webstatic.mihoyo.com/hk4e/event/e20190909gacha-v2/index.html?')) {
			let status = false
			fetch('http://127.0.0.1:22909/test_get_history?url=' + encodeURIComponent(url.value)).then(res => {
				return res.json()
			}).then(res => {
				if (res.retcode) {
					remind.value = res.message
				} else {
					remind.value = '可以正常访问！该抽卡地址的uid是：' + (res.data.list?. [0]?.uid ?? '【长期不抽卡无法获取uid值！】')
					if (func) {
						func()
					}
				}
			})
		} else {
			remind.value = '等待输入正确的抽卡地址...'
		}
	}
	const chan = function() {
		setTimeout(function() {
			if (document.documentElement.scrollHeight > 936) {
				document.getElementById('return_bottom').style.display = 'block'
			} else {
				document.getElementById('return_bottom').style.display = 'none'
			}
		}, 100)
	}
	const handle = function() {
		load.value = true
		result.value = false
		timeover = setTimeout(function() {
			load.value = false;
			alert('获取数据异常，超过设定时间10分钟，请尝试重新分析数据！')
		}, 600000) // 防止超时，设置10分钟，10分钟后关闭loading图标，提示用户重新操作！
		fetch('http://127.0.0.1:22909/get_history?url=' + encodeURIComponent(url.value)).then(res => {
			return res.json()
		}).then(res => {
			data.value = res
			load.value = false
			clearTimeout(timeover)
			choose.value = Object.keys(res)[0]
			let role_and_arms = {
				four_role: 0,
				four_arms: 0,
				five_role: 0,
				five_arms: 0,
				five: []
			}
			for (var d in data.value) {
				detail_statistics.value[d] = {
					five: [],
					four: []
				}
				let role_and_arms_temp = {
					four_role: [],
					four_arms: [],
					five_role: [],
					five_arms: []
				}
				let sort = data.value[d]
				let four_count = 0
				let five_count = 0
				for (var i in sort) {
					four_count++
					five_count++
					if (sort[i].rank_type == '4') {
						role_and_arms_temp[sort[i].item_type == '角色' ? 'four_role' : 'four_arms'].push(
							four_count)
						detail_statistics.value[d].four.push([sort[i], four_count])
						four_count = 0
					} else if (sort[i].rank_type == '5') {
						role_and_arms_temp[sort[i].item_type == '角色' ? 'five_role' : 'five_arms'].push(
							five_count)
						detail_statistics.value[d].five.push([sort[i], five_count])
						role_and_arms.five.push(sort[i])
						five_count = 0
					}
				}
				for (var f in role_and_arms_temp) {
					role_and_arms[f] += role_and_arms_temp[f]
				}
				statistics.value[d] = role_and_arms_temp
			}
			result.value = true
			chan()
		}).catch(err => {
			alert(JSON.stringify(err))
		})
	}
	const return_top = function() {
		document.documentElement.scrollTop = 0
	}
	const return_bottom = function() {
		document.documentElement.scrollTop = document.documentElement.scrollHeight
	}
	watch(url, async (newHex, oldHex) => {
		debounce(test)()
	})
	window.onscroll = function() {
		pageYOffset.value = window.pageYOffset
		if (window.pageYOffset > 400) {
			document.getElementById('titles').style.left = document.getElementsByClassName('cell')[0].offsetLeft + 'px'
			document.getElementById('titles').style.display = 'block'
			document.getElementById('return_top').style.display = 'block'
		} else {
			document.getElementById('titles').style.display = 'none'
			document.getElementById('return_top').style.display = 'none'
		}
		if (document.documentElement.scrollHeight - document.documentElement.scrollTop <= document.documentElement
			.clientHeight) {
			document.getElementById('return_bottom').style.display = 'none'
		} else {
			document.getElementById('return_bottom').style.display = 'block'
		}
	}
	window.onresize = function() {
		document.getElementById('titles').style.left = document.getElementsByClassName('cell')[0].offsetLeft + 'px'
	}
</script>

<style scoped>
	#pop {
		width: 1240px;
		padding: 20px;
		border: 1px solid black;
	}

	#up {
		width: 1200px;
		margin: 0 auto;
		text-align: center;
	}

	input {
		width: 800px;
		height: 20px;
	}

	a {
		font-size: 16px;
		cursor: pointer;
		padding: 0 10px;
	}

	table {
		border-collapse: collapse;
	}

	td {
		border: 1px solid black;
	}

	#choose {
		width: 400px;
		height: 40px;
		margin: 20px auto;
	}

	select {
		width: 100%;
		height: 100%;
		text-align: center;
	}

	p::before {
		content: '当前所输入抽卡网址的状态：';
	}

	#loading {
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		position: absolute;
		background-color: rgba(211, 211, 211, 0.6);
	}

	#loading div {
		padding: 0;
		width: 600px;
		margin: 120px auto;
		position: relative;
	}

	#loading img {
		width: 600px;
	}

	#info {
		width: 1204px;
		margin: 0 auto;
	}

	#left,
	#right {
		float: left;
		width: 600px;
		height: auto;
		font-size: 20px;
		border: 1px solid black;
	}

	.cell {
		padding: 5px 20px;
		line-height: 60px;
		border-bottom: 1px solid black;
	}

	#titles {
		top: 0;
		width: 1206px;
		display: none;
		position: fixed;
		line-height: 60px;
	}

	#titles>div {
		float: left;
		width: 559px;
		font-size: 20px;
		padding: 5px 20px;
		border: 1px solid black;
		background-color: white;
	}

	.return_button {
		left: 50px;
		width: 40px;
		height: 40px;
		bottom: 50px;
		padding: 4px;
		display: none;
		cursor: pointer;
		position: fixed;
		line-height: 20px;
		text-align: center;
		border-radius: 20px;
		border: 1px solid orange;
		background-color: orange;
	}

	#return_top {
		bottom: 50px;
	}

	#return_bottom {
		top: 50px;
	}
</style>
