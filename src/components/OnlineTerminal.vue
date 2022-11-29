<template>
	<h1>在线Shell终端 <a href="#/">[返回目录]</a></h1>
	<div id="terminal" class="console">
		<table>
			<tr>
				<td>主机地址：</td>
				<td><input type="text" v-model="option.host" /></td>
			</tr>
			<tr>
				<td>主机端口：</td>
				<td><input type="number" v-model="option.port" /></td>
			</tr>
			<tr>
				<td>用户名：</td>
				<td><input type="text" v-model="option.username" /></td>
			</tr>
			<tr>
				<td>密码：</td>
				<td><input type="password" v-model="option.password" /></td>
			</tr>
			<tr>
				<td>超时时间：</td>
				<td><input type="number" v-model="option.time" /></td>
			</tr>
			<tr>
				<td colspan="2" style="height: 40px;">
					<a @click="connected()">连接</a>
				</td>
			</tr>
		</table>
	</div>
</template>

<script setup>
	// npm install xterm == 3.1.0 （或写入package.json中，并执行npm install）【该插件 Alt + C 清除回滚】
	import {
		Terminal
	} from 'xterm'
	import {
		ref,
		onMounted,
		onUnmounted
	} from 'vue'
	import * as fit from 'xterm/lib/addons/fit/fit'
	import * as attach from 'xterm/lib/addons/attach/attach'
	import 'xterm/dist/xterm.css'
	const term = ref(null)
	const endpoint = ref(null)
	const connection = ref(null)
	const protocol = ref('')
	const option = ref({
		operate: 'connect', // 连接操作
		host: '110.42.181.215', // 主机地址
		port: 22, // 端口号
		username: 'root', // 用户名
		password: '就不告诉你！', // 密码
		time: 22 // 超时时间
	})
	var stop = false;
	var change = false;
	var history = [];
	var curr_line = '';
	var index = history.length;
	var terminalContainer = null;
	const connected = function() {
		terminalContainer.innerHTML = '';
		term.value.open(terminalContainer, true)
		term.value.write('Connecting...')
		if (window.WebSocket) { // 如果支持websocket
			connection.value = new WebSocket(endpoint.value) //后端接口位置
		} else {
			term.value.write('\n\rError: WebSocket Not Supported\r\n')
			console.log('Error: WebSocket Not Supported\r\n')
		}
		connection.value.onopen = function() {
			// 连接成功回调
			connection.value.send(JSON.stringify(option.value))
			term.value.focus()
		}
		connection.value.onclose = function() {
			// 连接关闭回调
			term.value.write('\n\rConnection closed.')
			console.log('Connection closed.')
			stop = true;
		}
		connection.value.onerror = function(error) {
			// 连接失败回调
			term.value.write('\n\rError: ' + error + '\r\n')
			console.log('Error: ' + error + '\r\n')
		}
		term.value.attach(connection.value)
	}
	onMounted(() => {
		terminalContainer = document.getElementById('terminal')
	})
	onUnmounted(() => {
		connection.value?.close()
		term.value?.destroy()
	})
	Terminal.applyAddon(attach)
	Terminal.applyAddon(fit)
	if (window.location.protocol.value == 'https:') {
		protocol.value = 'wss://'
	} else {
		protocol.value = 'ws://'
	}
	endpoint.value = protocol.value + 'localhost:2345/shell'
	term.value = new Terminal({
		cols: 150,
		rows: 50,
		rendererType: 'canvas', // 渲染类型
		scrollback: 1000, // 终端中的回滚行数
		disableStdin: false, // 是否禁用输入
		cursorStyle: 'block', // 光标样式
		cursorBlink: true, // 光标闪烁
		tabStopWidth: 4, // tab宽度
		fontFamily: 'Lucida Console', // 字体类型
		theme: {
			foreground: '#00FF00', // 字体颜色
			background: '#000', // 背景色
			// cursor: 'help', // 设置光标
			lineHeight: 16 // 行高
		}
	})
	term.value.onKey(e => {
		const printable = !(e.domEvent.altKey || e.domEvent.altGraphKey || // 控制键alt
				e.domEvent.ctrlKey || e.domEvent.metaKey || stop) && // 控制键ctrl
			(e.domEvent.keyCode == 32 || (e.domEvent.keyCode > 47 && e.domEvent.keyCode < 58) || // 空格和数字
				(e.domEvent.keyCode > 64 && e.domEvent.keyCode < 91) || // 大写字母
				(e.domEvent.keyCode > 95 && e.domEvent.keyCode < 108) || // 数字键盘数字与加乘符号
				(e.domEvent.keyCode > 108 && e.domEvent.keyCode < 111) || // 数字键盘减点斜杠符号
				(e.domEvent.keyCode > 185 && e.domEvent.keyCode < 223)) // 特殊符号
		if (printable) { // 可打印字符
			if (term.value._core.buffer.x - curr_line.length == 2) { // 光标在最后
				curr_line += e.key;
				term.value.write(e.key)
			} else { // 光标在当中
				curr_line = curr_line.slice(0, term.value._core.buffer.x - 2) + e.key + curr_line.slice(term.value._core.buffer.x - 2, curr_line.length + 1);
				term.value.write(curr_line.slice(term.value._core.buffer.x - 2, curr_line.length + 1))
				change = true;
			}
		} else { // 控制字符
			if (e.domEvent.keyCode == 13 || e.domEvent.keyCode == 108) { // 字母数字键盘与数字键盘的回车
				if (curr_line == 'exit') { // 退出登录
					stop = true;
				}
				if (change && curr_line.length > 1) { // 修改后的命令长度大于1时，由后端覆盖命令；未输入命令时，无法回车
					connection.value.send(curr_line)
					change = false;
				}
				history.push(curr_line);
				index = history.length;
				curr_line = '';
			} else if (e.domEvent.keyCode == 8) { // Backspace删除的情况
				if (term.value._core.buffer.x > 2 && curr_line) {
					term.value.write('\b \b')
					connection.value.send('\b')
					curr_line = curr_line.slice(0, term.value._core.buffer.x - 3) + curr_line.slice(term.value._core.buffer.x - 2, curr_line.length);
					change = true;
				}
			} else if (e.domEvent.keyCode == 38) { // 向上键
				while (term.value._core.buffer.x > 2 && curr_line) {
					term.value.write('\b \b')
					connection.value.send('\b')
					curr_line = curr_line.slice(0, -1);
				}
				index = index > 0 ? index - 1 : 0
				curr_line = history[index];
				term.value.write(curr_line);
				change = true;
			} else if (e.domEvent.keyCode == 40) { // 向下键
				while (term.value._core.buffer.x > 2 && curr_line) {
					term.value.write('\b \b')
					connection.value.send('\b')
					curr_line = curr_line.slice(0, -1);
				}
				index = index + 1 < history.length ? index + 1 : history.length - 1
				curr_line = history[index];
				term.value.write(curr_line);
				change = true;
			} else if (e.domEvent.keyCode == 37) { // 向左键
				term.value.write('\b')
			} else if (e.domEvent.keyCode == 39) { // 向右键
				term.value.write(curr_line[term.value._core.buffer.x - 2])
			} else if (e.domEvent.ctrlKey && e.domEvent.keyCode == 67) { // Ctrk+C终止程序，暂时用超时时间来代替源解决方案
				// connection.value.send(JSON.stringify({operate: 'ctrl+c'}))
			} else if (e.domEvent.ctrlKey && e.domEvent.keyCode == 68) { // Ctrl+D退出登录
				if (!stop) {
					term.value.write('exit')
				}
				stop = true;
				connection.value.send('exit')
				connection.value.send('\r')
			} else if (e.domEvent.ctrlKey && e.domEvent.keyCode == 86) { // Ctrl + Shift + V 粘贴，保留 Ctrl + V 快捷键
				term.value.write('\b\bPlease press " Ctrl + Shift + V " to parse content.')
				connection.value.send('\r')
			}
		}
	})
	term.value.on('paste', function(data) { // 粘贴事件
		term.value.write(data);
		curr_line += data;
	})
	term.value.on('selection', function() { // 选择事件
		if (term.value.hasSelection()) {
			document.execCommand('copy'); // 自动复制选择的内容
			console.log(term.value.getSelection()); // 打印选择的内容
		}
	})
</script>

<style>
	table {
		margin: 0 auto;
		text-align: center;
	}

	table a {
		color: red;
		cursor: pointer;
		padding: 2px 10px;
		border: 1px solid blue;
	}
</style>
