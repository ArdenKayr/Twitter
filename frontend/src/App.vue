<script setup>
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/Sidebar.vue'

const auth = useAuthStore()
</script>

<template>
  <div class="min-h-screen bg-white text-black font-sans">
    
    <div v-if="auth.isAuthenticated" class="flex justify-center min-h-screen">
      
      <header class="w-[68px] md:w-[88px] xl:w-[275px] flex-shrink-0 flex flex-col items-end">
        <div class="w-full xl:w-[275px] h-full">
           <Sidebar />
        </div>
      </header>

      <main class="flex-1 max-w-[600px] w-full border-x border-gray-100 min-h-screen">
        <RouterView />
      </main>

      <div class="hidden lg:block w-[290px] xl:w-[350px] pl-8 pt-4 flex-shrink-0">
        <div class="sticky top-4 h-screen overflow-y-auto pb-10">
          <div class="mb-5 relative group">
             <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400 group-focus-within:text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                   <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
             </div>
             <input type="text" placeholder="Поиск" class="bg-gray-100 border-none rounded-full py-3 pl-10 pr-4 w-full text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition" />
          </div>

          <div class="bg-gray-50 rounded-2xl p-4">
            <h2 class="font-extrabold text-xl mb-4 text-gray-900">Тренды для вас</h2>
            <div class="space-y-4">
               <div class="cursor-pointer hover:bg-gray-200 transition p-2 -mx-2 rounded-lg">
                  <p class="text-xs text-gray-500">Популярное в РФ</p>
                  <p class="font-bold text-gray-800">Vue.js 3</p>
                  <p class="text-xs text-gray-500">54.2 тыс. постов</p>
               </div>
               <div class="cursor-pointer hover:bg-gray-200 transition p-2 -mx-2 rounded-lg">
                  <p class="text-xs text-gray-500">Технологии · Актуально</p>
                  <p class="font-bold text-gray-800">Django + Python</p>
                  <p class="text-xs text-gray-500">22.1 тыс. постов</p>
               </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <div v-else class="min-h-screen flex items-center justify-center bg-gray-50">
       <div class="max-w-md w-full">
          <RouterView />
       </div>
    </div>

  </div>
</template>