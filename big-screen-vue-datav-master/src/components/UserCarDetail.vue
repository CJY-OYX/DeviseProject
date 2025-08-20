<template>
  <div class="info-card">
    <dv-border-box-12 class="info-card-border">
      <h3 class="info-title" style="text-align: center;">用户车辆详情</h3>
      <div v-if="userCarDetail" class="data-container">
          <div class="data-item" v-for="(value, key) in userCarDetail" :key="key">
            <span class="data-label">{{ formatKey(key) }}:</span>
            <span class="data-value">{{ value }}</span>
          </div>
        </div>
      <div v-else class="no-data">
        <p>加载用户车辆详情中...</p>
      </div>
    </dv-border-box-12>
  </div>
</template>

<script>
export default {
  props: {
    userCarDetail: {
      type: Object,
      default: null
    }
  },
  methods: {
    formatKey(key) {
      // 将蛇形命名转换为驼峰命名并首字母大写
      return key.replace(/([A-Z])/g, ' $1')
                .replace(/^./, function(str) { return str.toUpperCase(); })
                .replace(/_/g, ' ');
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/user-car-detail.scss';
</style>