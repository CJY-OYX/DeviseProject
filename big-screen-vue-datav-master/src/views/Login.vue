<template>
  <div class="login-container">
    <dv-loading v-if="isSubmitting">正在登录...</dv-loading>
    <dv-border-box-1 class="login-border-box">
      <div class="login-bg">
      <form class="login-form" @submit.prevent="handleLogin">
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
        <button class="login-btn" type="submit">登录</button>
        <div class="form-footer">
          <!-- <a href="#" class="forgot-password" style="color: white">忘记密码?</a>
          <span> | </span> -->
          <router-link to="/register" class="register" style="color: white">注册账号</router-link>
        </div>
      </form>
      </div>
    </dv-border-box-1>
  </div>
</template>

<script>
import Vue from 'vue'
import DataV from '@jiaminghi/data-view'
import axios from 'axios'

Vue.use(DataV)
axios.defaults.withCredentials = true

export default {
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      isSubmitting: false
    }
  },
  methods: {
    handleLogin () {
  if (this.isSubmitting) return
  this.isSubmitting = true
  if (!this.username || !this.password) {
    alert('请输入用户名和密码')
    this.isSubmitting = false
    return
  }
  axios.post(
    'http://localhost:18000/myApp/login/',
    { username: this.username, password: this.password }
  )
  .then(res => {
    if (res.data.success) {
      alert(res.data.message)
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('username', this.username);
      const redirect = this.$route.query.redirect;
      const target = redirect && redirect !== '/login' ? redirect : '/';
      this.$router.replace(target);
    } else {
      alert(res.data.message)
    }
  })
  .finally(() => {
    this.isSubmitting = false
  })
}
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/login.scss';
</style>
