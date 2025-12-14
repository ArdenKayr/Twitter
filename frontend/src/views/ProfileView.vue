<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { EnvelopeIcon } from '@heroicons/vue/24/outline'
import EditProfileModal from '@/components/EditProfileModal.vue' // <--- Импорт
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const chatStore = useChatStore()
const profile = ref(null)
const showEditModal = ref(false) // <--- Состояние модалки

const isMe = computed(() => {
  return profile.value && profile.value.username === auth.user?.username
})

const handleMessage = async () => {
    try {
        await chatStore.startChat(profile.value.username)
        router.push('/messages')
    } catch (e) {
        alert('Ошибка создания чата')
    }
}

const loadProfile = async () => {
  const usernameParam = route.params.username
  try {
    let url = ''
    if (usernameParam) {
      url = `http://127.0.0.1:8000/api/users/${usernameParam}/`
    } else {
      url = 'http://127.0.0.1:8000/api/users/me/'
    }
    const config = auth.accessToken 
      ? { headers: { Authorization: `Bearer ${auth.accessToken}` } } 
      : {}
    const response = await axios.get(url, config)
    profile.value = response.data
  } catch (e) {
    console.error(e)
  }
}

// Когда данные обновились в модалке - обновляем их и здесь
const handleProfileUpdate = (updatedData) => {
    profile.value = updatedData
}

onMounted(loadProfile)
watch(() => route.params.username, loadProfile)
</script>

<template>
  <div v-if="profile">
    <div class="sticky top-0 bg-white/90 backdrop-blur-md z-10 px-4 py-1 flex items-center space-x-6 border-b border-gray-100">
      <div class="py-2">
        <h2 class="font-bold text-xl text-black leading-tight">{{ profile.username }}</h2>
        <p class="text-xs text-gray-500">0 posts</p>
      </div>
    </div>

    <div class="h-32 md:h-48 bg-gray-300"></div>

    <div class="px-4 pb-4 border-b border-gray-100 relative">
      <div class="flex justify-between items-start">
        
        <div class="w-32 h-32 rounded-full border-4 border-white -mt-16 relative bg-white overflow-hidden">
             <img v-if="profile.avatar" :src="profile.avatar" class="w-full h-full object-cover" />
             <div v-else class="w-full h-full bg-gray-400 flex items-center justify-center text-4xl text-white font-bold">
                 {{ profile.username[0].toUpperCase() }}
             </div>
        </div>

        <div class="mt-3">
          <button 
            v-if="isMe"
            @click="showEditModal = true"
            class="border border-gray-300 font-bold py-2 px-4 rounded-full hover:bg-gray-100 transition"
          >
            Edit profile
          </button>
          
          <div v-else class="flex space-x-2">
              <button 
                @click="handleMessage"
                class="border border-gray-300 p-2 rounded-full hover:bg-gray-100 transition"
              >
                 <EnvelopeIcon class="h-5 w-5 text-black" />
              </button>
              <button class="bg-black text-white font-bold py-2 px-6 rounded-full hover:bg-gray-800 transition">
                Follow
              </button>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <h1 class="font-black text-xl leading-none">{{ profile.first_name || profile.username }}</h1>
        <p class="text-gray-500 text-sm">@{{ profile.username }}</p>
      </div>

      <div class="mt-4 text-gray-900 whitespace-pre-wrap">
        {{ profile.bio || "No bio yet." }}
      </div>

      <div class="mt-4 flex space-x-5 text-sm">
        <span class="hover:underline cursor-pointer"><span class="font-bold text-black">{{ profile.following_count || 0 }}</span> <span class="text-gray-500">Following</span></span>
        <span class="hover:underline cursor-pointer"><span class="font-bold text-black">{{ profile.followers_count || 0 }}</span> <span class="text-gray-500">Followers</span></span>
      </div>
    </div>
    
    <EditProfileModal 
       v-if="isMe" 
       :isOpen="showEditModal" 
       :user="profile"
       @close="showEditModal = false"
       @updated="handleProfileUpdate"
    />

  </div>
  <div v-else class="text-center mt-10">Загрузка...</div>
</template>