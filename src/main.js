import { createApp } from 'vue'
import { createPinia } from 'pinia'
// import './style.css'
import './assets/admin.css';
import App from './App.vue'
import router from './router' // Lát nữa tạo Router sẽ import vào
import { permissionDirective } from './directives/permission'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 2. Đăng ký directive với tên 'permission' (khi dùng sẽ là v-permission)
app.directive('permission', permissionDirective)

app.mount('#app')
