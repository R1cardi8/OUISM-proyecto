import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import IniciodeSesion from '../views/IniciodeSesion.vue'
import RegistroUsuario from '../views/RegistroUsuario.vue'
import ReportarIncidentes from '../views/ReportarIncidentes.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: IniciodeSesion
  },
  {
    path: '/registro',
    name: 'registro',
    component: RegistroUsuario
  },
  {
    path: '/reportar-incidentes',
    name: 'reportarIncidentes',
    component: ReportarIncidentes
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
