<template>
  <div class="info-card">
    <!-- <dv-border-box-8 class="info-card-border"> -->
      <div v-if="carInfo" class="data-container">
        <div class="car-image-container" v-if="carInfo.carImg">
          <img :src="carInfo.carImg" alt="车辆图片" class="car-image">
        </div>
        <div class="no-image" v-else>
          <p>无车辆图片</p>
        </div>
        <div class="car-name">
            <h1 class="data-value">{{ carInfo.carName }}</h1>
        </div>
      </div>
      <div v-else class="no-data">
        <p>加载车辆信息中...</p>
      </div>
      <dv-decoration-8 style="width:100%;height:50px;" />
    <!-- </dv-border-box-8> -->
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
  watch: {
    carInfo(newVal) {
      console.log('CarInfo数据:', newVal);
      if (newVal) {
        console.log('图片URL:', newVal.carImg);
      }
    }
  },
  mounted() {
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/car-img.scss';
</style>