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
          <li v-for="(car, index) in carData" :key="index + '-' + car.rank" @click="openModal(car)" style="cursor:pointer">
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
      <!-- 详情浮窗 -->
      <div v-if="showModal" class="custom-modal-container">
        <div class="custom-modal-overlay" @click="closeModal">
          <div class="custom-modal" @click.stop>
            <div class="custom-modal-header">
              <h3 class="custom-modal-title">车型详情</h3>
            </div>
            <div class="custom-modal-body">
              <div style="display:flex; gap:16px; align-items:center; justify-content:center;">
                <img :src="selectedCar.carImg" alt="car" style="width:120px;height:80px;object-fit:cover;border-radius:8px;" />
                <div style="text-align:left">
                  <p><strong>{{ selectedCar.carName }}</strong></p>
                  <p style="font-size:13px;color:#94a3b8;">{{ selectedCar.manufacturer }} / {{ selectedCar.brand }}</p>
                </div>
              </div>
              <div style="margin-top:12px;text-align:left">
                <p>指导价：<strong>{{ selectedCar.price }} 万元</strong></p>
                <p>销量：<strong>{{ selectedCar.saleVolume }} 辆</strong></p>
                <p>排名：<strong>{{ selectedCar.rank }}</strong></p>
                <p>能源类型：<strong>{{ selectedCar.energyType }}</strong></p>
                <p>上市时间：<strong>{{ selectedCar.marketTime }}</strong></p>
                <p>保修时间：<strong>{{ selectedCar.insure }}</strong></p>
              </div>
            </div>
            <div class="custom-modal-footer">
              <button class="custom-modal-cancel-btn" @click="closeModal">关闭</button>
              <button class="custom-modal-confirm-btn" @click="closeModal">知道了</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data(){
    return{
      carData:[],
      showModal: false,
      selectedCar: {}
    }
  },
  components: {},
  async mounted() {
    const res = await this.$http.get('myApp/bottomRight')
    const list = res && res.data && Array.isArray(res.data.carData) ? res.data.carData : []
    if (list.length > 0) {
      this.carData = list
    }
  },
  methods: {
    openModal(car) {
      this.selectedCar = car || {}
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.selectedCar = {}
    }
  }
};
</script>

<style lang="scss" scoped>
@import '../assets/scss/bottomRight.scss';
</style>