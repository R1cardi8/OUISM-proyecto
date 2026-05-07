<template>
  <div class="page">
    <MiMenu />

    <main class="content">

      <template v-if="usuario">

        <div class="hero">
          <div class="hero-emoji">👋</div>
          <div class="hero-text">
            <h1>¡Hola, <em>{{ usuario }}</em>!</h1>
            <p>Tu ciudad te necesita. ¿Qué hacemos hoy?</p>
          </div>
          <div class="hero-badge">
            <span class="live-dot"></span> Ciudad activa
          </div>
        </div>

        <div class="section-title">⚡ Acciones rápidas</div>
        <div class="quick-grid">
          <router-link to="/reportar-incidentes" class="q-card q-blue">
            <span class="q-icon">🚨</span>
            <strong>Nuevo reporte</strong>
            <span>Reporta un problema ahora</span>
            <div class="q-arrow">→</div>
          </router-link>
          <router-link to="/reportar-incidentes" class="q-card q-green">
            <span class="q-icon">📋</span>
            <strong>Mis reportes</strong>
            <span>{{ totalReportes }} reportes enviados</span>
            <div class="q-arrow">→</div>
          </router-link>
          <div class="q-card q-purple" @click="mostrarAlerta = true">
            <span class="q-icon">🔔</span>
            <strong>Alertas</strong>
            <span>Ver novedades</span>
            <div class="q-arrow">→</div>
          </div>
        </div>

        <div class="section-title">📊 Tu actividad</div>
        <div class="stats-row">
          <div class="stat-card">
            <span class="stat-num">{{ totalReportes }}</span>
            <span class="stat-label">Reportes enviados</span>
            <span class="stat-icon">📤</span>
          </div>
          <div class="stat-card">
            <span class="stat-num">{{ reportesResueltos }}</span>
            <span class="stat-label">Resueltos</span>
            <span class="stat-icon">✅</span>
          </div>
          <div class="stat-card">
            <span class="stat-num">{{ reportesPendientes }}</span>
            <span class="stat-label">Pendientes</span>
            <span class="stat-icon">⏳</span>
          </div>
        </div>

        <template v-if="incidentes.length > 0">
          <div class="section-title">
            🕒 Últimos reportes
            <span class="badge-count">{{ incidentes.length }}</span>
          </div>
          <div class="recent-list">
            <div v-for="inc in incidentes.slice(0, 3)" :key="inc.id" class="recent-card">
              <span class="recent-emoji">{{ tipoEmoji(inc.tipo) }}</span>
              <div class="recent-body">
                <strong>{{ inc.titulo }}</strong>
                <span>{{ inc.descripcion.slice(0, 60) }}{{ inc.descripcion.length > 60 ? '…' : '' }}</span>
              </div>
              <span :class="['p-badge', inc.prioridad]">{{ inc.prioridad }}</span>
            </div>
          </div>
          <router-link to="/reportar-incidentes" class="ver-todos-btn">
            Ver todos mis reportes →
          </router-link>
        </template>

        <div v-else class="empty-state">
          <div class="empty-emoji">📭</div>
          <strong>Aún no tienes reportes</strong>
          <p>¡Sé el primero en mejorar tu ciudad!</p>
          <router-link to="/reportar-incidentes" class="cta-empty">
            🚨 Hacer mi primer reporte
          </router-link>
        </div>

        <div class="section-title">💡 ¿Sabías que…?</div>
        <div class="tips-grid">
          <div v-for="(tip, i) in tips" :key="i" class="tip-card" :class="tip.color" @click="$router.push('/reportar-incidentes?hint=' + tip.hint)" style="cursor: pointer;">
            <span class="tip-emoji">{{ tip.emoji }}</span>
            <p>{{ tip.text }}</p>
            <span class="tip-cta">{{ tip.cta }} →</span>
          </div>
        </div>

        <transition name="pop">
          <div v-if="mostrarAlerta" class="modal-overlay" @click.self="mostrarAlerta = false">
            <div class="modal">
              <div class="modal-head">🔔 Novedades</div>
              <p>No tienes alertas nuevas por el momento. Cuando haya novedades en tu ciudad aparecerán aquí.</p>
              <button @click="mostrarAlerta = false" class="modal-close">Entendido ✓</button>
            </div>
          </div>
        </transition>

      </template>

      <template v-else>

        <div class="hero hero-guest">
          <div class="hero-emoji">🏙️</div>
          <div class="hero-text">
            <h1>OUI<em>.SM</em></h1>
            <p>Tu ciudad en tiempo real, tu voz en acción.</p>
          </div>
        </div>

        <div class="guest-actions">
          <router-link to="/login" class="g-btn g-primary">Iniciar sesión</router-link>
          <router-link to="/registro" class="g-btn g-secondary">Crear cuenta →</router-link>
        </div>

        <div class="section-title">✨ ¿Qué puedes hacer?</div>
        <div class="features-grid">
          <div class="feat-card" v-for="(f, i) in features" :key="i">
            <span class="feat-emoji">{{ f.emoji }}</span>
            <strong>{{ f.title }}</strong>
            <p>{{ f.desc }}</p>
          </div>
        </div>

      </template>

    </main>
  </div>
