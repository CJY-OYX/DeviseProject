<template>
  <div id="centerRight2">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="align-left" class="text-icon"></icon>
        </span>
        <span class="fs-xl text mx-2" style="font-size: 17px">汽车销售价格分布</span>
      </div>
      <div class="d-flex ai-center flex-column body-box">
        <dv-capsule-chart class="dv-cap-chart" :config="config" v-bind:key="config.data && config.data.length ? (config.data[0].value || 'default') : 'default'"
                          style="height: 200px"/>
        <dv-active-ring-chart :config="configTwo" style="width: 280px;height: 210px" v-bind:key="configTwo.data && configTwo.data.length ? (configTwo.data[0].name || 'default') : 'default'"/>

      </div>
    </div>
  </div>
</template>

<script>
// import centerRight2Chart1 from '@/components/echart/centerRight/centerRightChart'

export default {
  data() {
    return {
      config: {
        data: [
          {
            name: '0-5w',
            value: 96
          },
          {
            name: '5-10w',
            value: 516
          },
          {
            name: '10-20w',
            value: 864
          },
          {
            name: '20-30w',
            value: 327
          },
          {
            name: '30w以上',
            value: 196
          }
        ],
        unit: '台',
        colors: ['#37a2da', '#32c5e9', '#67e0e3', '#9fe6b4', '#ffdb5c']
      },
      configTwo:{
        data:[
          {
            name: '南阳',
            value: 167
          },
        ],
        radius:'60%',
        activeRadius:'70%',
      }
    }
  },
  async mounted() {
    try {
      const res = await this.$http.get('myApp/centerRight')
      const list = res && res.data && Array.isArray(res.data.realData) ? res.data.realData : []
      const safeList = list
        .filter(item => item && typeof item.name === 'string' && typeof item.value !== 'undefined')
        .map(item => ({ name: item.name, value: Number(item.value) || 0 }))
      const finalList = safeList.length > 0 ? safeList : [{ name: '暂无数据', value: 0 }]
      this.$set(this.config, 'data', finalList)
      this.$set(this.configTwo, 'data', finalList)
    } catch (error) {
      console.error('获取汽车销售价格分布数据失败:', error)
      // 使用默认数据，不改变现有数据
    }
  },
  components: {
    // centerRight2Chart1
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/centerRight2.scss';
</style>
