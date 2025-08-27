import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import dataV from '@jiaminghi/data-view';
// DataV MutationObserver 错误修复补丁
import patchDataV from './utils/dataViewPatch';
// 应用补丁
patchDataV();

// // 仅在开发模式下运行补丁测试 - 已禁用
// if (process.env.NODE_ENV === 'development') {
//   import('./utils/testDataViewPatch').then(({ default: testDataViewPatch }) => {
//     // 延迟执行测试，确保应用初始化完成
//     setTimeout(() => {
//       testDataViewPatch();
//     }, 1000);
//   }).catch(error => {
//     console.error('加载 DataV 补丁测试失败:', error);
//   });
// }
// 引入全局css
import './assets/scss/style.scss';
// 按需引入vue-awesome图标
import Icon from 'vue-awesome/components/Icon';
import 'vue-awesome/icons/chart-bar.js';
import 'vue-awesome/icons/chart-area.js';
import 'vue-awesome/icons/chart-pie.js';
import 'vue-awesome/icons/chart-line.js';
import 'vue-awesome/icons/align-left.js';
import $http from '@/api/index.js'

//引入echart
//4.x 引用方式
import echarts from 'echarts'
//5.x 引用方式为按需引用
//希望使用5.x版本的话,需要在package.json中更新版本号,并切换引用方式
//import * as echarts from 'echarts'
Vue.prototype.$echarts = echarts
Vue.config.productionTip = false;
Vue.prototype.$http = $http

// 引入自定义弹窗函数并全局替换原生alert
import { showModal } from './utils/index.js';
window.alert = showModal;
// 全局注册
Vue.component('icon', Icon);
Vue.use(dataV);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
