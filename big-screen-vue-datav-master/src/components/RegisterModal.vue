<template>
  <transition name="modal-fade">
    <div v-show="visible" class="register-modal-overlay" @click="handleOverlayClick">
      <div class="register-modal-content" @click.stop>
        <!-- 关闭按钮 -->
        <button class="modal-close" @click="close">
          <span class="close-icon">×</span>
        </button>

        <div class="register-form-container">
          <h2 class="form-title">用户注册</h2>
          
          <form class="register-form" @submit.prevent="handleRegister">
            <div class="form-group">
              <label for="modal-reg-username">用户名</label>
              <div class="input-wrapper">
                <input 
                  type="text" 
                  id="modal-reg-username" 
                  v-model="username" 
                  placeholder="请输入用户名"
                  autocomplete="username"
                >
              </div>
            </div>
            
            <div class="form-group">
              <label for="modal-reg-password">密码</label>
              <div class="input-wrapper">
                <input 
                  type="password" 
                  id="modal-reg-password" 
                  v-model="password" 
                  placeholder="请输入密码"
                  autocomplete="new-password"
                >
              </div>
            </div>

            <div class="form-group">
              <label for="modal-reg-confirm-password">确认密码</label>
              <div class="input-wrapper">
                <input 
                  type="password" 
                  id="modal-reg-confirm-password" 
                  v-model="confirmPassword" 
                  placeholder="请再次输入密码"
                  autocomplete="new-password"
                >
              </div>
            </div>
            
            <button class="register-btn" type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? '注册中...' : '注册' }}
            </button>
            
            <div class="form-footer">
              <span class="login-text">已有账号？</span>
              <a href="javascript:void(0)" class="login-link" @click="switchToLogin">立即登录</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      isSubmitting: false
    }
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        // 重置表单
        this.username = ''
        this.password = ''
        this.confirmPassword = ''
        this.isSubmitting = false
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.moveToBody()
    })
  },
  beforeDestroy() {
    this.removeFromBody()
  },
  methods: {
    close() {
      this.$emit('update:visible', false)
    },
    handleOverlayClick() {
      this.close()
    },
    moveToBody() {
      const element = this.$el
      if (element && element.parentElement !== document.body) {
        document.body.appendChild(element)
      }
    },
    removeFromBody() {
      const element = this.$el
      if (element && element.parentElement === document.body) {
        document.body.removeChild(element)
      }
    },
    switchToLogin() {
      this.$emit('switch-to-login')
    },
    handleRegister() {
      if (this.isSubmitting) return
      this.isSubmitting = true
      
      // 验证逻辑
      if (!this.username || !this.password || !this.confirmPassword) {
        alert('请填写所有字段');
        this.isSubmitting = false;
        return;
      }
      if (this.username.length > 8) {
        alert('用户名最多8个字符');
        this.isSubmitting = false;
        return;
      }
      if (this.password.length < 8 || this.password.length > 12) {
        alert('密码必须是8-12个字符');
        this.isSubmitting = false;
        return;
      }
      
      const hasUpper = /[A-Z]/.test(this.password);
      const hasLower = /[a-z]/.test(this.password);
      const hasDigit = /[0-9]/.test(this.password);
      const hasSymbol = /[^A-Za-z0-9]/.test(this.password);
      const complexityCount = [hasUpper, hasLower, hasDigit, hasSymbol].filter(Boolean).length;
      
      if (complexityCount < 2) {
        alert('密码必须包含大写字母、小写字母、数字、符号中的至少两种');
        this.isSubmitting = false;
        return;
      }
      
      if (this.password !== this.confirmPassword) {
        alert('两次输入的密码不一致');
        this.isSubmitting = false;
        return;
      }

      axios.post('http://localhost:8000/myApp/register/', {
        username: this.username,
        password: this.password,
        confirmPassword: this.confirmPassword
      })
      .then(response => {
        if (response.data.success) {
          alert('注册成功，请完善车辆信息');
          this.close();
          // 跳转到完善信息页面，或者发射事件让父组件处理
          // 这里保持原逻辑跳转，但要注意是在模态框中
          // 如果是模态框，可能需要关闭模态框并跳转
          this.$router.push({ path: '/user-detail-form', query: { userId: response.data.userId } });
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.error('注册失败:', error);
        alert('注册失败，请重试');
      })
      .finally(() => {
        this.isSubmitting = false;
      });
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
  .register-modal-content {
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.27);
  }
}
.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
  .register-modal-content {
    transform: scale(0.9) translateY(20px);
  }
}

.register-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.register-modal-content {
  position: relative;
  width: 400px;
  background: rgba(13, 20, 40, 0.95);
  border: 1px solid rgba(64, 158, 255, 0.3);
  box-shadow: 0 0 30px rgba(64, 158, 255, 0.2);
  border-radius: 8px;
  padding: 30px;
  
  // 科技感边角
  &::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 20px; height: 20px;
    border-top: 2px solid #00d1ff;
    border-left: 2px solid #00d1ff;
    border-radius: 4px 0 0 0;
  }
  &::after {
    content: '';
    position: absolute;
    bottom: -1px; right: -1px;
    width: 20px; height: 20px;
    border-bottom: 2px solid #00d1ff;
    border-right: 2px solid #00d1ff;
    border-radius: 0 0 4px 0;
  }
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 24px;
  cursor: pointer;
  line-height: 1;
  transition: color 0.3s;
  
  &:hover {
    color: #ef4444;
  }
}

.form-title {
  text-align: center;
  color: #fff;
  font-size: 24px;
  margin-bottom: 30px;
  font-weight: 600;
  letter-spacing: 2px;
  text-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
}

.form-group {
  margin-bottom: 20px;
  
  label {
    display: block;
    color: #94a3b8;
    margin-bottom: 8px;
    font-size: 14px;
  }
}

.input-wrapper {
  position: relative;
  
  input {
    width: 100%;
    padding: 10px 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    color: #fff;
    font-size: 16px;
    transition: all 0.3s;
    box-sizing: border-box;
    
    &:focus {
      outline: none;
      border-color: #00d1ff;
      background: rgba(255, 255, 255, 0.08);
      box-shadow: 0 0 10px rgba(0, 209, 255, 0.2);
    }
    
    &::placeholder {
      color: rgba(255, 255, 255, 0.3);
    }
  }
}

.register-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(90deg, #00d1ff, #0099ff);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 10px;
  letter-spacing: 2px;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 209, 255, 0.4);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.form-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  
  .login-text {
    color: #94a3b8;
  }
  
  .login-link {
    color: #00d1ff;
    text-decoration: none;
    margin-left: 5px;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
