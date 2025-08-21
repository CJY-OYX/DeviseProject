<template>
  <div class="digital-flop-container">
    <dv-border-box-11 class="dv-border-box" title="新车指导价">
      <dv-digital-flop :config="config" style="width:auto;height:200px;" />
    </dv-border-box-11>
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
  data() {
    return {
      sum: 0,
      config: {
        number: [this.carInfo.newprice[0]],
        toFixed: 2,
        content: '{nt}万',
        style: {
          color: '#2ecc71',
        }
      },
    }
  },
  mounted() {
    setInterval( ()=>{
      this.power();
      },5000);
  },
  methods: {
    power() {
    this.sum = this.sum ? 0 : 1;
    const raw = this.carInfo?.newprice?.[this.sum];
    const val = Number(raw);
    this.config = {
      ...this.config,
      number: isNaN(val) ? [0] : [val]
    };
  }
  }
}
</script>

<style lang="scss" scoped>
.digital-flop-container {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size:50px;
}
.dv-border-box {
  // width: auto;
  height: 150px;
  align-items: center;
  font-size: 100px;
}
</style>