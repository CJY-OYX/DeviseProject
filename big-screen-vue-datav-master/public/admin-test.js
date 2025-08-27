// 管理员测试脚本
// 这个脚本用于在localStorage中设置管理员权限，以便测试管理员面板

// 设置登录状态和管理员角色
function setAdminUser() {
  localStorage.setItem('isLoggedIn', 'true');
  localStorage.setItem('userRole', 'admin');
  localStorage.setItem('username', 'admin');
  console.log('管理员账户已设置，请访问 /admin 路径');
}

// 清除管理员权限
function clearAdminUser() {
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('userRole');
  localStorage.removeItem('username');
  console.log('管理员账户已清除');
}

// 添加全局函数，方便在控制台调用
window.setAdminUser = setAdminUser;
window.clearAdminUser = clearAdminUser;

// 检查是否需要自动设置（仅在没有登录状态时）
if (!localStorage.getItem('isLoggedIn')) {
  console.log('检测到没有登录状态，已自动设置管理员账户以便测试');
  setAdminUser();
}