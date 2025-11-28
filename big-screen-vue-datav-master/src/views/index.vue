<template>
  <div id="index" ref="appRef">
    <div class="bg themed-bg-home">
      <dv-loading v-if="loading">Loading...</dv-loading>
      <div v-else class="host-body">
        <div class="header-bar">
          <div class="header-left">
            <div class="nav-item" :class="isHomePage ? 'nav-active' : 'nav-inactive'" @click="goToHome">
              <span class="text">首页</span>
            </div>
            <div class="nav-item" :class="isEdit ? 'nav-active' : 'nav-inactive'" @click="goToEdit">
              <span class="text">编辑</span>
            </div>
          </div>
          <div class="header-title">
            <span class="title-text">大数据可视化平台</span>
          </div>
          <div class="header-right">
            <div class="user-block" v-if="isLoggedIn" ref="userBlock">
              <span class="username fw-b" @click="toggleUserMenu">{{ username }}</span>
              <div class="user-menu" v-if="showUserMenu">
                <ul class="menu-list">
                  <li class="menu-item" @click="handleUserMenu('detail')">进入详情页</li>
                  <li class="menu-item" @click="handleUserMenu('logout')">登出</li>
                </ul>
              </div>
            </div>
            <div class="user-block" v-else>
              <router-link to="/login" class="username fw-b">登录</router-link>
            </div>
            <div class="date-block">
              <span class="date-text">{{ dateYear }} {{ dateWeek }} {{ dateDay }}</span>
            </div>
          </div>
        </div>
      <div>
        <div class="body-box">
          <!-- 第三行数据 -->
          <div class="content-box">
            <div>
              <dv-border-box-8>
                <centerRight1 />

              </dv-border-box-8>
            </div>
            <div>
              <dv-border-box-6>
                <centerLeft2 />
              </dv-border-box-6>
            </div>
            <!-- 中间 -->
            <div>
              <center />
            </div>
            <!-- 中间 -->
            <div>
              <dv-border-box-12>
              <centerLeft1 />
              </dv-border-box-12>
            </div>
            <div>

                <centerRight2 />

            </div>
          </div>

          <!-- 第四行数据 -->
          <div class="bottom-box">
            <dv-border-box-13>
              <bottomRight />
            </dv-border-box-13>
            <dv-border-box-12>
              <bottomLeft />

            </dv-border-box-12>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import drawMixin from "../utils/drawMixin";
import { formatTime } from '../utils/index.js'
import centerLeft1 from './centerLeft1'
import centerLeft2 from './centerLeft2'
import centerRight1 from './centerRight1'
import centerRight2 from './centerRight2'
import center from './center'
import bottomLeft from './bottomLeft'
import bottomRight from './bottomRight'
import axios from "axios";

export default {
  mixins: [ drawMixin ],
  data() {
    return {
      timing: null,
      loading: true,
      dateDay: null,
      dateYear: null,
      dateWeek: null,
      weekday: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
      decorationColor: ['#568aea', '#000000'],
      isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
      isHomePage: this.$route.path === '/',
      isEdit: this.$route.path === '/user-car-detail-edit',
      username: localStorage.getItem('username') || ''
    ,
      showUserMenu: false
    };
  },
  components: {
    centerLeft1,
    centerLeft2,
    centerRight1,
    centerRight2,
    center,
    bottomLeft,
    bottomRight
  },
  mounted() {
    this.timeFn();
    this.cancelLoading();
    // 初始化首页状态
    this.isHomePage = this.$route.path === '/';
    // 监听登录状态变化
    window.addEventListener('storage', this.handleStorageChange);
    // 监听路由变化
    this.$watch('$route', (to) => {
      this.isHomePage = to.path === '/';
    });
    document.addEventListener('click', this.handleDocumentClick);
  },
  beforeDestroy() {
    clearInterval(this.timing);
    window.removeEventListener('storage', this.handleStorageChange);
    document.removeEventListener('click', this.handleDocumentClick);
  },
  methods: {
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    handleDocumentClick(e) {
      const el = this.$refs.userBlock;
      if (el && !el.contains(e.target)) this.showUserMenu = false;
    },
    handleUserMenu(action) {
      if (action === 'detail') {
        this.entryInfo();
      } else if (action === 'logout') {
        this.logout();
      }
      this.showUserMenu = false;
    },
    handleStorageChange(event) {
      if (event.key === 'isLoggedIn') {
        this.isLoggedIn = event.newValue === 'true';
      }
      if (event.key === 'username') {
        this.username = event.newValue || '';
      }
    },
    timeFn() {
      this.timing = setInterval(() => {
        this.dateDay = formatTime(new Date(), 'HH: mm: ss');
        this.dateYear = formatTime(new Date(), 'yyyy-MM-dd');
        this.dateWeek = this.weekday[new Date().getDay()];
      }, 1000);
    },
    cancelLoading() {
      setTimeout(() => {
        this.loading = false;
      }, 500);
    },
    entryInfo(){
      axios.post('http://localhost:8000/myApp/entry-user-info/', {username:this.username})
        .then(res => {
          if (res.data.success){
            sessionStorage.setItem('userData', JSON.stringify(res.data));
            sessionStorage.setItem('userInfo', JSON.stringify(res.data.userinfo));
            sessionStorage.setItem('userCarInfo', JSON.stringify(res.data.usercarinfo));
            this.$router.push({ path: '/user-detail' });
          }
          else{
            alert(res.data.message || '请求失败');
          }
        })
        .catch(error => {
          console.error('Request error:', error);
          alert('网络请求错误: ' + error.message);
        });
    },
    goToHome() {
      if (this.$route.path === '/') return;
      this.$router.push('/');
    },
    goToEdit() {
      if (!this.isLoggedIn) {
        alert('请先登录');
        if (this.$route.path !== '/login') this.$router.push('/login');
        return;
      }
      if (!this.username) {
        alert('未找到用户名，请先登录');
        if (this.$route.path !== '/login') this.$router.push('/login');
        return;
      }
      axios.post('http://localhost:8000/myApp/entry-user-info/', {username: this.username})
        .then(res => {
          if (res.data.success) {
            const userId = res.data.userinfo?.id;
            const carId = res.data.usercarinfo?.id;
            if (!userId || !carId) {
              alert('未找到用户或车辆信息，请先完善用户详情');
              if (this.$route.path !== '/user-detail') this.$router.push('/user-detail');
              return;
            }
            sessionStorage.setItem('userData', JSON.stringify(res.data));
            sessionStorage.setItem('userInfo', JSON.stringify(res.data.userinfo));
            sessionStorage.setItem('userCarInfo', JSON.stringify(res.data.usercarinfo));
            if (this.$route.path !== '/user-car-detail-edit') {
              this.$router.push({ path: '/user-car-detail-edit' });
            }
          } else {
            alert(res.data.message || '获取用户信息失败');
          }
        })
        .catch(error => {
          console.error('获取用户信息错误:', error);
          alert('网络请求错误: ' + error.message);
        });
    },
    logout() {
      // 清除本地存储中的登录状态
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('username');
      localStorage.removeItem('userRole');
      
      // 跳转到登录页面
      this.$router.push('/login');
    }
  }
};
</script>

<style lang="scss" scoped>
@import '../assets/scss/index.scss';
</style>
