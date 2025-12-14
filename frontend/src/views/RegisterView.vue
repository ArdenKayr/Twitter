<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const submit = async () => {
  try {
    await auth.register(username.value, email.value, password.value)
    alert('Успешно! Теперь войдите.')
    router.push('/login')
  } catch (e) {
    alert('Ошибка регистрации')
  }
}
</script>

<template>
  <div class="max-w-md mx-auto bg-white p-6 rounded shadow">
    <h2 class="text-2xl mb-4 font-bold text-gray-700">Регистрация</h2>
    <form @submit.prevent="submit" class="space-y-4">
      <input v-model="username" type="text" placeholder="Логин" class="w-full border p-2 rounded" required />
      <input v-model="email" type="email" placeholder="Email" class="w-full border p-2 rounded" required />
      <input v-model="password" type="password" placeholder="Пароль" class="w-full border p-2 rounded" required />
      <button type="submit" class="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700">Зарегистрироваться</button>
    </form>
  </div>
</template>