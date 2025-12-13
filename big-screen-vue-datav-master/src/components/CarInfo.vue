<template>
  <div class="info-card">
    <dv-border-box-11 title="详细参数" class="info-card-border">
      <div v-if="carInfo" class="data-container">
        <!-- 基础参数区域 -->
        <div class="section-title">
          <dv-decoration-3 style="width:200px;height:30px;" />
          <span>基础参数</span>
        </div>
        <div class="info-grid">
          <div class="info-item" v-for="(value, key) in filteredCarInfo" :key="key">
            <div class="item-label">{{ formatKey(key) }}</div>
            <div class="item-value">{{ value }}</div>
            <div class="item-bg"></div>
          </div>
        </div>

        <!-- 配置详情区域 -->
        <div class="section-title" v-if="hasConfig">
          <dv-decoration-3 style="width:200px;height:30px;" />
          <span>车辆配置</span>
        </div>
        <div class="config-grid" v-if="hasConfig">
           <div class="config-item" v-for="(value, key) in parsedConfiguration" :key="key">
             <div class="config-label">{{ key }}</div>
             <div class="config-value">{{ value }}</div>
           </div>
        </div>
      </div>
      
      <div v-else class="no-data">
        <dv-loading>加载车辆信息中...</dv-loading>
      </div>
    </dv-border-box-11>
  </div>
</template>

<script>
export default {
  props: {
    carInfo: {
      type: Object,
      default: null
    },
    userCarDetail: {
      type: Object,
      default: null
    }
  },
  computed: {
    filteredCarInfo() {
      // 过滤掉carImg和carName字段
      if (!this.carInfo) return {}
      // eslint-disable-next-line no-unused-vars
      const { carImg, carName, id, price, newprice, ...rest } = this.carInfo
      return rest
    },
    parsedConfiguration() {
      // 解析配置信息（TextField可能存储JSON字符串或普通字符串）
      if (!this.userCarDetail || !this.userCarDetail.configuration) return {}
      try {
        // 尝试将字符串解析为JSON对象
        if (typeof this.userCarDetail.configuration === 'string') {
          // 检查是否为有效的JSON
          if (this.userCarDetail.configuration.trim().startsWith('{') && this.userCarDetail.configuration.trim().endsWith('}')) {
            return JSON.parse(this.userCarDetail.configuration)
          } else {
            // 不是JSON格式，直接作为配置值返回
            return { '配置信息': this.userCarDetail.configuration }
          }
        } else {
          return this.userCarDetail.configuration
        }
      } catch (e) {
        console.error('解析配置信息失败:', e)
        // 解析失败时，将原始字符串作为配置值返回
        return { '配置信息': this.userCarDetail.configuration }
      }
    },
    hasConfig() {
      return Object.keys(this.parsedConfiguration).length > 0;
    }
  },
  methods: {
    formatKey(key) {
      // 确保key是字符串类型
      key = String(key);
      
      // 字段名到注释的映射
      const fieldComments = {
        'brand': '品牌',
        'saleVolume': '销量',
        'manufacturer': '厂商',
        'carModel': '车型',
        'energyType': '能源类型',
        'marketTime': '上市时间',
        'insure': '保修时间',
        'creteTime': '创建时间',
        'rank':'排名'
      };

      // 如果字段名在映射中存在，则返回对应的注释
      if (Object.prototype.hasOwnProperty.call(fieldComments, key)) {
        return fieldComments[key];
      }

      // 否则，使用默认的格式化方式
      return key.replace(/([A-Z])/g, ' $1')
                .replace(/^./, function(str) { return str.toUpperCase(); })
                .replace(/_/g, ' ');
    }
  }
}
</script>

<style lang="scss" scoped>
.info-card {
  width: 100%;
  height: 100%;
  // padding: 20px;
}

.info-card-border {
  width: 100%;
  height: 100%;
  padding: 60px 20px 20px 20px; // 留出标题空间
  box-sizing: border-box;
}

.data-container {
  height: 100%;
  overflow-y: auto;
  padding-right: 10px;
  
  /* Scrollbar styling */
  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(0, 209, 255, 0.3);
    border-radius: 3px;
  }
  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
  }
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
  
  span {
    position: absolute;
    left: 20px;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    text-shadow: 0 0 10px #00d1ff;
  }
}

/* 基础参数网格布局 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.info-item {
  position: relative;
  background: rgba(6, 30, 93, 0.4);
  border: 1px solid rgba(0, 209, 255, 0.2);
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 4px;
  transition: all 0.3s;
  
  &:hover {
    background: rgba(6, 30, 93, 0.7);
    border-color: rgba(0, 209, 255, 0.6);
    box-shadow: 0 0 15px rgba(0, 209, 255, 0.2);
    
    .item-label {
      color: #fff;
    }
  }
  
  .item-label {
    color: #8cc5ff;
    font-size: 16px;
    font-weight: 500;
  }
  
  .item-value {
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    text-align: right;
  }
  
  // 装饰角
  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 10px; height: 10px;
    border-top: 2px solid #00d1ff;
    border-left: 2px solid #00d1ff;
  }
  &::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 10px; height: 10px;
    border-bottom: 2px solid #00d1ff;
    border-right: 2px solid #00d1ff;
  }
}

/* 配置详情网格布局 */
.config-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.config-item {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px 20px;
  border-radius: 4px;
  display: flex;
  align-items: flex-start;
  border-left: 3px solid #409EFF;
  
  .config-label {
    min-width: 150px;
    color: #409EFF;
    font-size: 16px;
    font-weight: bold;
    margin-right: 20px;
  }
  
  .config-value {
    color: #eee;
    font-size: 16px;
    line-height: 1.5;
    flex: 1;
  }
}

.no-data {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}
</style>