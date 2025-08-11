<template>
  <div class="login-container">
    <dv-border-box-1 class="login-border-box">
      <div class="login-bg">
      <div class="login-form">
        <h2 class="form-title">用户登录</h2>
        <div class="form-group">
          <label for="username" style="color: white">用户名</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名">
        </div>
        <div class="form-group">
          <label for="password" style="color: white">密码</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码">
        </div>
        <div class="form-group remember-me">
          <input type="checkbox" id="remember" v-model="rememberMe">
          <label for="remember" style="color: white">记住我</label>
        </div>
        <button class="login-btn" @click="handleLogin">登录</button>
        <div class="form-footer">
          <!-- <a href="#" class="forgot-password" style="color: white">忘记密码?</a>
          <span> | </span> -->
          <router-link to="/register" class="register" style="color: white">注册账号</router-link>
        </div>
      </div>
      </div>
    </dv-border-box-1>
  </div>
</template>

<script>
import Vue from 'vue'
import DataV from '@jiaminghi/data-view'

Vue.use(DataV)

export default {
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false
    }
  },
  methods: {
    handleLogin() {
      // 简单的表单验证
      if (!this.username || !this.password) {
        alert('请输入用户名和密码');
        return;
      }
      // 模拟登录成功
      alert('登录成功');
      // 存储登录状态和用户名
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('username', this.username);
      // 获取重定向路径
      const redirect = this.$route.query.redirect || '/';
      this.$router.push(redirect);
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/login.scss';
</style>