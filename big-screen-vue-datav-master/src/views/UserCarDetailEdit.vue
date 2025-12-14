<template>
  <div id="userCarDetailEdit" ref="appRef">
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
            <span class="title-text">编辑用户车辆详情</span>
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
          <div class="edit-layout">
            <div class="left-preview">
              <div class="greeting">
                <span>你好，{{ username || '用户' }}</span>
              </div>
              <div class="preview-media">
                <img v-if="carImageUrl" :src="carImageUrl" alt="车辆图片" class="car-image"/>
                <svg v-else class="car-silhouette" viewBox="0 0 512 256" xmlns="http://www.w3.org/2000/svg">
                  <path fill="#1b2337" d="M32 160c0-48 64-80 96-96s128-32 160-32 64 64 96 80 64 16 64 48-16 48-48 48H80c-32 0-48-16-48-48z"/>
                  <circle cx="128" cy="192" r="28" fill="#2a3a5a"/>
                  <circle cx="384" cy="192" r="28" fill="#2a3a5a"/>
                </svg>
              </div>
              <div class="preview-name">
                <span>{{ carName || '未填写车辆名称' }}</span>
              </div>
            </div>
            <div class="right-form">
              <dv-border-box-1 class="user-detail-border-box">
                <div class="user-detail-form">
                  <div class="form-group">
                    <label for="carName" style="color: white">车辆名字</label>
                    <div class="search-input-container">
                      <input type="text" id="carName" v-model="carName" @input="searchCars" placeholder="请输入车辆名字">
                      <div class="search-results" v-if="searchResults.length > 0">
                        <div v-for="car in searchResults" :key="car.id" @click="selectCar(car)">{{ car.carName }} ({{ car.carModel }})</div>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="carModel" style="color: white">车辆型号</label>
                    <input type="text" id="carModel" v-model="carModel" placeholder="请输入车辆型号">
                  </div>
                  <div class="form-group">
                    <label for="mileage" style="color: white">车辆公里数</label>
                    <input type="number" id="mileage" v-model="mileage" placeholder="请输入车辆公里数">
                  </div>
                  <div class="form-group">
                    <label for="purchaseDate" style="color: white">车辆购买时间</label>
                    <input type="date" id="purchaseDate" v-model="purchaseDate">
                  </div>
                  <div class="form-group">
                    <label for="configuration" style="color: white">车辆配置</label>
                    <textarea id="configuration" v-model="configuration" placeholder="请输入车辆配置"></textarea>
                  </div>
                  <button class="submit-btn" @click="submitForm">更新</button>
                </div>
              </dv-border-box-1>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import DataV from '@jiaminghi/data-view'
import service from '@/api/index'
import drawMixin from "../utils/drawMixin"

Vue.use(DataV)

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
      username: localStorage.getItem('username') || '',
      userId: null,
      isHomePage: this.$route.path === '/',
      carId: null,
      carName: '',
      carModel: '',
      mileage: 0,
      purchaseDate: '',
      configuration: '',
      searchResults: [],
      carImageUrl: '',
      showUserMenu: false
    }
  },
  mounted() {
    // 从localStorage获取用户名
    this.username = localStorage.getItem('username') || '';
    
    // 参数验证
    if (!this.username) {
      alert('用户未登录，请先登录');
      this.$router.push('/login');
      return;
    }
    
    // 设置时间
    this.updateTime();
    this.timing = setInterval(() => {
      this.updateTime();
    }, 1000 * 60);

    // 监听路由变化以同步导航状态
    this.$watch('$route', (to) => {
      this.isHomePage = to.path === '/';
    });

    document.addEventListener('click', this.handleDocumentClick);

    // 获取车辆详情
    this.fetchCarDetail();
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleDocumentClick);
  },
  methods: {
    updateTime() {
      const now = new Date();
      this.dateYear = now.getFullYear() + '年';
      this.dateWeek = now.getMonth() + 1 + '月' + now.getDate() + '日';
      this.dateDay = this.weekday[now.getDay()];
    },
    
    goToHome() {
    this.$router.push('/');
    },
    goToEdit() {
    // 已经在编辑页，什么都不做
    },
    entryInfo() {
      this.$router.push({ name: 'user-detail' });
    },
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
      } else if (action === 'edit') {
        this.goToEdit();
      } else if (action === 'logout') {
        this.logout();
      }
      this.showUserMenu = false;
    },
    logout() {
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('username');
      localStorage.removeItem('userRole');
      this.$router.push('/');
    },
    
    fetchCarDetail() {
      // 从localStorage获取用户名（登录信息存储在此处）
      const username = localStorage.getItem('username');

      // 参数验证
      if (!username) {
        alert('用户未登录，请先登录');
        this.$router.push('/login');
        return;
      }

      // 请求用户车辆详情（与后端 urls.py 一致的下划线路径）
      service.post('/myApp/if_user_car_detail/', {
        username: username
      })
      .then(response => {
        if (response.data.success) {
          // 保存用户ID
          this.userId = response.data.userid;
          this.carId = response.data.user_car_detail.car_id;

          // 从car_data字段获取车辆基本信息
          const carData = response.data.car_data;
          if (carData) {
            this.carName = carData.carName || carData.car_name;
            this.carModel = carData.carModel || carData.car_model;
            this.carImageUrl = carData.carImg || '';
          }

          // 从user_car_detail字段获取用户车辆详情
          const userCarData = response.data.user_car_detail;
          if (userCarData) {
            this.mileage = userCarData.mileage;
            this.purchaseDate = userCarData.purchase_date || userCarData.purchaseDate;
            this.configuration = userCarData.configuration;
          }

          if (!carData || !userCarData) {
            alert('未找到完整的车辆信息');
          }
        } else {
          alert(response.data.message || '获取车辆信息失败');
        }
      })
      .catch(error => {
        console.error('获取车辆信息失败:', error);
        alert('获取车辆信息失败，请重试');
      })
      .finally(() => {
        this.loading = false;
      })
    },

    // 移除不再需要的方法
    

    searchCars() {
      if (this.carName.length < 1) {
        this.searchResults = []
        return
      }

      service.get('/myApp/search-cars/', {
        params: {
          name: this.carName
        }
      })
      .then(response => {
        this.searchResults = response.data.cars
        const match = this.searchResults.find(item => item.carName === this.carName)
        if (match && match.carImg) this.carImageUrl = match.carImg
      })
      .catch(error => {
        console.error('搜索车辆失败:', error)
      })
    },

    selectCar(car) {
      this.carName = car.carName
      this.carModel = car.carModel
      this.carImageUrl = car.carImg || ''
      this.searchResults = []
    },

    submitForm() {
      // 表单验证
      if (!this.carName || !this.carModel || !this.mileage || !this.purchaseDate || !this.configuration) {
        alert('请填写所有字段');
        return;
      }

      if (!this.userId) {
        alert('用户ID不存在，请重新登录');
        this.$router.push('/login');
        return;
      }

      // 发送更新请求到后端API（与后端 urls.py 一致的下划线路径）
      service.post('/myApp/save_user_car_detail/', {
        userId: this.userId,
        carName: this.carName,
        carModel: this.carModel,
        mileage: this.mileage,
        purchaseDate: this.purchaseDate,
        configuration: this.configuration
      })
      .then(response => {
        if (response.data.success) {
          alert('车辆详情更新成功');
          // 可以跳转到用户详情页或其他页面
          this.$router.push({ name: 'user-detail', query: { userId: this.userId } });
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.error('更新车辆详情失败:', error);
        alert('更新车辆详情失败，请重试');
      });
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/user-car-detail-edit.scss';
</style>
