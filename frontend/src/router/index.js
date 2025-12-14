import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import FeedView from '../views/FeedView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import MessagesView from '../views/MessagesView.vue'
import TweetDetailView from '../views/TweetDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/feed'
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/me',
      name: 'me',
      component: ProfileView
    },
    {
       path: '/user/:username',
       name: 'user-profile',
       component: ProfileView
    },
    {
       path: '/messages',
       name: 'messages',
       component: MessagesView
    },
    {
       path: '/tweet/:id',
       name: 'tweet-detail',
       component: TweetDetailView
    }
  ]
})

// Проверка авторизации перед каждым переходом
router.beforeEach(async (to, from, next) => {
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const auth = useAuthStore()

  // Пытаемся восстановить токен из localStorage, если страницы защищена
  if (authRequired && !auth.isAuthenticated) {
      auth.initStore()
      if (!auth.isAuthenticated) {
          return next('/login')
      }
  }
  next()
})

export default router