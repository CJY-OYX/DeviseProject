<template>
  <div class="register-container">
    <dv-border-box-1 class="register-border-box">
      <div class="register-form">
        <h2 class="form-title">用户注册</h2>
        <div class="form-group">
          <label for="username" style="color: white">用户名</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名">
        </div>
        <div class="form-group">
          <label for="password" style="color: white">密码</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码">
        </div>
        <div class="form-group">
          <label for="confirmPassword" style="color: white">确认密码</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="请确认密码">
        </div>
        <button class="register-btn" @click="handleRegister">注册</button>
        <div class="form-footer">
          <span>已有账号？</span>
          <router-link to="/login" style="color: white">立即登录</router-link>
        </div>
      </div>
    </dv-border-box-1>
  </div>
</template>

<script>
import Vue from 'vue'
import DataV from '@jiaminghi/data-view'
import axios from 'axios'

Vue.use(DataV)

export default {
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    handleRegister() {
      // 表单验证
      if (!this.username || !this.password || !this.confirmPassword) {
        alert('请填写所有字段');
        return;
      }

      // 验证用户名长度
      if (this.username.length > 8) {
        alert('用户名最多8个字符');
        return;
      }

      // 验证密码长度
      if (this.password.length < 8 || this.password.length > 12) {
        alert('密码必须是8-12个字符');
        return;
      }

      // 验证密码复杂度（至少包含两种字符类型）
      const hasUpper = /[A-Z]/.test(this.password);
      const hasLower = /[a-z]/.test(this.password);
      const hasDigit = /[0-9]/.test(this.password);
      const hasSymbol = /[^A-Za-z0-9]/.test(this.password);
      const complexityCount = [hasUpper, hasLower, hasDigit, hasSymbol].filter(Boolean).length;

      if (complexityCount < 2) {
        alert('密码必须包含大写字母、小写字母、数字、符号中的至少两种');
        return;
      }

      if (this.password !== this.confirmPassword) {
        alert('两次输入的密码不一致');
        return;
      }

      // 发送注册请求到后端API
      axios.post('http://localhost:8000/myApp/register/', {
        username: this.username,
        password: this.password,
        confirmPassword: this.confirmPassword
      })
      .then(response => {
        if (response.data.success) {
          alert('注册成功，请完善车辆信息');
          // 跳转到用户详情信息填写页，并传递用户ID
          this.$router.push({ path: '/user-detail-form', query: { userId: response.data.userId } });
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.error('注册失败:', error);
        alert('注册失败，请重试');
      });
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/register.scss';
</style>