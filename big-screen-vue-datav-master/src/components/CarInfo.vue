<template>
  <div class="info-card">
    <dv-border-box-6 class="info-card-border" style="width: 100%; min-width: 600px;">
      <!-- <h3 class="info-title" style="text-align: center;">车辆详细信息</h3> -->
      <div v-if="carInfo" class="data-container">
          <div class="data-item" v-for="(value, key) in mergedCarInfo" :key="key">
              <template v-if="key === 'configSeparator'">
                <div class="configuration-separator">{{ value }}</div>
              </template>
              <template v-else>
                <span class="data-label" :data-config="isConfigField(key)">{{ formatKey(key) }}:</span>
                <span class="data-value">{{ value }}</span>
              </template>
            </div>
        </div>
      <div v-else class="no-data">
        <p>加载车辆信息中...</p>
      </div>
    </dv-border-box-6>
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
    mergedCarInfo() {
      // 合并车辆基本信息和配置信息
      const basicInfo = this.filteredCarInfo
      const configInfo = this.parsedConfiguration
      
      // 添加配置信息的标记
      if (Object.keys(configInfo).length > 0) {
        basicInfo['configSeparator'] = '车辆配置'
        Object.assign(basicInfo, configInfo)
      }
      
      return basicInfo
    }
  },
  methods: {
    isConfigField(key) {
      // 判断是否为配置字段
      const basicFields = Object.keys(this.filteredCarInfo)
      return !basicFields.includes(key) && key !== 'configSeparator'
    },
    formatKey(key) {
      // 确保key是字符串类型
      key = String(key);
      
      // 特殊字段处理
      if (key === 'configSeparator') {
        return ''; // 配置分隔符不需要标签
      }
      
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
@import '../assets/scss/car-info.scss';

.info-card {
  min-width: 600px; /* 增加最小宽度 */
  padding: 20px; /* 增加内边距 */
}

.configuration-separator {
  width: 100%;
  color: #409EFF;
  font-size: 20px; /* 增大分隔符字体 */
  margin: 25px 0 15px; /* 增加间距 */
  padding-top: 20px;
  border-top: 1px solid #409EFF;
  font-weight: bold;
}

.data-label {
  font-size: 20px; /* 增大标签字体大小 */
  margin-right: 30px; /* 增加标签与数据之间的间距 */
  min-width: 180px; /* 固定标签宽度确保对齐 */
  &[data-config="true"] {
    color: #409EFF;
  }
}

.data-value {
  font-size: 20px; /* 增大数据字体大小 */
}

.data-item {
  margin-bottom: 5px; /* 增加项目之间的间距 */
  padding: 10px; /* 增加项目内边距 */
  display: flex; /* 使用flex布局 */
  align-items: center; /* 垂直居中对齐 */
}

.data-container {
  padding: 15px; /* 增加容器内边距 */
}
</style>