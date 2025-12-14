<template>
  <transition name="modal-fade">
    <div v-show="visible" class="login-modal-overlay" @click="handleOverlayClick">
      <div class="login-modal-content" @click.stop>
        <!-- 关闭按钮 -->
        <button class="modal-close" @click="close">
          <span class="close-icon">×</span>
        </button>

        <div class="login-form-container">
          <h2 class="form-title">用户登录</h2>
          
          <form class="login-form" @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="modal-username">用户名</label>
              <div class="input-wrapper">
                <input 
                  type="text" 
                  id="modal-username" 
                  v-model="username" 
                  placeholder="请输入用户名"
                  autocomplete="username"
                >
              </div>
            </div>
            
            <div class="form-group">
              <label for="modal-password">密码</label>
              <div class="input-wrapper">
                <input 
                  type="password" 
                  id="modal-password" 
                  v-model="password" 
                  placeholder="请输入密码"
                  autocomplete="current-password"
                >
              </div>
            </div>
            
            <div class="form-group remember-me">
              <input type="checkbox" id="modal-remember" v-model="rememberMe">
              <label for="modal-remember" class="checkbox-label">记住我</label>
            </div>
            
            <button class="login-btn" type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? '登录中...' : '登录' }}
            </button>
            
            <div class="form-footer">
              <span class="register-text">还没有账号？</span>
              <a href="javascript:void(0)" class="register-link" @click="switchToRegister">立即注册</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import service from '@/api/index'

export default {
  name: 'LoginModal',
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
      rememberMe: false,
      isSubmitting: false
    }
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        // 重置表单
        this.username = ''
        this.password = ''
        this.isSubmitting = false
        // 尝试自动填充上次记住的用户名
        const savedUsername = localStorage.getItem('savedUsername')
        if (savedUsername) {
          this.username = savedUsername
          this.rememberMe = true
        }
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
    switchToRegister() {
      this.$emit('switch-to-register')
    },
    handleLogin() {
      if (this.isSubmitting) return
      this.isSubmitting = true
      
      if (!this.username || !this.password) {
        alert('请输入用户名和密码')
        this.isSubmitting = false
        return
      }

      service.post(
        '/myApp/login/',
        { username: this.username, password: this.password }
      )
      .then(res => {
        if (res.data.success) {
          // 处理记住我
          if (this.rememberMe) {
            localStorage.setItem('savedUsername', this.username)
          } else {
            localStorage.removeItem('savedUsername')
          }

          // 保存登录状态
          localStorage.setItem('isLoggedIn', 'true')
          localStorage.setItem('username', this.username)
          
          // 如果是管理员，设置角色并跳转到管理后台
          if (this.username === 'admin') {
            localStorage.setItem('userRole', 'admin')
            this.$router.push('/admin')
          } else {
            localStorage.setItem('userRole', 'user')
          }

          this.$emit('login-success', {
            username: this.username
          })
          
          this.close()
          alert(res.data.message)
        } else {
          alert(res.data.message)
        }
      })
      .catch(err => {
        console.error(err)
        alert('登录请求失败，请检查网络')
      })
      .finally(() => {
        this.isSubmitting = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
  .login-modal-content {
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.27);
  }
}
.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
  .login-modal-content {
    transform: scale(0.9) translateY(20px);
  }
}

.login-modal-overlay {
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

.login-modal-content {
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
    box-sizing: border-box; // 确保padding不撑大宽度
    
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

.remember-me {
  display: flex;
  align-items: center;
  
  input[type="checkbox"] {
    margin-right: 8px;
    cursor: pointer;
  }
  
  .checkbox-label {
    margin-bottom: 0;
    cursor: pointer;
    user-select: none;
  }
}

.login-btn {
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
  
  .register-text {
    color: #94a3b8;
  }
  
  .register-link {
    color: #00d1ff;
    text-decoration: none;
    margin-left: 5px;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
