<template>
  <div id="admin-panel" ref="appRef" >
    <div class="bg" style="background: url('/VCG41N1312873566.jpg') center/cover no-repeat;position: relative;">
      <dv-loading v-if="loading">Loading...</dv-loading>
      <div v-else class="host-body">
        <!-- 标题区域 -->
        <div class="d-flex jc-center">
          <div class="d-flex jc-center">
            <div class="title">
              <span class="title-text">管理员控制面板</span>
            </div>
          </div>
        </div>

        <!-- 导航区域 -->
        <div class="admin-nav">
          <button 
            v-for="item in menuItems" 
            :key="item.id"
            :class="['nav-btn', { active: activeModule === item.id }]"
            @click="switchModule(item.id)"
          >
            {{ item.name }}
          </button>
          <button class="nav-btn logout-btn" @click="logout">退出登录</button>
        </div>

        <!-- 内容区域 -->
        <div class="body-box">
          <!-- 用户管理模块 -->
          <div v-if="activeModule === 'userManagement'" class="admin-module">
            <h2>用户管理</h2>
            <div class="module-content">
              <div class="search-bar">
                <input type="text" v-model="searchQuery" placeholder="搜索用户..." class="search-input" @keyup.enter="searchUser">
                <button class="search-btn" @click="searchUser">搜索</button>
                <button class="add-btn" @click="addUser">添加用户</button>
              </div>
              <div class="user-table-container">
                <table class="user-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>用户名</th>
                      <th>角色</th>
                      <th>创建时间</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="usersData.length === 0">
                      <td colspan="5" class="no-data">暂无用户数据</td>
                    </tr>
                    <tr v-for="user in usersData" :key="user.id">
                      <td>{{ user.id }}</td>
                      <td>{{ user.username }}</td>
                      <td>{{ user.role }}</td>
                      <td>{{ user.createdAt }}</td>
                      <td>
                        <button class="edit-btn" @click="editUser(user)">编辑</button>
                        <button class="delete-btn" @click="deleteUser(user)">删除</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- 用户信息管理模块 -->
          <div v-else-if="activeModule === 'userInfoManagement'" class="admin-module">
            <h2>用户信息管理</h2>
            <div class="module-content">
              <div class="info-cards">
                <div class="info-card">
                  <h3>用户总数</h3>
                  <p class="info-number">{{ userCount }}</p>
                </div>
                <div class="info-card">
                  <h3>今日新增</h3>
                  <p class="info-number">{{ todayNewUsers }}</p>
                </div>
                <div class="info-card">
                  <h3>活跃用户</h3>
                  <p class="info-number">{{ activeUsers }}</p>
                </div>
              </div>
              <div class="user-info-list">
                <h3>用户车辆详情</h3>
                <div class="user-table-container">
                  <table class="user-table">
                    <thead>
                    <tr>
                      <th>用户</th>
                      <th>车辆</th>
                      <th>型号</th>
                      <th>购买时间</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                    <tbody>
                      <tr v-if="userCarDetails.length === 0">
                        <td colspan="5" class="no-data">暂无用户车辆数据</td>
                      </tr>
                      <tr v-for="(detail, index) in userCarDetails" :key="index">
                        <td>{{ detail.username || '未知用户' }}</td>
                        <td>{{ detail.carName || '未知车辆' }}</td>
                        <td>{{ detail.model || '未知型号' }}</td>
                        <td>{{ detail.purchaseDate || '-' }}</td>
                        <td>
                          <button class="edit-btn" @click="editUserCarDetail(detail)">编辑</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- 数据管理模块 -->
          <div v-else-if="activeModule === 'dataManagement'" class="admin-module">
            <h2>数据管理</h2>
            <div class="module-content">
              <div class="data-stats">
                <div class="data-stat">
                  <h3>数据总量</h3>
                  <p class="stat-number">{{ totalData }}</p>
                </div>
                <div class="data-stat">
                  <h3>数据类型</h3>
                  <p class="stat-number">{{ dataTypes }}</p>
                </div>
              </div>
              <div class="search-bar">
                <input type="text" v-model="searchQuery" placeholder="搜索车辆信息..." class="search-input" @keyup.enter="searchCar">
                <button class="search-btn" @click="searchCar">搜索</button>
              </div>
              <div class="data-table-container">
                <table class="car-table">
                  <thead>
                    <tr>
                      <th>品牌</th>
                      <th>车型</th>
                      <th>能源类型</th>
                      <th>价格(新车指导价)</th>
                      <th>上市时间</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="carInfoList.length === 0">
                      <td colspan="5" class="no-data">暂无车辆数据</td>
                    </tr>
                    <tr v-for="car in carInfoList" :key="car.id || car.idx">
                      <td>{{ car.brand}}</td>
                      <td>{{ car.carName}}</td>
                      <td>{{ car.energyType}}</td>
                      <td>{{ car.price ? '¥' + car.price.toLocaleString() : '-' }}</td>
                      <td>{{ car.marketTime || '-' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import drawMixin from "../utils/drawMixin";
import {
  getAdminDashboardData,
  getUsersList,
  searchUsers,
  addUser,
  updateUser,
  deleteUser,
  getUserStats,
  getUserCarDetails,
  getCarInfoList,
  searchCarInfo,
  updateUserCarDetail,
  getCarDataStats
} from '../api/adminApi.js';
import { showPrompt } from '../utils/index.js';

export default {
  mixins: [drawMixin],
  data() {
    return {
      loading: false,
      activeModule: 'userManagement',
      menuItems: [
        { id: 'userManagement', name: '用户管理' },
        { id: 'userInfoManagement', name: '用户信息管理' },
        { id: 'dataManagement', name: '数据管理' }
      ],
      searchQuery: '',
      // 真实数据存储
      usersData: [],
      userCount: 0,
      todayNewUsers: 0,
      activeUsers: 0,
      userCarDetails: [],
      carInfoList: [],
      totalData: 0,
      dataTypes: 0
    }
  },
  methods: {
    switchModule(moduleId) {
      this.activeModule = moduleId;
      // 切换模块时加载对应数据
      if (moduleId === 'userManagement') {
        this.fetchUsers();
      } else if (moduleId === 'userInfoManagement') {
        this.fetchUserStats();
        this.fetchUserCarDetails();
      } else if (moduleId === 'dataManagement') {
        this.fetchCarInfoList();
        this.fetchCarDataStats();
      }
    },
    logout() {
      // 退出登录逻辑
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('userRole');
      this.$router.push('/login');
    },
    async fetchUsers() {
      // 获取用户数据逻辑
      try {
        this.loading = true;
        const res = await getUsersList();
        if (res.success) {
          // 直接使用后端返回的已格式化数据
          this.usersData = res.users || [];
        } else {
          alert(res.message || '获取用户数据失败');
        }
      } catch (error) {
        console.error('获取用户数据失败:', error);
        alert('获取用户数据失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    async searchUser() {
      // 搜索用户逻辑
      if (!this.searchQuery.trim()) {
        this.fetchUsers();
        return;
      }
      
      try {
        this.loading = true;
        const res = await searchUsers(this.searchQuery);
        if (res.success) {
          // 直接使用后端返回的已格式化数据
          this.usersData = res.users || [];
        } else {
          alert(res.message || '搜索用户失败');
        }
      } catch (error) {
        console.error('搜索用户失败:', error);
        alert('搜索用户失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    async addUser() {
      // 添加用户逻辑
      const username = await showPrompt('请输入用户名:', '', '添加用户');
      if (!username) return;
      
      const password = await showPrompt('请输入密码:', '', '添加用户');
      if (!password) return;
      
      try {
        this.loading = true;
        const res = await addUser(username, password);
        if (res.success) {
          alert('用户添加成功');
          this.fetchDashboardData(); // 使用综合API更新所有数据
        } else {
          alert(res.message || '添加用户失败');
        }
      } catch (error) {
        console.error('添加用户失败:', error);
        alert('添加用户失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    async editUser(user) {
      // 编辑用户逻辑
      const username = await showPrompt('请输入新用户名:', user.username, '编辑用户');
      if (username === null) return;
      
      const password = await showPrompt('请输入新密码(留空则不修改):', '', '编辑用户');
      
      try {
        this.loading = true;
        const res = await updateUser(user.id, username, password);
        if (res.success) {
          alert('用户更新成功');
          this.fetchDashboardData(); // 使用综合API更新所有数据
        } else {
          alert(res.message || '更新用户失败');
        }
      } catch (error) {
        console.error('更新用户失败:', error);
        alert('更新用户失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    async deleteUser(user) {
      // 删除用户逻辑
      if (!confirm(`确定要删除用户 ${user.username} 吗？`)) return;
      
      try {
        this.loading = true;
        const res = await deleteUser(user.id);
        if (res.success) {
          alert('用户删除成功');
          this.fetchDashboardData(); // 使用综合API更新所有数据
        } else {
          alert(res.message || '删除用户失败');
        }
      } catch (error) {
        console.error('删除用户失败:', error);
        alert('删除用户失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    async fetchUserStats() {
      // 获取用户统计信息
      try {
        const res = await getUserStats();
        if (res.success) {
          this.userCount = res.stats.totalUsers || 0;
          this.todayNewUsers = res.stats.todayNewUsers || 0;
          this.activeUsers = res.stats.activeUsers || 0;
        }
      } catch (error) {
        console.error('获取用户统计信息失败:', error);
      }
    },
    async fetchUserCarDetails() {
      // 获取用户汽车详情
      try {
        const res = await getUserCarDetails();
        if (res.success) {
          console.log(res.details)
          this.userCarDetails = (res.details || []).map(d => ({
            username: d.user_name || '未知用户',  // 从后端返回的user_name字段获取用户名
            carName: d.car_name || '-',
            model: d.car_model || '-',
            purchaseDate: d.purchase_date || '-' 
          }));
        }
      } catch (error) {
        console.error('获取用户汽车详情失败:', error);
      }
    },
    async fetchCarInfoList() {
      // 获取汽车信息列表
      try {
        this.loading = true;
        const res = await getCarInfoList();
        if (res.success) {
          this.carInfoList = res.cars || [];
        }
      } catch (error) {
        console.error('获取汽车信息列表失败:', error);
      } finally {
        this.loading = false;
      }
    },
    async searchCar() {
      // 搜索汽车信息
      if (!this.searchQuery.trim()) {
        this.fetchCarInfoList();
        return;
      }
      
      try {
        this.loading = true;
        const res = await searchCarInfo(this.searchQuery);
        if (res.success) {
          this.carInfoList = res.carInfoList || [];
        } else {
          alert(res.message || '搜索汽车信息失败');
        }
      } catch (error) {
        console.error('搜索汽车信息失败:', error);
        alert('搜索汽车信息失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    
    async fetchCarDataStats() {
      // 获取汽车数据统计
      try {
        const res = await getCarDataStats();
        if (res.success) {
          this.totalData = res.stats.totalData || 0;
          this.dataTypes = res.stats.dataTypes || 0;
        }
      } catch (error) {
        console.error('获取汽车数据统计失败:', error);
      }
    },
    
    async editUserCarDetail(detail) {
      // 编辑用户车辆详情
      try {
        const userId = prompt('请输入用户ID:', '');
        if (!userId) return;
        
        const carName = prompt('请输入车辆名称:', detail.carName || '');
        if (!carName) return;
        
        const carModel = prompt('请输入车辆型号:', detail.model || '');
        if (!carModel) return;
        
        const purchaseDate = prompt('请输入购买日期 (YYYY-MM-DD):', detail.purchaseDate || '');
        if (!purchaseDate) return;
        
        const mileage = prompt('请输入行驶里程:', '');
        const configuration = prompt('请输入车辆配置:', '');
        
        this.loading = true;
        const res = await updateUserCarDetail({
          userId,
          carName,
          carModel,
          purchaseDate,
          mileage,
          configuration
        });
        
        if (res.success) {
          alert('用户车辆详情更新成功');
          this.fetchDashboardData(); // 使用综合API更新所有数据
        } else {
          alert(res.message || '更新用户车辆详情失败');
        }
      } catch (error) {
        console.error('更新用户车辆详情失败:', error);
        alert('更新用户车辆详情失败，请稍后重试');
      } finally {
        this.loading = false;
      }
    },
    
    async fetchDashboardData() {
      // 调用综合API一次性获取所有数据
      try {
        this.loading = true;
        const res = await getAdminDashboardData();
        if (res.success) {
          this.usersData = res.users || [];
          this.userCount = res.userStats.totalUsers || 0;
          this.todayNewUsers = res.userStats.todayNewUsers || 0;
          this.activeUsers = res.userStats.activeUsers || 0;
          this.carInfoList = res.carInfoList || [];
          this.userCarDetails = res.userCarDetails || [];
          this.totalData = res.totalData || 0;
          this.dataTypes = res.dataTypes || 0;
        }
      } catch (error) {
        console.error('获取仪表盘数据失败:', error);
        // 如果综合API失败，回退到单独调用各个API
        try {
          await Promise.all([
            this.fetchUsers(),
            this.fetchUserStats(),
            this.fetchCarInfoList(),
            this.fetchUserCarDetails(),
            this.fetchCarDataStats()
          ]);
        } catch (fallbackError) {
          console.error('回退API调用也失败:', fallbackError);
        }
      } finally {
        this.loading = false;
      }
    }
  },
  created() {
    // 在组件创建时调用综合API加载所有数据
    this.fetchDashboardData();
  },
  mounted() {
    // 组件挂载时调用综合API加载所有数据
    this.fetchDashboardData();
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/admin-panel.scss';
</style>