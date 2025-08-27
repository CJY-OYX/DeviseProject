<template>
  <div class="user-detail-container">
    <dv-border-box-1 class="user-detail-border-box">
      <div class="user-detail-form">
        <h2 class="form-title">用户车辆详情</h2>
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
        <button class="submit-btn" @click="submitForm">提交</button>
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
      carName: '',
      carModel: '',
      mileage: 0,
      purchaseDate: '',
      configuration: '',
      searchResults: [],
      userId: this.$route.query.userId || null
    }
  },
  methods: {
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

      // 发送表单数据到后端API
      axios.post('http://localhost:8000/myApp/save-user-car-detail/', {
        userId: this.userId,
        carName: this.carName,
        carModel: this.carModel,
        mileage: this.mileage,
        purchaseDate: this.purchaseDate,
        configuration: this.configuration
      })
      .then(response => {
        if (response.data.success) {
          alert('车辆详情保存成功');
          // 可以跳转到其他页面，例如首页
          this.$router.push('/login');
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.error('保存车辆详情失败:', error);
        alert('保存车辆详情失败，请重试');
      });
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/user-detail-form.scss';
</style>