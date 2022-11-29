<template>
	<h1>点格棋 <a href="#/">[返回目录]</a></h1>
	<div id="app">
		<table :style="{width: width * 110 - 100 + 'px'}">
			<tr v-for="(row,ir) in data">
				<td v-for="(col,ic) in row" v-if="ir % 2 == 0" :class="col">
					<!-- 奇数行 -->
					<div v-if="ic % 2 == 1" :class="col" :id="'wire' + (ir * width + ic / 2 - (ir + 1) / 2)"
						v-on:click.once="handle(ir,ic,ir * width + ic / 2 - (ir + 1) / 2);"></div><!-- 偶数列 -->
				</td>
				<td v-for="(col,ic) in row" v-if="ir % 2 == 1" :class="col">
					<!-- 偶数行 -->
					<div v-if="ic % 2 == 0" :class="col" :id="'wire' + (ir * width + (ic + 1) / 2 - ir / 2 - 1)"
						v-on:click.once="handle(ir,ic,ir * width + (ic + 1) / 2 - ir / 2 - 1);"></div><!-- 奇数列 -->
					<div v-if="ic % 2 == 1" :class="col" :id="'noodle' + ((ir - 1) / 2 * (width - 1) + (ic - 1) / 2)">
					</div><!-- 偶数列 -->
				</td>
			</tr>
		</table>
	</div>
	<div id="tip" :style="'color:'+color">下一步：{{color}}</div>
</template>

<script setup>
	import {
		ref
	} from 'vue'
	const width = ref(0);
	const height = ref(0);
	const data = ref([]);
	const color = ref('red')
	const handle = (ir, ic, index) => {
		var sites = [];
		document.getElementById('wire' + index).style.backgroundColor = color.value;
		if ((ir % 2) < (ic % 2)) { // 仅 ir 为偶数，ic为奇数，即奇数行偶数列，上下可能有方块
			if (ir > 0) { // 非第一行，可以获取上方方块
				sites.push((ir / 2 - 1) * (width.value - 1) + (ic - 1) / 2);
			}
			if (ir < 2 * (height.value - 1)) { // 非最后一行，可以获取下方方块
				sites.push(ir / 2 * (width.value - 1) + (ic - 1) / 2);
			}
		} else { //偶数行奇数列，左右可能有方块
			if (ic > 0) { // 非第一列，可以获取左方方块
				sites.push(((ir - 1) / 2) * (width.value - 1) + ic / 2 - 1);
			}
			if (ic < 2 * (width.value - 1)) { // 非最后一列，可以获取右方方块
				sites.push(((ir - 1) / 2) * (width.value - 1) + ic / 2);
			}
		}
		var ok = false;
		for (var s in sites) {
			if (check_round(sites[s])) {
				ok = true;
			}
		}
		if (!ok) {
			color.value = (color.value == 'red' ? 'blue' : 'red');
		}
	}
	const check_round = function(site) {
		const x = Math.floor(site / (width.value - 1));
		const y = site % (width.value - 1);
		const up = x * (2 * width.value - 1) + y;
		const left = x * (2 * width.value - 1) + width.value + y - 1;
		const right = x * (2 * width.value - 1) + width.value + y;
		const down = (x + 1) * (2 * width.value - 1) + y;
		if (document.getElementById('wire' + up).style.backgroundColor &&
			document.getElementById('wire' + left).style.backgroundColor &&
			document.getElementById('wire' + right).style.backgroundColor &&
			document.getElementById('wire' + down).style.backgroundColor) {
			document.getElementById('noodle' + site).style.backgroundColor = color.value;
			count[color.value] += 1;
			document.getElementById('noodle' + site).innerText = count[color.value];
			if (count[color.value] + count[color.value == 'red' ? 'blue' : 'red'] == (width.value - 1) * (height.value -
					1)) {
				alert(count.red < count.blue ? 'Blue\nWin!' : count.red > count.blue ? 'Red\nWin!' :
					'Draw!');
				location.reload();
			} else if (count[color.value] > (width.value - 1) * (height.value - 1) / 2) {
				alert(color.value + '\nWin!');
				location.reload();
			}
			return true;
		}
		return false;
	}
	var count = {
			red: 0,
			blue: 0
		};
	const size = prompt('请输入点格棋大小【宽x高】（ 建议 5x5 - 17x8 ）', '5x5');
	if (size != null && size.toLowerCase().split('x').length == 2 && size.toLowerCase().split('x')[0] && size
		.toLowerCase().split('x')[1]) {
		width.value = parseInt(size.toLowerCase().split('x')[0]);
		height.value = parseInt(size.toLowerCase().split('x')[1]);
		data.value = (function() {
			const dat = [];
			for (var row = 0; row < 2 * height.value - 1; row++) {
				const temp = [];
				if (row % 2) {
					for (var col = 0; col < 2 * width.value - 1; col++) {
						if (col % 2) {
							temp.push('noodle');
						} else {
							temp.push('wire_col');
						}
					}
				} else {
					for (var col = 0; col < 2 * width.value - 1; col++) {
						if (col % 2) {
							temp.push('wire_row');
						} else {
							temp.push('point');
						}
					}
				}
				dat.push(temp);
			}
			return dat;
		})();
	} else {
		window.location.hash = '#/';
	}
</script>

<style scoped>
	a {
		color: blue;
		font-size: 20px;
		list-style: none;
		text-decoration: none;
	}

	#app>table {
		margin: 0 auto;
		border-spacing: 0;
		text-align: center;
		border: 1px solid lightgray;
	}

	.point {
		padding: 0;
		width: 10px;
		border-radius: 5px;
		background-color: black;
	}

	.wire_row {
		padding: 0;
		width: 100px;
		height: 10px;
	}

	.wire_col {
		padding: 0;
		width: 10px;
		height: 100px;
	}

	.noodle {
		padding: 0;
		width: 98px;
		height: 98px;
		font-size: 36px;
		line-height: 98px;
		font-weight: bolder;
		border: 1px solid lightgray;
	}
	
	#tip{
		top: 25px;
		left: 50px;
		width: 100px;
		height: 20px;
		padding: 4px;
		cursor: pointer;
		position: fixed;
		line-height: 20px;
		text-align: center;
		border: 1px solid;
	}
</style>
