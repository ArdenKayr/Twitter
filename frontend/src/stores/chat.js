import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useChatStore = defineStore('chat', {
  state: () => ({
    conversations: [],      // Список всех диалогов
    activeChat: null,       // Текущий открытый диалог (ID)
    messages: [],           // Сообщения текущего диалога
  }),
  
  actions: {
    // 1. Загрузить список диалогов
    async fetchConversations() {
      const auth = useAuthStore()
      if (!auth.accessToken) return
      
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/chat/conversations/', {
          headers: { Authorization: `Bearer ${auth.accessToken}` }
        })
        this.conversations = response.data
      } catch (e) {
        console.error("Ошибка загрузки диалогов", e)
      }
    },

    // 2. Начать чат (или открыть существующий) по username
    async startChat(username) {
       const auth = useAuthStore()
       try {
         const response = await axios.post(`http://127.0.0.1:8000/api/chat/conversations/start/${username}/`, {}, {
            headers: { Authorization: `Bearer ${auth.accessToken}` }
         })
         
         const newChat = response.data
         
         // 1. Делаем этот чат активным сразу
         this.activeChat = newChat.id
         
         // 2. Очищаем сообщения (т.к. чат только открылся)
         this.messages = []

         // 3. Проверяем, есть ли этот чат уже в списке, если нет - добавляем
         const exists = this.conversations.find(c => c.id === newChat.id)
         if (!exists) {
            this.conversations.unshift(newChat)
         }
         
         return newChat
       } catch (e) {
         console.error("Не удалось начать чат", e)
         throw e
       }
    },

    // 3. Загрузить сообщения конкретного чата
    async fetchMessages(conversationId) {
        const auth = useAuthStore()
        this.activeChat = conversationId
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/chat/conversations/${conversationId}/messages/`, {
                headers: { Authorization: `Bearer ${auth.accessToken}` }
            })
            this.messages = response.data
        } catch (e) {
            console.error("Ошибка загрузки сообщений", e)
        }
    },

    // 4. Отправить сообщение
    async sendMessage(content) {
        const auth = useAuthStore()
        if (!this.activeChat || !content.trim()) return

        try {
            const response = await axios.post(`http://127.0.0.1:8000/api/chat/conversations/${this.activeChat}/messages/`, 
                { content },
                { headers: { Authorization: `Bearer ${auth.accessToken}` } }
            )
            // Добавляем сообщение в список сразу же
            this.messages.push(response.data)
        } catch (e) {
            console.error("Ошибка отправки", e)
        }
    }
  }
})