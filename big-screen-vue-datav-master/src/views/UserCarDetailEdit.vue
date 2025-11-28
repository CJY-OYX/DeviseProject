<template>
  <div id="userCarDetailEdit" ref="appRef">
    <div class="bg themed-bg-edit">
      <dv-loading v-if="loading">Loading...</dv-loading>
      <div v-else class="host-body">
        <div class="d-flex jc-center">
          <dv-decoration-10 class="dv-dec-10" />
          <div class="d-flex jc-center">
            <dv-decoration-8 class="dv-dec-8" :color="decorationColor" />
            <div class="title">
              <span class="title-text">编辑用户车辆详情</span>
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
            <div class="react-left ml-4 react-l-s" :class="isHomePage ? 'nav-active' : 'nav-inactive'" style="display:flex;justify-content:center;align-items:center;cursor:pointer;" @click="goToHome">
              <span class="text">首页</span>
            </div>
            <div class="react-left ml-3 react-l-s" :class="(!isHomePage) ? 'nav-active' : 'nav-inactive'" style="display:flex;justify-content:center;align-items:center;cursor:pointer;" @click="goToEdit">
              <span class="text">编辑</span>
            </div>
          </div>
          <div class="d-flex aside-width">
            <div class="react-right bg-color-green mr-3" v-if="isLoggedIn" style="display: flex; justify-content: center; align-items: center; width: 300px;">
              <span class="text fw-b" @click="entryInfo">{{ username }}</span>
            </div>
            <div class="react-right mr-4 react-l-s">
              <span class="react-after"></span>
              <span class="text">{{ dateYear }} {{ dateWeek }} {{ dateDay }}</span>
            </div>
          </div>
        </div>

        <div class="body-box">
          <div class="content-box">
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
</template>

<script>
import Vue from 'vue'
import DataV from '@jiaminghi/data-view'
import axios from 'axios'
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
      isLoggedIn: true,
      username: localStorage.getItem('username') || '',
      userId: null,
      isHomePage: false,
      carId: null,
      carName: '',
      carModel: '',
      mileage: 0,
      purchaseDate: '',
      configuration: '',
      searchResults: []
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

    // 获取车辆详情
    this.fetchCarDetail();
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
      axios.post('http://localhost:8000/myApp/if_user_car_detail/', {
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

      axios.get('http://localhost:8000/myApp/search-cars/', {
        params: {
          name: this.carName
        }
      })
      .then(response => {
        this.searchResults = response.data.cars
      })
      .catch(error => {
        console.error('搜索车辆失败:', error)
      })
    },

    selectCar(car) {
      this.carName = car.carName
      this.carModel = car.carModel
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
      axios.post('http://localhost:8000/myApp/save_user_car_detail/', {
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
