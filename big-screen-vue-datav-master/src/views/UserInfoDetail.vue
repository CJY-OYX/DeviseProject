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
            <div class="react-left ml-3" :style="{ backgroundColor: isEdit ? '#9c27b0' : '#2196f3', display: 'flex', justifyContent: 'center', alignItems: 'center' }
              "><span class="text" @click="goToEdit">编辑</span>
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
            <div class="carleft">
              <CarImg :carInfo="carInfo" />
              <NumInfo :carInfo="carInfo" />
              <UserCarInfo :userCarDetail="userCarDetail" />
              <CarTimers :carDetail="userCarDetail" :carInfo="carInfo" />
            </div>
            <div class="carcenter">
              <UserCarDetail :userCarDetail="userCarDetail" />
              <CarInfo :carInfo="carInfo" :userCarDetail="userCarDetail"/>
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
import axios from "axios";
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
      isEdit: this.$route.path === '/user-car-detail-edit'
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
  },
  beforeDestroy() {
    clearInterval(this.timing);
    window.removeEventListener('storage', this.handleStorageChange);
  },
  methods: {
    goToEdit() {
        // 根据用户名获取用户和车辆信息
        axios.post('http://localhost:8000/myApp/entry-user-info/', {username: this.username})
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
        console.log('开始获取用户数据...');
        if (!this.username) {
          this.loading = false;
          return;
        }

        // 获取用户信息 车辆信息 用户车辆详情
        Promise.all([
          this.fetchUserInfo(),
          this.fetchCarInfo(),
          this.fetchUserCarDetail()
        ]).then(() => {
          console.log('数据获取完成，userCarDetail:', this.userCarDetail);
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
      console.log('【1】开始调用 /get-user-car-detail');
      return axios
        .post('http://localhost:8000/myApp/get-user-car-detail/', {
          username: this.username
        })
        .then(res => {
          console.log('【2】接口返回：', res.data);
          if (res.data.success) {
            this.userCarDetail = res.data.userCarDetail;
            console.log('【3】已写入 this.userCarDetail', this.userCarDetail);
          } else {
            console.error('获取用户车辆详情失败：', res.data.message);
          }
        })
        .catch(err => {
          console.error('请求用户车辆详情失败：', err);
        });
    },
      goToHome() {
        this.$router.push('/');
      }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/user-info-detail.scss';
</style>
