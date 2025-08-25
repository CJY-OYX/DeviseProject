<template>
  <div class="info-card">
    <dv-border-box-4 :reverse="true" class="info-card-border">
      <div class="final-result">
        <span class="final-label">
          车辆当前价值:
          <span class="final-value">￥{{ currentValue.toFixed(2) }} 万元</span>
        </span>
      </div>

      <dv-decoration-8 style="width:95%;height:50px;" />
      <div class="calc-row">
        <div class="flip-item">
          <span class="label">新车指导价</span>
          <dv-digital-flop :config="guidePriceFlop" />
        </div>
        <div class="flip-item">
          <span class="label">使用年数</span>
          <dv-digital-flop :config="yearsFlop" />
        </div>
        <div class="flip-item">
          <span class="label">年折旧率</span>
          <dv-digital-flop :config="rateFlop" />
        </div>
        <div class="flip-item">
          <span class="label">折旧后价值</span>
          <dv-digital-flop :config="afterDeprFlop" />
        </div>
        <div class="flip-item">
          <span class="label">里程折旧</span>
          <dv-digital-flop :config="mileageFlop" />
        </div>
        <div class="flip-item">
          <span class="label">市场折价</span>
          <dv-digital-flop :config="marketFlop" />
        </div>
      </div>
    </dv-border-box-4>
  </div>
</template>

<script>
export default {
  name: 'UserCarDetail',
  props: {
    userCarDetail: { type: Object, default: null }
  },
  data() {
    return {
      annualDepreciationRate: 0.095,
      mileageDepreciation: 0.2,
      marketAdjustment: 0.5,

      guidePriceFlop: null,
      yearsFlop: null,
      rateFlop: null,
      afterDeprFlop: null,
      mileageFlop: null,
      marketFlop: null
    };
  },
  computed: {
    newCarPrice() {
      const range = this.userCarDetail?.priceRange || [6.78, 11.38];
      return (range[0] + range[1]) / 2;
    },
    yearsOfUse() {
      const buy = this.userCarDetail?.purchaseDate
        ? new Date(this.userCarDetail.purchaseDate)
        : new Date('2021-01-15');
      return (Date.now() - buy) / (365 * 24 * 3600 * 1000);
    },
    depreciationValue() {
      return this.newCarPrice * (1 - this.annualDepreciationRate * this.yearsOfUse);
    },
    currentValue() {
      return this.depreciationValue - this.mileageDepreciation - this.marketAdjustment;
    }
  },
  watch: {
    userCarDetail: {
      deep: true,
      handler(nv) {
        console.log('UserCarDetail watch 触发，userCarDetail =', nv);
        this.updateFlopConfigs();
      }
    }
  },
  created() {
    console.log('UserCarDetail created, userCarDetail =', this.userCarDetail);
    this.updateFlopConfigs();
  },
  methods: {
    buildFlop(num, toFixed, suffix) {
      return {
        number: [Number(Number(num).toFixed(toFixed))],
        content: `{nt}${suffix}`,
        style: { fontSize: 32, fill: '#2ecc71', fontWeight: 'bold' }
      };
    },
    updateFlopConfigs() {
      // Data-V 2.x 必须深拷贝才能刷新
      this.guidePriceFlop = JSON.parse(
        JSON.stringify(this.buildFlop(this.newCarPrice, 2, '万元'))
      );
      this.yearsFlop = JSON.parse(
        JSON.stringify(this.buildFlop(this.yearsOfUse, 2, '年'))
      );
      this.rateFlop = JSON.parse(
        JSON.stringify(this.buildFlop(this.annualDepreciationRate * 100, 1, '%'))
      );
      this.afterDeprFlop = JSON.parse(
        JSON.stringify(this.buildFlop(this.depreciationValue, 2, '万元'))
      );
      this.mileageFlop = JSON.parse(
        JSON.stringify(this.buildFlop(this.mileageDepreciation, 2, '万元'))
      );
      this.marketFlop = JSON.parse(
        JSON.stringify(this.buildFlop(this.marketAdjustment, 2, '万元'))
      );
    }
  },
  mounted() {
  console.log('UserCarDetail mounted, userCarDetail =', this.userCarDetail);
}
};
</script>

<style lang="scss" scoped>
.info-card-border {
  height: 300px;
}
.calc-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin: 20px 0;
}
.flip-item {
  width: 80%;
  height: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .label {
    font-size: 18px;
    color: #fff;
    margin-bottom: 1px;
  }
}
.final-result {
  height: 100px;
  padding-top: 60px;
  text-align: center;
  margin-top: 30px;
  .final-label {
    display: block;
    font-size: 30px;
    color: #fff;
    margin-bottom: 10px;
    padding-left: 20px;
  }
  .final-value {
    font-size: 90px;
    color: #fee83d;
    font-weight: bold;
  }
}
</style>
