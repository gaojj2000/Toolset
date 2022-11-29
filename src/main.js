import {
	createApp
} from 'vue'
import App from './App.vue'
// npm run build 后进入 dist 文件夹，运行 python -m http.server --directory . 即可访问网页（npm run serve）
createApp(App).mount('#app')
// npm cache clear --force
// npm install
// npm run build
// npm run start
// nohup npm run start > npm_dev.log 2>&1 &
// 110.42.181.215:22812
// ps -aux | grep -v grep | grep npm
// ps -aux | grep -v grep | grep node
// cat /dev/null > ~/.bash_history && history -c && exit