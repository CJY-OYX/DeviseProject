<script>
export default {
  data() {
    return {
      message: '用户信息详情',
      userData: null,
      userInfo: null
    }
  },
  mounted() {
    // 从sessionStorage获取数据
    const userData = sessionStorage.getItem('userData');
    const userInfo = sessionStorage.getItem('userInfo');
    console.log('sessionStorage数据:', { userData, userInfo });
    
    if (userData) {
      try {
        this.userData = JSON.parse(userData);
      } catch (error) {
        console.error('解析userData失败:', error);
        this.userData = null;
      }
    }
    
    if (userInfo) {
      try {
        this.userInfo = JSON.parse(userInfo);
      } catch (error) {
        console.error('解析userInfo失败:', error);
        this.userInfo = null;
      }
    }
  },
  methods: {
    formatKey(key) {
      // 将蛇形命名转换为驼峰命名并首字母大写
      return key.replace(/([A-Z])/g, ' $1')
                .replace(/^./, function(str) { return str.toUpperCase(); })
                .replace(/_/g, ' ');
    }
  }
}
</script>

<template>
  <div class="user-info-container">
    <h2>{{ message }}</h2>
    
    <div v-if="userData" class="data-card">
      <h3>车辆信息</h3>
      <div class="data-item" v-for="(value, key) in userData" :key="key">
        <span class="data-label">{{ formatKey(key) }}:</span>
        <span class="data-value">{{ value }}</span>
      </div>
    </div>
    
    <div v-if="userInfo" class="data-card">
      <h3>用户车辆详情</h3>
      <div class="data-item" v-for="(value, key) in userInfo" :key="key">
        <span class="data-label">{{ formatKey(key) }}:</span>
        <span class="data-value">{{ value }}</span>
      </div>
    </div>
    
    <div v-else-if="!userData && !userInfo" class="no-data">
      <p>没有找到用户信息</p>
      <p>请先完善您的车辆信息</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.user-info-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

h2 {
  color: #333;
  border-bottom: 2px solid #42b983;
  padding-bottom: 10px;
}

h3 {
  color: #444;
  margin-top: 20px;
}

.data-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.data-item {
  display: flex;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #eee;
}

.data-item:last-child {
  border-bottom: none;
}

.data-label {
  flex: 0 0 120px;
  font-weight: bold;
  color: #666;
}

.data-value {
  flex: 1;
  color: #333;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
  background-color: #f5f5f5;
  border-radius: 8px;
}
</style>
