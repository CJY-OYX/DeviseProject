<template>
  <transition name="modal-fade">
    <div v-show="visible" class="car-rank-modal-overlay" @click="handleOverlayClick">
      <div class="car-rank-modal-content" @click.stop>
        <!-- 装饰性边角 -->
        <div class="corner top-left"></div>
        <div class="corner top-right"></div>
        <div class="corner bottom-left"></div>
        <div class="corner bottom-right"></div>

        <!-- 关闭按钮 (绝对定位) -->
        <button class="car-rank-modal-close" @click="close">
          <span class="close-icon">×</span>
        </button>

        <!-- 车辆图片区域 -->
        <div class="car-image-wrapper">
          <div class="image-overlay"></div>
          <img :src="car.carImg" :alt="car.carName" class="car-image" />
        </div>

        <div class="car-rank-modal-body">
          <div class="car-info-header">
            <div class="car-title">
              <span class="rank-number">NO.{{ car.rank }}</span>
              {{ car.carName }}
            </div>
          </div>
          
          <div class="divider"></div>

          <div class="car-details">
            <div class="detail-item highlight">
              <span class="value">{{ car.manufacturer }}</span>
            </div>
            <div class="detail-item highlight">
              <span class="value">{{ car.price }} <span class="unit">万</span></span>
            </div>
            <div class="detail-item highlight">
              <span class="value">{{ car.saleVolume }} <span class="unit">辆</span></span>
            </div>
            <!-- 可以根据需要添加更多字段 -->
          </div>
        </div>
        
        <div class="modal-footer-decoration">
          <span></span><span></span><span></span><span></span>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'CarRankModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    car: {
      type: Object,
      default: () => ({})
    }
  },
  watch: {
    // visible 变化时不需要再移动DOM，因为mounted时已经移动了
  },
  mounted() {
    console.log('CarRankModal mounted - Size updated to 520x780')
    // 确保组件挂载后立即移动到body，避免受父级transform缩放影响
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
    }
  }
}
</script>

<style lang="scss" scoped>
// 动画定义
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
  .car-rank-modal-content {
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.27);
  }
}
.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
  .car-rank-modal-content {
    transform: scale(0.9) translateY(10px);
  }
}

.car-rank-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.car-rank-modal-content {
  position: relative;
  // 深色科技感背景
  background: rgba(13, 20, 40, 0.95);
  // 使用 drop-shadow 替代 box-shadow 以适应 clip-path
  filter: drop-shadow(0 0 15px rgba(64, 158, 255, 0.3));
  width: 320px !important;
  height: 480px !important;
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  
  // 切角效果
  clip-path: polygon(
    0 10px, 10px 0, 
    100% 0, 100% calc(100% - 10px), 
    calc(100% - 10px) 100%, 0 100%
  );
  
  // 内部边框效果 (通过伪元素模拟或直接使用border但需注意切角)
  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border: 1px solid rgba(64, 158, 255, 0.5);
    pointer-events: none;
    z-index: 2;
    // 确保边框也被切角
    clip-path: polygon(
      0 10px, 10px 0, 
      100% 0, 100% calc(100% - 10px), 
      calc(100% - 10px) 100%, 0 100%
    );
  }
}

// 角落装饰
.corner {
  position: absolute;
  width: 8px;
  height: 8px;
  border-color: #00d1ff;
  border-style: solid;
  pointer-events: none;
  z-index: 10;
  
  &.top-left {
    top: 0;
    left: 0;
    border-width: 2px 0 0 2px;
  }
  &.top-right {
    top: 0;
    right: 0;
    border-width: 2px 2px 0 0;
  }
  &.bottom-left {
    bottom: 0;
    left: 0;
    border-width: 0 0 2px 2px;
  }
  &.bottom-right {
    bottom: 0;
    right: 0;
    border-width: 0 2px 2px 0;
  }
}

.car-rank-modal-close {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  border: none;
  width: 20px;
  height: 20px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  z-index: 20;
  border-radius: 50%;
  transition: all 0.2s;
  
  &:hover {
    background: #ef4444;
    transform: rotate(90deg);
  }
}

.car-image-wrapper {
  width: 100%;
  height: 200px;
  position: relative;
  overflow: hidden;
  background: #1a233a; // 图片加载前的背景色
}

.car-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.car-image-wrapper:hover .car-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  // 增强底部渐变，使图片与深色背景融合更自然
  background: linear-gradient(to bottom, transparent 50%, rgba(13, 20, 40, 0.8) 90%, rgba(13, 20, 40, 1) 100%);
  z-index: 1;
  pointer-events: none;
}

.car-rank-modal-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 10px 15px;
  position: relative;
  z-index: 3;
}

.car-info-header {
  text-align: center;
  margin-bottom: 8px;
}

.car-title {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.rank-number {
  background: linear-gradient(135deg, #ff4d4d, #f7b733);
  color: white;
  padding: 2px 8px;
  font-size: 14px;
  border-radius: 3px;
  transform: skewX(-10deg);
  display: inline-block;
}

.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(64, 158, 255, 0.3), transparent);
  margin: 4px 0 10px 0;
}

.car-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.03);
  padding: 6px 10px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s;
  
  &:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(0, 209, 255, 0.3);
  }
}

.value {
  color: #00d1ff;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Consolas', monospace;
  
  .unit {
    font-size: 12px;
    color: #94a3b8;
    margin-left: 2px;
    font-weight: normal;
  }
}

.modal-footer-decoration {
  display: flex;
  justify-content: center;
  gap: 4px;
  padding-bottom: 8px;
  opacity: 0.5;
  
  span {
    width: 20px;
    height: 2px;
    background: #409eff;
    border-radius: 1px;
  }
}
</style>