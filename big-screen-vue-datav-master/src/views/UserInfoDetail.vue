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
            <!-- 用户基本信息 -->
            <div class="info-card">
              <dv-border-box-8 class="info-card-border">
                <h3 class="info-title">用户基本信息</h3>
                <div v-if="userInfo" class="data-container">
                    <div class="data-item" v-for="(value, key) in userInfo" :key="key">
                      <span class="data-label">{{ formatKey(key) }}:</span>
                      <span class="data-value">{{ value }}</span>
                    </div>
                  </div>
                <div v-else class="no-data">
                  <p>加载用户信息中...</p>
                </div>
              </dv-border-box-8>
            </div>

            <!-- 车辆信息 -->
            <div class="info-card">
              <dv-border-box-6 class="info-card-border">
                <h3 class="info-title">车辆信息</h3>
                <div v-if="carInfo" class="data-container">
                    <div class="data-item" v-for="(value, key) in carInfo" :key="key">
                      <span class="data-label">{{ formatKey(key) }}:</span>
                      <span class="data-value">{{ value }}</span>
                    </div>
                  </div>
                <div v-else class="no-data">
                  <p>加载车辆信息中...</p>
                </div>
              </dv-border-box-6>
            </div>

            <!-- 用户车辆详情 -->
            <div class="info-card">
              <dv-border-box-12 class="info-card-border">
                <h3 class="info-title">用户车辆详情</h3>
                <div v-if="userCarDetail" class="data-container">
                    <div class="data-item" v-for="(value, key) in userCarDetail" :key="key">
                      <span class="data-label">{{ formatKey(key) }}:</span>
                      <span class="data-value">{{ value }}</span>
                    </div>
                  </div>
                <div v-else class="no-data">
                  <p>加载用户车辆详情中...</p>
                </div>
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
    formatKey(key) {
        // 将蛇形命名转换为驼峰命名并首字母大写
        return key.replace(/([A-Z])/g, ' $1')
                  .replace(/^./, function(str) { return str.toUpperCase(); })
                  .replace(/_/g, ' ');
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

#userInfoDetail {
  color: #d3d6dd;
  width: 1920px;
  height: 1080px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transform-origin: left top;
  overflow: hidden;
}

.host-body {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.body-box {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  
  .content-box {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  justify-content: space-between;
}

.info-card {
  flex: 1 1 calc(33.333% - 20px);
  min-width: 300px;
  box-sizing: border-box;
}

.info-card-border {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.data-container {
  flex: 1;
  overflow-y: auto;
  max-height: calc(100% - 50px);
  padding: 15px;
}

.data-item {
  display: flex;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.2);
}

.data-label {
  flex: 0 0 120px;
  font-weight: bold;
  color: #8cc5ff;
}

.data-value {
  flex: 1;
  color: #fff;
  word-break: break-word;
}

.no-data {
  text-align: center;
  padding: 30px 0;
  color: #999;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
}



@media (max-width: 1200px) {
  .info-card {
    flex: 1 1 calc(50% - 20px);
  }
}

@media (max-width: 768px) {
  .info-card {
    flex: 1 1 100%;
  }
}
</style>
