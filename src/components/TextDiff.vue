<template>
	<h1>字符串对比 <a href="#/">[返回目录]</a></h1>
	<div id="app">
		<table style="width:100%">
			<tr>
				<td style="width:50%">
					<div class="edit_div">
						<pre id="edit_pre_1"></pre>
						<textarea id="edit_textarea_1" @scroll="test1_scroll()" @input="textchange()"
							@change="textchange()"></textarea>
					</div>
				</td>
				<td style="width:50%">
					<div class="edit_div">
						<pre id="edit_pre_2"></pre>
						<textarea id="edit_textarea_2" @scroll="test2_scroll()" @input="textchange()"
							@change="textchange()"></textarea>
					</div>
				</td>
			</tr>
		</table>
	</div>
</template>

<script setup>
	import {onMounted} from 'vue'
	const test1_scroll = function() {
		document.getElementById("edit_pre_1").scrollTop = document.getElementById("edit_textarea_1").scrollTop;
		document.getElementById("edit_pre_2").scrollTop = document.getElementById("edit_pre_1").scrollTop;
		document.getElementById("edit_textarea_2").scrollTop = document.getElementById("edit_textarea_1").scrollTop;
	}

	const test2_scroll = function() {
		document.getElementById("edit_pre_2").scrollTop = document.getElementById("edit_textarea_2").scrollTop;
		document.getElementById("edit_pre_1").scrollTop = document.getElementById("edit_pre_2").scrollTop;
		document.getElementById("edit_textarea_1").scrollTop = document.getElementById("edit_textarea_2").scrollTop;
	}

	const textchange = function() {
		var op = eq({
			value1: document.getElementById("edit_textarea_1").value,
			value2: document.getElementById("edit_textarea_2").value
		});
		document.getElementById("edit_pre_1").innerHTML = op.value1 + "\r\n";
		document.getElementById("edit_pre_2").innerHTML = op.value2 + "\r\n";
	}

	const eq = function(op) {
		if (!op) {
			return op;
		}
		if (!op.value1_style) {
			op.value1_style = "background-color:#FEC8C8;";
		}
		if (!op.value2_style) {
			op.value2_style = "background-color:#00ff00;";
		}
		if (!op.eq_min) {
			op.eq_min = 3;
		}
		if (!op.eq_index) {
			op.eq_index = 5;
		}
		if (!op.value1 || !op.value2) {
			return op;
		}
		var ps = {
			v1_i: 0,
			v1_new_value: "",
			v2_i: 0,
			v2_new_value: ""
		};
		while (ps.v1_i < op.value1.length && ps.v2_i < op.value2.length) {
			if (op.value1[ps.v1_i] == op.value2[ps.v2_i]) {
				ps.v1_new_value += op.value1[ps.v1_i].replace(/</g, "&lt;").replace(">", "&gt;");
				ps.v2_new_value += op.value2[ps.v2_i].replace(/</g, "&lt;").replace(">", "&gt;");
				ps.v1_i += 1;
				ps.v2_i += 1;
				if (ps.v1_i >= op.value1.length) {
					ps.v2_new_value += "<span style='" + op.value2_style + "'>" + op.value2.substr(ps.v2_i).replace(
						/</g,
						"&lt;").replace(">", "&gt;") + "</span>";
					break;
				}
				if (ps.v2_i >= op.value2.length) {
					ps.v1_new_value += "<span style='" + op.value1_style + "'>" + op.value1.substr(ps.v1_i).replace(
						/</g,
						"&lt;").replace(">", "&gt;") + "</span>";
					break;
				}
			} else {
				ps.v1_index = ps.v1_i + 1;
				ps.v1_eq_length = 0;
				ps.v1_eq_max = 0;
				ps.v1_start = ps.v1_i + 1;
				while (ps.v1_index < op.value1.length) {
					if (op.value1[ps.v1_index] == op.value2[ps.v2_i + ps.v1_eq_length]) {
						ps.v1_eq_length += 1;
					} else if (ps.v1_eq_length > 0) {
						if (ps.v1_eq_max < ps.v1_eq_length) {
							ps.v1_eq_max = ps.v1_eq_length;
							ps.v1_start = ps.v1_index - ps.v1_eq_length;
						}
						ps.v1_eq_length = 0;
						break; //只寻找最近的
					}
					ps.v1_index += 1;
				}
				if (ps.v1_eq_max < ps.v1_eq_length) {
					ps.v1_eq_max = ps.v1_eq_length;
					ps.v1_start = ps.v1_index - ps.v1_eq_length;
				}

				ps.v2_index = ps.v2_i + 1;
				ps.v2_eq_length = 0;
				ps.v2_eq_max = 0;
				ps.v2_start = ps.v2_i + 1;
				while (ps.v2_index < op.value2.length) {
					if (op.value2[ps.v2_index] == op.value1[ps.v1_i + ps.v2_eq_length]) {
						ps.v2_eq_length += 1;
					} else if (ps.v2_eq_length > 0) {
						if (ps.v2_eq_max < ps.v2_eq_length) {
							ps.v2_eq_max = ps.v2_eq_length;
							ps.v2_start = ps.v2_index - ps.v2_eq_length;
						}
						ps.v1_eq_length = 0;
						break; //只寻找最近的
					}
					ps.v2_index += 1;
				}
				if (ps.v2_eq_max < ps.v2_eq_length) {
					ps.v2_eq_max = ps.v2_eq_length;
					ps.v2_start = ps.v2_index - ps.v2_eq_length;
				}
				if (ps.v1_eq_max < op.eq_min && ps.v1_start - ps.v1_i > op.eq_index) {
					ps.v1_eq_max = 0;
				}
				if (ps.v2_eq_max < op.eq_min && ps.v2_start - ps.v2_i > op.eq_index) {
					ps.v2_eq_max = 0;
				}
				if ((ps.v1_eq_max == 0 && ps.v2_eq_max == 0)) {
					ps.v1_new_value += "<span style='" + op.value1_style + "'>" + op.value1[ps.v1_i].replace(/</g,
						"&lt;").replace(">", "&gt;") + "</span>";
					ps.v2_new_value += "<span style='" + op.value2_style + "'>" + op.value2[ps.v2_i].replace(/</g,
						"&lt;").replace(">", "&gt;") + "</span>";
					ps.v1_i += 1;
					ps.v2_i += 1;

					if (ps.v1_i >= op.value1.length) {
						ps.v2_new_value += "<span style='" + op.value2_style + "'>" + op.value2.substr(ps.v2_i)
							.replace(
								/</g, "&lt;").replace(">", "&gt;") + "</span>";
						break;
					}
					if (ps.v2_i >= op.value2.length) {
						ps.v1_new_value += "<span style='" + op.value1_style + "'>" + op.value1.substr(ps.v1_i)
							.replace(
								/</g, "&lt;").replace(">", "&gt;") + "</span>";
						break;
					}
				} else if (ps.v1_eq_max > ps.v2_eq_max) {
					ps.v1_new_value += "<span style='" + op.value1_style + "'>" + op.value1.substr(ps.v1_i, ps
						.v1_start -
						ps.v1_i).replace(/</g, "&lt;").replace(">", "&gt;") + "</span>";
					ps.v1_i = ps.v1_start;
				} else {
					ps.v2_new_value += "<span style='" + op.value2_style + "'>" + op.value2.substr(ps.v2_i, ps
						.v2_start -
						ps.v2_i).replace(/</g, "&lt;").replace(">", "&gt;") + "</span>";
					ps.v2_i = ps.v2_start;
				}
			}
		}
		op.value1 = ps.v1_new_value;
		op.value2 = ps.v2_new_value;
		return op;
	}
	const settextheight = function() {
		var heigth = (document.documentElement.clientHeight - 64) + "px"
		document.getElementById("edit_pre_1").style.height = heigth;
		document.getElementById("edit_textarea_1").style.height = heigth;
		document.getElementById("edit_pre_2").style.height = heigth;
		document.getElementById("edit_textarea_2").style.height = heigth;
	}
	onMounted(settextheight)
	window.onresize = function() {
		settextheight();
	}
</script>

<style scoped>
	* {
		padding: 0px;
		margin: 0px;
	}

	html,
	body {
		overflow-y: hidden;
	}

	#app {
		width: 100%;
	}

	.edit_div {
		border: 1px solid #CCCCCC;
		overflow: auto;
		position: relative;
	}

	.edit_div textarea {
		resize: none;
		background: none repeat scroll 0 0 transparent;
		border: 0 none;
		width: 100%;
		height: 200px;
		overflow-y: scroll;
		position: absolute;
		left: 0px;
		top: 0px;
		z-index: 2;
		font-size: 18px;
		white-space: pre-wrap;
		word-wrap: break-word;
		word-break: break-all;
	}

	.edit_div pre {
		overflow-y: scroll;
		white-space: pre-wrap;
		word-wrap: break-word;
		word-break: break-all;
		width: 100%;
		height: 200px;
		text-align: left;
		color: #ffffff;
		z-index: 1;
		font-size: 18px;
	}
</style>
