<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()
const error = ref('')

const submit = async () => {
  try {
    await auth.login(username.value, password.value)
    router.push('/feed') // Перенаправляем на ленту
  } catch (e) {
    error.value = 'Неверный логин или пароль'
  }
}
</script>

<template>
  <div class="flex h-screen bg-white">
    <div class="hidden lg:flex w-1/2 bg-blue-500 items-center justify-center">
       <svg viewBox="0 0 24 24" class="h-1/2 w-1/2 text-white fill-current">
          <g><path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"></path></g>
       </svg>
    </div>

    <div class="w-full lg:w-1/2 flex items-center justify-center p-10">
      <div class="w-full max-w-md">
        <svg viewBox="0 0 24 24" class="h-10 w-10 text-blue-500 fill-current mb-8 lg:hidden">
            <g><path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"></path></g>
        </svg>

        <h1 class="text-4xl font-black mb-12 text-slate-900">Happening now</h1>
        <h2 class="text-2xl font-bold mb-8 text-slate-900">Join today.</h2>

        <form @submit.prevent="submit" class="flex flex-col space-y-4">
          <input 
            v-model="username" 
            type="text" 
            placeholder="Username" 
            class="w-full border border-gray-300 p-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition" 
            required 
          />
          <input 
            v-model="password" 
            type="password" 
            placeholder="Password" 
            class="w-full border border-gray-300 p-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition" 
            required 
          />
          
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>

          <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 rounded-full transition duration-200">
            Log in
          </button>
        </form>

        <div class="mt-8 text-sm text-gray-600">
          Don't have an account? 
          <RouterLink to="/register" class="text-blue-500 hover:underline">Sign up</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>