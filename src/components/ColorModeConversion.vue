<template>
	<h1>颜色转换 <a href="#/">[返回目录]</a></h1>
	<div id="app">
		<table>
			<tr>
				<td>Hex颜色值：</td>
				<td><input v-model="hex" @focus="isFocus = true" /></td>
			</tr>
			<tr>
				<td>R颜色值：</td>
				<td><input v-model="r" @focus="isFocus = false" /></td>
			</tr>
			<tr>
				<td>G颜色值：</td>
				<td><input v-model="g" @focus="isFocus = false" /></td>
			</tr>
			<tr>
				<td>B颜色值：</td>
				<td><input v-model="b" @focus="isFocus = false" /></td>
			</tr>
		</table>
	</div>
</template>

<script setup>
	import {
		ref,
		watch
	} from 'vue'
	const hex = ref('ABCDEF')
	const r = ref(171)
	const g = ref(205)
	const b = ref(239)
	const isFocus = ref(true)
	const hex2dec = function(h) {
		return h < 58 ? h - 48 : h - 55;
	}
	const dec2hex = function(d) {
		return "0123456789ABCDEF".charAt(Math.floor(d / 16)) + "0123456789ABCDEF".charAt(d % 16)
	}
	watch(hex, async (newHex, oldHex) => {
		if (isFocus.value) {
			var temp = null;
			let last = newHex.slice(-1).toUpperCase()
			if ((last >= '0' && last <= '9') || (last >= 'A' && last <= 'F')) {
				if (newHex.length == 3) {
					temp = newHex.charAt(0) + newHex.charAt(0) + newHex.charAt(1) + newHex.charAt(1) + newHex.charAt(2) + newHex.charAt(2);
				}
				if (newHex.length > 6) {
					hex.value = oldHex;
				}
				if (newHex.length == 6) {
					temp = newHex;
				}
				if (temp) {
					r.value = hex2dec(temp.charCodeAt(0)) * 16 + hex2dec(temp.charCodeAt(1));
					g.value = hex2dec(temp.charCodeAt(2)) * 16 + hex2dec(temp.charCodeAt(3));
					b.value = hex2dec(temp.charCodeAt(4)) * 16 + hex2dec(temp.charCodeAt(5));
				} else {
					r.value = 0;
					g.value = 0;
					b.value = 0;
				}
			} else {
				hex.value = oldHex
			}
			hex.value = hex.value.toUpperCase();
		}
	})
	watch(r, async (newR, oldR) => {
		if (!isFocus.value) {
			if (newR && !/^\d+$/.test(newR)) {
				r.value = oldR;
			}
			newR = parseInt(newR);
			if (newR > 255) {
				r.value = 255;
			}
			hex.value = dec2hex(r.value) + dec2hex(g.value) + dec2hex(b.value);
		}
	})
	watch(g, async (newR, oldR) => {
		if (!isFocus.value) {
			if (newR && !/^\d+$/.test(newR)) {
				g.value = oldR;
			}
			newR = parseInt(newR);
			if (newR > 255) {
				g.value = 255;
			}
			hex.value = dec2hex(r.value) + dec2hex(g.value) + dec2hex(b.value);
		}
	})
	watch(b, async (newR, oldR) => {
		if (!isFocus.value) {
			if (newR && !/^\d+$/.test(newR)) {
				b.value = oldR;
			}
			newR = parseInt(newR);
			if (newR > 255) {
				b.value = 255;
			}
			hex.value = dec2hex(r.value) + dec2hex(g.value) + dec2hex(b.value);
		}
	})
</script>

<style scoped>
	* {
		color: black;
		font-size: 20px;
	}

	a {
		color: blue;
		font-size: 20px;
		list-style: none;
		text-decoration: none;
	}

	#app {
		width: 250px;
		padding: 12px;
		margin: 0 auto;
		text-align: center;
	}

	input {
		width: 90px;
		border: 0px;
		text-align: center;
		border-bottom: 1px solid gray;
	}
</style>
