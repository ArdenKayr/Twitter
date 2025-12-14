<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useAuthStore } from '@/stores/auth'
import { PaperAirplaneIcon } from '@heroicons/vue/24/outline'

const chatStore = useChatStore()
const auth = useAuthStore()
const newMessage = ref('')
let pollingInterval = null

// Вспомогательная функция (с защитой от null)
const getPartnerName = (participants) => {
    // ЗАЩИТА: Если данные пользователя еще не загрузились
    if (!auth.user) return 'Loading...'
    
    // Ищем участника, который НЕ я
    const partner = participants.find(p => p.username !== auth.user.username)
    return partner ? partner.username : 'Unknown'
}

onMounted(async () => {
    await chatStore.fetchConversations()
    
    // Если мы пришли из профиля и activeChat уже задан - грузим сообщения
    if (chatStore.activeChat) {
        await chatStore.fetchMessages(chatStore.activeChat)
    }
    
    // Опрос сервера каждые 2 секунды
    pollingInterval = setInterval(() => {
        if (chatStore.activeChat) {
            chatStore.fetchMessages(chatStore.activeChat)
        }
    }, 2000)
})

onUnmounted(() => {
    clearInterval(pollingInterval)
})

const selectChat = (id) => {
    chatStore.fetchMessages(id)
}

const send = async () => {
    if (!newMessage.value.trim()) return;
    await chatStore.sendMessage(newMessage.value)
    newMessage.value = ''
}
</script>

<template>
  <div class="flex h-screen border-r border-gray-100">
    
    <div class="w-1/3 border-r border-gray-100 overflow-y-auto">
        <div class="p-4 border-b border-gray-100 font-bold text-xl sticky top-0 bg-white">
            Messages
        </div>
        
        <div 
            v-for="chat in chatStore.conversations" 
            :key="chat.id"
            @click="selectChat(chat.id)"
            class="p-4 hover:bg-gray-50 cursor-pointer border-b border-gray-100 transition"
            :class="{'bg-blue-50 border-r-4 border-r-blue-500': chatStore.activeChat === chat.id}"
        >
            <div class="font-bold text-gray-900">
                {{ getPartnerName(chat.participants) }}
            </div>
            <div class="text-sm text-gray-500 truncate">
                {{ chat.last_message ? chat.last_message.content : 'No messages yet' }}
            </div>
        </div>
        
        <div v-if="chatStore.conversations.length === 0" class="p-4 text-gray-500 text-center text-sm">
            У вас пока нет диалогов.
        </div>
    </div>

    <div class="w-2/3 flex flex-col relative">
        
        <div v-if="!chatStore.activeChat" class="flex-1 flex items-center justify-center text-gray-500">
            Select a message to start chatting
        </div>

        <div v-else class="flex flex-col h-full">
            <div class="flex-1 overflow-y-auto p-4 space-y-4"> 
                 <div class="flex flex-col space-y-2">
                    <div 
                        v-for="msg in chatStore.messages" 
                        :key="msg.id"
                        class="max-w-[70%] p-3 rounded-2xl text-sm break-words"
                        :class="msg.sender.username === auth.user?.username 
                            ? 'bg-blue-500 text-white self-end rounded-br-none' 
                            : 'bg-gray-100 text-black self-start rounded-bl-none'"
                    >
                        {{ msg.content }}
                    </div>
                 </div>
            </div>

            <div class="p-4 border-t border-gray-100 bg-white">
                <form @submit.prevent="send" class="flex space-x-2">
                    <input 
                        v-model="newMessage"
                        type="text" 
                        placeholder="Start a new message" 
                        class="flex-1 bg-gray-100 rounded-full px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button 
                        type="submit" 
                        :disabled="!newMessage"
                        class="p-2 text-blue-500 hover:bg-blue-50 rounded-full disabled:opacity-50"
                    >
                        <PaperAirplaneIcon class="h-6 w-6 rotate-90" />
                    </button>
                </form>
            </div>
        </div>

    </div>
  </div>
</template>