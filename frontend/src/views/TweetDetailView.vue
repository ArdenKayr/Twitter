<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Tweet from '@/components/Tweet.vue' // Переиспользуем наш компонент твита
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import axios from 'axios'

const route = useRoute()
const auth = useAuthStore()

const tweet = ref(null)
const comments = ref([])
const newComment = ref('')
const loading = ref(true)

// ID твита из URL
const tweetId = route.params.id

// Загрузка данных
const loadData = async () => {
  try {
    const config = auth.accessToken 
      ? { headers: { Authorization: `Bearer ${auth.accessToken}` } } 
      : {}

    // 1. Загружаем сам твит
    const tweetRes = await axios.get(`http://127.0.0.1:8000/api/tweets/${tweetId}/`, config)
    tweet.value = tweetRes.data

    // 2. Загружаем комментарии
    const commentsRes = await axios.get(`http://127.0.0.1:8000/api/tweets/${tweetId}/comments/`, config)
    comments.value = commentsRes.data
  } catch (e) {
    console.error("Ошибка загрузки", e)
  } finally {
    loading.value = false
  }
}

// Отправка комментария
const submitComment = async () => {
  if (!newComment.value.trim()) return

  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/api/tweets/${tweetId}/comments/`, 
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${auth.accessToken}` } }
    )
    
    // Добавляем новый коммент в список и очищаем поле
    comments.value.push(response.data)
    newComment.value = ''
    
    // Увеличиваем счетчик комментов у твита (визуально)
    if (tweet.value) {
        tweet.value.comments_count++
    }
  } catch (e) {
    alert("Ошибка отправки комментария")
  }
}

onMounted(loadData)
</script>

<template>
  <div v-if="loading" class="p-10 text-center text-gray-500">Загрузка...</div>
  
  <div v-else-if="tweet">
    <div class="sticky top-0 bg-white/90 backdrop-blur-md z-10 px-4 py-3 flex items-center space-x-6 border-b border-gray-100">
      <router-link to="/feed" class="p-2 rounded-full hover:bg-gray-200 transition">
        <ArrowLeftIcon class="h-5 w-5 text-black" />
      </router-link>
      <h2 class="font-bold text-xl text-black">Твит</h2>
    </div>

    <Tweet :tweet="tweet" />

    <div class="border-b border-gray-100 p-4 flex space-x-4">
       <div class="h-12 w-12 bg-gray-300 rounded-full flex-shrink-0 flex items-center justify-center text-xl font-bold text-gray-600">
          {{ auth.user?.username[0].toUpperCase() }}
       </div>
       <div class="flex-1">
          <textarea 
            v-model="newComment"
            rows="2"
            class="w-full text-lg placeholder-gray-500 border-none focus:ring-0 resize-none outline-none"
            placeholder="Tweet your reply"
          ></textarea>
          <div class="flex justify-end pt-2">
             <button 
               @click="submitComment"
               :disabled="!newComment"
               class="bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white font-bold py-2 px-5 rounded-full transition"
             >
               Reply
             </button>
          </div>
       </div>
    </div>

    <div v-for="comment in comments" :key="comment.id" class="p-4 border-b border-gray-100 hover:bg-gray-50 transition">
       <div class="flex space-x-3">
          <div class="h-10 w-10 bg-gray-300 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-gray-600">
             {{ comment.author.username[0].toUpperCase() }}
          </div>
          <div>
             <div class="flex items-center space-x-2">
                <span class="font-bold text-gray-900">{{ comment.author.username }}</span>
                <span class="text-gray-500 text-sm">· {{ new Date(comment.created_at).toLocaleDateString() }}</span>
             </div>
             <p class="text-gray-900 mt-1">{{ comment.content }}</p>
          </div>
       </div>
    </div>
    
    <div v-if="comments.length === 0" class="p-8 text-center text-gray-500">
        Пока нет комментариев. Будьте первым!
    </div>

  </div>
</template>