import axios from 'axios'

const host = (typeof window !== 'undefined' && window.location && window.location.hostname) ? window.location.hostname : '127.0.0.1'
const service = axios.create({
    baseURL:`http://${host}:18000/`,
    timeout:40000,
    withCredentials: true
})

export default service
