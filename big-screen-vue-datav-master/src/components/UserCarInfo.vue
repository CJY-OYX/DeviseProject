<template>
  <div class="digital-flop-container">
    <dv-border-box-1 class="dv-border-box">
      <div class="title"><span>已行驶公里数</span></div>
      <dv-digital-flop :config="config" style="width:auto;height:100px;" />
    </dv-border-box-1>
  </div>
</template>

<script>
export default {
  props: {
    userCarDetail: { type: Object, default: null }
  },
  data() {
    return {
      config: {
        number: [0],
        content: '{nt}公里',
        style: { color: '#2ecc71' }
      }
    };
  },
  watch: {
    'userCarDetail.mileage': {
      immediate: true,   // 第一次拿到值也触发
      handler(val) {
        const km = Number(val || 0);
        this.config = {
          ...this.config,
          number: [km]
        };
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.digital-flop-container {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.dv-border-box {
  height: 150px;
  align-items: center;
  .title {
  width: 100%;
  height: 30px;
  font-size: 30px;
  font-weight: bold;
  text-align: center;
}
}

</style>