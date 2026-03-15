import { createApp } from 'vue'
import { createPinia } from 'pinia'
// import './style.css'
import './assets/common.css';
import App from './App.vue'
import router from './router'
import { permissionDirective } from './directives/permission'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 2. Đăng ký directive với tên 'permission' (khi dùng sẽ là v-permission)
app.directive('permission', permissionDirective)

app.mount('#app')
