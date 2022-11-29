import Menu from './components/Menu.vue'
import NotFound from './components/NotFound.vue'
import DotsAndBoxes from './components/DotsAndBoxes.vue'
import ColorModeConversion from './components/ColorModeConversion.vue'
import SocialSecurityCalculator from './components/SocialSecurityCalculator.vue'
import OnlineExcel from './components/OnlineExcel.vue'
import OnlineTerminal from './components/OnlineTerminal.vue'
import Debounce from "./components/Debounce.vue"
import StringHandling from './components/StringHandling.vue'
import TextDiff from './components/TextDiff.vue'
import YuanShenHistroyAnalysis from './components/YuanShenHistroyAnalysis.vue'

const routes = {
	'/dab': DotsAndBoxes,
	'/cmc': ColorModeConversion,
	'/ssc': SocialSecurityCalculator,
	'/excel': OnlineExcel,
	'/shell': OnlineTerminal,
	'/debounce': Debounce,
	'/words': StringHandling,
	'/diff': TextDiff,
	'/yuanshen': YuanShenHistroyAnalysis,
	'/404': NotFound,
}

const titles = {
	'/dab': '点格棋',
	'/cmc': '颜色转换',
	'/ssc': '社保计算器',
	'/excel': 'Excel表格编辑器',
	'/shell': '在线Shell终端',
	'/debounce': '实现防抖函数',
	'/words': '字符串处理',
	'/diff': '字符串对比',
	'/yuanshen': '原神抽卡分析',
	'/404': '访问不到的页面',
}

export {
	routes,
	titles,
	Menu,
	NotFound
}
