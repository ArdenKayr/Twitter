import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    // ВАЖНО: Тот самый метод, которого не хватало
    initStore() {
      if (this.accessToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
      } else {
        this.user = null
        this.accessToken = null
        this.refreshToken = null
      }
    },

    async login(username, password) {
      try {
        // 1. Получаем токены
        const response = await axios.post('http://127.0.0.1:8000/api/users/token/', {
          username,
          password
        })

        this.accessToken = response.data.access
        this.refreshToken = response.data.refresh
        
        // Сохраняем токены в браузере
        localStorage.setItem('accessToken', this.accessToken)
        localStorage.setItem('refreshToken', this.refreshToken)

        axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`

        // 2. Получаем данные пользователя (имя, аватар и т.д.)
        const userResponse = await axios.get('http://127.0.0.1:8000/api/users/me/')
        this.user = userResponse.data
        localStorage.setItem('user', JSON.stringify(this.user))

      } catch (error) {
        console.error("Login failed", error)
        throw error
      }
    },

    async register(userData) {
      try {
        await axios.post('http://127.0.0.1:8000/api/users/register/', userData)
        // После регистрации сразу логинимся
        await this.login(userData.username, userData.password)
      } catch (error) {
        console.error("Registration failed", error)
        throw error
      }
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      
      localStorage.removeItem('user')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      
      delete axios.defaults.headers.common['Authorization']
    }
  }
})