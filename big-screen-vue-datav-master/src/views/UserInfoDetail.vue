<template>
  <div id="userInfoDetail" ref="appRef">
    <div class="bg" style="background: url('/VCG41N1312873566.jpg') center/cover no-repeat;position: relative;">
      <dv-loading v-if="loading">Loading...</dv-loading>
      <div v-else class="host-body">
        <div class="d-flex jc-center">
          <dv-decoration-10 class="dv-dec-10" />
          <div class="d-flex jc-center">
            <dv-decoration-8 class="dv-dec-8" :color="decorationColor" />
            <div class="title">
              <span class="title-text">用户详情信息</span>
              <dv-decoration-5
                class="dv-dec-6"
                :reverse="true"
              />
            </div>
            <dv-decoration-8
              class="dv-dec-8"
              :reverse="true"
              :color="decorationColor"
            />
          </div>
          <dv-decoration-10 class="dv-dec-10-s" />
        </div>

        <!-- 第二行 -->
        <div class="d-flex jc-between px-2">
          <div class="d-flex aside-width">
            <div class="react-left ml-4 react-l-s" :style="{ backgroundColor: isHomePage ? '#9c27b0' : '#2196f3', display: 'flex', justifyContent: 'center', alignItems: 'center' }">
              <span class="text" @click="goToHome">首页</span>
            </div>
            <div class="react-left ml-3">
              <span class="text">PK</span>
            </div>
          </div>
          <div class="d-flex aside-width">
            <div class="react-right bg-color-green mr-3" v-if="isLoggedIn">
              <span class="text fw-b">{{ username }}</span>
            </div>
            <div class="react-right mr-4 react-l-s">
              <span class="react-after"></span>
              <span class="text">{{ dateYear }} {{ dateWeek }} {{ dateDay }}</span>
            </div>
          </div>
        </div>

        <div class="body-box">
          <div class="content-box">
                <!-- 车辆图片和详细信息 -->
            <div class="car-container">
              <!-- 车辆图片信息 -->
              <CarImg :carInfo="carInfo" />

              <!-- 新增的车辆详细信息组件 -->
              <CarInfo :carInfo="carInfo" />
            </div>

            <!-- 车辆信息 -->
            <UserCarInfo :carInfo="carInfo" />

            <!-- 用户车辆详情 -->
            <UserCarDetail :userCarDetail="userCarDetail" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import drawMixin from "../utils/drawMixin";
import { formatTime } from '../utils/index.js'
import axios from "axios";
/* eslint-disable no-unused-vars */
import CarImg from '../components/CarImg.vue'
import CarInfo from '../components/CarInfo.vue'
import UserCarInfo from '../components/UserCarInfo.vue'
import UserCarDetail from '../components/UserCarDetail.vue';
/* eslint-enable no-unused-vars */



export default {
  mixins: [ drawMixin ],
  components: {
    CarImg,
    CarInfo,
    UserCarInfo,
    UserCarDetail
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
      isHomePage: this.$route.path === '/' 
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
    this.$watch('$route', (to) => {
      this.isHomePage = to.path === '/';
    });
  },
  beforeDestroy() {
    clearInterval(this.timing);
    window.removeEventListener('storage', this.handleStorageChange);
  },
  methods: {
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

        // 分别获取用户信息、车辆信息和用户车辆详情
        Promise.all([
          this.fetchUserInfo(),
          this.fetchCarInfo(),
          this.fetchUserCarDetail()
        ]).then(() => {
          this.loading = false;
        }).catch(error => {
          console.error('获取数据失败:', error);
          this.loading = false;
        });
      },
    fetchUserInfo() {
      return axios.post('http://localhost:8000/myApp/get-user-info/', {
        username: this.username
      }).then(res => {
        if (res.data.success) {
          this.userInfo = res.data.userInfo;
        } else {
          console.error('获取用户信息失败:', res.data.message);
        }
      }).catch(error => {
        console.error('请求用户信息失败:', error);
      });
    },
    fetchCarInfo() {
      return axios.post('http://localhost:8000/myApp/get-car-info/', {
        username: this.username
      }).then(res => {
        if (res.data.success) {
          this.carInfo = res.data.carInfo;
        } else {
          console.error('获取车辆信息失败:', res.data.message);
        }
      }).catch(error => {
        console.error('请求车辆信息失败:', error);
      });
    },
    fetchUserCarDetail() {
      return axios.post('http://localhost:8000/myApp/get-user-car-detail/', {
        username: this.username
      }).then(res => {
        if (res.data.success) {
          this.userCarDetail = res.data.userCarDetail;
        } else {
          console.error('获取用户车辆详情失败:', res.data.message);
        }
      }).catch(error => {
        console.error('请求用户车辆详情失败:', error);
      });
    },
      goToHome() {
        this.$router.push('/');
      }
  }
}
</script>

<style lang="scss" scoped>
// @import '../assets/scss/index.scss';
@import '../assets/scss/user-info-detail.scss';
</style>
