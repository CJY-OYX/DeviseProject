<template>
  <transition name="modal-fade">
    <div v-show="visible" class="edit-modal-overlay" @click="handleOverlayClick">
      <div class="edit-modal-content" @click.stop>
        <!-- 关闭按钮 -->
        <button class="modal-close" @click="close">
          <span class="close-icon">×</span>
        </button>

        <h2 class="modal-title">编辑车辆信息</h2>

        <div class="edit-body">
          <!-- 左侧预览 -->
          <div class="left-preview">
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

          <!-- 右侧表单 -->
          <div class="right-form">
            <div class="form-group">
              <label for="edit-carName">车辆名字</label>
              <div class="search-input-container">
                <input type="text" id="edit-carName" v-model="carName" @input="searchCars" placeholder="请输入车辆名字">
                <div class="search-results" v-if="searchResults.length > 0">
                  <div v-for="car in searchResults" :key="car.id" @click="selectCar(car)">{{ car.carName }} ({{ car.carModel }})</div>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label for="edit-carModel">车辆型号</label>
              <input type="text" id="edit-carModel" v-model="carModel" placeholder="请输入车辆型号">
            </div>
            <div class="form-group">
              <label for="edit-mileage">车辆公里数</label>
              <input type="number" id="edit-mileage" v-model="mileage" placeholder="请输入车辆公里数">
            </div>
            <div class="form-group">
              <label for="edit-purchaseDate">车辆购买时间</label>
              <input type="date" id="edit-purchaseDate" v-model="purchaseDate">
            </div>
            <div class="form-group">
              <label for="edit-configuration">车辆配置</label>
              <textarea id="edit-configuration" v-model="configuration" placeholder="请输入车辆配置"></textarea>
            </div>
            <button class="submit-btn" @click="submitForm" :disabled="isSubmitting">
              {{ isSubmitting ? '更新中...' : '更新信息' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EditModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      username: '',
      userId: null,
      carId: null,
      carName: '',
      carModel: '',
      mileage: 0,
      purchaseDate: '',
      configuration: '',
      searchResults: [],
      carImageUrl: '',
      isSubmitting: false
    }
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        this.username = localStorage.getItem('username') || ''
        this.fetchCarDetail()
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.moveToBody()
    })
  },
  beforeDestroy() {
    this.removeFromBody()
  },
  methods: {
    close() {
      this.$emit('update:visible', false)
    },
    handleOverlayClick() {
      this.close()
    },
    moveToBody() {
      const element = this.$el
      if (element && element.parentElement !== document.body) {
        document.body.appendChild(element)
      }
    },
    removeFromBody() {
      const element = this.$el
      if (element && element.parentElement === document.body) {
        document.body.removeChild(element)
      }
    },
    fetchCarDetail() {
      if (!this.username) return

      axios.post('http://localhost:8000/myApp/if_user_car_detail/', {
        username: this.username
      })
      .then(response => {
        if (response.data.success) {
          this.userId = response.data.userid;
          this.carId = response.data.user_car_detail.car_id;

          const carData = response.data.car_data;
          if (carData) {
            this.carName = carData.carName || carData.car_name;
            this.carModel = carData.carModel || carData.car_model;
            this.carImageUrl = carData.carImg || '';
          }

          const userCarData = response.data.user_car_detail;
          if (userCarData) {
            this.mileage = userCarData.mileage;
            this.purchaseDate = userCarData.purchase_date || userCarData.purchaseDate;
            this.configuration = userCarData.configuration;
          }
        }
      })
      .catch(error => {
        console.error('获取车辆信息失败:', error)
      })
    },
    searchCars() {
      if (this.carName.length < 1) {
        this.searchResults = [];
        return;
      }
      axios.post('http://localhost:8000/myApp/search_cars/', {
        query: this.carName
      })
      .then(response => {
        this.searchResults = response.data.results;
      })
      .catch(error => {
        console.error('搜索车辆失败:', error);
      });
    },
    selectCar(car) {
      this.carId = car.id;
      this.carName = car.carName;
      this.carModel = car.carModel;
      this.carImageUrl = car.carImg;
      this.searchResults = [];
    },
    submitForm() {
      if (this.isSubmitting) return
      this.isSubmitting = true

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
          this.$emit('edit-success')
          this.close()
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.error('更新车辆详情失败:', error);
        alert('更新车辆详情失败，请重试');
      })
      .finally(() => {
        this.isSubmitting = false
      });
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
  .edit-modal-content {
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.27);
  }
}
.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
  .edit-modal-content {
    transform: scale(0.9) translateY(20px);
  }
}

.edit-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.edit-modal-content {
  position: relative;
  width: 900px;
  max-width: 95vw;
  background: rgba(13, 20, 40, 0.98);
  border: 1px solid rgba(64, 158, 255, 0.3);
  box-shadow: 0 0 30px rgba(64, 158, 255, 0.2);
  border-radius: 8px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  
  // 科技感边角
  &::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 20px; height: 20px;
    border-top: 2px solid #00d1ff;
    border-left: 2px solid #00d1ff;
    border-radius: 4px 0 0 0;
  }
  &::after {
    content: '';
    position: absolute;
    bottom: -1px; right: -1px;
    width: 20px; height: 20px;
    border-bottom: 2px solid #00d1ff;
    border-right: 2px solid #00d1ff;
    border-radius: 0 0 4px 0;
  }
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 24px;
  cursor: pointer;
  line-height: 1;
  transition: color 0.3s;
  z-index: 10;
  
  &:hover {
    color: #ef4444;
  }
}

.modal-title {
  text-align: center;
  color: #fff;
  font-size: 24px;
  margin-bottom: 30px;
  font-weight: 600;
  letter-spacing: 2px;
  text-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
}

.edit-body {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  
  .left-preview {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);

    .preview-media {
      width: 100%;
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 15px;
      
      .car-image {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        border-radius: 4px;
      }
      
      .car-silhouette {
        width: 80%;
        fill: #2a3a5a;
      }
    }
    
    .preview-name {
      color: #00d1ff;
      font-size: 18px;
      font-weight: bold;
      text-align: center;
    }
  }
  
  .right-form {
    flex: 1.5;
  }
}

.form-group {
  margin-bottom: 15px;
  
  label {
    display: block;
    color: #94a3b8;
    margin-bottom: 8px;
    font-size: 14px;
  }
}

input, textarea {
  width: 100%;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
  transition: all 0.3s;
  box-sizing: border-box;
  
  &:focus {
    outline: none;
    border-color: #00d1ff;
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 10px rgba(0, 209, 255, 0.2);
  }
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }
}

textarea {
  height: 80px;
  resize: vertical;
}

.search-input-container {
  position: relative;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #0f172a;
  border: 1px solid #334155;
  border-radius: 0 0 4px 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 20;

  div {
    padding: 10px;
    cursor: pointer;
    color: #cbd5e1;
    font-size: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);

    &:hover {
      background-color: #1e293b;
      color: #fff;
    }
    
    &:last-child {
      border-bottom: none;
    }
  }
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(90deg, #00d1ff, #0099ff);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 10px;
  letter-spacing: 2px;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 209, 255, 0.4);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}
</style>
