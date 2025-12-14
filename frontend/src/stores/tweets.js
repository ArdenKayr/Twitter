import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useTweetStore = defineStore('tweets', {
  state: () => ({
    tweets: [],
  }),
  actions: {

    async fetchTweets(username = null, feedType = null) {
        try {
            let url = 'http://127.0.0.1:8000/api/tweets/?' // Добавим вопросительный знак сразу
            
            if (username) {
                url += `username=${username}&`
            }
            if (feedType) {
                url += `feed_type=${feedType}&`
            }

            const auth = useAuthStore()
            const config = auth.accessToken 
                 ? { headers: { Authorization: `Bearer ${auth.accessToken}` } } 
                 : {}
                 
            const response = await axios.get(url, config)
            this.tweets = response.data
        } catch (e) {
            console.error("Ошибка при загрузке твитов", e)
        }
    },
    
    async fetchTweets(username = null) {
        // ... старый код ...
        try {
            let url = 'http://127.0.0.1:8000/api/tweets/'
            if (username) {
                url += `?username=${username}`
            }
            const auth = useAuthStore()
            // Важно передать токен, чтобы бэкенд посчитал поле is_liked!
            const config = auth.accessToken 
                 ? { headers: { Authorization: `Bearer ${auth.accessToken}` } } 
                 : {}
                 
            const response = await axios.get(url, config)
            this.tweets = response.data
        } catch (e) {
            console.error("Ошибка при загрузке твитов", e)
        }
    },

    async createTweet(content) {
        // ... старый код ...
        const auth = useAuthStore()
        const response = await axios.post('http://127.0.0.1:8000/api/tweets/', 
            { content },
            { headers: { Authorization: `Bearer ${auth.accessToken}` }}
        )
        this.tweets.unshift(response.data)
    },

    // --- НОВОЕ ДЕЙСТВИЕ ---
    async toggleLike(tweetId) {
        const auth = useAuthStore()
        if (!auth.accessToken) return; // Если не авторизован - нельзя лайкать

        try {
            // 1. Ищем твит в локальном списке
            const tweet = this.tweets.find(t => t.id === tweetId)
            
            // 2. Оптимистичное обновление (меняем интерфейс сразу, не ожидая сервера)
            if (tweet) {
                tweet.is_liked = !tweet.is_liked
                tweet.likes_count += tweet.is_liked ? 1 : -1
            }

            // 3. Шлем запрос
            await axios.post(`http://127.0.0.1:8000/api/tweets/${tweetId}/like/`, {}, 
                { headers: { Authorization: `Bearer ${auth.accessToken}` }}
            )
        } catch (e) {
            console.error("Ошибка лайка", e)
            // Если ошибка - можно откатить изменения обратно, но для MVP пропустим
        }
    }
  }
})