<template>
  <div class="car-timers-container">
    <!-- 购买时间 -->
    <div class="timer-item">
      <dv-border-box-10 class="dv-10">
      <div class="timer-title">车辆购买时间</div>
      <dv-decoration-7 class="dv-7">
        <span class="static-text">&nbsp;&nbsp;{{ carDetail.purchaseDate || '----' }}&nbsp;&nbsp;</span>
      </dv-decoration-7>
      </dv-border-box-10>
    </div>

    <!-- 拥有车辆时间（静态文本） -->
    <div class="timer-item">
      <dv-border-box-10 class="dv-10">
      <div class="timer-title">拥有车辆时间</div>
      <dv-decoration-7 class="dv-7">
        <span class="static-text">&nbsp;&nbsp;{{ ownTimeText }}&nbsp;&nbsp;</span>
      </dv-decoration-7>
      </dv-border-box-10>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CarTimers',
  props: {
    carDetail: { type: Object, required: true }
  },
  computed: {
    ownTimeText() {
      const buy = new Date(this.carDetail?.purchaseDate || Date.now());
      const diff = Date.now() - buy;
      const totalDays = Math.floor(diff / 86400000);
      return `${totalDays}天`;
    }
  }
};
</script>

<style lang="scss" scoped>
.car-timers-container { 
  padding: 10px;
  height: 170px; 
}
.timer-item { 
  // padding: 15px;
  margin-bottom: 15px; 
  // height: 170px;
}
.dv-10 {
  padding: 10px;
}
.timer-title {
  font-size: 30px;
  font-weight: bold;
  color: #fff;
  padding-top: 25px;
  margin-bottom: 10px;
  text-align: center;
}
.static-text {
  font-size: 35px;
  color: #2ecc71;
  display: block;
  line-height: 1;
  padding: 15px;
  // margin-top: 15px;
}
</style>
