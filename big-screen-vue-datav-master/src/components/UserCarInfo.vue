<template>
  <div class="digital-flop-container">
    <dv-border-box-1 class="dv-border-box">
      <div class="title"><span>已行驶距离</span></div>
      <dv-digital-flop :config="config" style="width:auto;height:80px;" />
    </dv-border-box-1>
  </div>
</template>

<script>
export default {
  props: {
    userCarDetail: { type: Object, required: true }
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
  mounted() {
    // 1 秒后再显示真实里程
    setTimeout(() => {
      const km = Number(this.userCarDetail?.mileage || 0);
      this.config = {
        ...this.config,
        number: [km]
      };
    }, 1000);   // 需要 5 秒就写 5000
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  .title {
  width: 100%;
  height: 40px;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
}

</style>