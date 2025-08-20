<template>
  <div class="digital-flop-container">
    <dv-border-box-11 class="dv-border-box" title="购车指导价">
      <div>
      <dv-digital-flop :config="config" style="width:auto;height:200px;" />
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
    }
  },
  data() {
    return {
      sum: 0,
      config: {
        number: [this.carInfo.newprice[0]],
        // digitHeight: 30,
        // digitWidth: 20,
        toFixed: 2,
        content: '{nt}万',
        style: {
          color: '#2ecc71',
          // backgroundColor: 'transparent'
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
    // power(){
    //   if(this.sum == 0){
    //     this.sum = 1;
    //   }
    //   else{
    //   this.sum = 0
    //   }
    //   this.config.number = [this.carInfo.newprice[this.sum]];
    // }
    power() {
    this.sum = this.sum ? 0 : 1;
    const raw = this.carInfo?.newprice?.[this.sum];
    const val = Number(raw);                       // 转数字
    this.config = {
      ...this.config,
      number: isNaN(val) ? [0] : [val]             // 永远是非空 [number]
    };
    console.log('赋值后 number:', this.config.number);
  }
  }
}
</script>

<style lang="scss" scoped>
.digital-flop-container {
  margin-top: 10px;
  // width: 300px;
  // height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}
.dv-border-box {
  height: 150px;
  align-items: center;
}
</style>