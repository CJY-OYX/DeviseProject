import service from './index.js'

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
    const response = await service.get('/myApp/searchUsers/', {
      params: { username }
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

// 获取更新日志
export const getUpdateLogs = async () => {
  try {
    const response = await service.get('/myApp/getUpdateLogs/')
    return response.data
  } catch (error) {
    console.error('获取更新日志失败:', error)
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