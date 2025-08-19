<template>
  <div id="centerLeft1">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="chart-pie" class="text-icon"></icon>
        </span>
        <div class="d-flex" style="margin-left: 35px">
          <span class="fs-xl text mx-2" style="font-size: 17px">汽车词云图</span>
          <dv-decoration-1 class="dv-dec-1" />
        </div>
      </div>
      <div class="d-flex jc-center">
        <img src="../../public/car_clond.png" alt="词云图" style="height: 300px;width: 330px;margin-top: 20px">
      </div>
    </div>
  </div>
</template>

<script>
// import CenterLeft2Chart from "@/components/echart/centerLeft/centerLeft2Chart";
export default {
  components: {
    // CenterLeft2Chart
  },
};
</script>

<style lang="scss" scoped>
@import '../assets/scss/centerLeft2.scss';
</style>