<template>
  <transition name="modal-fade">
    <div v-show="visible" class="user-detail-modal-overlay" @click="handleOverlayClick">
      <div class="user-detail-modal-content" @click.stop>
        <button class="modal-close" @click="close">
          <span class="close-icon">×</span>
        </button>
        <h2 class="modal-title">我的车辆详情</h2>
        
        <div class="modal-body-content">
             <dv-loading v-if="loading">Loading...</dv-loading>
             <div v-else class="detail-grid">
                <!-- 左侧栏：图片和基础指标 -->
                <div class="left-panel">
                  <div class="panel-item car-img-box">
                    <CarImg :carInfo="safeCarInfo" />
                  </div>
                  <div class="metrics-row">
                    <div class="metric-item">
                      <NumInfo :carInfo="safeCarInfo" />
                    </div>
                    <div class="metric-item">
                       <UserCarInfo :userCarDetail="safeUserCarDetail" />
                    </div>
                  </div>
                  <div class="panel-item">
                    <CarTimers :carDetail="safeUserCarDetail" :carInfo="safeCarInfo" />
                  </div>
                </div>

                <!-- 右侧栏：价值分析和详细参数 -->
                <div class="right-panel">
                  <div class="panel-item">
                    <UserCarDetail :userCarDetail="safeUserCarDetail" />
                  </div>
                  <div class="panel-item flex-grow">
                    <CarInfo :carInfo="safeCarInfo" :userCarDetail="safeUserCarDetail"/>
                  </div>
                </div>
             </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
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
  name: 'UserDetailModal',
  components: {
    CarImg,
    CarInfo,
    NumInfo,
    UserCarInfo,
    UserCarDetail,
    CarTimers
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      loading: false,
      userInfo: null,
      carInfo: null,
      userCarDetail: null,
      username: localStorage.getItem('username') || ''
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
  watch: {
    visible(val) {
      if (val) {
        this.moveToBody();
        this.username = localStorage.getItem('username') || '';
        this.fetchUserData();
      } else {
        this.removeFromBody();
      }
    }
  },
  methods: {
    close() {
      this.$emit('update:visible', false);
    },
    handleOverlayClick() {
      this.close();
    },
    moveToBody() {
      if (this.$el && this.$el.parentNode !== document.body) {
        document.body.appendChild(this.$el);
      }
    },
    removeFromBody() {
      if (this.$el && this.$el.parentNode === document.body) {
        this.$el.parentNode.removeChild(this.$el);
      }
    },
    fetchUserData() {
      if (!this.username) {
        this.loading = false;
        return;
      }
      this.loading = true;
      axios.post('http://localhost:8000/myApp/entry-user-info/', { username: this.username })
        .then(res => {
          if (res.data && res.data.success) {
            this.userInfo = res.data.userinfo || null;
            this.userCarDetail = res.data.usercarinfo || null;
            this.carInfo = res.data.data || null;
          }
        })
        .catch(err => {
          console.error('获取用户数据失败:', err);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  beforeDestroy() {
    this.removeFromBody();
  }
}
</script>

<style lang="scss" scoped>
.user-detail-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.user-detail-modal-content {
  position: relative;
  width: 1500px;
  max-width: 95vw;
  height: 90vh;
  background: rgba(13, 20, 40, 0.95);
  border: 1px solid rgba(0, 209, 255, 0.3);
  box-shadow: 0 0 40px rgba(0, 209, 255, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 4px;
  
  /* Tech corners */
  &::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 30px; height: 30px;
    border-top: 3px solid #00d1ff;
    border-left: 3px solid #00d1ff;
    z-index: 1;
  }
  &::after {
    content: '';
    position: absolute;
    bottom: -1px; right: -1px;
    width: 30px; height: 30px;
    border-bottom: 3px solid #00d1ff;
    border-right: 3px solid #00d1ff;
    z-index: 1;
  }
}

.modal-close {
  position: absolute;
  top: 20px;
  right: 25px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 32px;
  line-height: 1;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s;
  
  &:hover {
    color: #00d1ff;
    transform: rotate(90deg);
  }
}

.modal-title {
  text-align: center;
  color: #fff;
  font-size: 28px;
  margin: 25px 0;
  letter-spacing: 2px;
  text-shadow: 0 0 15px rgba(0, 209, 255, 0.6);
  flex-shrink: 0;
  font-weight: bold;
}

.modal-body-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 30px 30px 30px;
  
  /* Scrollbar styling */
  &::-webkit-scrollbar {
    width: 8px;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(0, 209, 255, 0.4);
    border-radius: 4px;
  }
  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
  }
}

.detail-grid {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 25px;
  padding-bottom: 20px;
}

.left-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

.metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  
  .metric-item {
    overflow: hidden;
  }
}

/* Modal Fade Transition */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
  .user-detail-modal-content {
    transition: transform 0.3s ease;
  }
}
.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
  .user-detail-modal-content {
    transform: scale(0.95);
  }
}

/* Responsive */
@media (max-width: 1400px) {
  .detail-grid {
    grid-template-columns: 350px 1fr;
  }
}

@media (max-width: 1100px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .left-panel {
    flex-direction: row;
    flex-wrap: wrap;
    
    .car-img-box {
      width: 100%;
    }
    .metrics-row {
      flex: 1;
      min-width: 300px;
    }
    .panel-item {
      flex: 1;
    }
  }
}
</style>