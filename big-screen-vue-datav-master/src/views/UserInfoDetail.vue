<template>
  <div id="userInfoDetail" ref="appRef">
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
            <span class="title-text">用户详情信息</span>
          </div>
          <div class="header-right">
            <div class="user-block" v-if="isLoggedIn" ref="userBlock">
              <span class="username fw-b" @click="toggleUserMenu">{{ username }}</span>
              <div class="user-menu" v-if="showUserMenu">
                <ul class="menu-list">
                  <li class="menu-item" @click="handleUserMenu('detail')">进入详情页</li>
                  <li class="menu-item" @click="handleUserMenu('edit')">编辑</li>
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

        <div class="body-box">
          <div class="content-box">
            <div class="carleft">
              <CarImg :carInfo="safeCarInfo" />
              <NumInfo :carInfo="safeCarInfo" />
              <UserCarInfo :userCarDetail="safeUserCarDetail" />
              <CarTimers :carDetail="safeUserCarDetail" :carInfo="safeCarInfo" />
            </div>
            <div class="carcenter">
              <UserCarDetail :userCarDetail="safeUserCarDetail" />
              <CarInfo :carInfo="safeCarInfo" :userCarDetail="safeUserCarDetail"/>
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
import service from '@/api/index'
/* eslint-disable no-unused-vars */
import CarImg from '../components/CarImg.vue'
import CarInfo from '../components/CarInfo.vue'
import NumInfo from '../components/NumInfo.vue'
import UserCarInfo from '../components/UserCarInfo.vue'
import UserCarDetail from '../components/UserCarDetail.vue';
import CarTimers from '../components/CarTimers.vue';
/* eslint-enable no-unused-vars */



export default {
  mixins: [ drawMixin ],
  components: {
    CarImg,
    CarInfo,
    NumInfo,
    UserCarInfo,
    UserCarDetail,
    CarTimers
  },
  data() {
    return {
      timing: null,
      loading: true,
      dateDay: null,
      dateYear: null,
      dateWeek: null,
      weekday: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
      decorationColor: ['#568aea', '#000000'],
      userInfo: null,
      carInfo: null,
      userCarDetail: null,
      username: localStorage.getItem('username') || '',
      isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
      isHomePage: this.$route.path === '/' ,
      isEdit: this.$route.path === '/user-car-detail-edit',
      showUserMenu: false
    }
  },
  computed: {
    safeCarInfo() {
      const info = this.carInfo || {};
      const def = {
        id: null,
        brand: '',
        carName: '',
        carImg: '',
        saleVolume: 0,
        price: '[]',
        manufacturer: '',
        rank: 0,
        carModel: '',
        energyType: '',
        marketTime: '',
        insure: '',
        newprice: []
      };
      return { ...def, ...info };
    },
    safeUserCarDetail() {
      const d = this.userCarDetail || {};
      const def = {
        id: null,
        car_name: '',
        car_model: '',
        mileage: 0,
        purchaseDate: new Date().toISOString().slice(0, 10),
        configuration: '',
        createTime: '',
        priceRange: [6.78, 11.38]
      };
      return { ...def, ...d };
    }
  },
  mounted() {
    this.timeFn();
    this.fetchUserData();
    // 初始化登录状态
    this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    // 初始化首页状态
    this.isHomePage = this.$route.path === '/';
    // 监听登录状态变化
    window.addEventListener('storage', this.handleStorageChange);
    // 监听路由变化
    this.$watch('$route', (to, from) => {
      this.isHomePage = to.path === '/';
      // 当从编辑页面返回时，重新获取数据
      if (from.name === 'userCarDetailEdit' && to.name === 'user-detail') {
        console.log('从编辑页面返回详情页，重新获取数据');
        this.fetchUserData();
      }
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
        if (this.$route.path !== '/user-detail') {
          this.$router.push({ name: 'user-detail' });
        }
      } else if (action === 'edit') {
        this.goToEdit();
      } else if (action === 'logout') {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('username');
        localStorage.removeItem('userRole');
        
        // 如果当前不是首页，则跳转回首页
        if (this.$route.path !== '/') {
          this.$router.push('/');
        }
      }
      this.showUserMenu = false;
    },
    goToEdit() {
        // 根据用户名获取用户和车辆信息
        service.post('/myApp/entry-user-info/', {username: this.username})
          .then(res => {
            if (res.data.success) {
              const userId = res.data.userinfo?.id;
              const carId = res.data.usercarinfo?.id;
              

              if (!userId || !carId) {
                alert('未找到用户或车辆信息，请先完善用户详情');
                this.$router.push('/user-detail');
                return;
              }

              // 存储用户数据
              sessionStorage.setItem('userData', JSON.stringify(res.data));
              sessionStorage.setItem('userInfo', JSON.stringify(res.data.userinfo));
              sessionStorage.setItem('userCarInfo', JSON.stringify(res.data.usercarinfo));

              // 跳转到编辑页面（不携带参数在URL中）
              this.$router.push({
                path: '/user-car-detail-edit'
              });
            } else {
              alert(res.data.message || '获取用户信息失败');
            }
          })
          .catch(error => {
            console.error('获取用户信息错误:', error);
            alert('网络请求错误: ' + error.message);
          });
      },
    handleStorageChange(event) {
      if (event.key === 'username') {
        this.username = event.newValue || '';
        this.fetchUserData();
      }
      if (event.key === 'isLoggedIn') {
        this.isLoggedIn = event.newValue === 'true';
      }
    },
    timeFn() {
      this.timing = setInterval(() => {
        this.dateDay = formatTime(new Date(), 'HH: mm: ss');
        this.dateYear = formatTime(new Date(), 'yyyy-MM-dd');
        this.dateWeek = this.weekday[new Date().getDay()];
      }, 1000);
    },
    fetchUserData() {
      if (!this.username) {
        this.loading = false;
        return;
      }
      service.post('/myApp/entry-user-info/', { username: this.username })
        .then(res => {
          if (res.data && res.data.success) {
            this.userInfo = res.data.userinfo || null;
            this.userCarDetail = res.data.usercarinfo || null;
            this.carInfo = res.data.data || null;
          }
        })
        .catch(err => {
          console.error('统一获取用户数据失败:', err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchUserInfo() { return Promise.resolve(); },
    fetchCarInfo() { return Promise.resolve(); },
    fetchUserCarDetail() { return Promise.resolve(); },
      goToHome() {
        if (this.$route.path === '/') return;
        this.$router.push('/');
      }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/user-info-detail.scss';
</style>
