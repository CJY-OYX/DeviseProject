<template>
  <div class="info-card">
    <dv-border-box-6 class="info-card-border">
      <!-- <h3 class="info-title" style="text-align: center;">车辆详细信息</h3> -->
      <div v-if="carInfo" class="data-container">
          <div class="data-item" v-for="(value, key) in filteredCarInfo" :key="key">
            <span class="data-label">{{ formatKey(key) }}:</span>
            <span class="data-value">{{ value }}</span>
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
    }
  },
  computed: {
    filteredCarInfo() {
      // 过滤掉carImg和carName字段
      if (!this.carInfo) return {}
      // eslint-disable-next-line no-unused-vars
      const { carImg, carName, id, price,rank, ...rest } = this.carInfo
      return rest
    }
  },
  methods: {
    formatKey(key) {
      // 字段名到注释的映射
      const fieldComments = {
        'brand': '品牌',
        'carName': '车名',
        'carImg': '图片链接',
        'saleVolume': '销量',
        'price': '价格',
        'manufacturer': '厂商',
        'rank': '排名',
        'carModel': '车型',
        'energyType': '能源类型',
        'marketTime': '上市时间',
        'insure': '保修时间',
        'creteTime': '创建时间'
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
</style>