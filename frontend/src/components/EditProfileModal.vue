<script setup>
import { ref } from 'vue'
import { XMarkIcon, CameraIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps({
  user: Object,
  isOpen: Boolean
})

const emit = defineEmits(['close', 'updated'])
const auth = useAuthStore()

// Данные формы
const form = ref({
  first_name: props.user?.first_name || '',
  bio: props.user?.bio || '',
})

const file = ref(null)
const previewUrl = ref(props.user?.avatar || null)
const loading = ref(false)

// Обработка выбора файла
const handleFileChange = (event) => {
  const selectedFile = event.target.files[0]
  if (selectedFile) {
    file.value = selectedFile
    // Создаем ссылку для предпросмотра
    previewUrl.value = URL.createObjectURL(selectedFile)
  }
}

// Сохранение
const save = async () => {
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('first_name', form.value.first_name)
    formData.append('bio', form.value.bio)
    if (file.value) {
      formData.append('avatar', file.value)
    }

    const response = await axios.patch('http://127.0.0.1:8000/api/users/me/', formData, {
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'multipart/form-data' // Важно для файлов
      }
    })

    // Обновляем данные в store (если нужно) и закрываем
    emit('updated', response.data)
    emit('close')
  } catch (e) {
    console.error(e)
    alert('Ошибка при сохранении')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
    <div class="bg-white rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl relative">
      
      <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        <div class="flex items-center space-x-4">
           <button @click="$emit('close')" class="p-2 rounded-full hover:bg-gray-200 transition">
             <XMarkIcon class="h-6 w-6 text-black" />
           </button>
           <h2 class="font-bold text-xl text-black">Edit profile</h2>
        </div>
        <button 
          @click="save" 
          :disabled="loading"
          class="bg-black text-white font-bold py-1.5 px-5 rounded-full hover:bg-gray-800 disabled:opacity-50"
        >
          {{ loading ? 'Saving...' : 'Save' }}
        </button>
      </div>

      <div class="p-4 relative">
        <div class="h-32 bg-gray-300 mb-12 relative">
             </div>

        <div class="absolute top-24 left-4">
           <div class="relative w-28 h-28 rounded-full border-4 border-white bg-gray-200 overflow-hidden group cursor-pointer">
              
              <img v-if="previewUrl" :src="previewUrl" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-4xl font-bold text-gray-500">
                  {{ user.username[0].toUpperCase() }}
              </div>

              <div class="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition" @click="$refs.fileInput.click()">
                 <CameraIcon class="h-8 w-8 text-white opacity-80" />
              </div>
           </div>
           <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="handleFileChange" />
        </div>

        <div class="space-y-6 mt-2">
            <div class="border border-gray-300 rounded px-3 py-2 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500">
               <label class="block text-xs text-gray-500 mb-1">Name</label>
               <input v-model="form.first_name" type="text" class="w-full outline-none text-black font-medium" />
            </div>

            <div class="border border-gray-300 rounded px-3 py-2 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500">
               <label class="block text-xs text-gray-500 mb-1">Bio</label>
               <textarea v-model="form.bio" rows="3" class="w-full outline-none text-black font-medium resize-none"></textarea>
            </div>
        </div>
      </div>

    </div>
  </div>
</template>