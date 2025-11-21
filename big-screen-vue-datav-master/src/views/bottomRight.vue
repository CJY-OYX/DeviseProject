<template>
  <div id="bottomRight">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="chart-area" class="text-icon"></icon>
        </span>
        <div class="d-flex">
          <span class="fs-xl text mx-2"><h1 style="font-size: 27px">汽车排行榜</h1></span>
          <div class="decoration2">
            <dv-decoration-2 :reverse="true" style="width:5px;height:6rem;" />
          </div>
        </div>
      </div>
      <div class="row_list">
        <ul class="car_rank" style="width: 100%;height: 420px;overflow: auto">
          <li style="font-size: 23px">
            <div>销售排名</div>
            <div>图片</div>
            <div>汽车信息</div>
            <div>销售价格</div>
            <div>销售趋势</div>
            <div>保修时间</div>
            <div>上市时间</div>
          </li>
          <li v-for="(car, index) in carData" v-bind:key="index + '-' + car.rank">
            <div>{{ car.rank }}</div>
            <div class="list_img"><img :src="car.carImg" style="height: 100%;width: 100%" alt=""></div>
            <div class="list_info">
              <p>{{ car.carName }}</p>
              <p>{{ car.manufacturer }}/{{ car.brand }}</p>
            </div>
            <div class="list_price">{{ car.price }}万元</div>
            <div class="list_volume">{{ car.saleVolume }}辆</div>
            <div class="list_insure">{{ car.insure }}</div>
            <div class="list_market">{{ car.marketTime }}</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data(){
    return{
      carData:[]
    }
  },
  components: {},
  async mounted() {
    const res = await this.$http.get('myApp/bottomRight')
    const list = res && res.data && Array.isArray(res.data.carData) ? res.data.carData : []
    if (list.length > 0) {
      this.carData = list
    }
  }
};
</script>

<style lang="scss" scoped>
@import '../assets/scss/bottomRight.scss';
</style>