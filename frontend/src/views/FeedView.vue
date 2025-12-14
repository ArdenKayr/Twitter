<script setup>
import { ref, onMounted, watch } from 'vue'
import { useTweetStore } from '@/stores/tweets'
import Tweet from '@/components/Tweet.vue'
import { UserCircleIcon } from '@heroicons/vue/24/outline'

const tweetStore = useTweetStore()
const content = ref('')
const activeTab = ref('for_you') // 'for_you' или 'following'

// Функция загрузки в зависимости от вкладки
const loadTweets = () => {
  if (activeTab.value === 'following') {
      // Передаем feed_type=following (но username=null, чтобы не фильтровать по юзеру)
      // Нам придется чуть поправить store, чтобы он принимал этот параметр
      tweetStore.fetchTweets(null, 'following')
  } else {
      tweetStore.fetchTweets(null, null)
  }
}

// Загружаем при старте и при смене вкладки
onMounted(loadTweets)
watch(activeTab, loadTweets)

const handlePublish = async () => {
    if (!content.value) return;
    try {
        await tweetStore.createTweet(content.value)
        content.value = ''
        // Если мы были во вкладке "Подписки", а твит написали мы сами,
        // он там может не появиться (если я не подписан сам на себя).
        // Поэтому переключимся на "Для вас", чтобы увидеть свой твит.
        activeTab.value = 'for_you' 
    } catch (e) {
        alert("Не удалось отправить твит")
    }
}
</script>

<template>
  <div>
    <div class="sticky top-0 bg-white/80 backdrop-blur-md border-b border-gray-100 z-10">
        <h2 class="font-bold text-xl px-4 py-3 cursor-pointer hidden">Home</h2>
        
        <div class="flex">
           <div 
             @click="activeTab = 'for_you'"
             class="flex-1 text-center py-4 hover:bg-gray-200 cursor-pointer transition relative"
           >
              <span :class="{'font-bold text-black': activeTab === 'for_you', 'text-gray-500 font-medium': activeTab !== 'for_you'}">
                  For you
              </span>
              <div v-if="activeTab === 'for_you'" class="absolute bottom-0 left-1/2 -translate-x-1/2 w-14 h-1 bg-blue-500 rounded-full"></div>
           </div>

           <div 
             @click="activeTab = 'following'"
             class="flex-1 text-center py-4 hover:bg-gray-200 cursor-pointer transition relative"
           >
              <span :class="{'font-bold text-black': activeTab === 'following', 'text-gray-500 font-medium': activeTab !== 'following'}">
                  Following
              </span>
              <div v-if="activeTab === 'following'" class="absolute bottom-0 left-1/2 -translate-x-1/2 w-20 h-1 bg-blue-500 rounded-full"></div>
           </div>
        </div>
    </div>

    <div class="hidden md:flex border-b border-gray-100 p-4 space-x-4">
        <UserCircleIcon class="h-12 w-12 text-gray-400" />
        <div class="flex-1">
            <textarea 
                v-model="content"
                class="w-full text-xl placeholder-gray-500 border-none focus:ring-0 resize-none mt-2 outline-none"
                placeholder="What is happening?!"
                rows="2"
            ></textarea>
            <div class="flex justify-end border-t border-gray-100 pt-3 mt-2">
                <button 
                    @click="handlePublish"
                    :disabled="!content"
                    class="bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white font-bold py-2 px-5 rounded-full transition"
                >
                    Tweet
                </button>
            </div>
        </div>
    </div>

    <div>
        <Tweet 
            v-for="tweet in tweetStore.tweets" 
            :key="tweet.id" 
            :tweet="tweet" 
        />
        
        <div v-if="tweetStore.tweets.length === 0 && activeTab === 'following'" class="p-8 text-center">
            <h3 class="text-2xl font-bold mb-2">Welcome to Twitter!</h3>
            <p class="text-gray-500">This is the best place to see what’s happening in your world. Find some people and topics to follow now.</p>
        </div>
        
        <div v-else-if="tweetStore.tweets.length === 0" class="p-8 text-center text-gray-500">
            Лента пуста.
        </div>
    </div>
  </div>
</template>