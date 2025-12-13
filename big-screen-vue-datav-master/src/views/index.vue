<template>
  <div id="index" ref="appRef">
    <div class="bg bg-image-cover">
      <dv-loading v-if="loading">Loading...</dv-loading>
      <div v-else class="host-body">
        <div class="header-bar">
          <div class="header-left">
            <div class="nav-item" :class="isHomePage ? 'nav-active' : 'nav-inactive'" @click="goToHome">
              <span class="text">首页</span>
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
                  <li class="menu-item" @click="handleUserMenu('detail')">我的车辆</li>
                  <li class="menu-item" @click="handleUserMenu('edit')">编辑</li>
                  <li class="menu-item" @click="handleUserMenu('logout')">登出</li>
                </ul>
              </div>
            </div>
            <div class="user-block" v-else>
              <span class="username fw-b" @click="openLoginModal" style="cursor:pointer">登录</span>
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
              <bottomRight @car-selected="openCarRankModal" />
            </dv-border-box-13>
            <dv-border-box-12>
              <bottomLeft />

            </dv-border-box-12>
          </div>
        </div>
      </div>
      </div>
    </div>
    
    <!-- 全屏汽车排行榜详情 -->
    <car-rank-modal 
      :visible.sync="showCarRankModal" 
      :car="selectedCar" 
    />
    
    <!-- 登录浮窗 -->
    <login-modal 
      :visible.sync="showLoginModal" 
      @login-success="handleLoginSuccess"
      @switch-to-register="handleSwitchToRegister"
    />

    <!-- 注册浮窗 -->
    <register-modal 
      :visible.sync="showRegisterModal" 
      @switch-to-login="handleSwitchToLogin"
    />

    <!-- 编辑浮窗 -->
    <edit-modal 
      :visible.sync="showEditModal"
      @edit-success="handleEditSuccess"
    />

    <!-- 用户详情浮窗 -->
    <user-detail-modal 
      :visible.sync="showUserDetailModal"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import drawMixin from "../utils/drawMixin";
import { formatTime } from '../utils/index.js'
import centerLeft1 from './centerLeft1'
import centerLeft2 from './centerLeft2'
import centerRight1 from './centerRight1'
import centerRight2 from './centerRight2'
import center from './center'
import bottomLeft from './bottomLeft'
import bottomRight from './bottomRight'
import CarRankModal from '../components/CarRankModal'
import LoginModal from '../components/LoginModal'
import RegisterModal from '../components/RegisterModal'
import EditModal from '../components/EditModal'
import UserDetailModal from '../components/UserDetailModal'

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
      username: localStorage.getItem('username') || ''
    ,
      showUserMenu: false,
      showCarRankModal: false,
      selectedCar: {},
      showLoginModal: false,
      showRegisterModal: false,
      showEditModal: false,
      showUserDetailModal: false
    };
  },
  components: {
    centerLeft1,
    centerLeft2,
    centerRight1,
    centerRight2,
    center,
    bottomLeft,
    bottomRight,
    CarRankModal,
    LoginModal,
    RegisterModal,
    EditModal,
    UserDetailModal
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
  computed: {
    ...mapState(['userData'])
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
        this.showUserDetailModal = true;
      } else if (action === 'edit') {
        this.goToEdit();
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
    goToHome() {
      if (this.$route.path === '/') return;
      this.$router.push('/');
    },
    goToEdit() {
      if (!this.isLoggedIn) {
        alert('请先登录');
        this.openLoginModal();
        return;
      }
      if (!this.username) {
        alert('未找到用户名，请先登录');
        this.openLoginModal();
        return;
      }
      // 直接打开编辑浮窗，数据由浮窗内部获取
      this.showEditModal = true;
    },
    handleEditSuccess() {
      // 编辑成功后，重新获取用户数据更新页面
      this.fetchUserData();
    },
    logout() {
      // 清除本地存储中的登录状态
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('username');
      localStorage.removeItem('userRole');
      
      // 跳转到登录页面
      this.$router.push('/login');
    },
    openCarRankModal(car) {
      this.selectedCar = car || {}
      this.showCarRankModal = true
    },
    openLoginModal() {
      this.showLoginModal = true
    },
    handleSwitchToRegister() {
      this.showLoginModal = false
      setTimeout(() => {
        this.showRegisterModal = true
      }, 300) // 等待登录框动画结束
    },
    handleSwitchToLogin() {
      this.showRegisterModal = false
      setTimeout(() => {
        this.showLoginModal = true
      }, 300) // 等待注册框动画结束
    },
    handleLoginSuccess(user) {
      this.isLoggedIn = true
      this.username = user.username
      this.fetchUserData() // 获取用户信息
    }
  }
};
</script>

<style lang="scss" scoped>
@import '../assets/scss/index.scss';
</style>