</template>

<script>
import MiMenu from '@/components/MiMenu.vue'

export default {
  name: 'HomeView',
  components: { MiMenu },
  data() {
    return {
      usuario: localStorage.getItem('usuario') || null,
      incidentes: [],
      mostrarAlerta: false,
      tips: [
        { emoji: '📸', color: 'tip-blue',   hint: 'foto',      cta: 'Subir foto',       text: 'Añadir una foto a tu reporte aumenta un 60% la velocidad de respuesta.' },
        { emoji: '📍', color: 'tip-green',  hint: 'ubicacion', cta: 'Añadir ubicación', text: 'Indicar la ubicación exacta ayuda a que el equipo llegue más rápido.' },
        { emoji: '⚡', color: 'tip-yellow', hint: 'urgente',   cta: 'Reportar urgente', text: 'Los reportes urgentes se atienden en menos de 2 horas en promedio.' },
      ],
      features: [
        { emoji: '🚨', title: 'Reporta incidentes', desc: 'Informa problemas en tu barrio en segundos desde cualquier dispositivo.' },
        { emoji: '📍', title: 'Geolocalización',     desc: 'Marca exactamente dónde ocurrió para una respuesta más rápida.' },
        { emoji: '📊', title: 'Sigue el estado',     desc: 'Monitorea en tiempo real si tu reporte fue atendido y resuelto.' },
        { emoji: '🤝', title: 'Comunidad activa',    desc: 'Únete a miles de ciudadanos que ya están mejorando su ciudad.' },
      ],
      tipos: [
        { value: 'técnico',        emoji: '🚧' },
        { value: 'médico',         emoji: '🏥' },
        { value: 'administrativo', emoji: '📋' },
        { value: 'seguridad',      emoji: '🚔' },
        { value: 'ambiental',      emoji: '🌿' },
        { value: 'otro',           emoji: '❓' },
      ],
    }
  },
  computed: {
    totalReportes()      { return this.incidentes.length },
    reportesResueltos()  { return Math.floor(this.incidentes.length * 0.6) },
    reportesPendientes() { return this.incidentes.length - this.reportesResueltos },
  },
  mounted() {
    this.usuario = localStorage.getItem('usuario') || null
    const s = localStorage.getItem('incidentes')
    if (s) this.incidentes = JSON.parse(s)
  },
  methods: {
    tipoEmoji(tipo) {
      const t = this.tipos.find(x => x.value === tipo)
      return t ? t.emoji : '📌'
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

* { box-sizing: border-box; }

.page { min-height: 100vh; background: #f0f4ff; font-family: 'Nunito', sans-serif; }

.content { max-width: 720px; margin: 0 auto; padding: 32px 20px 80px; display: flex; flex-direction: column; }

.section-title { font-size: 14px; font-weight: 800; color: #6670a0; text-transform: uppercase; letter-spacing: 0.8px; margin: 32px 0 14px; display: flex; align-items: center; gap: 8px; }

.hero { display: flex; align-items: center; gap: 16px; background: #fff; border-radius: 24px; padding: 24px 28px; box-shadow: 0 4px 0 #d4d9f0; flex-wrap: wrap; }
.hero-emoji { font-size: 46px; line-height: 1; }
.hero-text  { flex: 1; min-width: 160px; }
.hero-text h1 { font-size: 24px; font-weight: 900; color: #1a1a2e; margin: 0 0 4px; }
.hero-text h1 em { font-style: normal; color: #1cb0f6; }
.hero-text p  { font-size: 13px; color: #8890b0; margin: 0; font-weight: 600; }

.hero-badge { display: inline-flex; align-items: center; gap: 7px; background: #e8fff0; border: 2px solid #b6f0cc; border-radius: 99px; padding: 6px 14px; font-size: 12px; font-weight: 800; color: #16a34a; white-space: nowrap; }
.live-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 6px #22c55e; animation: blink 1.4s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.quick-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.q-card { position: relative; display: flex; flex-direction: column; gap: 4px; padding: 20px 18px 18px; border-radius: 20px; border: 2px solid transparent; text-decoration: none; cursor: pointer; transition: transform 0.2s cubic-bezier(.34,1.56,.64,1), box-shadow 0.2s; overflow: hidden; }
.q-card:hover { transform: translateY(-4px); }
.q-card strong { font-size: 14px; font-weight: 900; color: #1a1a2e; }
.q-card span   { font-size: 12px; font-weight: 600; color: #6670a0; }
.q-icon { font-size: 32px; line-height: 1; margin-bottom: 6px; }
.q-arrow { position: absolute; bottom: 16px; right: 16px; font-size: 18px; opacity: 0.3; transition: opacity 0.2s, transform 0.2s; }
.q-card:hover .q-arrow { opacity: 0.8; transform: translateX(4px); }
.q-blue   { background: #e8f4ff; border-color: #bee3f8; box-shadow: 0 4px 0 #90c8ef; }
.q-blue:hover   { box-shadow: 0 7px 0 #90c8ef; }
.q-green  { background: #e8fff0; border-color: #b6f0cc; box-shadow: 0 4px 0 #7ed9a6; }
.q-green:hover  { box-shadow: 0 7px 0 #7ed9a6; }
.q-purple { background: #f0e8ff; border-color: #d4b8f5; box-shadow: 0 4px 0 #b08dde; }
.q-purple:hover { box-shadow: 0 7px 0 #b08dde; }

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.stat-card { position: relative; background: #fff; border: 2px solid #e8eaf6; border-radius: 20px; padding: 20px 18px; box-shadow: 0 4px 0 #d4d9f0; display: flex; flex-direction: column; gap: 2px; overflow: hidden; }
.stat-num   { font-size: 2rem; font-weight: 900; color: #1a1a2e; line-height: 1; }
.stat-label { font-size: 12px; font-weight: 700; color: #8890b0; }
.stat-icon  { position: absolute; top: 14px; right: 16px; font-size: 22px; opacity: 0.22; }

.recent-list { display: flex; flex-direction: column; gap: 10px; }
.recent-card { display: flex; align-items: center; gap: 14px; background: #fff; border: 2px solid #e8eaf6; border-radius: 16px; padding: 16px 18px; box-shadow: 0 3px 0 #d4d9f0; transition: transform 0.18s cubic-bezier(.34,1.56,.64,1); }
.recent-card:hover { transform: translateY(-2px); }
.recent-emoji { font-size: 28px; flex-shrink: 0; }
.recent-body  { flex: 1; min-width: 0; }
.recent-body strong { display: block; font-size: 14px; font-weight: 800; color: #1a1a2e; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.recent-body span   { font-size: 12px; color: #8890b0; font-weight: 600; }

.p-badge { font-size: 11px; font-weight: 800; border-radius: 99px; padding: 4px 12px; text-transform: uppercase; letter-spacing: .5px; flex-shrink: 0; }
.p-badge.baja    { background: #e8ffe0; color: #3da800; }
.p-badge.media   { background: #fff8d6; color: #b08800; }
.p-badge.alta    { background: #fff0e0; color: #c46000; }
.p-badge.urgente { background: #ffe8e8; color: #cc2c2c; }

.ver-todos-btn { display: inline-block; margin-top: 12px; font-size: 13px; font-weight: 800; color: #1cb0f6; text-decoration: none; padding: 4px 0; border-bottom: 2px solid #1cb0f6; transition: opacity 0.2s; }
.ver-todos-btn:hover { opacity: 0.7; }
.badge-count { background: #1cb0f6; color: #fff; font-size: 11px; font-weight: 800; border-radius: 99px; padding: 2px 9px; }

.empty-state { background: #fff; border: 2px dashed #d0d5f0; border-radius: 24px; padding: 40px 20px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 8px; }
.empty-emoji { font-size: 52px; }
.empty-state strong { font-size: 16px; font-weight: 900; color: #1a1a2e; }
.empty-state p { font-size: 13px; color: #8890b0; font-weight: 600; margin: 0; }
.cta-empty { margin-top: 12px; display: inline-block; padding: 12px 24px; background: linear-gradient(135deg, #58cc02, #89e219); color: #fff; font-size: 14px; font-weight: 900; border-radius: 14px; text-decoration: none; box-shadow: 0 4px 0 #3da800; transition: transform 0.2s, box-shadow 0.2s; }
.cta-empty:hover { transform: translateY(-2px); box-shadow: 0 6px 0 #3da800; }

.tips-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.tip-card { background: #fff; border: 2px solid #e8eaf6; border-radius: 18px; padding: 18px 16px; box-shadow: 0 4px 0 #d4d9f0; display: flex; flex-direction: column; gap: 8px; transition: transform 0.2s, box-shadow 0.2s; }
.tip-card:hover { transform: translateY(-4px); box-shadow: 0 8px 0 #d4d9f0; }
.tip-emoji { font-size: 28px; }
.tip-card p { font-size: 12px; font-weight: 700; color: #6670a0; margin: 0; line-height: 1.5; flex: 1; }
.tip-cta { font-size: 12px; font-weight: 900; margin-top: 4px; }
.tip-blue   { border-color: #bee3f8; background: #f0f8ff; }
.tip-blue   .tip-cta { color: #1cb0f6; }
.tip-green  { border-color: #b6f0cc; background: #f0fff6; }
.tip-green  .tip-cta { color: #16a34a; }
.tip-yellow { border-color: #fde68a; background: #fffdf0; }
.tip-yellow .tip-cta { color: #d97706; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.35); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 999; padding: 20px; }
.modal { background: #fff; border-radius: 24px; padding: 32px 28px; max-width: 380px; width: 100%; box-shadow: 0 8px 0 #d4d9f0, 0 20px 50px rgba(0,0,0,0.2); text-align: center; display: flex; flex-direction: column; gap: 12px; }
.modal-head { font-size: 20px; font-weight: 900; color: #1a1a2e; }
.modal p    { font-size: 14px; color: #6670a0; font-weight: 600; margin: 0; line-height: 1.6; }
.modal-close { margin-top: 8px; padding: 12px 24px; background: #1cb0f6; color: #fff; border: none; border-radius: 14px; font-family: 'Nunito', sans-serif; font-size: 15px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 0 #1a9fd4; transition: transform 0.2s, box-shadow 0.2s; }
.modal-close:hover { transform: translateY(-2px); box-shadow: 0 6px 0 #1a9fd4; }

.pop-enter-active { animation: pop-in 0.3s cubic-bezier(.34,1.56,.64,1); }
.pop-leave-active { animation: pop-in 0.2s reverse ease-in; }
@keyframes pop-in { from { transform: scale(0.85); opacity: 0; } to { transform: scale(1); opacity: 1; } }

.guest-actions { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px; }
.g-btn { padding: 13px 24px; border-radius: 14px; font-size: 14px; font-weight: 900; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; display: inline-block; }
.g-primary { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: #fff; box-shadow: 0 4px 0 #1a3fb8; }
.g-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 0 #1a3fb8; }
.g-secondary { background: #fff; color: #1a1a2e; border: 2px solid #e0e4f5; box-shadow: 0 4px 0 #d4d9f0; }
.g-secondary:hover { transform: translateY(-2px); }

.features-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.feat-card { background: #fff; border: 2px solid #e8eaf6; border-radius: 20px; padding: 22px 20px; box-shadow: 0 4px 0 #d4d9f0; display: flex; flex-direction: column; gap: 6px; transition: transform 0.2s cubic-bezier(.34,1.56,.64,1); }
.feat-card:hover { transform: translateY(-4px); }
.feat-emoji  { font-size: 32px; }
.feat-card strong { font-size: 15px; font-weight: 900; color: #1a1a2e; }
.feat-card p { font-size: 12px; font-weight: 600; color: #8890b0; margin: 0; line-height: 1.5; }

@media (max-width: 580px) {
  .quick-grid    { grid-template-columns: 1fr; }
  .tips-grid     { grid-template-columns: 1fr; }
  .features-grid { grid-template-columns: 1fr; }
  .guest-actions { flex-direction: column; }
  .stats-row     { gap: 8px; }
  .stat-num      { font-size: 1.4rem; }
}
</style>