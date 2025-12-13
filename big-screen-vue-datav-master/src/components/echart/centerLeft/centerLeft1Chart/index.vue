<template>
  <div>
<!--    <Chart :cdata="cdata" />-->
    <div
      ref="chart"
      style="width: 300px;height: 340px"
      v-bind:key="cdata.seriesData && cdata.seriesData.length ? cdata.seriesData[0].name : 'default'"
    ></div>
  </div>
</template>

<script>
// import Chart from './chart.vue';
export default {
  data () {
    return {
      currentIndex: 0,
      timer: null,
      cdata: {
        xData: ["data1", "data2", "data3", "data4", "data5", "data6"],
        seriesData: [
          { value: 10, name: "data1" },
          { value: 5, name: "data2" },
          { value: 15, name: "data3" },
          { value: 25, name: "data4" },
          { value: 20, name: "data5" },
          { value: 35, name: "data6" }
        ]
      }
    }
  },
  components: {
    // Chart,
  },
  async mounted() {
    const res = await this.$http.get('myApp/centerLeft')
    this.$set(this.cdata, 'seriesData', res.data.lastPieList)
  },
  updated() {
    this.initChart()
    this.loopAnimation()
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
      this.timer = null
    }
  },
  methods: {
    initChart(){
      this.myChart = this.$echarts.init(this.$refs.chart)
      const option = {
        color: [
            "#37a2da",
            "#32c5e9",
            "#9fe6b8",
            "#ffdb5c",
            "#ff9f7f",
            "#fb7293",
            "#e7bcf3",
            "#8378ea"
          ],
          tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          toolbox: {
            show: true
          },
          calculable: true,
          legend: {
            show: true,
            orient: "horizontal",
            icon: "circle",
            bottom: 0,
            x: "center",
            data: this.cdata.seriesData.map(item => item.name),
            textStyle: {
              color: "#fff"
            }
          },
          series: [
            {
              name: "销量总占比",
              type: "pie",
              radius: [20, 80],
              roseType: "area",
              center: ["50%", "35%"],
              data: this.cdata.seriesData,
              label: {
                normal: {
                  show: true
                }
              },
              labelLine: {
                normal: {
                  show: true
                }
              },
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                },
                label: {
                  show: true,
                  fontSize: 20,
                  fontWeight: 'bold'
                }
              }
            }
          ]
      };
      this.myChart.setOption(option);
    },
    loopAnimation(){
      if (!this.cdata.seriesData || this.cdata.seriesData.length === 0) return
      if (this.timer) {
        clearInterval(this.timer)
      }
      this.timer = setInterval(() => {
        this.myChart.dispatchAction({
          type: 'downplay',
          seriesIndex: 0,
          dataIndex: this.currentIndex
        })
        this.currentIndex = (this.currentIndex + 1) % this.cdata.seriesData.length
        this.myChart.dispatchAction({
          type: 'highlight',
          seriesIndex: 0,
          dataIndex: this.currentIndex
        })
      }, 2000)
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
