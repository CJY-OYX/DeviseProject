import service from './index.js'

// 获取管理员面板综合数据 - 一次性获取所有需要的数据
export const getAdminDashboardData = async () => {
  try {
    const response = await service.get('/myApp/getAdminDashboardData/')
    return response.data
  } catch (error) {
    console.error('获取管理员面板数据失败:', error)
    throw error
  }
}

// 获取所有用户列表
export const getUsersList = async () => {
  try {
    const response = await service.get('/myApp/getUsersList/')
    return response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
    throw error
  }
}

// 搜索用户
export const searchUsers = async (username) => {
  try {
    const response = await service.post('/myApp/searchUser/', {
      keyword: username
    })
    return response.data
  } catch (error) {
    console.error('搜索用户失败:', error)
    throw error
  }
}

// 添加用户
export const addUser = async (username, password) => {
  try {
    const response = await service.post('/myApp/addUser/', {
      username,
      password
    })
    return response.data
  } catch (error) {
    console.error('添加用户失败:', error)
    throw error
  }
}

// 更新用户
export const updateUser = async (id, username, password) => {
  try {
    const response = await service.post('/myApp/updateUser/', {
      id,
      username,
      password
    })
    return response.data
  } catch (error) {
    console.error('更新用户失败:', error)
    throw error
  }
}

// 删除用户
export const deleteUser = async (id) => {
  try {
    const response = await service.post('/myApp/deleteUser/', {
      id
    })
    return response.data
  } catch (error) {
    console.error('删除用户失败:', error)
    throw error
  }
}

// 获取用户统计信息
export const getUserStats = async () => {
  try {
    const response = await service.get('/myApp/getUserStats/')
    return response.data
  } catch (error) {
    console.error('获取用户统计信息失败:', error)
    throw error
  }
}

// 获取汽车数据统计
export const getCarDataStats = async () => {
  try {
    const response = await service.get('/myApp/getCarDataStats/')
    return response.data
  } catch (error) {
    console.error('获取汽车数据统计失败:', error)
    throw error
  }
}

// 获取所有用户汽车详情
export const getUserCarDetails = async () => {
  try {
    const response = await service.get('/myApp/getUserCarDetails/')
    return response.data
  } catch (error) {
    console.error('获取用户汽车详情失败:', error)
    throw error
  }
}

// 获取汽车信息列表
export const getCarInfoList = async () => {
  try {
    const response = await service.get('/myApp/getCarInfoList/')
    return response.data
  } catch (error) {
    console.error('获取汽车信息列表失败:', error)
    throw error
  }
}

// 搜索汽车信息
export const searchCarInfo = async (carName) => {
  try {
    const response = await service.get('/myApp/searchCarInfo/', {
      params: { carName }
    })
    return response.data
  } catch (error) {
    console.error('搜索汽车信息失败:', error)
    throw error
  }
}

// 更新汽车信息
export const updateCarInfo = async (carData) => {
  try {
    const response = await service.post('/myApp/updateCarInfo/', carData)
    return response.data
  } catch (error) {
    console.error('更新汽车信息失败:', error)
    throw error
  }
}

// 获取爬虫日志
export const getCrawlerLogs = async () => {
  try {
    const response = await service.get('/myApp/getCrawlerLogs/')
    return response.data
  } catch (error) {
    console.error('获取爬虫日志失败:', error)
    throw error
  }
}

// 获取自动更新服务日志
export const getAutoUpdateLogs = async () => {
  try {
    const response = await service.get('/myApp/getAutoUpdateLogs/')
    return response.data
  } catch (error) {
    console.error('获取自动更新日志失败:', error)
    throw error
  }
}

// 启动自动更新服务
export const startAutoUpdateService = async () => {
  try {
    const response = await service.post('/myApp/startAutoUpdate/')
    return response.data
  } catch (error) {
    console.error('启动自动更新服务失败:', error)
    throw error
  }
}

// 停止自动更新服务
export const stopAutoUpdateService = async () => {
  try {
    const response = await service.post('/myApp/stopAutoUpdate/')
    return response.data
  } catch (error) {
    console.error('停止自动更新服务失败:', error)
    throw error
  }
}

// 检查自动更新服务状态
export const checkAutoUpdateServiceStatus = async () => {
  try {
    const response = await service.get('/myApp/checkAutoUpdateStatus/')
    return response.data
  } catch (error) {
    console.error('检查自动更新服务状态失败:', error)
    throw error
  }
}

// 执行数据更新
export const executeDataUpdate = async (updateType) => {
  try {
    const response = await service.post('/myApp/executeDataUpdate/', {
      updateType
    })
    return response.data
  } catch (error) {
    console.error('执行数据更新失败:', error)
    throw error
  }
}

// 更新用户车辆详情
export const updateUserCarDetail = async (detailData) => {
  try {
    const response = await service.post('/myApp/save_user_car_detail/', detailData)
    return response.data
  } catch (error) {
    console.error('更新用户车辆详情失败:', error)
    throw error
  }
}