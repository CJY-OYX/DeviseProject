import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
  path: '/',
  name: 'index',
  component: () => import('../views/index.vue')
}, {
  path: '/login',
  name: 'login',
  component: () => import('../views/Login.vue')
}, {
  path: '/register',
  name: 'register',
  component: () => import('../views/Register.vue')
}, {
  path: '/user-detail-form',
  name: 'userDetailForm',
  component: () => import('../views/UserDetailForm.vue')
},{  path: '/user-detail',
  name: 'user-detail',
  component: () => import('../views/UserInfoDetail.vue')
},
{
  path: '/user-car-detail-edit',
  name: 'userCarDetailEdit',
  component: () => import('../views/UserCarDetailEdit.vue')
}]

const router = new VueRouter({
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查是否需要登录
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 从localStorage中获取登录状态
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (!isLoggedIn) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next() // 确保一定要调用 next()
  }
})

export default router