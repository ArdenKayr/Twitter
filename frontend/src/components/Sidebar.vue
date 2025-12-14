<script setup>
import { RouterLink } from 'vue-router'
// Добавили EnvelopeIcon в импорт
import { HomeIcon, UserIcon, ArrowLeftOnRectangleIcon, PencilSquareIcon, EnvelopeIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="flex flex-col h-screen sticky top-0 px-2 xl:px-4 py-2 overflow-y-auto">
    
    <div class="mb-2 p-3 rounded-full hover:bg-blue-50 w-min cursor-pointer transition ml-1 xl:ml-0">
      <svg viewBox="0 0 24 24" class="h-8 w-8 text-blue-500 fill-current">
        <g><path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"></path></g>
      </svg>
    </div>

    <nav class="space-y-1 flex-1 mt-2">
      
      <RouterLink to="/feed" class="group flex items-center xl:space-x-4 p-3 rounded-full hover:bg-gray-100 transition duration-200 w-max xl:w-full">
        <HomeIcon class="h-7 w-7 text-gray-900" />
        <span class="text-xl hidden xl:block text-gray-900 mr-4">Главная</span>
      </RouterLink>

      <RouterLink to="/me" class="group flex items-center xl:space-x-4 p-3 rounded-full hover:bg-gray-100 transition duration-200 w-max xl:w-full">
        <UserIcon class="h-7 w-7 text-gray-900" />
        <span class="text-xl hidden xl:block text-gray-900 mr-4">Профиль</span>
      </RouterLink>

      <RouterLink to="/messages" class="group flex items-center xl:space-x-4 p-3 rounded-full hover:bg-gray-100 transition duration-200 w-max xl:w-full">
        <EnvelopeIcon class="h-7 w-7 text-gray-900" />
        <span class="text-xl hidden xl:block text-gray-900 mr-4">Сообщения</span>
      </RouterLink>
      
      <button @click="logout" class="group flex items-center xl:space-x-4 p-3 rounded-full hover:bg-gray-100 transition duration-200 w-max xl:w-full">
        <ArrowLeftOnRectangleIcon class="h-7 w-7 text-gray-900" />
        <span class="text-xl hidden xl:block text-gray-900 mr-4">Выйти</span>
      </button>
    </nav>

    <button class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-3 xl:px-4 rounded-full shadow-lg transition duration-200 mt-4 w-min xl:w-11/12 flex justify-center items-center mb-4">
      <PencilSquareIcon class="h-6 w-6 xl:hidden" />
      <span class="hidden xl:block">Опубликовать</span>
    </button>
    
    <div class="mb-4 flex items-center p-3 rounded-full hover:bg-gray-100 transition cursor-pointer w-max xl:w-full">
       <div class="h-10 w-10 bg-gray-300 rounded-full flex-shrink-0"></div>
       <div class="hidden xl:block ml-3">
          <p class="text-sm font-bold text-gray-900">{{ auth.user?.username || 'User' }}</p>
          <p class="text-sm text-gray-500">@{{ auth.user?.username || 'user' }}</p>
       </div>
    </div>

  </div>
</template>