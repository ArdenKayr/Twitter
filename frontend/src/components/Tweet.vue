<script setup>
import { formatDistanceToNow } from 'date-fns'
import { UserCircleIcon, ChatBubbleOvalLeftIcon, HeartIcon, ArrowPathRoundedSquareIcon } from '@heroicons/vue/24/outline'
import { HeartIcon as HeartIconSolid } from '@heroicons/vue/24/solid'
import { useTweetStore } from '@/stores/tweets'
import { useRouter } from 'vue-router'

const props = defineProps({
  tweet: Object
})

const tweetStore = useTweetStore()
const router = useRouter()

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString()
}

const handleLike = () => {
    tweetStore.toggleLike(props.tweet.id)
}

const goToTweet = () => {
    router.push(`/tweet/${props.tweet.id}`)
}
</script>

<template>
  <div 
    @click="goToTweet" 
    class="border-b border-gray-100 p-4 hover:bg-gray-50 transition duration-200 cursor-pointer"
  >
    <div class="flex space-x-3">
      <UserCircleIcon class="h-12 w-12 text-gray-400" />
      
      <div class="flex-1">
        <div class="flex items-center space-x-1">
          <router-link 
            :to="'/user/' + tweet.author.username" 
            class="font-bold text-gray-900 hover:underline" 
            @click.stop
          >
            {{ tweet.author.username }}
          </router-link>
          
          <span class="text-gray-500 text-sm">@{{ tweet.author.username }}</span>
          <span class="text-gray-500 text-sm">· {{ formatDate(tweet.created_at) }}</span>
        </div>

        <p class="text-gray-900 mt-1 text-base leading-snug">
          {{ tweet.content }}
        </p>

        <div class="flex justify-between mt-3 text-gray-500 max-w-md">
            <div class="flex items-center hover:text-blue-500 space-x-2 group">
                <div class="p-2 rounded-full group-hover:bg-blue-50">
                    <ChatBubbleOvalLeftIcon class="h-5 w-5" />
                </div>
                <span class="text-sm">{{ tweet.comments_count }}</span>
            </div>
            
            <div class="flex items-center hover:text-green-500 space-x-2 group">
                <div class="p-2 rounded-full group-hover:bg-green-50">
                    <ArrowPathRoundedSquareIcon class="h-5 w-5" />
                </div>
                 <span class="text-sm">0</span>
            </div>

            <div 
                @click.stop="handleLike"
                class="flex items-center space-x-2 group cursor-pointer transition"
                :class="tweet.is_liked ? 'text-pink-600' : 'hover:text-pink-500'"
            >
                <div class="p-2 rounded-full group-hover:bg-pink-50 relative">
                    <HeartIconSolid v-if="tweet.is_liked" class="h-5 w-5" />
                    <HeartIcon v-else class="h-5 w-5" />
                </div>
                 <span class="text-sm" :class="{'text-pink-600': tweet.is_liked}">
                    {{ tweet.likes_count }}
                 </span>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>