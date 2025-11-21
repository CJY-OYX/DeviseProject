<template>
  <div id="center">
    <div class="up">
      <div
        class="bg-color-black item"
      >
        <p class="ml-3 colorBlue fw-b fs-xl">车辆总数据</p>
        <div style="text-align: center;line-height: 2">
          {{this.result.sumCar}}条
        </div>
      </div>
      <div
        class="bg-color-black item"
      >
        <p class="ml-3 colorBlue fw-b fs-xl">销售最多汽车</p>
        <div style="text-align: center;line-height: 2">
          {{this.result.topCar}}
        </div>
      </div>
      <div
        class="bg-color-black item"
      >
        <p class="ml-3 colorBlue fw-b fs-xl">车辆最高销售额</p>
        <div style="text-align: center;line-height: 2">
          {{this.result.highVolume}}辆
        </div>
      </div>
      <div
        class="bg-color-black item"
      >
        <p class="ml-3 colorBlue fw-b fs-xl">销售最多车型</p>
        <div style="text-align: center;line-height: 2">
          {{this.result.mostModel}}
        </div>
      </div>
      <div
        class="bg-color-black item"
      >
        <p class="ml-3 colorBlue fw-b fs-xl">车型最多品牌</p>
        <div style="text-align: center;line-height: 2">
          {{this.result.mostBrand}}
        </div>
      </div>
      <div
        class="bg-color-black item"
      >
        <p class="ml-3 colorBlue fw-b fs-xl">车辆车辆平均价格</p>
        <div style="text-align: center;line-height: 2">
          {{this.result.averagePrice}}万
        </div>
      </div>
    </div>
    <div class="down">
      <div class="ranking bg-color-black">
        <span>
          <icon name="chart-pie" class="text-icon"></icon>
        </span>
        <span class="fs-xl text mx-2 mb-1 pl-3">汽车品牌榜</span>
        <dv-scroll-ranking-board
          class="dv-scr-rank-board mt-1"
          :config="ranking"
          v-bind:key="ranking.data && ranking.data.length ? (ranking.data[0].value || 'default') : 'default'"
        />
      </div>
      <div class="percent">
        <div class="item bg-color-black">
          <span>油车占有率</span>
          <CenterChart
            :id="rate[0].id"
            :tips="rate[0].tips"
            :colorObj="rate[0].colorData"
          />
        </div>
        <div class="item bg-color-black">
          <span>电车占有率</span>
          <CenterChart
            :id="rate[1].id"
            :tips="rate[1].tips"
            :colorObj="rate[1].colorData"
          />
        </div>
        <div class="water" style="text-align: center">
          <p>油电混合比率</p>
          <dv-water-level-pond
            class="dv-wa-le-po"
            :config="water"
            v-bind:key="Array.isArray(water.data) && water.data.length ? String(water.data[0]) : 'default'"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CenterChart from '@/components/echart/center/centerChartRate'

export default {
  data() {
    return {
      result:'',

      ranking: {
        data: [
          {
            'name': '1',
            'value': '1',
          }
        ],
        carousel: 'single',
        unit: ' 款'
      },
      water: {
        data: [24],
        shape: 'round',
        formatter: '{value}%',
        waveNum: 3
      },
      // 通过率和达标率的组件复用数据
      rate: [
        {
          id: 'centerRate1',
          tips: 60,
          colorData: {
            textStyle: '#3fc0fb',
            series: {
              color: ['#00bcd44a', 'transparent'],
              dataColor: {
                normal: '#03a9f4',
                shadowColor: '#97e2f5'
              }
            }
          }
        },
        {
          id: 'centerRate2',
          tips: 40,
          colorData: {
            textStyle: '#67e0e3',
            series: {
              color: ['#faf3a378', 'transparent'],
              dataColor: {
                normal: '#ff9800',
                shadowColor: '#fcebad'
              }
            }
          }
        }
      ]
    }
  },
  components: {
    CenterChart
  },
  async mounted() {
    try {
      const res = await this.$http.get('myApp/center')
      if (res && res.data) {
        this.result = res.data
        if (Array.isArray(res.data.lastSortList) && res.data.lastSortList.length > 0) {
          this.$set(this.ranking, 'data', res.data.lastSortList)
        }
        if (typeof res.data.oilRate === 'number') {
          this.$set(this.rate[0], 'tips', res.data.oilRate)
        }
        if (typeof res.data.electricRare === 'number') {
          this.$set(this.rate[1], 'tips', res.data.electricRare)
        }
        if (typeof res.data.mixRate === 'number') {
          this.$set(this.water, 'data', [res.data.mixRate])
        }
      }
    } catch (error) {
      console.error('获取中心数据失败:', error)
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/center.scss';
</style>
