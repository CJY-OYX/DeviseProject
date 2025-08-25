<template>
  <div class="user-detail-container">
    <dv-border-box-1 class="user-detail-border-box">
      <div class="user-detail-form">
        <h2 class="form-title">编辑用户车辆详情</h2>
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
</template>

<script>
import Vue from 'vue'
import DataV from '@jiaminghi/data-view'
import axios from 'axios'

Vue.use(DataV)

export default {
  data() {
    return {
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
    const username = localStorage.getItem('username');
    
    // 参数验证
    if (!username) {
      alert('用户未登录，请先登录');
      this.$router.push('/login');
      return;
    }

    // 获取车辆详情
    this.fetchCarDetail();
  },
  methods: {
    fetchCarDetail() {
      // 从localStorage获取用户名（登录信息存储在此处）
      const username = localStorage.getItem('username');

      // 参数验证
      if (!username) {
        alert('用户未登录，请先登录');
        this.$router.push('/login');
        return;
      }

      // 发送请求到新的if-user-car-detail接口
      axios.post('http://localhost:8000/myApp/if-user-car-detail/', {
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
      });
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

      if (!this.userId || !this.carId) {
        alert('用户ID或车辆ID不存在，请重新登录');
        this.$router.push('/login');
        return;
      }

      // 发送更新请求到后端API
      axios.post('http://localhost:8000/myApp/save-user-car-detail/', {
        carId: this.carId,
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
.user-detail-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #0f172a;
}

.user-detail-border-box {
  width: 500px;
  padding: 10px;
}

.user-detail-form {
  width: 100%;
  padding: 30px;
}

.form-title {
  color: white;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

textarea {
  height: 100px;
  resize: vertical;
}

.submit-btn {
  width: 100%;
  padding: 30px;
  background-color: #165dff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.submit-btn:hover {
  background-color: #0e4cca;
}

.search-input-container {
  position: relative;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #1e293b;
  border: 1px solid #334155;
  border-radius: 0 0 4px 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.search-results div {
  padding: 8px;
  cursor: pointer;
  color: white;
}

.search-results div:hover {
  background-color: #334155;
}
</style>