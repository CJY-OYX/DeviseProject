import axios from 'axios'

const service = axios.create({
    baseURL:'/api',
    timeout:40000,
    withCredentials: true
})

export default service
